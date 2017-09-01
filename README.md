# Magen Policy Service

[![Build Status](https://travis-ci.org/magengit/magen-ps.svg?branch=master)](https://travis-ci.org/magengit/magen-ps)

Magen Policy Service is a microservice responsible for managing policies and validating asset access requests against the current policies in force. It exposes REST APIs for managing policies. By assets we understand any sensitive resources that could be encrypted or wrapped in order to restrict access to them.

The Magen Policy Service also includes a prototype policy information
provider known as the Location Service that can provide user/device
context for a policy decision. For example, imagine the Policy Service
is evaluating an asset access request against a policy that allows
access to devices in a specific geographical area. The Location
Service could be the Policy Service's source for the needed device location information.

Current version: ```1.0a1```

For This Service there are available ```make``` commands. Makefile is located under [**policy/**](policy)

Make Default Target: ```make default```. Here is the list of targets available for policy

```make
default:
	@echo 'Makefile for Magen Policy Service'
	@echo
	@echo 'Usage:'
	@echo '	make clean    		:Remove packages from system and pyc files'
	@echo '	make test     		:Run the test suite'
	@echo '	make package  		:Create Python wheel package'
	@echo '	make install  		:Install Python wheel package'
	@echo '	make all      		:clean->package->install'
	@echo '	make list     		:List of All Magen Dependencies'
	@echo '	make build_docker 	:Pull Base Docker Image and Current Image'
	@echo '	make run_docker   	:Build and Run required Docker containers with mounted source'
	@echo '	make runpkg_docker	:Build and Run required Docker containers with created wheel'
	@echo '	make test_docker  	:Build, Start and Run tests inside main Docker container interactively'
	@echo '	make stop_docker  	:Stop and Remove All running Docker containers'
	@echo '	make clean_docker 	:Remove Docker unused images'
	@echo '	make rm_docker    	:Remove All Docker images if no containers running'
	@echo '	make doc		:Generate Sphinx API docs'
	@echo
	@echo
```

## Requirements: MacOS X
0. ```python3 -V```: Python **3.5.2** (>=**3.4**)
0. ```pip3 -V```: pip **9.0.1**
0. ```make -v```: GNU Make **3.81**
1. ```docker -v```: Docker version **17.03.0-ce**, build 60ccb22
2. ```docker-compose -v```: docker-compose version **1.11.2**, build dfed245
3. Make sure you have correct rights to clone Cisco-Magen github organization

## Requirements: AWS EC2 Ubuntu
0. ```python3 -V```: Python **3.5.2**
1. ```pip3 -V```: pip **9.0.1**
2. ```make -v```: GNU Make **4.1**
3. ```docker -v```: Docker version **17.03.0-ce**, build 60ccb22
4. ```docker-compose -v```: docker-compose version **1.11.2**, build dfed245
5. Make sure AWS user and **root** have correct rights to Cisco-Magen github organization

## Targets

1. ```make all```  -> Install *Magen-Core* dependencies, clean, package and install **policy** package
2. ```make test``` -> run **policy** tests

## Adopt this Infrastructure

1. get [**helper_scripts**](policy/helper_scripts) to the repo
2. follow the structure in [**docker_policy**](policy/docker_policy) to create ```docker-compose.yml``` and ```Dockerfile``` files
3. use [**Makefile**](policy/Makefile) as an example for building make automation

## Sphinx Documentation SetUp

There is a configured Sphinx API docs for the service.
To compile docs execute:

```make doc``` in the [```policy```](policy) directory
