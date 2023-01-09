python3 = $(shell python3.8 --version)
virtualenv = $(shell pip freeze | grep virtualenv)
environmentName = 'task-env'
awsCreds = $(shell cat ~/.aws/credentials | grep aws_access_key)
SHELL := /bin/bash
.ONESHELL:


clean:
	rm -rf $(environmentName)

undeploy: 
ifneq (,$(findstring aws_access,$(awsCreds)))
	$(info -------------------------------------)
	$(info AWS credentials found! continuing...)
	$(info -------------------------------------)
	source ./task-env/bin/activate
	zappa undeploy
	deactivate
else
	$(info -------------------------------------)
	$(error please run aws configure and add credentials(access key, secret key))
	$(info -------------------------------------)
endif

check-python:
ifneq (,$(findstring 3.8,$(python3)))
	$(info -------------------------------------)
	$(info $(python3) detected! continuing...)
	$(info -------------------------------------)
else
	$(info -------------------------------------)
	$(info installing python3.8 and distutils...)
	$(info -------------------------------------)
	sudo apt install python3.8 python3.8-distutils
endif

install-virtual-env: check-python
ifneq (,$(findstring virtualenv,$(virtualenv)))
	$(info -------------------------------------)
	$(info $(virtualenv) detected! continuing...)
	$(info -------------------------------------)
else
	$(info -------------------------------------)
	$(info installing virtualenv package...)
	$(info -------------------------------------)
	sudo pip install virtualenv
endif

setup-virtual-env: install-virtual-env
	$(info -------------------------------------)
	$(info setting up virtual env $(environmentName)...)
	$(info -------------------------------------)
	virtualenv $(environmentName) -p python3.8;

$(environmentName)/bin/activate: setup-virtual-env
	$(info -------------------------------------)
	$(info activating virtual evvironment $(environmentName)...)
	$(info -------------------------------------)
	$(shell source ./task-env/bin/activate)
	
install-required-libraries: setup-virtual-env
	$(info -------------------------------------)
	$(info installing packages from requirements.txt...)
	$(info -------------------------------------)
	./$(environmentName)/bin/pip install -r requirements.txt

setup: install-required-libraries

deploy:
ifneq (,$(findstring aws_access,$(awsCreds)))
	$(info -------------------------------------)
	$(info AWS credentials found! continuing...)
	$(info -------------------------------------)
	source ./task-env/bin/activate
	zappa deploy
	deactivate
else
	$(info -------------------------------------)
	$(error please run aws configure and add credentials(access key, secret key))
	$(info -------------------------------------)
endif

deploy-update:
ifneq (,$(findstring aws_access,$(awsCreds)))
	$(info -------------------------------------)
	$(info AWS credentials found! continuing...)
	$(info -------------------------------------)
	source ./task-env/bin/activate
	zappa update
	deactivate
else
	$(info -------------------------------------)
	$(error please run aws configure and add credentials(access key, secret key))
	$(info -------------------------------------)
endif


.PHONY: undeploy deploy setup install-prerequisities clean install-virtual-env check-python installing-requirements