# 🚀 ZeroHour Chat - Backend API

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.110.1-green?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/MongoDB-5.0-green?style=for-the-badge&logo=mongodb" alt="MongoDB">
  <img src="https://img.shields.io/badge/WebSocket-Real--time-orange?style=for-the-badge" alt="WebSocket">
  <img src="https://img.shields.io/badge/JWT-Authentication-red?style=for-the-badge" alt="JWT">
</div>

## 📖 Overview

The ZeroHour Chat backend is a high-performance FastAPI application that provides real-time messaging capabilities, secure user authentication, and a comprehensive REST API for chat management. Built with modern Python async/await patterns and WebSocket support.

## ✨ Features

### 🔐 Authentication & Security
- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - pbkdf2_sha256 encryption for user passwords
- **Security Phrase** - Additional account recovery mechanism
- **CORS Protection** - Configurable cross-origin resource sharing
- **Input Validation** - Pydantic models for request/response validation

### 🚀 Real-time Features
- **WebSocket Support** - Bidirectional real-time communication
- **Connection Management** - Automatic connection handling and cleanup
- **Message Broadcasting** - Efficient message distribution to chat participants
- **Online Status** - Real-time user online/offline status tracking

### 💾 Data Management
- **MongoDB Integration** - Async MongoDB operations with Motor driver
- **User Management** - Complete user registration and profile management
- **Chat System** - One-to-one chat creation and management
- **Message Storage** - Persistent message history with timestamps

## 🏗️ Architecture

### API Structure
```
/api/
├── 🔐 auth/
│   ├── POST /register     # User registration
│   ├── POST /login        # User authentication  
│   └── POST /logout       # User logout
├── 👥 users/
│   └── GET /search        # Search users by name/username
├── 💬 chats/
│   ├── GET /              # Get user's chats
│   ├── POST /create       # Create new chat
│   └── GET /{id}/messages # Get chat messages
└── 🔌 /ws/{user_id}       # WebSocket connection
```

### Database Schema
```python
# User Document
{
  "user_id": "uuid4-string",
  "first_name": "string", 
  "last_name": "string",
  "mobile_no": "string",
  "email": "email-string",
  "username": "unique-string",
  "password_hash": "hashed-password",
  "security_phrase": "string",
  "created_at": "datetime",
  "is_online": "boolean"
}

# Chat Document  
{
  "chat_id": "uuid4-string",
  "participants": ["user_id_1", "user_id_2"],
  "created_at": "datetime",
  "last_message": "string",
  "last_message_time": "datetime"
}

# Message Document
{
  "message_id": "uuid4-string",
  "chat_id": "string",
  "sender_id": "string", 
  "content": "string",
  "timestamp": "datetime",
  "message_type": "text"
}
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- MongoDB 5.0 or higher
- pip or poetry for dependency management

### Installation
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### Configuration
```bash
# .env file
MONGO_URL=mongodb://localhost:27017
DB_NAME=zerohour_chat
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Running the Server
```bash
# Development server with auto-reload
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Production server
uvicorn server:app --host 0.0.0.0 --port 8001

# With specific number of workers
uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4
```

### Verify Installation
```bash
# Check API health
curl http://localhost:8001/api/

# Access interactive API documentation
open http://localhost:8001/docs
```

## 📦 Dependencies

### Core Dependencies
```python
fastapi==0.110.1          # Modern web framework
uvicorn==0.25.0           # ASGI server
mongodb==4.5.0            # MongoDB driver
motor==3.3.1              # Async MongoDB driver
pydantic>=2.6.4           # Data validation
```

### Authentication & Security
```python
python-jose[cryptography]>=3.3.0  # JWT handling
passlib[bcrypt]>=1.7.4            # Password hashing
pyjwt>=2.10.1                     # JWT tokens
cryptography>=42.0.8              # Cryptographic functions
```

### Utilities
```python
python-dotenv>=1.0.1      # Environment variables
python-multipart>=0.0.9   # Form data handling
requests>=2.31.0          # HTTP client
websockets>=15.0.1        # WebSocket support
```

## 🔧 Configuration

### Environment Variables
```bash
# Database Configuration
MONGO_URL=mongodb://localhost:27017        # MongoDB connection string
DB_NAME=zerohour_chat                      # Database name

# Security Configuration  
SECRET_KEY=your-secret-jwt-key            # JWT secret (change in production)
ACCESS_TOKEN_EXPIRE_MINUTES=30            # Token expiration time

# CORS Configuration
CORS_ORIGINS=http://localhost:3000         # Allowed origins (comma-separated)
```

### MongoDB Setup
```bash
# Install MongoDB locally
# macOS with Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community

# Ubuntu/Debian
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb

# Windows
# Download and install from https://www.mongodb.com/try/download/community

# Verify MongoDB is running
mongosh --eval "db.adminCommand('ping')"
```

## 🔌 API Reference

### Authentication Endpoints

#### POST `/api/auth/register`
Register a new user account.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe", 
  "mobile_no": "9876543210",
  "email": "john.doe@example.com",
  "username": "johndoe123",
  "password": "password123",
  "security_phrase": "my favorite color is blue"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_data": {
    "user_id": "uuid-string",
    "username": "johndoe123",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }
}
```

#### POST `/api/auth/login`
Authenticate user and get access token.

**Request Body:**
```json
{
  "username": "johndoe123",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer", 
  "user_data": {
    "user_id": "uuid-string",
    "username": "johndoe123",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }
}
```

#### POST `/api/auth/logout`
Logout user and update online status.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

### User Management Endpoints

#### GET `/api/users/search`
Search users by name or username.

**Query Parameters:**
- `query` (string): Search term

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "user_id": "uuid-string",
    "username": "janedoe",
    "first_name": "Jane",
    "last_name": "Doe", 
    "is_online": true
  }
]
```

### Chat Management Endpoints

#### GET `/api/chats`
Get all chats for the authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "chat_id": "uuid-string",
    "other_user": {
      "user_id": "uuid-string",
      "username": "janedoe",
      "first_name": "Jane",
      "last_name": "Doe",
      "is_online": true
    },
    "last_message": "Hello there!",
    "last_message_time": "2024-01-01T12:00:00Z",
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

#### POST `/api/chats/create`
Create a new chat with another user.

**Query Parameters:**
- `other_user_id` (string): ID of the user to chat with

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "chat_id": "uuid-string",
  "participants": ["user_id_1", "user_id_2"],
  "created_at": "2024-01-01T12:00:00Z",
  "last_message": null,
  "last_message_time": null
}
```

#### GET `/api/chats/{chat_id}/messages`
Get all messages for a specific chat.

**Path Parameters:**
- `chat_id` (string): Chat ID

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "message_id": "uuid-string",
    "content": "Hello there!",
    "timestamp": "2024-01-01T12:00:00Z",
    "sender": {
      "user_id": "uuid-string",
      "username": "johndoe123",
      "first_name": "John",
      "last_name": "Doe"
    },
    "is_own_message": true
  }
]
```

### WebSocket Connection

#### WS `/ws/{user_id}`
Real-time messaging WebSocket connection.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8001/ws/user-id-here');
```

**Send Message:**
```json
{
  "chat_id": "uuid-string",
  "content": "Hello there!"
}
```

**Receive Message:**
```json
{
  "message_id": "uuid-string", 
  "chat_id": "uuid-string",
  "content": "Hello there!",
  "timestamp": "2024-01-01T12:00:00Z",
  "sender": {
    "user_id": "uuid-string",
    "username": "johndoe123",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

## 🔧 Core Components

### WebSocket Connection Manager
```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message_to_chat(self, message: dict, chat_id: str):
        # Broadcast message to all chat participants
        chat = await db.chats.find_one({"chat_id": chat_id})
        if chat:
            for participant_id in chat.get("participants", []):
                if participant_id in self.active_connections:
                    await self.active_connections[participant_id].send_text(json.dumps(message))
```

### Authentication Middleware
```python
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await db.users.find_one({"username": username})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(**user)
```

### Password Security
```python
from passlib.context import CryptContext

# Password encryption using pbkdf2_sha256 (more compatible than bcrypt)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
```

### Database Models
```python
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str
    last_name: str
    mobile_no: str
    email: EmailStr
    username: str
    security_phrase: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_online: bool = False

class Chat(BaseModel):
    chat_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    participants: List[str]  # List of user_ids
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None

class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chat_id: str
    sender_id: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_type: str = "text"  # text, image, file
```

## 🚀 Performance Optimizations

### Database Indexing
```python
# Recommended MongoDB indexes
db.users.create_index("username", unique=True)
db.users.create_index("email", unique=True)
db.users.create_index([("first_name", 1), ("last_name", 1)])
db.chats.create_index("participants")
db.messages.create_index([("chat_id", 1), ("timestamp", 1)])
```

### Connection Pooling
```python
# MongoDB connection with pooling
client = AsyncIOMotorClient(
    mongo_url,
    maxPoolSize=50,
    minPoolSize=5,
    maxIdleTimeMS=30000,
    serverSelectionTimeoutMS=5000
)
```

### Async Operations
```python
# All database operations are async
async def get_user_chats(user_id: str):
    chats = await db.chats.find({
        "participants": user_id
    }).sort("last_message_time", -1).to_list(100)
    return chats
```

## 🧪 Testing

### Manual API Testing
```bash
# Test user registration
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "mobile_no": "1234567890",
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "security_phrase": "test phrase"
  }'

# Test user login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'

# Test protected endpoint (replace TOKEN with actual token)
curl -X GET http://localhost:8001/api/chats \
  -H "Authorization: Bearer TOKEN"
```

### WebSocket Testing
```javascript
// Test WebSocket connection
const ws = new WebSocket('ws://localhost:8001/ws/user-id-here');

ws.onopen = () => {
  console.log('Connected to WebSocket');
  
  // Send a test message
  ws.send(JSON.stringify({
    chat_id: 'chat-id-here',
    content: 'Hello WebSocket!'
  }));
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};
```

### Unit Testing Setup
```python
# pytest setup for testing
import pytest
from fastapi.testclient import TestClient
from server import app

@pytest.fixture
def client():
    return TestClient(app)

def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "first_name": "Test",
        "last_name": "User", 
        "mobile_no": "1234567890",
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "security_phrase": "test phrase"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## 🚢 Deployment

### Production Configuration
```python
# Use production-ready settings
import os

# Security
SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "zerohour_chat")

# CORS
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8001

# Run application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Cloud Deployment

**Railway/Heroku**
```bash
# Procfile
web: uvicorn server:app --host 0.0.0.0 --port $PORT
```

**AWS Lambda**
```python
# Using Mangum for serverless deployment
from mangum import Mangum
from server import app

handler = Mangum(app)
```

**Google Cloud Run**
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/zerohour-api', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/zerohour-api']
```

## 🐛 Troubleshooting

### Common Issues

**MongoDB Connection Error**
```bash
# Check if MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Check connection string format
MONGO_URL=mongodb://username:password@host:port/database
```

**WebSocket Connection Fails**
```python
# Check CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Be more specific in production
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**JWT Token Issues**
```python
# Verify token creation and validation
import jwt

# Check if SECRET_KEY is consistent
SECRET_KEY = "your-secret-key"
token = jwt.encode({"sub": "username"}, SECRET_KEY, algorithm="HS256")
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

**Password Hashing Error**
```python
# If bcrypt fails, use pbkdf2_sha256
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
hashed = pwd_context.hash("password")
verified = pwd_context.verify("password", hashed)
```

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, debug=True)
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **MongoDB Python Driver**: https://pymongo.readthedocs.io
- **JWT Authentication**: https://pyjwt.readthedocs.io
- **WebSocket Guide**: https://fastapi.tiangolo.com/advanced/websockets/
- **Pydantic Models**: https://pydantic-docs.helpmanual.io

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create virtual environment
3. Install dependencies with `pip install -r requirements.txt`
4. Set up pre-commit hooks
5. Make changes and test thoroughly
6. Submit pull request

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Add docstrings for public methods
- Include proper error handling
- Write tests for new features

---

<div align="center">
  <strong>High-Performance FastAPI Backend for ZeroHour Chat</strong>
  <br>
  <sub>Real-time messaging with modern Python async/await</sub>
</div>