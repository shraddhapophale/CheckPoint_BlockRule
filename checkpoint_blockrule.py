#!/usr/bin/bash

from cortexutils.responder import Responder
from __future__ import print_function
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cpapi import APIClient, APIClientArgs

class CheckPoint_BlockRule(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.checkpoint_apikey = self.get_param('config.checkpoint_apikey', None, "Checkpoint API key missing!")
        self.server_ip = self.get_param('config.server_ip', None, "Checkpoint Server IP missing!")
        self.rule_name = self.get_param('config.rule_name', None, "Rule Name missing!")

    def run(self):
        Responder.run(self)

        #data_type = self.get_param('data.dataType')
        auth = client.login(self.checkpoint_apikey)
        if self.server_ip == "ip":
           try:
               ipaddress.ip_address(self.server_ip)
           except ValueError:
               self.error({'message': "Not a valid IPv4/IPv6 address!"})
        else:
           self.error({'message': "Not a valid IPv4/IPv6 address!"})

        if auth.success is False:
            print("Login failed:\n{}".format(auth.error_message))
            exit(1)

        # add a rule to the top of the "Network" layer
        add_rule_response = client.api_call("add-access-rule",
                                            {"name": self.rule_name, "layer": "Network", "position": "top"})

        if add_rule_response.success:

            print("The rule: '{}' has been added successfully".format(self.rule_name))

            # publish the result
            publish_res = client.api_call("publish", {})
            if publish_res.success:
                print("The changes were published successfully.")
            else:
                print("Failed to publish the changes.")
         else:
            print("Failed to add the access-rule: '{}', Error:\n{}".format(self.rule_name, add_rule_response.error_message))


if __name__ == "__main__":
    main()

