SHELL := /bin/bash
BASE_DIR := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))
BUILD_DIR:=$(BASE_DIR)/build


PIPELINE_NAME:= "tf-sample-model"
PIPELINE_VERSION := $(shell python setup.py --version)

clean:
	@rm -rf $(BUILD_DIR)


.PHONY: prepare-dev-env format test clean build

prepare-dev-env:
	@source $(BASE_DIR)/create-virtual-dev-env.sh

format: prepare-dev-env
	@( \
	   source $(BASE_DIR)/venv/bin/activate; \
	   autopep8 --in-place --aggressive --recursive --in-place --verbose tf_sample_model/; \
	)

test: prepare-dev-env
	@( \
	   source $(BASE_DIR)/venv/bin/activate; \
	   python setup.py test; \
	)


build: clean
	@cd $(BASE_DIR) && zip -r $(PIPELINE_NAME)_model.zip tf_sample_model  -x "*.pyc"
	@rm -rf $(BUILD_DIR)/airflow
	@mkdir -p $(BUILD_DIR)/airflow
	@mv $(BASE_DIR)/$(PIPELINE_NAME)_model.zip $(BUILD_DIR)/airflow/$(PIPELINE_NAME)_$(PIPELINE_VERSION).zip

airflow-validate-dag: build
	@unzip $(BUILD_DIR)/airflow/$(PIPELINE_NAME)_$(PIPELINE_VERSION).zip -d $(BUILD_DIR)/airflow
	@docker run --rm -v $(BUILD_DIR)/airflow:/airflow/dags eu.gcr.io/kubeflow-in-action/local-airflow:tfx-master


publish: airflow-validate-dag
	gsutil -m cp -r $(BUILD_DIR)/airflow/$(PIPELINE_NAME)_$(PIPELINE_VERSION).zip gs://ubm-kfp-software-repository/pipelines/$(PIPELINE_NAME)/$(PIPELINE_VERSION)/airflow/$(PIPELINE_NAME)-$(PIPELINE_VERSION).zip

local-plateform-up:
	@docker-compose up

local-plateform-clean:
	@docker-compose stop
	@docker-compose rm -f
	@docker volume prune

airflow-run:
	@docker-compose up -d airflow
	@docker exec tyre_wear-airflow airflow list_dags
	@docker exec tyre_wear-airflow airflow unpause tyre-wear
	@docker exec tyre_wear-airflow airflow trigger_dag tyre-wear -e `date '+%Y-%m-%dT%H:%M:%SZ'`
	@open http://localhost:8080

open-airflow:
	@docker-compose up -d airflow
	@open http://localhost:8080


open-jupyter:
	@docker-compose up -d jupyter
	@open http://localhost:8081

open-mlflow:
	@docker-compose up -d mlflow
	@open http://localhost:5000

open-tensorboard:
	@docker-compose up -d tensorboard
	@open http://localhost:6006
