from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(title="Server Time API", version="1.0.0")


class TimeResponse(BaseModel):
    """Response model for time endpoint"""
    server_time: str
    timestamp: float


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Server Time API",
        "endpoints": {
            "/time": "Get current server time",
            "/docs": "Interactive API documentation"
        }
    }


@app.get("/time", response_model=TimeResponse, tags=["Time"])
async def get_server_time():
    """
    Returns the current server time
    
    Returns:
        TimeResponse: Current server time in ISO format and Unix timestamp
    """
    now = datetime.now()
    return TimeResponse(
        server_time=now.isoformat(),
        timestamp=now.timestamp()
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

