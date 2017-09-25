#! /bin/sh

# Docker install instructions for centos 7.*
# url source:  https://docs.docker.com/engine/installation/linux/centos/
# changes to the host name
sudo hostnamectl set-hostname rc-docker-rancher

# update the box (vagrant base image)
sudo yum update

# add the yup repo
sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
    
# install the docker package
sudo yum install -y docker-engine

# FOR DEV ONLY:  disable service
# sudo systemctl disable firewalld

# enable the service
sudo systemctl enable docker.service

# start the Docker daemon
sudo systemctl start docker

# verfity docker is installed and correctly, run a test image in a container.
sudo docker run --rm hello-world

# install docker-compose...  first python


# sudo yum install epel-release
# python2 pip
# sudo yum -y install python-pip
# sudo yum -y install python-virtualenv


## VAGRANT ONLY
# adding vagrant to the docker group to easy running commands.
# make the docker group
# sudo groupadd docker

# add vagrant to the docker group.  (it's just easier to be the vagrant user)
sudo usermod -aG docker vagrant

# rancher
sudo docker run -d --restart=unless-stopped -p 8080:8080 rancher/server:latest

# is it possible to just go and add the agent?
# sudo docker run -e CATTLE_AGENT_IP="192.168.33.50"  -e CATTLE_HOST_LABELS='name=rc-base-agent'  -d --privileged -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/rancher:/var/lib/rancher rancher/agent:v1.0.2 http://129.219.115.197:8080/v1/scripts/F8B8C1CE4D73F9C8CA57:1476381600000:RI43fGHxhXotAjSdpiOeyYyNL8

# confluence ready on host...  confluence requires a host volumecd...
# no home directory or group or login
sudo useradd --no-create-home --no-user-group confluence --shell=/sbin/nologin
sudo mkdir /usr/local/confluence
sudo chown confluence:vagrant /usr/local/confluence

