"""llaminate model."""

import functools

import keras
import tensorflow as tf

import mlable.layers.embedding

import llaminate.layers

# CONSTANTS ###################################################################

EPSILON = 1e-5

# WITH CACHE ##################################################################

@keras.saving.register_keras_serializable(package='models')
class CacheTransformer(tf.keras.models.Model):
    def __init__(
        self,
        num_layers: int,
        num_heads: int,
        input_dim: int,
        embed_dim: int,
        head_dim: int,
        hidden_dim: int,
        epsilon: float=EPSILON,
        **kwargs
    ) -> None:
        # init
        super(CacheTransformer, self).__init__(**kwargs)
        # config
        self._config = {
            'num_layers': num_layers,
            'num_heads': num_heads,
            'input_dim': input_dim,
            'embed_dim': embed_dim,
            'head_dim': head_dim,
            'hidden_dim': hidden_dim,
            'epsilon': epsilon,}
        # the inputs is always UTF-32-BE bytes => 256
        self._embed = mlable.layers.embedding.TokunEmbedding(input_dim=256, output_dim=embed_dim // input_dim, name='embed')
        # blocks
        self._blocks = [
            llaminate.layers.CacheDecoderBlock(
                num_heads=num_heads,
                embed_dim=embed_dim,
                head_dim=head_dim,
                hidden_dim=hidden_dim,
                sequence_axis=1,
                epsilon=epsilon,
                name='block-{}'.format(__i))
            for __i in range(num_layers)]
        # 8 bits for each input byte
        self._head = tf.keras.layers.Dense(units=8 * input_dim, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', name='head')

    def build(self, inputs_shape: tf.TensorShape) -> None:
        __inputs_shape = list(inputs_shape)
        # the embeddings are entirely defined in the constructor
        self._embed.build(__inputs_shape)
        # update the feature axis after embedding
        __inputs_shape[-1] = self._config['embed_dim']
        # propagate the shapes through the child layers
        for __b in self._blocks: __b.build(__inputs_shape)
        self._head.build(__inputs_shape)
        # register
        self.built = True

    def call(self, inputs: tf.Tensor, attention_mask: tf.Tensor=None, return_logits: bool=True, **kwargs) -> tf.Tensor:
        # embed
        __outputs = self._embed(inputs)
        # blocks
        __outputs = functools.reduce(lambda __x, __b: __b(inputs=__x, attention_mask=attention_mask, position=0, training=True, cache=None)[0], self._blocks, __outputs)
        # decompress
        __outputs = self._head(__outputs)
        # scale
        return __outputs if return_logits else tf.nn.softmax(__outputs, axis=-1)

    def infer(
        self,
        inputs: tf.Tensor,
        attention_mask: tf.Tensor=None,
        return_logits: bool=True,
        cache: list=None,
        position: int=0,
        **kwargs,
    ) -> tuple:
        # init
        __cache = self._config['num_layers'] * [None] if cache is None else cache
        # embed
        __outputs = self._embed(inputs)
        # blocks
        for __i, __block in enumerate(self._blocks):
            __outputs, __cache[__i] = __block(inputs=__outputs, cache=__cache[__i], attention_mask=attention_mask, position=position, training=False)
        # decompress
        __outputs = self._head(__outputs)
        # scale
        __outputs = __outputs if return_logits else tf.nn.softmax(__outputs, axis=-1)
        # used in inference only
        return (__outputs, __cache)

    def get_config(self) -> dict:
        __config = super(CacheTransformer, self).get_config()
        __config.update(self._config)
        return __config

    @classmethod
    def from_config(cls, config) -> tf.keras.layers.Layer:
        return cls(**config)
