import os 
from jinja2 import Environment, PackageLoader, FileSystemLoader
VIRTUAL_ENV =  os.environ.get('VIRTUAL_ENV')
if not VIRTUAL_ENV:
    raise EnvironmentError('Virtualenv must be active.')
env = Environment(loader=FileSystemLoader(os.path.join(VIRTUAL_ENV, 'proj', 'skel')))

SHARED = {'ENVIRONMENT_DIR':VIRTUAL_ENV, 'APP_NAME':'birdflew', 'APP_USER':'p2p', 'WEB_USER':'www-data', 'GROUP':'worker'}

mapping = [ 
('nginx/nginx.conf', os.path.join(VIRTUAL_ENV, 'etc', 'nginx', 'nginx.conf'), dict({}, **SHARED)),
('nginx/server.conf', os.path.join(VIRTUAL_ENV, 'etc', 'nginx', 'server.conf'), dict({}, **SHARED)),
('nginx/locations.conf', os.path.join(VIRTUAL_ENV, 'etc', 'nginx', 'locations.conf'), dict({}, **SHARED)),
('nginx/django.conf', os.path.join(VIRTUAL_ENV, 'etc', 'nginx', 'django.conf'), dict({}, **SHARED)),
('nginx/conf/fastcgi.conf', os.path.join(VIRTUAL_ENV, 'etc', 'nginx', 'conf','fastcgi.conf'), dict({}, **SHARED)),
('nginx/conf/mime.types', os.path.join(VIRTUAL_ENV, 'etc', 'nginx', 'conf','mime.types'), dict({}, **SHARED)),
('nginx/conf/proxy.conf', os.path.join(VIRTUAL_ENV, 'etc', 'nginx', 'conf','proxy.conf'), dict({}, **SHARED)),
('redis/redis.conf', os.path.join(VIRTUAL_ENV, 'etc', 'redis', 'redis.conf'), dict({}, **SHARED)),
('bin/start_fastcgi.sh', os.path.join(VIRTUAL_ENV, 'bin', 'start_fastcgi.sh'), dict({}, **SHARED)),
('bin/start_nginx.sh', os.path.join(VIRTUAL_ENV, 'bin', 'start_nginx.sh'), dict({}, **SHARED)),
('bin/start_twisted.sh', os.path.join(VIRTUAL_ENV, 'bin', 'start_twisted.sh'), dict({}, **SHARED)),
]

for source, dest, context in mapping:
    if os.path.isfile(dest):
        print "EXISTS"
    template = env.get_template(source)
    print "======================================================="
    print "== %s" % dest
    print "========================================================"
    print template.render(**context)
