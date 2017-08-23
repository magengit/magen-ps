PACKAGE_TAG=location
PACKAGE_NAME = magen_$(PACKAGE_TAG)_service
WHEEL := $(PACKAGE_NAME)-1.0a2-py3-none-any.whl
PYTHON=python3
MAKE=make
SPHINX_DIR=./docs
OS := $(shell uname)
DOCKER_DIR=docker_$(PACKAGE_TAG)

MAGEN_HELPER=../lib/magen_helper

include $(MAGEN_HELPER)/make_common/docker_common.mk
include $(MAGEN_HELPER)/make_common/package_common.mk
include $(MAGEN_HELPER)/make_common/doc_common.mk


default: common_default

clean_docker: common_clean_docker

stop_docker: common_stop_docker

all: common_all

clean: common_clean

package: common_package

install: common_install

upload: common_update

uninstall: common_uninstall

SPHINX_API_DCTX_AGT_SERVER_OMITS= \
	../magen_dctx/dctx_agt_server/dctx_agt_server.py \
	../magen_dctx/dctx_agt_server/dctx_magen_env.py

DOC_PACKAGES=location_server

doc_api:
	$(SPHINX_APIDOC) -o $(SPHINX_DIR) --force ../magen_dctx/dctx_agt_server $(SPHINX_API_DCTX_AGT_SERVER_OMITS)

doc: doc_api common_doc_api common_doc

doc_clean:
	make -C docs clean

check: common_check

build_docker: common_build_docker

run_docker: common_run_docker

.PHONY:  pre_test coverage_report all build_docker<Paste>
