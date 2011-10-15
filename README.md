# Introduction 
Share files using BirdFlew!


ENVIORNMENT SETUP

1) apt-get install python-virtualenv libxml libxml-dev libxslt libxslt-dev

2) virtualenv --no-site-packges p2p

3) cd p2p; . ./bin/activate

4) mkdir proj; cd proj

5) git clone git@github.com:DePaulSE560/jasinskij.git birdflew; cd birdflew

6) pip install -r requirements.pip

7) ./manage.py syncdb 



DETAIL SERVER SETUP
Create Amazon instance using AMI: ebs/ubuntu-images/ubuntu-natty-11.04-i386-server-20110426 (ami-06ad526f)


    ssh -i xxxxxx.pem ubuntu@ec2-xxxxxxxxxxx.compute-1.amazonaws.com
    
    # create admin user
    sudo adduser joe 
      # - follow prompts 
    sudo usermod -G admin -a joe
	sudo usermod -G worker -a joe
      
    # install needed apt packages
    sudo aptitude install python-virtualenv git build-essential python-dev 
    sudo aptitude install libxml-dev libxslt-dev 
    sudo aptitude install nginx htop
    sudo aptitude install postgresql  libpq-dev
    sudo aptitude install redis-server
    
    # create base for site environment
    sudo mkdir /sites/
    sudo groupadd worker
    sudo chgrp worker /sites/
    sudo chmod g+ws /sites/
    
    # create application and db user 
    sudo useradd p2p
    sudo usermod -G worker -a p2p
    sudo -u postgres createuser p2p
    sudo -u postgres createdb p2p -O p2p
    

    sudo su - joe 
    echo "set -o vi" >> ~/.bashrc
    echo "umask 002" >> ~/.bashrc
    bash 
    ssh-keygen -t dsa
      # - enter prompts 
      # - copy /home/joe/.ssh/id_dsa.pub contents to githup
    cd /sites/
    virtualenv --no-site-packages p2p 
    cd p2p; . ./bin/activate
    mkdir log var etc run data htdocs
    mkdir etc/django
    mkdir data/redis/ 
    mkdir log/redis/
    git clone git@github.com:DePaulSE560/jasinskij.git proj; cd proj
    pip install -r requirements.pip
    cd birdflew

	# setup skelaton files
    cd ${VIRTUAL_ENV}
    cp -r ${VIRTUAL_ENV}/proj/skel/nginx/ ${VIRTUAL_ENV}/etc/nginx
    cp -r ${VIRTUAL_ENV}/proj/skel/bfsettings/ ${VIRTUAL_ENV}/etc/django/
    echo "${VIRTUAL_ENV}/etc/django/" >> ${VIRTUAL_ENV}/lib/python2.7/site-packages/birdflew.pth

	# grant permission of all project files to app user
    sudo chown -R p2p:worker ${VIRTUAL_ENV}
	sudo chmod -R g+w ${VIRTUAL_ENV}
	
	# log in as app user and sync the database
	sudo su - p2p 
	cd /sites/p2p/
	. ./bin/activate
	cd proj/birdflew
    ./manage syncdb 
      # - follow prompts 
    ./manage collectstatic
      # - follow prompts 
    exit
    
	# prep start scripts and execute
    cd ${VIRTUAL_ENV}/bin/
    ln -s ${VIRTUAL_ENV}/proj/skel/bin/start_nginx.sh
    ln -s ${VIRTUAL_ENV}/proj/skel/bin/start_fastcgi.sh
    ln -s ${VIRTUAL_ENV}/proj/skel/bin/start_twisted.sh
    
    ln -s  ${VIRTUAL_ENV}/proj/skel/redis/  ${VIRTUAL_ENV}/etc/redis
    
    sudo ./start_nginx.sh 
    sudo -u p2p ./start_fastcgi.sh
    sudo -u p2p ./start_twisted.sh

Running the client service. 

    cd /sites/p2p/bin/
    . ./bin/activate
    ./manage.py bf_run_client -i 500