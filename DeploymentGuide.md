# ZeroHour Chat Application - Deployment Guide

## Overview
ZeroHour is a real-time chat application built with FastAPI (Python), React, and MongoDB. It features a beautiful Dark Neumorphic UI with real-time WebSocket messaging, user authentication, and theme switching.

## Features
- ✅ **Real-time Messaging**: WebSocket-based instant messaging
- ✅ **User Authentication**: JWT-based secure authentication with username/password
- ✅ **Beautiful UI**: Dark Neumorphic design with theme toggle (Dark/Light)
- ✅ **User Search**: Find and start conversations with other users
- ✅ **Responsive Design**: Works on desktop and mobile devices
- ✅ **Persistent Chats**: All messages and chat history stored in MongoDB

## Tech Stack
- **Frontend**: React 19, Tailwind CSS, Shadcn/UI components
- **Backend**: FastAPI, WebSocket support, JWT authentication
- **Database**: MongoDB with Motor async driver
- **Real-time**: WebSocket connections for instant messaging
- **Styling**: Neumorphic design with custom CSS and Tailwind

## Prerequisites
- Node.js (v16 or higher)
- Python 3.11+
- MongoDB
- Git

## Local Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd zerohour-chat
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
MONGO_URL=mongodb://localhost:27017
DB_NAME=zerohour_chat
CORS_ORIGINS=http://localhost:3000
EOF

# Start MongoDB (make sure MongoDB is running)
# On macOS with Homebrew: brew services start mongodb/brew/mongodb-community
# On Ubuntu: sudo systemctl start mongod
# On Windows: Start MongoDB service

# Run the backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
yarn install
# or npm install

# Create .env file
cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
EOF

# Start the frontend
yarn start
# or npm start
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Documentation: http://localhost:8001/docs

## Docker Deployment (Optional)

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install

COPY . .
RUN yarn build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - MONGO_URL=mongodb://mongodb:27017
      - DB_NAME=zerohour_chat
      - CORS_ORIGINS=http://localhost:3000
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:8001

  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

## Environment Variables

### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=zerohour_chat
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## Production Deployment

### 1. Update Environment Variables
Update the frontend .env file with your production backend URL:
```env
REACT_APP_BACKEND_URL=https://api.yourdomain.com
```

### 2. Build for Production
```bash
# Frontend
cd frontend
yarn build

# Backend (no build needed, but ensure all dependencies are installed)
cd backend
pip install -r requirements.txt
```

### 3. Deploy to Cloud Platforms

#### Vercel/Netlify (Frontend)
- Connect your GitHub repository
- Set build command: `yarn build`
- Set build directory: `build`
- Set environment variable: `REACT_APP_BACKEND_URL`

#### Railway/Heroku (Backend)
- Connect your GitHub repository
- Set environment variables in dashboard
- Ensure MongoDB connection string is properly configured

#### MongoDB Atlas (Database)
- Create a MongoDB Atlas cluster
- Update MONGO_URL in backend environment variables
- Whitelist your application IPs

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Users
- `GET /api/users/search?query={query}` - Search users

### Chats
- `GET /api/chats` - Get user's chats
- `POST /api/chats/create?other_user_id={user_id}` - Create new chat
- `GET /api/chats/{chat_id}/messages` - Get chat messages

### WebSocket
- `WS /ws/{user_id}` - Real-time messaging connection

## User Registration Fields
- First Name
- Last Name
- Mobile Number (10 digits)
- Email Address
- Username (unique)
- Password (minimum 6 characters)
- Security Phrase (for account recovery)

## Testing

### Create Test Users
1. Navigate to `/register`
2. Fill out the registration form
3. Login and test messaging

### Test Real-time Messaging
1. Open two browser windows/tabs
2. Login as different users in each
3. Start a chat between them
4. Send messages and verify real-time delivery

## Troubleshooting

### WebSocket Connection Issues
- Ensure backend is running and accessible
- Check CORS configuration
- Verify WebSocket URL format (ws:// for HTTP, wss:// for HTTPS)

### Database Connection
- Verify MongoDB is running
- Check connection string format
- Ensure database permissions

### Authentication Issues
- Verify JWT secret key consistency
- Check token expiration settings
- Ensure proper CORS headers

## Security Considerations
- Change JWT secret key in production
- Use HTTPS in production
- Implement rate limiting
- Validate user input
- Use environment variables for sensitive data

## Performance Optimization
- Enable MongoDB indexing
- Implement message pagination
- Use connection pooling
- Compress static assets
- Enable caching headers

## Support
For issues and questions, please check the logs and ensure all dependencies are properly installed and configured.