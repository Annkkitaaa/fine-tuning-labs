# backend/app/core/transfer_learning.py
import torch
import tensorflow as tf
from typing import Dict, Any

class TransferLearningManager:
    def __init__(self, framework: str):
        self.framework = framework
        self.available_models = self._get_available_models()
    
    def _get_available_models(self) -> Dict[str, Any]:
        if self.framework == "pytorch":
            return {
                "resnet18": torch.hub.load('pytorch/vision', 'resnet18', pretrained=True),
                "vgg16": torch.hub.load('pytorch/vision', 'vgg16', pretrained=True),
                "mobilenet": torch.hub.load('pytorch/vision', 'mobilenet_v2', pretrained=True)
            }
        elif self.framework == "tensorflow":
            return {
                "resnet50": tf.keras.applications.ResNet50(weights='imagenet'),
                "mobilenet": tf.keras.applications.MobileNetV2(weights='imagenet'),
                "efficientnet": tf.keras.applications.EfficientNetB0(weights='imagenet')
            }
    
    def adapt_model(self, base_model: str, num_classes: int, freeze_layers: bool = True) -> Any:
        model = self.available_models[base_model]
        
        if self.framework == "pytorch":
            if freeze_layers:
                for param in model.parameters():
                    param.requires_grad = False
                    
            # Replace final layer
            if isinstance(model, torch.nn.Module):
                num_features = model.fc.in_features
                model.fc = torch.nn.Linear(num_features, num_classes)
                
        elif self.framework == "tensorflow":
            if freeze_layers:
                model.trainable = False
                
            # Add new classification head
            x = tf.keras.layers.GlobalAveragePooling2D()(model.output)
            x = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
            model = tf.keras.Model(inputs=model.input, outputs=x)
            
        return model