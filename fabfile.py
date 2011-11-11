from __future__ import with_statement
import os
from fabric.api import local, settings, abort, run, cd

python_requirements = ['django','south','django-extensions','django-debug-toolbar',]

def env_create(env_name, user=None, group="worker", sites_path="/Users/jjasinsk/testenv/"):
     
    with settings(warn_only=True):
        if run("test -d %s" % sites_path).failed:
            abort("SIte path must exist before proceeding.")
    environment_dir = os.path.join(sites_path, env_name)
    with cd(sites_path): 
        run("whoami")
        run("pwd")
        run("mkdir %s" % env_name)
        #sudo("useradd %s" % user)
    with cd(environment_dir):
        run("virtualenv --no-site-packages .")
        run("mkdir -p etc/django/ etc/nginx log/ pid/ htdocs/ proj/")
        run("git init proj/")
        run("echo '%s' > proj/requirements.pip" % '\n'.join(python_requirements))
