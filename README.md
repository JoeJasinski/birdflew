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
    sudo adduser joe 
    sudo usermod -G admin -a joe
      # - follow prompts 
    sudo aptitude install python-virtualenv git build-essential python-dev 
    sudo aptitude install libxml-dev libxslt-dev 
    sudo aptitude install nginx htop
    sudo mkdir /sites/
    sudo groupadd worker
    sudo chgrp worker /sites/
    sudo chmod g+ws /sites/
    sudo useradd p2p
    sudo usermod -G worker -a joe
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
    git clone git@github.com:DePaulSE560/jasinskij.git proj; cd proj
    pip install -r requirements.pip
    cd birdflew
    ./manage syncdb 
    ./manage collectstatic
      # - follow prompts 
    cd /sites/p2p/
    cp -r proj/birdflew/skel/nginx/ etc/nginx
    cd /sites/p2p/bin/
    ln -s /sites/p2p/proj/skel/bin/start_nginx.sh
    ln -s /sites/p2p/proj/skel/bin/start_fastcgi.sh
    sudo ./start_nginx.sh 
    ./start_fastcgi.sh


Running the client service. 

    cd /sites/p2p/bin/
    . ./bin/activate
    ./manage.py bf_run_client -i 500