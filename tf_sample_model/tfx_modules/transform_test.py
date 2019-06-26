import os
import tempfile
import unittest
import apache_beam as beam
import tensorflow_data_validation as tfdv
import tensorflow_transform as tft
from tensorflow_transform.tf_metadata import dataset_metadata
from tensorflow_transform.tf_metadata import dataset_schema
from tensorflow_transform.tf_metadata import schema_utils
from tensorflow_transform.beam import impl as beam_impl
from .transform import preprocessing_fn


class TransformExecutorTest(unittest.TestCase):

    def setUp(self):
        super(TransformExecutorTest, self).setUp()
        #datasets_path = "gs://tf-sample-model-dev/datasets"
        #self.schema_path = os.path.join(
        #    datasets_path, 'schema_gen/schema.pbtxt')
        #self.input_dir = os.path.join(
        #    datasets_path, 'exam_gen/train/*.gz')


    def test_preprocessing_fn(self):
        print("implement me!")

if __name__ == '__main__':
    unittest.main()
