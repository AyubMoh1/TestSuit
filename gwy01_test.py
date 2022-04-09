import shutil
import pytest
import sys
import os
from gwy01_testlib import * 

# Run tests: pytest -q -s --gwyos gwyos123.itb --githash cafebabe123

@pytest.fixture(scope="session")
def gwyos(pytestconfig):
    return pytestconfig.getoption("gwyos")

@pytest.fixture(scope="session")
def githash(pytestconfig):
    return pytestconfig.getoption("githash")

def test_bootup(gwyos, githash):
        #print(f"\nTest if this boots: {gwyos} {githash}")
        pwr = GwyPower()
        ser = GwySerial()
        # 1 Copy file to TFTP
        shutil.move("/srv/tftp/file.foo", "path/to/new/home/pi/file.foo")
        #   Assert file exists
        if os.path.isfile("gwy01_testlib.py"):
            print("file exists")
            # 2 Reboot using lib
            pwr.reboot(gwy)

                
        
        
        # 3 Wait for row containing start message
        # 3.1 If timeout, Do steps 1-3 up to 3 times. If OK continue
        # 4. Send command to read sw_versions
        # 5. Assert githash == sw_version's hash
        # 6. Done
        assert True

test_bootup(2,2)