import jax
import jax.numpy as jnp
import numpy as np
from jaxflow.layers.Layer import Layer

# Assume these are in scope:
# from .layer_base import Layer

class Dense(Layer):
    """
    A fully-connected layer: output = inputs @ weight + bias.

    Attributes:
        units (int): Number of output features.
        device (str): 'auto', 'cpu', 'gpu', or 'tpu'. Passed to Variable for device placement.
        shard_devices (list|str|None): Used for multi-device sharding if desired.
        dtype (dtype): The data type of the layer's parameters.
    """
    def __init__(self,
                 units: int,
                 name=None,
                 device='auto',
                 shard_devices=None,
                 dtype=jnp.float32,
                 trainable=True,

                activation=None,
                use_bias=True,
                kernel_initializer='glorot_uniform',
                bias_initializer='zeros',
                kernel_regularizer=None,
                bias_regularizer=None,
                activity_regularizer=None,
                kernel_constraint=None,
                bias_constraint=None,
                 seed = None):
        """
        Initialize the Dense layer.

        Args:
            units (int): Number of output features.
            activation (str or callable, optional): Activation function to apply. Defaults to None.
            use_bias (bool, optional): Whether to include a bias term. Defaults to True.
            kernel_initializer (str or callable, optional): Initializer for the kernel weights. Defaults to 'glorot_uniform'.
            bias_initializer (str or callable, optional): Initializer for the bias
            kernel_regularizer (callable, optional): Regularizer function for the kernel weights. Defaults to None.
            bias_regularizer (callable, optional): Regularizer function for the bias. Defaults to None.
            activity_regularizer (callable, optional): Regularizer function for the layer's output.
            kernel_constraint (callable, optional): Constraint function for the kernel weights. Defaults to None.
            bias_constraint (callable, optional): Constraint function for the bias. Defaults to None.
        """
        super().__init__()
        self.units = units
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer(seed = seed, dtype=dtype)
        self.bias_initializer = bias_initializer(seed = seed, dtype=dtype)
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint
        self.device = device
        self.shard_devices = shard_devices
        self.dtype = dtype
        self.trainable = trainable
        self.seed = seed


    def build(self, input_shape):
        """
        Create weight and bias variables based on input_shape.

        Args:
            input_shape: tuple describing the shape of the inputs.
                         Typically [..., in_features].
        """
        if len(input_shape) == 0:
            raise ValueError("input_shape is empty. Dense layer expects at least one dimension.")
        in_features = input_shape[-1]
        if not isinstance(in_features, int):
            raise ValueError("Could not determine in_features from the last dimension of input_shape.")

        # Initialize parameters (Glorot uniform for weights, zeros for bias).
        w_init = self.kernel_initializer(shape=(in_features, self.units))
        b_init = self.bias_initializer(shape=(self.units,)) if self.use_bias else None

        # Create Variables using the base class add_variable method.
        self.weight = self.add_variable(
            name="weight",
            initial_value=w_init,
            device=self.device,
            shard_devices=self.shard_devices,
            dtype=self.dtype,
            trainable=self.trainable
        )
        if self.use_bias:
            self.bias = self.add_variable(
                name="bias",
                initial_value=b_init,
                device=self.device,
                shard_devices=self.shard_devices,
                dtype=self.dtype,
                trainable=self.trainable
            )

    def call(self, inputs,**kwargs):
        """
        Perform the forward pass: output = inputs @ weight + bias.

        Args:
            inputs (jax.numpy.ndarray): A 2D or higher-rank tensor where
                                        the last dimension = in_features.

        Returns:
            jax.numpy.ndarray: The result of the matrix multiplication + bias addition.
        """
        # Optional shape check
        if inputs.shape[-1] != self.weight.shape[0]:
            raise ValueError(
                f"Expected inputs.shape[-1] ({inputs.shape[-1]}) "
                f"to match weight.shape[0] ({self.weight.shape[0]})."
            )


        outputs = inputs @ self.weight
        if self.use_bias:
            outputs += self.bias
        if self.activation is not None:
            outputs = self.activation(outputs)
        return outputs
