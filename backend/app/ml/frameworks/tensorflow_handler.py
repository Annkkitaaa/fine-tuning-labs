import tensorflow as tf
from typing import Any, Dict
from .base_handler import BaseModelHandler

class TensorFlowHandler(BaseModelHandler):
    def load_model(self, path: str) -> tf.keras.Model:
        return tf.keras.models.load_model(path)
    
    def save_model(self, model: tf.keras.Model, path: str) -> str:
        model.save(path)
        return path
    
    def predict(self, model: tf.keras.Model, data: Any) -> Any:
        return model.predict(data)
    
    def compile_model(
        self,
        model: tf.keras.Model,
        optimizer: str = 'adam',
        loss: str = 'categorical_crossentropy',
        metrics: list = ['accuracy']
    ) -> tf.keras.Model:
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        return model
    
    def train(
        self,
        model: tf.keras.Model,
        train_data: tuple,
        validation_data: tuple = None,
        epochs: int = 10,
        batch_size: int = 32
    ) -> Dict:
        history = model.fit(
            train_data[0],
            train_data[1],
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size
        )
        return history.history