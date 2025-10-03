from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from auth.routes import router as auth_router
#from chat.websocket import websocket_endpoint
from chat.routes import router as chat_router
from users.routes import router as user_router
from erroremail import send_error_email
import traceback

app = FastAPI(title="ZeroHour Chat API", version="1.0.0", debug=True)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "ZeroHour Chat API is running!"}


# Allow origins (frontend URLs)
origins = [
    "https://zerohour-react.vercel.app",  # deployed React app
    "http://localhost:3000"  # React local
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# @app.on_event("shutdown")
# async def shutdown_event():
#     await close_db()

# Register WebSocket manually
#app.websocket("/ws/{user_id}")(websocket_endpoint)


@app.middleware("http")
async def error_email_middleware(request: Request, call_next):
    """Catch all responses and send email on 3xx/4xx/5xx with full traceback."""
    try:
        response = await call_next(request)

        # For HTTP errors (e.g., raised via HTTPException)
        if 300 <= response.status_code < 600 and response.status_code != 307 and request.method != 'OPTIONS':
            body = (
                f"URL: {request.url}\n"
                f"Method: {request.method}\n"
                f"Status Code: {response.status_code}\n"
                f"Full Traceback:\n{traceback.format_exc()}"
            )
            send_error_email(f"🚨 FastAPI Error {response.status_code}", body)

        return response

    except Exception as e:
        # Catch unhandled exceptions
        tb = traceback.format_exc()
        body = (
            f"URL: {request.url}\n"
            f"Method: {request.method}\n"
            f"Error: {str(e)}\n\n"
            f"Full Traceback:\n{tb}"
        )
        send_error_email("🚨 FastAPI Unhandled Exception", body)
        raise


