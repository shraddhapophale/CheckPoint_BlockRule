#!/usr/bin/python3
import cortexutils
import sys, os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cpapi import APIClient, APIClientArgs

class CheckPoint_AddRule(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.checkpoint_apikey = self.get_param('config.checkpoint_apikey', None, "Checkpoint API key missing!")
        self.server_ip = self.get_param('config.server_ip', None, "Checkpoint Server IP missing!")
        self.rule_name = self.get_param('config.rule_name', None, "Rule Name missing!")

    def run(self):
        Responder.run(self)

        client_args = APIClientArgs(server=self.server_ip, unsafe=True)

        with APIClient(client_args) as client:

             POST {{server}}/login
             Content-Type: application/json

             {
               "api-key" : "hqreK1MmmM4T1AYA0jOJpg=="
             }
if __name__ == "__main__":
    CheckPoint_AddRule().run()
