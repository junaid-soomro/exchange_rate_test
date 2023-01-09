python3 = $(shell python3.8 --version)
virtualenv = $(shell pip freeze | grep virtualenv)
environmentName = 'task-env'
awsCreds = $(shell cat ~/.aws/credentials | grep aws_access_key)

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

$(environmentName)/bin/activate: install-virtual-env
	$(info -------------------------------------)
	$(info setting up virtual env $(environmentName)...)
	$(info -------------------------------------)
	virtualenv $(environmentName) -p python3.8;
	
install-required-libraries: $(environmentName)/bin/activate
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
	zappa deploy
else
	$(info -------------------------------------)
	$(error please run aws configure and add credentials(access key, secret key))
	$(info -------------------------------------)
endif

clean:
	rm -rf $(environmentName)

undeploy: 
zappa undeploy


.PHONY: undeploy deploy setup install-prerequisities clean install-virtual-env check-python installing-requirements