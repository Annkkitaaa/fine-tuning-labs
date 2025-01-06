from typing import Dict, Any, List, Optional, Union
import torch
import torch.nn as nn
import tensorflow as tf
from abc import ABC, abstractmethod

class TransferLearningBase(ABC):
    @abstractmethod
    def freeze_layers(self, layers: List[str]) -> None:
        pass
    
    @abstractmethod
    def unfreeze_layers(self, layers: List[str]) -> None:
        pass
    
    @abstractmethod
    def add_new_head(self, head_config: Dict[str, Any]) -> None:
        pass

class PyTorchTransfer(TransferLearningBase):
    def __init__(self, base_model: nn.Module):
        self.model = base_model
        self.layer_dict = dict(self.model.named_modules())
    
    def freeze_layers(self, layers: List[str]) -> None:
        for name, param in self.model.named_parameters():
            if any(layer in name for layer in layers):
                param.requires_grad = False
    
    def unfreeze_layers(self, layers: List[str]) -> None:
        for name, param in self.model.named_parameters():
            if any(layer in name for layer in layers):
                param.requires_grad = True
    
    def add_new_head(self, head_config: Dict[str, Any]) -> nn.Module:
        num_features = head_config.get('input_dim')
        num_classes = head_config.get('output_dim')
        dropout_rate = head_config.get('dropout_rate', 0.5)
        
        new_head = nn.Sequential(
            nn.Linear(num_features, num_features // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(num_features // 2, num_classes)
        )
        
        return nn.Sequential(self.model, new_head)

class TensorFlowTransfer(TransferLearningBase):
    def __init__(self, base_model: tf.keras.Model):
        self.model = base_model
    
    def freeze_layers(self, layers: List[str]) -> None:
        for layer in self.model.layers:
            if any(layer_name in layer.name for layer_name in layers):
                layer.trainable = False
    
    def unfreeze_layers(self, layers: List[str]) -> None:
        for layer in self.model.layers:
            if any(layer_name in layer.name for layer_name in layers):
                layer.trainable = True
    
    def add_new_head(self, head_config: Dict[str, Any]) -> tf.keras.Model:
        num_classes = head_config.get('output_dim')
        dropout_rate = head_config.get('dropout_rate', 0.5)
        
        x = self.model.output
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(1024, activation='relu')(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        predictions = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
        
        return tf.keras.Model(inputs=self.model.input, outputs=predictions)