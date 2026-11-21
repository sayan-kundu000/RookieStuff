"""
Root application entrypoint for RookieStuff.
Allows running with:
    uvicorn main:app --reload
as specified in the project requirements.
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.config import get_settings

    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=(settings.environment == "development"),
    )
