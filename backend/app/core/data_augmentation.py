# backend/app/core/data_augmentation.py
import torch
import tensorflow as tf
import albumentations as A
import numpy as np
from typing import List, Dict, Any, Optional, Union
from PIL import Image

class DataAugmentor:
   def __init__(self, framework: str):
       self.framework = framework
       self.transforms = self._get_default_transforms()
       
   def augment(self, data: Any) -> Any:
       if self.framework == "pytorch":
           return self._augment_pytorch(data)
       elif self.framework == "tensorflow":
           return self._augment_tensorflow(data)
   
   def _get_default_transforms(self) -> List[Dict[str, Any]]:
       return [
           A.HorizontalFlip(p=0.5),
           A.RandomBrightnessContrast(p=0.2),
           A.GaussNoise(p=0.2),
           A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=45, p=0.2),
           A.RandomResizedCrop(height=224, width=224, scale=(0.8, 1.0), p=0.5),
           A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=0.3),
           A.Blur(blur_limit=3, p=0.1),
           A.ElasticTransform(alpha=1, sigma=50, alpha_affine=50, p=0.2)
       ]

   def _augment_pytorch(self, data: torch.Tensor) -> torch.Tensor:
       transform = A.Compose(self.transforms)
       augmented = []
       for item in data:
           # Convert tensor to numpy for augmentation
           np_image = item.numpy()
           if np_image.shape[0] in [1, 3, 4]:  # Handle CHW format
               np_image = np.transpose(np_image, (1, 2, 0))
           
           # Apply augmentation
           augmented_image = transform(image=np_image)["image"]
           
           # Convert back to tensor format
           if len(augmented_image.shape) == 3:
               augmented_image = np.transpose(augmented_image, (2, 0, 1))
           augmented.append(augmented_image)
           
       return torch.tensor(augmented)

   def _augment_tensorflow(self, data: tf.Tensor) -> tf.Tensor:
       transform = A.Compose(self.transforms)
       augmented = []
       
       # Convert tensor to numpy for augmentation
       np_images = data.numpy()
       
       for image in np_images:
           augmented_image = transform(image=image)["image"]
           augmented.append(augmented_image)
           
       return tf.convert_to_tensor(augmented)

   def add_transform(self, transform: Dict[str, Any]) -> None:
       """Add custom transform to the pipeline"""
       self.transforms.append(transform)

   def remove_transform(self, transform_name: str) -> None:
       """Remove transform from pipeline by name"""
       self.transforms = [t for t in self.transforms if t.__class__.__name__ != transform_name]

   def get_transforms(self) -> List[Dict[str, Any]]:
       """Get current transform pipeline"""
       return self.transforms

   def set_transforms(self, transforms: List[Dict[str, Any]]) -> None:
       """Set custom transform pipeline"""
       self.transforms = transforms

   def augment_batch(self, data: Union[torch.Tensor, tf.Tensor], batch_size: int) -> Union[torch.Tensor, tf.Tensor]:
       """Augment a batch of images"""
       augmented_data = []
       for i in range(0, len(data), batch_size):
           batch = data[i:i + batch_size]
           augmented_batch = self.augment(batch)
           augmented_data.append(augmented_batch)
           
       if self.framework == "pytorch":
           return torch.cat(augmented_data)
       else:
           return tf.concat(augmented_data, axis=0)