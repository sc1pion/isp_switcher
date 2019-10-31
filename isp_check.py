import requests
import json
import time
import base64
import re

from isp_cpapi import CpAPI
from isp_settings import Settings

class ISPCheck:
    """ Class for checking ISP status """
    
    def __init__(self, sid):
        self.sid = sid
        self.mysett = Settings()
        self.cpapi = CpAPI()

    #checking public ip of the machine this script started from
    def ext_ip_check(self):
        ip = requests.get('https://api.ipify.org').text
        return ip

    #checking ISP status
    def check_isp(self):
        for gw in self.mysett.target_gws:
            cpstat = self.cpapi.run_script("cpstat","cpstat fw",self.sid,gw)
            task_id=cpstat["tasks"][0]["task-id"]

            result=self.cpapi.show_task(task_id, self.sid)

            task_status=result["tasks"][0]["status"]

            time.sleep(2)

            task_time = 0
            print ("\nGathering ISP information about " + gw + " gateway")

            while task_status != "succeeded":
                result=self.cpapi.show_task(task_id, self.sid)
                task_status=result["tasks"][0]["status"]
                print (".", end = '')
                time.sleep(1)
                task_time += 1
                if task_time == 60:
                    print ("\nTask time is exceeded. Please check if ISP information gathered!")
                    break
            task_message=result["tasks"][0]["task-details"][0]["responseMessage"]
            #print (result) #to delete
            task_message_decoded=base64.b64decode(task_message)

            try:
                isp_info1=re.search(self.mysett.isp1_name + '(.*)', task_message_decoded.decode('utf-8')).group(0)
            except AttributeError:
                isp_info1="not_found"
        
            try:
                isp_info2=re.search(self.mysett.isp2_name + '(.*)', task_message_decoded.decode('utf-8')).group(0)
            except AttributeError:
                isp_info2="not_found"
        
            print ("\n************************************************")
            print(self.mysett.isp1_desc + " information:\n" + isp_info1 + "\n")
            print(self.mysett.isp2_desc + " information:\n" + isp_info2)
            print ("\n************************************************")
        
            if isp_info1 != "not_found" and isp_info2 != "not_found":
                isp1_stat = re.split("\\|", isp_info1.strip())
                isp2_stat = re.split("\\|", isp_info2.strip())

                if isp1_stat[1].strip() == "OK" and isp1_stat[2].strip() == "Primary":
                    print("\nYour current ISP: " + self.mysett.isp1_desc)
                elif isp2_stat[1].strip() == "OK":
                    print("\nYour current ISP: " + self.mysett.isp2_desc)
                else:
                    print("\nCan't determine your current Internet provider!")
            else:
                print("\nCan't determine your current Internet provider!")
            
        print ("\nYour public IP address: " + self.ext_ip_check())