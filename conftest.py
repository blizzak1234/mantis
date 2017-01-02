# данный фаил позволяет использовать фикстуру во всех вспомогательных методах
import pytest
from fixture.application import Application
import json
import os.path
#from fixture.db import DbFixture
import importlib
#import jsonpickle



fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        # определяем путь конф.файла (target.json) относильного директории проекта
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file) #путь к файлу
        with open(config_file) as f:
            target = json.load(f)
    return target


# функция инициализирующая фикстуру
@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    return fixture



@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")


# функция, помогающая питону определять какой фаил с тестовыми данными использовать. пробегает по именам и определять какой фаил брать
def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_json(file):
    # путь к файлу
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())
