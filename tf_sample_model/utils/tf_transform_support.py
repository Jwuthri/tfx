# -*- coding: utf-8 -*-

import tensorflow as tf


def fill_in_missing(x):  # copied from taxi_utils example
    """Replace missing values in a SparseTensor.

    Fills in missing values of `x` with '' or 0, and converts to a dense tensor.

    Args:
      x: A `SparseTensor` of rank 2.  Its dense shape should have size at most 1
        in the second dimension.

    Returns:
      A rank 1 tensor where missing values of `x` have been filled in.
    """
    default_value = '' if x.dtype == tf.string else 0
    return tf.squeeze(
        tf.sparse_to_dense(x.indices, [x.dense_shape[0], 1], x.values,
                           default_value),
        axis=1)


def is_numeric(x):
    return x.dtype != tf.string
