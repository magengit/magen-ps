#
# Makefile for Policy Server
#
# This Makefile has section very specific to policy since
# it needs to also start location during testing,
# and kill location after testing  is done.
#

PACKAGE_TAG=policy
PACKAGE_NAME = magen_$(PACKAGE_TAG)_service
WHEEL := $(PACKAGE_NAME)-1.0a1-py3-none-any.whl
# below are needed for installing location, wrapper when building docker image
LOCATION_WHEEL := ../magen_location/dist/magen_location_service-1.0a2-py3-none-any.whl
PYTHON=python3
MAKE=make
SPHINX_DIR=./docs
OS := $(shell uname)
PIP := pip3
SERVER_NAME=policy_server.py
DOCKER_SRC_TAG=magen_policy:v1.0
DOCKER_IMAGE=magen-ps
DOCKER_DIR=docker_$(PACKAGE_TAG)

SERVER_WRAPPER=bash ../policy_scripts/$(PACKAGE_TAG)_server_wrapper.sh

MAGEN_HELPER=../lib/magen_helper

include $(MAGEN_HELPER)/make_common/docker_common.mk
include $(MAGEN_HELPER)/make_common/package_common.mk
include $(MAGEN_HELPER)/make_common/doc_common.mk

default: common_default

update: common_update

stop_docker: common_stop_docker

clean_docker: common_clean_docker

rm_docker: common_rm_docker

all: common_all

clean:
	$(MAKE) -C ../magen_location $@
	$(MAKE) common_clean

package:
	$(MAKE) -C ../magen_location $@
	@cp $(LOCATION_WHEEL) docker_$(PACKAGE_TAG)/
	$(MAKE) common_package

install:
	$(MAKE) -C ../magen_location $@
	$(MAKE) common_install

upload:
	$(MAKE) -C ../magen_location $@
	$(MAKE) common_upload

uninstall:
	$(MAKE) -C ../magen_location $@
	$(MAKE) common_uninstall

SPHINX_API_POLICY_SERVER_OMITS=policy_server/magen_env.py
SPHINX_API_POLICY_APIS_OMITS=

doc_api:
	$(SPHINX_APIDOC) -o $(SPHINX_DIR) --force policy_server $(SPHINX_API_POLICY_SERVER_OMITS)
	$(SPHINX_APIDOC) -o $(SPHINX_DIR) --force policy_apis $(SPHINX_API_POLICY_APIS_OMITS)

# core of "make doc", but which does not also trigger a make for location
doc_build: doc_api common_doc

doc:
	@$(MAKE) -C ../magen_location $@
	@$(MAKE) doc_build

doc_clean:
	@$(MAKE) -C ../magen_location $@
	make -C docs clean

list: common_list

run_unit_test:
	@$(SERVER_WRAPPER) -mode test

pre_test: ;
coverage_report: ;

test: common_test

# see test: for documentation
test_travis: common_test_travis

check: common_check

build_docker: common_build_docker

test_docker_travis: common_test_docker

test_docker: test_docker_travis

run_docker: common_run_docker

runpkg_docker: common_runpkg_docker

.PHONY:  pre_test all build_docker
