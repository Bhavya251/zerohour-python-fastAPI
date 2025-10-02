from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging
from auth.routes import router as auth_router
from chat.websocket import websocket_endpoint
from chat.routes import router as chat_router
from users.routes import router as user_router
from database import close_db

app = FastAPI(title="ZeroHour Chat API", version="1.0.0")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "ZeroHour Chat API is running!"}


# Allow origins (frontend URLs)
origins = [
    "http://localhost:3000",  # React local
    "https://zerohour-react.vercel.app/",  # deployed React app
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# Register WebSocket manually
app.websocket("/ws/{user_id}")(websocket_endpoint)
