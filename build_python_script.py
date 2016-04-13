#
# This script uses the Duffy node management api to get fresh machines to run
# your CI tests on. Once allocated you will be able to ssh into that machine
# as the root user and setup the environ
#
# XXX: You need to add your own api key below, and also set the right cmd= line 
#      needed to run the tests
#
# Please note, this is a basic script, there is no error handling and there are
# no real tests for any exceptions. Patches welcome!

import json, urllib, subprocess, sys

url_base="http://admin.ci.centos.org:8080"

# This file was generated on your slave.  See https://wiki.centos.org/QaWiki/CI/GettingStarted
api=open('duffy.key').read().strip()

ver="7"
arch="x86_64"
count=1
git_url="https://example.com/test.git"

get_nodes_url="%s/Node/get?key=%s&ver=%s&arch=%s&count=%s" % (url_base,api,ver,arch,count)

dat=urllib.urlopen(get_nodes_url).read()
b=json.loads(dat)
for h in b['hosts']:
  cmd="ssh -t -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@%s 'yum -y install git && git clone %s tests && cd tests && chmod +x ./run_tests && ./run_tests'" % (h, git_url)
  print cmd
  rtn_code=subprocess.call(cmd, shell=True)
  
done_nodes_url="%s/Node/done?key=%s&ssid=%s" % (url_base, api, b['ssid'])
das=urllib.urlopen(done_nodes_url).read()

sys.exit(rtn_code)
