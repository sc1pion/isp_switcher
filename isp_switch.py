import requests
import json
import time
import base64
import re

from isp_cpapi import CpAPI
from isp_settings import Settings


class ISPSwitch:
    def __init__(self, sid):
        self.sid = sid
        self.mysett = Settings()
        self.cpapi = CpAPI()

    def isp_switch(self, isp_up, isp_down, d=False):
        for gw in self.mysett.target_gws:
            print("\nSwitching ISP for " + gw + " gateway")
            switch_up = "fw isp_link " + isp_up + " up"
            switch_down = "fw isp_link " + isp_down + " down"
            switch_up1 = "fw isp_link " + isp_down + " up"

            isp_up_task = self.cpapi.run_script("isp_switch", switch_up, self.sid, gw)
            task_id = isp_up_task["tasks"][0]["task-id"]

            result = self.cpapi.show_task(task_id, self.sid)

            task_status = result["tasks"][0]["status"]

            task_time = 0

            time.sleep(2)

            print("\nTurning " + isp_up + " link up...", end="")

            while task_status != "succeeded":
                result = self.cpapi.show_task(task_id, self.sid)
                task_status = result["tasks"][0]["status"]
                print(".", end="")
                time.sleep(1)
                task_time += 1
                if task_time == 20:
                    print("\nTask time is exceeded. Please check if ISP link is up!")
                    break

            if d == False:
                isp_down_task = self.cpapi.run_script(
                    "isp_switch", switch_down, self.sid, gw
                )
                task_id = isp_down_task["tasks"][0]["task-id"]

                result = self.cpapi.show_task(task_id, self.sid)

                task_status = result["tasks"][0]["status"]

                task_time = 0

                time.sleep(2)

                print("\nTurning " + isp_down + " link down...", end="")

                while task_status != "succeeded":
                    result = self.cpapi.show_task(task_id, self.sid)
                    task_status = result["tasks"][0]["status"]
                    print(".", end="")
                    time.sleep(1)
                    task_time += 1
                    if task_time == 20:
                        print(
                            "\nTask time is exceeded. Please check if ISP link is down!"
                        )
                        break

                print("\nPlease check if ISP was changed!")
            else:
                isp_down_task = self.cpapi.run_script(
                    "isp_switch", switch_up1, self.sid, gw
                )
                task_id = isp_down_task["tasks"][0]["task-id"]

                result = self.cpapi.show_task(task_id, self.sid)

                task_status = result["tasks"][0]["status"]

                task_time = 0

                time.sleep(2)

                print("\nTurning " + isp_down + " link up...", end="")

                while task_status != "succeeded":
                    result = self.cpapi.show_task(task_id, self.sid)
                    task_status = result["tasks"][0]["status"]
                    print(".", end="")
                    time.sleep(1)
                    task_time += 1
                    if task_time == 20:
                        print(
                            "\nTask time is exceeded. Please check if ISP link is up!"
                        )
                        break

                print("\nPlease check if all ISP is up!")
