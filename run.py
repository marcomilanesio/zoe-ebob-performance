#!/usr/bin/python3

import json
import time
import re
from zoe_lib.executions import ZoeExecutionsAPI
from zoe_lib.services import ZoeServiceAPI


class Test:
    def __init__(self, user, pwd, url, name, zapp):
        self.user = user
        self.pwd = pwd
        self.url = url
        self.name = name
        try:
            with open(zapp, 'r') as infile:
                self.zapp = json.load(infile)
        except:
            exit("Unable to load zapp file.")
        self.exec_api = ZoeExecutionsAPI(self.url, self.user, self.pwd)
        self.service_api = ZoeServiceAPI(self.url, self.user, self.pwd)

    def start_exec(self):
        exec_id = self.exec_api.start(self.name, self.zapp)
        return exec_id

    def get_services_id(self, exec_id):
        services = self.exec_api.get(exec_id)
        return services['services']

    def get_submit_service(self, exec_id):
        while len(self.get_services_id(exec_id)) < 4:
            print('waiting')
            time.sleep(0.5)
        for service_id in self.get_services_id(exec_id):
            srv = self.service_api.get(service_id)
            if re.search('submit', srv['name']):
                return srv['id']

    def is_running(self, exec_id):
        return self.exec_api.get(exec_id)['status'] == 'running'

    def run_test(self):
        exec_id = self.start_exec()
        outfilename = './logs/{}'.format(exec_id)
        submit_id = self.get_submit_service(exec_id)
        while not self.is_running(exec_id):
            time.sleep(0.5)
        with open(outfilename, 'w') as out:
            for line in self.service_api.get_logs(submit_id):
                out.write("{}\n".format(line))
        self.exec_api.terminate(exec_id)
        print('Terminated {}'.format(exec_id))

if __name__ == "__main__":
    import sys
    from configparser import ConfigParser
    cfgfile = '/home/marco/credentials/zoe.cred'
    name = sys.argv[1]
    zapp = sys.argv[2]
    num_run = int(sys.argv[3])

    conf = ConfigParser()
    conf.read(cfgfile)
    t = Test(conf['default']['ZOE_USER'], conf['default']['ZOE_PASS'], conf['default']['ZOE_URL'], name, zapp)

    for i in range(num_run):
        print('RUN #{}'.format(i))
        t.run_test()

