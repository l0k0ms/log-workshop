#!/bin/bash
#####################
# Installing docker #
#####################

sudo apt-get update

sudo apt-get --assume-yes  install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get update

sudo apt-get --assume-yes install docker-ce

############################
#Installing docker compose #
############################

sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

##############################################
# Launching Docker with the good permissions #
##############################################
sudo service docker start

sudo apt-get --assume-yes install apache2

################################
# Giving the right permissions #
################################

sudo chmod 666 /var/run/docker.sock
sudo chmod +s /usr/sbin/tcpdump