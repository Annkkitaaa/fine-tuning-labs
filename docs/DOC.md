# API Documentation

## REST API Endpoints

### Models

#### POST /api/models/upload
Upload model file for fine-tuning.

Request:
- Content-Type: multipart/form-data
- Body: file

Response:
```json
{
  "model_id": "string",
  "path": "string"
}
```

#### GET /api/models/list 
List available models.

Response:
```json
{
  "models": [
    {
      "id": "string",
      "name": "string", 
      "framework": "string"
    }
  ]
}
```

### Training

#### POST /api/training/start
Start fine-tuning process.

Request:
```json
{
  "model_id": "string",
  "framework": "string",
  "hyperparameters": {
    "learning_rate": number,
    "batch_size": number,
    "epochs": number
  }
}
```

Response:
```json
{
  "training_id": "string",
  "status": "pending"
}
```

#### GET /api/training/status/{training_id}
Get training status and metrics.

Response:
```json
{
  "status": "string",
  "metrics": {
    "loss": number,
    "accuracy": number
  }
}
```

# Setup Guide

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

## Backend Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start server:
```bash
uvicorn app.main:app --reload
```

## Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm start
```

## Environment Variables

Backend:
- `MODEL_STORAGE_PATH`: Path to store uploaded models
- `MLFLOW_TRACKING_URI`: MLflow tracking server URI

Frontend:
- `REACT_APP_API_BASE`: Backend API base URL

# Usage Guide

## Model Upload

1. Navigate to Models page
2. Click "Upload Model" button
3. Select model file (.pth, .h5, .pkl)
4. Wait for upload confirmation

## Configuration

1. Select framework matching your model
2. Configure hyperparameters:
   - Learning rate
   - Batch size
   - Number of epochs
3. Adjust advanced settings if needed

## Training

1. Select uploaded model
2. Verify configuration
3. Click "Start Training"
4. Monitor progress in real-time:
   - Loss curves
   - Accuracy metrics
   - Resource usage

## Model Export

1. Wait for training completion
2. Download fine-tuned model
3. Export training metrics

## Best Practices

- Pre-process data before upload
- Start with conservative learning rates
- Monitor validation metrics
- Use early stopping when needed
- Save checkpoints regularly