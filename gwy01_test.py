import shutil
import pytest
import os
from flaky import flaky
from gwy01_testlib import GwyPower, GwySerial

@flaky(max_runs = 2, min_passes = 1)
def test_bootup():
    
    substring = "Running on gwy01 Revision"    
    bootfile="/srv/tftp/gwyos.itb"
    
    gwyos = os.environ['GWYOSFILE']
    githash = os.environ['GWYOSHASH']
    print(f"\nTest if this boots: {gwyos} {githash}")
  
    
    # 1 Copy file to TFTP
    assert(os.path.isfile(gwyos))
    shutil.copy(gwyos, bootfile)
    assert(os.path.isfile(bootfile)) 

    # 2 Reboot gwy and wait for row containing start message
    pwr = GwyPower()
    pwr.gwy('reboot')
    ser = GwySerial()    
     
    is_found, rev_str = ser.find(substring,60)
    assert is_found == True
    
    # 3 list versions and check that correct gwyos has booted
    ser.cmd("cat /etc/sw-versions \n")
    
    is_found, hash_str = ser.find("gwyos [A-Z0-9a-z.-]+",5)
    assert is_found and githash in hash_str
    
