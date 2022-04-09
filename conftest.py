

def pytest_addoption(parser):

    parser.addoption("--gwyos", action="store", default="gwyos.itb")

    parser.addoption("--githash", action="store", default="XXXXXX")

