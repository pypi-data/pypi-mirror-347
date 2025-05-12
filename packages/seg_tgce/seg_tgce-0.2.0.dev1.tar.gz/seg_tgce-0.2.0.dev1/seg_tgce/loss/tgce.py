from typing import Any, Literal

import tensorflow as tf
from keras.losses import Loss
from tensorflow import Tensor, cast
from tensorflow import float32 as tf_float32

TARGET_DATA_TYPE = tf_float32

ReliabilityType = Literal["scalar", "features", "pixel"]


def safe_divide(
    numerator: Tensor, denominator: Tensor, epsilon: float = 1e-8
) -> Tensor:
    """Safely divide two tensors, avoiding division by zero."""
    return tf.math.divide(
        numerator, tf.clip_by_value(denominator, epsilon, tf.reduce_max(denominator))
    )


def stable_pow(x: Tensor, p: Tensor, epsilon: float = 1e-8) -> Tensor:
    """Compute x^p safely by ensuring x is within a valid range."""
    return tf.pow(tf.clip_by_value(x, epsilon, 1.0 - epsilon), p)


class TcgeSs(Loss):
    """
    Truncated generalized cross entropy
    for semantic segmentation loss.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        num_classes: int,
        name: str = "TGCE_SS",
        q: float = 0.1,
        noise_tolerance: float = 0.1,
        reliability_type: ReliabilityType = "pixel",
    ) -> None:
        self.q = q
        self.num_classes = num_classes
        self.noise_tolerance = noise_tolerance
        self.reliability_type = reliability_type
        super().__init__(name=name)

    def call(
        self, y_true: tf.Tensor, y_pred: tf.Tensor, lambda_r: tf.Tensor
    ) -> tf.Tensor:
        y_true = cast(y_true, TARGET_DATA_TYPE)
        y_pred = cast(y_pred, TARGET_DATA_TYPE)
        lambda_r = cast(lambda_r, TARGET_DATA_TYPE)

        if self.reliability_type == "scalar":
            lambda_r = tf.reshape(lambda_r, [-1, tf.shape(lambda_r)[-1]])
            lambda_r = tf.expand_dims(tf.expand_dims(lambda_r, 1), 1)
            lambda_r = tf.tile(
                lambda_r, [1, tf.shape(y_pred)[1], tf.shape(y_pred)[2], 1]
            )
        elif self.reliability_type == "features":
            lambda_r = tf.image.resize(lambda_r, tf.shape(y_pred)[1:3])

        y_true_shape = tf.shape(y_true)
        new_shape = tf.concat(
            [y_true_shape[:-2], [self.num_classes, tf.shape(lambda_r)[-1]]], axis=0
        )
        y_true = tf.reshape(y_true, new_shape)

        n_samples = tf.shape(y_pred)[0]
        width = tf.shape(y_pred)[1]
        height = tf.shape(y_pred)[2]

        y_pred = y_pred[..., tf.newaxis]
        y_pred = tf.repeat(y_pred, repeats=[tf.shape(lambda_r)[-1]], axis=-1)

        epsilon = 1e-8
        y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)

        term_r = tf.math.reduce_mean(
            tf.math.multiply(
                y_true,
                safe_divide(
                    (
                        tf.ones(
                            [
                                n_samples,
                                width,
                                height,
                                self.num_classes,
                                tf.shape(lambda_r)[-1],
                            ]
                        )
                        - stable_pow(y_pred, self.q)
                    ),
                    (self.q + epsilon),
                ),
            ),
            axis=-2,
        )

        term_c = tf.math.multiply(
            tf.ones([n_samples, width, height, tf.shape(lambda_r)[-1]]) - lambda_r,
            safe_divide(
                (
                    tf.ones([n_samples, width, height, tf.shape(lambda_r)[-1]])
                    - stable_pow(
                        (1 / self.num_classes)
                        * tf.ones([n_samples, width, height, tf.shape(lambda_r)[-1]]),
                        self.q,
                    )
                ),
                (self.q + epsilon),
            ),
        )

        loss = tf.math.reduce_mean(tf.math.multiply(lambda_r, term_r) + term_c)
        loss = tf.where(tf.math.is_nan(loss), tf.constant(1e-8), loss)

        return loss

    def get_config(
        self,
    ) -> Any:
        """
        Retrieves loss configuration.
        """
        base_config = super().get_config()
        return {**base_config, "q": self.q, "reliability_type": self.reliability_type}
