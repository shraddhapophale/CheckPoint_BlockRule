#!/usr/bin/python3

from cortexutils.responder import Responder
import requests, json

class CheckPoint_BlockRule(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.username = self.get_param('config.username', None, "Checkpoint username missing!")
        self.password = self.get_param('config.password', None, "Checkpoint password missing!")
        self.host_ip = self.get_param('config.host_ip', None, "Host IP missing!")

    def run(self):
        Responder.run(self)

        def api_call(ip_addr, port, command, json_payload, sid):
               url = 'https://' + str(ip_addr) + ':' + str(port) + '/web_api/' + command
               if sid == '':
                      request_headers = {'Content-Type' : 'application/json'}
               else:
                      request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
               r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, verify=False)
               return r.json()


        def login(user,password):
               payload = {'user':user, 'password' : password}
               response = api_call('192.168.50.52', 443, 'login',payload, '')
               return response['sid']

        sid = login(self.username,self.password)
        #print("session id: " + sid)

        new_host_data = {'name':'new host name', 'ip-address':self.host_ip}
        new_host_result = api_call('192.168.50.52', 443,'add-host', new_host_data ,sid)
        #print(json.dumps(new_host_result))

        publish_result = api_call('192.168.50.52', 443,"publish", {},sid)
        #print("publish result: " + json.dumps(publish_result))

        logout_result = api_call('192.168.50.52', 443,"logout", {},sid)
        #print("logout result: " + json.dumps(logout_result))

if __name__ == '__main__':
    CheckPoint_BlockRule().run()
