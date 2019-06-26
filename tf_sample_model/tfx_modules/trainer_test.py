import os
import unittest

from tensorflow_metadata.proto.v0 import schema_pb2
from tfx.utils import io_utils
import tensorflow as tf
from .trainer import trainer_fn


class TrainerExecutorTest(unittest.TestCase):
    def setUp(self):
        super(TrainerExecutorTest, self).setUp()
        #datasets_path = "gs://tf-sample-model-dev/datasets"
        #
        #schema_path = os.path.join(datasets_path, 'schema_gen/schema.pbtxt')
        #self.hparams = tf.contrib.training.HParams(
        #    train_files=os.path.join(
        #        datasets_path,
        #        'transform/transformed_examples/train/transformed_examples-00000-of-00001.gz'),
        #    eval_files=os.path.join(
        #        datasets_path,
        #        'transform/transformed_examples/eval/transformed_examples-00000-of-00001.gz'),
        #    transform_output=os.path.join(
        #        datasets_path, 'transform/transform_output'),
        #    serving_model_dir=os.path.join(datasets_path, 'serving_model'),
        #)
        #self.schema = io_utils.parse_pbtxt_file(
        #    schema_path, schema_pb2.Schema())

    def test_train(self):
        #tf.logging.set_verbosity(tf.logging.DEBUG)
        #training_spec = trainer_fn(self.hparams, self.schema)
        #
        #tf.estimator.train_and_evaluate(training_spec['estimator'],
        #                                training_spec['train_spec'],
        #                                training_spec['eval_spec'])
        print("implement me!")


if __name__ == '__main__':
    unittest.main()
