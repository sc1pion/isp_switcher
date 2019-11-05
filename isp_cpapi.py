import requests
import json

from isp_settings import Settings


class CpAPI:
    """ Check Point API functions class """

    def __init__(self):
        self.mysett = Settings()

    def api_call(self, command, json_payload, sid):
        url = (
            "https://"
            + self.mysett.mgmt_server
            + ":"
            + str(self.mysett.mgmt_port)
            + "/web_api/"
            + command
        )
        if sid == "":
            request_headers = {"Content-Type": "application/json"}
        else:
            request_headers = {"Content-Type": "application/json", "X-chkp-sid": sid}
        r = requests.post(
            url, data=json.dumps(json_payload), headers=request_headers, verify=False
        )
        return r.json()

    def login(self):
        payload = {
            "user": self.mysett.mgmt_username,
            "password": self.mysett.mgmt_password,
        }
        response = self.api_call("login", payload, "")
        return response["sid"]

    def run_script(self, script_name, script_command, sid, gw):
        payload = {"script-name": script_name, "script": script_command, "targets": gw}
        response = self.api_call("run-script", payload, sid)
        return response

    def show_task(self, task_id, sid):
        payload = {"task-id": task_id, "details-level": "full"}
        response = self.api_call("show-task", payload, sid)
        return response
