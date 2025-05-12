from keras.models import Model
from tensorflow import GradientTape

from seg_tgce.loss.tgce import TcgeSs


class ModelMultipleAnnotators(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def train_step(self, data):
        x, y = data

        with GradientTape() as tape:
            y_pred, lambda_r = self(x, training=True)
            loss = self.loss_function.call(y_true=y, y_pred=y_pred, lambda_r=lambda_r)

        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))
        for metric in self.metrics:
            if metric.name == "loss":
                metric.update_state(loss)
            else:
                metric.update_state(y, y_pred)
        return {m.name: m.result() for m in self.metrics}
