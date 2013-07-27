"""Implements the inner product layer."""

from decaf import base
from decaf.layers import fillers
import numpy as np

class DropoutLayer(base.Layer):
    """A layer that implements the inner product."""

    def __init__(self, **kwargs):
        """Initializes a ReLU layer.
        """
        base.Layer.__init__(self, **kwargs)
        self._ratio = self.spec['ratio']
        filler = fillers.DropoutFiller(ratio=self._ratio)
        self._mask = base.Blob(filler=filler)

    def forward(self, bottom, top):
        """Computes the forward pass."""
        # Get features and output
        features = bottom[0].data()
        output = top[0].init_data(features.shape, features.dtype)
        self._mask.init_data(features.shape, np.bool)
        output[:] = features
        output *= self._mask.data()

    def backward(self, bottom, top, propagate_down):
        """Computes the backward pass."""
        if not propagate_down:
            return 0.
        top_diff = top[0].diff()
        bottom_diff = bottom[0].init_diff()
        bottom_diff[:] = top_diff
        bottom_diff *= self._mask.data()
        return 0.

    def update(self):
        """ReLU has nothing to update."""
        pass
