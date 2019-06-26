import os

import datetime
import logging
from tfx.orchestration.airflow.airflow_runner import AirflowDAGRunner
from ml_metadata.proto import metadata_store_pb2
from airflow.models import Variable
from tf_sample_model.pipeline import create_pipeline # pylint: disable=relative-import


PIPELINE_NAME = Variable.get("tf_sample_model.pipeline_name", "tf_sample_model")
TFX_ROOT = Variable.get("tf_sample_model.tfx_root", "/tmp/tfx")
PIPELINE_ROOT = Variable.get(
    "tf_sample_model.pipeline_root", os.path.join(
        TFX_ROOT, PIPELINE_NAME))
METADATA_DB = Variable.get(
    "tf_sample_model.metadata_db",
    os.path.join(
        PIPELINE_ROOT,
        'metadata'))

metadata_connection_config = None
DB_HOST = Variable.get("tf_sample_model.metadata_connection_config.mysql.host",None)
if DB_HOST :
    DB_PORT = Variable.get("tf_sample_model.metadata_connection_config.mysql.port",3306)
    DB_NAME = Variable.get("tf_sample_model.metadata_connection_config.mysql.database",'tfx_metadata')
    DB_USERNAME = Variable.get("tf_sample_model.metadata_connection_config.mysql.user",'tfx')
    DB_PASSWORD = Variable.get("tf_sample_model.metadata_connection_config.mysql.password",'changeme')
    metadata_connection_config = metadata_store_pb2.ConnectionConfig()
    metadata_connection_config.mysql.host = DB_HOST
    metadata_connection_config.mysql.port = int(DB_PORT)
    metadata_connection_config.mysql.database = DB_NAME
    metadata_connection_config.mysql.user = DB_USERNAME
    metadata_connection_config.mysql.password = DB_PASSWORD


LOGS_ROOT = Variable.get(
    "tf_sample_model.logs.root",
    os.path.join(
        PIPELINE_ROOT,
        'logs'))
LOGS_LEVEL_NAME = Variable.get("tf_sample_model.logs.level", 'INFO')
LOGS_LEVEL = logging.getLevelName(LOGS_LEVEL_NAME)

SCHEDULE_INTERVAL = Variable.get("tf_sample_model.airflow.schedule_interval", None)
START_DATE = Variable.get(
    "tf_sample_model.airflow.start_date",
    datetime.datetime(
        2019,
        1,
        1))

TF_TRANSFORM_FILE = Variable.get(
    "tf_sample_model.tfx.transform_module",
    "/airflow/dags/tf_sample_model/tfx_modules/transform.py")
TF_TRAINER_FILE = Variable.get(
    "tf_sample_model.tfx.tainer_module",
    "/airflow/dags/tf_sample_model/tfx_modules/trainer.py")


INPUT_PATH = Variable.get("tf_sample_model.input_path",
                          'gs://renault-ml-tf-sample-model-dev/datasets/input/tf-records')

TF_SERVING_MODEL_BASEDIR = Variable.get(
    "tf_sample_model.serving_model_basedir",
    'gs://renault-ml-tf-sample-model-dev/datasets/saved_models')


_AIRFLOW_CONFIG = {
    'schedule_interval': SCHEDULE_INTERVAL,
    'start_date': START_DATE,
}

# Logging overrides
_LOGGER_OVERRIDES = {
    'log_root': LOGS_ROOT,
    'log_level': LOGS_LEVEL
}



TFX_PIPELINE = create_pipeline(pipeline_name=PIPELINE_NAME,
                                pipeline_root=PIPELINE_ROOT,
                                input_path=INPUT_PATH,
                                tf_transform_file=TF_TRANSFORM_FILE,
                                tf_trainer_file=TF_TRAINER_FILE,
                                serving_model_basedir=TF_SERVING_MODEL_BASEDIR,
                                metadata_db_root=METADATA_DB,
                                metadata_connection_config=metadata_connection_config,
                                enable_cache=True,
                                additional_pipeline_args={
                                    'logger_args': _LOGGER_OVERRIDES})




AIRFLOW_DAG = AirflowDAGRunner(
    config=_AIRFLOW_CONFIG).run(
        pipeline=TFX_PIPELINE)
