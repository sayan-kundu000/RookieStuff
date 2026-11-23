"""
Root application entrypoint for RookieStuff.
Allows running with:
    uvicorn main:app --port 3000
as specified in the project requirements.
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.config import get_settings

    settings = get_settings()
    is_dev = settings.environment == "development"
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=is_dev,
        reload_dirs=["app"] if is_dev else None,
    )
