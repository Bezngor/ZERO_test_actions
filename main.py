from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(title="Server Time API", version="1.0.0")


class TimeResponse(BaseModel):
    """Response model for time endpoint"""
    server_time: str
    timestamp: float


class DateResponse(BaseModel):
    """Response model for date endpoint"""
    date: str
    year: int
    month: int
    day: int
    weekday: str


class DateTimeResponse(BaseModel):
    """Response model for datetime endpoint"""
    datetime: str
    date: str
    time: str
    timestamp: float
    timezone: str


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Server Time API",
        "endpoints": {
            "/time": "Get current server time",
            "/date": "Get current server date",
            "/datetime": "Get current server date and time",
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


@app.get("/date", response_model=DateResponse, tags=["Date"])
async def get_server_date():
    """
    Returns the current server date
    
    Returns:
        DateResponse: Current date with year, month, day, and weekday
    """
    now = datetime.now()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    return DateResponse(
        date=now.date().isoformat(),
        year=now.year,
        month=now.month,
        day=now.day,
        weekday=weekdays[now.weekday()]
    )


@app.get("/datetime", response_model=DateTimeResponse, tags=["DateTime"])
async def get_server_datetime():
    """
    Returns the current server date and time with detailed information
    
    Returns:
        DateTimeResponse: Complete datetime information including date, time, and timezone
    """
    now = datetime.now()
    
    return DateTimeResponse(
        datetime=now.isoformat(),
        date=now.date().isoformat(),
        time=now.time().isoformat(),
        timestamp=now.timestamp(),
        timezone=now.astimezone().tzname() or "UTC"
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

