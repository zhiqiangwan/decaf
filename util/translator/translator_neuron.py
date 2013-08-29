"""Translates the neuron layers."""
from decaf.util.translator import registerer
from decaf.layers import core_layers
import logging


def translator_neuron(cuda_layer, output_shapes):
    """Translates the neuron layers.
    Note: not all neuron layers are supported. We only implemented those that
    are needed for imagenet.
    """
    output_shapes[cuda_layer['name']] = \
        output_shapes[cuda_layer['inputLayers'][0]['name']]
    neurontype = cuda_layer['neuron']['type']
    if neurontype == 'relu':
        return core_layers.ReLULayer(
            name=cuda_layer['name'])
    elif neurontype == 'dropout':
        logging.warning('Using Jeff\'s definition of dropout (no scaling'
                        ' during test). Make sure this is what you need.')
        return core_layers.IdentityLayer(
            name=cuda_layer['name'])
    else:
        raise NotImplementedError('Neuron type %s not implemented yet.'
                                  % neurontype)

registerer.register_translator('neuron', translator_neuron)
