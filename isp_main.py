import requests
import json
import time
import base64
import re
import warnings

from isp_settings import Settings
from isp_cpapi import CpAPI
from isp_check import ISPCheck
from isp_switch import ISPSwitch

def main():
    warnings.filterwarnings("ignore")
    print ("\n************************************************")
    print ("\nISP manual switcher by Sc1pion, version 1.1")
    print ("\n************************************************\n")
    
    my_sett = Settings()
    my_cpapi = CpAPI()

    sid = my_cpapi.login()

    mycheck = ISPCheck(sid)

    myswitch = ISPSwitch(sid)

    mycheck.check_isp()

    while True:

        print ("\n Menu:")
        print ("\n1. Check ISP status")
        print ("\n2. Switch to " + my_sett.isp1_desc)
        print ("\n3. Switch to " + my_sett.isp2_desc)
        print ("\n4. Return to ISP redundancy mode (default configuration)")
        print ("\n5. Exit")
    
        choice = input ("\n\nMake your choice: ")
    
        if choice == "1":
            mycheck.check_isp()
        elif choice == "2":
            myswitch.isp_switch(my_sett.isp1_name,my_sett.isp2_name)
            mycheck.check_isp()
        elif choice == "3":
            myswitch.isp_switch(my_sett.isp2_name,my_sett.isp1_name)
            mycheck.check_isp()
        elif choice == "4":
            myswitch.isp_switch(my_sett.isp1_name,my_sett.isp2_name,True)
            mycheck.check_isp()
        elif choice == "5":
            print ("\nExiting...")
            break
        else:
            print ("\nWrong number! Please enter correct number!")

    logout_result = my_cpapi.api_call("logout", {},sid)
    print("logout result: " + json.dumps(logout_result))

if __name__ == '__main__':
    main()