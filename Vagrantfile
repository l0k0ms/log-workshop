# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
	config.vm.box = "bento/ubuntu-16.04"
	config.vm.define "Workshop"
	config.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true

	config.vm.provision :file, source: './setup.sh', destination: '~/setup.sh'	
  	config.vm.provision "shell", path: "./setup.sh", privileged: false
end