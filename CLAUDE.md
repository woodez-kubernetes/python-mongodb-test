# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python application designed to test MongoDB connectivity in a Kubernetes environment. The application continuously attempts to connect to MongoDB, insert test documents, and retrieve them.

## Architecture

- **app.py**: Main application that connects to MongoDB and performs basic CRUD operations
- **Dockerfile**: Containerizes the Python application using Python 3.10-slim base image
- **python-app-pod.yaml**: Kubernetes deployment configuration for the Python app
- **requirements.txt**: Python dependencies (pymongo)

## Environment Configuration

The application uses environment variables for MongoDB connection:
- `MONGO_HOST`: MongoDB hostname (defaults to 'mongodb-service' for K8s)
- `MONGO_PORT`: MongoDB port (defaults to 27017)

## Development Commands

### Python Environment Setup
Always activate a virtual environment before installing dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
```

### Docker Commands
```bash
# Build the Docker image
docker build -t python-mongo-app .

# Run the container
docker run python-mongo-app
```

### Kubernetes Deployment
```bash
kubectl apply -f python-app-pod.yaml
```

## Application Behavior

The app runs in an infinite loop, attempting MongoDB connections every 10 seconds. It:
1. Connects to MongoDB using the configured URI
2. Inserts a test document with timestamp
3. Retrieves the inserted document
4. Handles connection failures gracefully
5. Waits 10 seconds before next attempt

This design accommodates Kubernetes environments where MongoDB may not be immediately available when the Python pod starts.