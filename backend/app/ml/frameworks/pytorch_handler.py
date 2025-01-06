import torch
from typing import Any, Dict
from .base_handler import BaseModelHandler

class PyTorchHandler(BaseModelHandler):
    def load_model(self, path: str) -> torch.nn.Module:
        return torch.load(path)
    
    def save_model(self, model: torch.nn.Module, path: str) -> str:
        torch.save(model, path)
        return path
    
    def predict(self, model: torch.nn.Module, data: torch.Tensor) -> torch.Tensor:
        model.eval()
        with torch.no_grad():
            return model(data)
    
    def train_step(
        self,
        model: torch.nn.Module,
        data: torch.Tensor,
        labels: torch.Tensor,
        optimizer: torch.optim.Optimizer,
        criterion: torch.nn.Module
    ) -> float:
        model.train()
        optimizer.zero_grad()
        outputs = model(data)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        return loss.item()
    
    def train(
        self,
        model: torch.nn.Module,
        train_loader: torch.utils.data.DataLoader,
        criterion: torch.nn.Module,
        optimizer: torch.optim.Optimizer,
        epochs: int,
        device: str = 'cuda'
    ) -> Dict:
        model.to(device)
        history = {'train_loss': []}
        
        for epoch in range(epochs):
            epoch_loss = 0
            for batch_data, batch_labels in train_loader:
                batch_data = batch_data.to(device)
                batch_labels = batch_labels.to(device)
                loss = self.train_step(model, batch_data, batch_labels, optimizer, criterion)
                epoch_loss += loss
            
            history['train_loss'].append(epoch_loss / len(train_loader))
        
        return history