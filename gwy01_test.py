import pytest
import GwyPower as gwypwr from gwy01_testlib
import GwySerial as gwyser from gwy01_testlib
# Run tests: pytest -q -s --gwyos gwyos123.itb --githash cafebabe123

@pytest.fixture(scope="session")
def gwyos(pytestconfig):
    return pytestconfig.getoption("gwyos")

@pytest.fixture(scope="session")
def githash(pytestconfig):
    return pytestconfig.getoption("githash")

def test_bootup(gwyos, githash):
        print(f"\nTest if this boots: {gwyos} {githash}")
        # 1 Copy file to TFTP
        #   Assert file exists
        # 2 Reboot using lib
        # 3 Wait for row containing start message
        # 3.1 If timeout, Do steps 1-3 up to 3 times. If OK continue
        # 4. Send command to read sw_versions
        # 5. Assert githash == sw_version's hash
        # 6. Done
        assert False

