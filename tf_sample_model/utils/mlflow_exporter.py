from mlflow.entities import Experiment
from tensorflow.python.platform import tf_logging
from tensorflow.python.util.tf_export import estimator_export
from tensorflow_estimator.python.estimator.exporter import Exporter
from mlflow.tracking import MlflowClient
from datetime import datetime

@estimator_export('estimator.MLFlowExporter')
class MLFlowExporter(Exporter):
    """Logs metrics and params to mlflow
    Run :  mlflow ui --backend-store-uri /tmp/mlruns
    to see your dashboard.
    """

    def __init__(self,
                 params={},
                 metrics=[],
                 tracking_uri='/tmp/mlruns',
                 experiment_name=Experiment.DEFAULT_EXPERIMENT_NAME,
                 export_only_final_eval=False):
        self.client = MlflowClient(tracking_uri=tracking_uri)
        self.export_only_final_eval = export_only_final_eval
        experiment = self.client.get_experiment_by_name(experiment_name)
        self.run = self.client.create_run(
            experiment_id=experiment.experiment_id)
        for param, value in params.items():
            self.client.log_param(self.run.info.run_uuid, param, value)
        self.metrics = metrics

    @property
    def name(self):
        return "mlflow-exporter"

    def export(self, estimator, export_path, checkpoint_path,
               eval_result, is_the_final_export):
        if (self.export_only_final_eval and is_the_final_export) or not self.export_only_final_eval:
            tf_logging.info("will export to metrics to mlflow")
            for metric, value in eval_result.items():
                if not self.metrics or (metric in self.metrics):
                    self.client.log_metric(
                        self.run.info.run_uuid, metric, value, int(
                            datetime.now().timestamp()))

        if is_the_final_export:
            self.client.set_terminated(
                self.run.info.run_uuid, end_time=int(
                    datetime.now().timestamp()))

        return None
