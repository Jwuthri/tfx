# -*- coding: utf-8 -*-

from tf_sample_model.utils.tf_transform_support import fill_in_missing, is_numeric

def preprocessing_fn(inputs):
    result = {}
    for feat,tensor in inputs.iteritems():
        tensor = fill_in_missing(tensor)
        result[feat]=tensor
    return result
