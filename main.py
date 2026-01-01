from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, time
from pydantic import BaseModel, Field
from typing import Optional
import pytz

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


class TimezoneConvertRequest(BaseModel):
    """Request model for timezone conversion"""
    time: str = Field(..., description="Time in HH:MM or HH:MM:SS format", example="15:00")
    from_timezone: str = Field(default="UTC", description="Source timezone", example="UTC")
    to_timezone: str = Field(..., description="Target timezone name or city", example="Москва")


class TimezoneConvertResponse(BaseModel):
    """Response model for timezone conversion"""
    original_time: str
    original_timezone: str
    converted_time: str
    converted_timezone: str
    timezone_offset: str


# Маппинг городов на часовые пояса pytz
CITY_TIMEZONE_MAP = {
    # Россия
    "москва": "Europe/Moscow",
    "moscow": "Europe/Moscow",
    "екатеринбург": "Asia/Yekaterinburg",
    "yekaterinburg": "Asia/Yekaterinburg",
    "новосибирск": "Asia/Novosibirsk",
    "novosibirsk": "Asia/Novosibirsk",
    "владивосток": "Asia/Vladivostok",
    "vladivostok": "Asia/Vladivostok",
    "красноярск": "Asia/Krasnoyarsk",
    "krasnoyarsk": "Asia/Krasnoyarsk",
    "иркутск": "Asia/Irkutsk",
    "irkutsk": "Asia/Irkutsk",
    "калининград": "Europe/Kaliningrad",
    "kaliningrad": "Europe/Kaliningrad",
    "самара": "Europe/Samara",
    "samara": "Europe/Samara",
    "омск": "Asia/Omsk",
    "omsk": "Asia/Omsk",
    "якутск": "Asia/Yakutsk",
    "yakutsk": "Asia/Yakutsk",
    "магадан": "Asia/Magadan",
    "magadan": "Asia/Magadan",
    "петропавловск-камчатский": "Asia/Kamchatka",
    "kamchatka": "Asia/Kamchatka",
    
    # Другие популярные города
    "нью-йорк": "America/New_York",
    "new york": "America/New_York",
    "лондон": "Europe/London",
    "london": "Europe/London",
    "париж": "Europe/Paris",
    "paris": "Europe/Paris",
    "берлин": "Europe/Berlin",
    "berlin": "Europe/Berlin",
    "токио": "Asia/Tokyo",
    "tokyo": "Asia/Tokyo",
    "пекин": "Asia/Shanghai",
    "beijing": "Asia/Shanghai",
    "дубай": "Asia/Dubai",
    "dubai": "Asia/Dubai",
    "сидней": "Australia/Sydney",
    "sydney": "Australia/Sydney",
    
    # Сокращения
    "utc": "UTC",
    "gmt": "GMT",
    "est": "US/Eastern",
    "pst": "US/Pacific",
    "msk": "Europe/Moscow",
}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Server Time API",
        "endpoints": {
            "/time": "Get current server time",
            "/date": "Get current server date",
            "/datetime": "Get current server date and time",
            "/convert": "Convert time between timezones",
            "/timezones": "List available timezones",
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


@app.get("/convert", response_model=TimezoneConvertResponse, tags=["Timezone"])
async def convert_timezone(
    time_str: str = Query(..., description="Time in HH:MM or HH:MM:SS format", example="15:00"),
    from_timezone: str = Query(default="UTC", description="Source timezone", example="UTC"),
    to_timezone: str = Query(..., description="Target timezone or city name", example="Москва")
):
    """
    Convert time from one timezone to another
    
    Args:
        time_str: Time in HH:MM or HH:MM:SS format (e.g., "15:00" or "15:30:45")
        from_timezone: Source timezone (default: UTC). Can be city name or timezone code
        to_timezone: Target timezone or city name (e.g., "Москва", "Екатеринбург", "Europe/Moscow")
    
    Returns:
        TimezoneConvertResponse: Converted time with timezone information
    
    Examples:
        - /convert?time_str=15:00&to_timezone=Екатеринбург (from UTC to Yekaterinburg)
        - /convert?time_str=12:00&from_timezone=UTC&to_timezone=Москва (from UTC to Moscow)
    """
    try:
        # Парсим входное время
        time_parts = time_str.strip().split(":")
        if len(time_parts) == 2:
            hour, minute = int(time_parts[0]), int(time_parts[1])
            second = 0
        elif len(time_parts) == 3:
            hour, minute, second = int(time_parts[0]), int(time_parts[1]), int(time_parts[2])
        else:
            raise ValueError("Invalid time format")
        
        if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
            raise ValueError("Time values out of range")
        
    except (ValueError, IndexError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid time format. Use HH:MM or HH:MM:SS format (e.g., '15:00' or '15:30:45')"
        )
    
    # Получаем часовые пояса
    def get_timezone(tz_name: str) -> pytz.timezone:
        tz_lower = tz_name.lower().strip()
        
        # Проверяем в маппинге городов
        if tz_lower in CITY_TIMEZONE_MAP:
            tz_name = CITY_TIMEZONE_MAP[tz_lower]
        
        # Пробуем получить timezone
        try:
            return pytz.timezone(tz_name)
        except pytz.exceptions.UnknownTimeZoneError:
            # Если не нашли, пробуем добавить континент
            possible_zones = [z for z in pytz.all_timezones if tz_name.lower() in z.lower()]
            if possible_zones:
                return pytz.timezone(possible_zones[0])
            raise HTTPException(
                status_code=400,
                detail=f"Unknown timezone: {tz_name}. Use /timezones endpoint to see available options."
            )
    
    try:
        from_tz = get_timezone(from_timezone)
        to_tz = get_timezone(to_timezone)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing timezones: {str(e)}")
    
    # Создаем datetime объект для сегодняшнего дня с указанным временем
    today = datetime.now().date()
    naive_dt = datetime.combine(today, time(hour, minute, second))
    
    # Локализуем время в исходной timezone
    localized_dt = from_tz.localize(naive_dt)
    
    # Конвертируем в целевую timezone
    converted_dt = localized_dt.astimezone(to_tz)
    
    # Вычисляем offset
    offset = converted_dt.utcoffset()
    hours, remainder = divmod(int(offset.total_seconds()), 3600)
    minutes = remainder // 60
    offset_str = f"UTC{hours:+03d}:{minutes:02d}"
    
    return TimezoneConvertResponse(
        original_time=localized_dt.strftime("%H:%M:%S"),
        original_timezone=f"{from_tz.zone}",
        converted_time=converted_dt.strftime("%H:%M:%S"),
        converted_timezone=f"{to_tz.zone}",
        timezone_offset=offset_str
    )


@app.get("/timezones", tags=["Timezone"])
async def get_available_timezones(
    search: Optional[str] = Query(None, description="Search for specific timezone or city")
):
    """
    Get list of available timezones and cities
    
    Args:
        search: Optional search string to filter timezones
    
    Returns:
        Dictionary with supported cities and all pytz timezones
    """
    cities = list(set(CITY_TIMEZONE_MAP.keys()))
    cities.sort()
    
    if search:
        search_lower = search.lower()
        cities = [c for c in cities if search_lower in c.lower()]
        all_zones = [z for z in pytz.all_timezones if search_lower in z.lower()]
    else:
        all_zones = pytz.all_timezones
    
    return {
        "supported_cities": cities,
        "total_cities": len(cities),
        "pytz_timezones_sample": all_zones[:50] if not search else all_zones,
        "total_pytz_timezones": len(pytz.all_timezones),
        "usage": "Use city name (e.g., 'Москва') or pytz timezone (e.g., 'Europe/Moscow') in convert endpoint"
    }

