#import sys, json, os
#from django.template import Template, Context
#
#
#config = {
#  'HOST':'birdflew.com',
#  'PORT':'80',
#  'VENV_ROOT':'/sites/p2p/',
#}
#
## import json
## print json.dumps(config, sort_keys=True, indent=4)
#
#
#finput = open(sys.argv[1], 'r')
#t = Template(finput.read())
#finput.close()
#
#
#config_path = os.path.join(os.path.abspath(__file__),'config.json')
#c = Context(json.load(open(config_path)))
#fout = open(sys.argv[2], 'w')
#config_text = t.render(c).encode('utf-8')
#fout.write(config_text)
#fout.close()