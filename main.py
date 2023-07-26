from fastapi import FastAPI, Depends
from Routes import Jobs, Logs, Settings, Auth
from Routes.Auth import get_current_active_user
from database import init_db

tags_metadata = [
    {"name": "Job Methods", "description": "Any methods that interact with the Jobs"},
    {"name": "Settings Methods", "description": "Settings methods for viewing/saving Settings in ARM"},
    {"name": "Log Methods", "description": "Log file methods"},
    {"name": "Auth Methods", "description": "Authorize sections"},
]
app = FastAPI(openapi_tags=tags_metadata)

app.include_router(Jobs.router,tags=["Job Methods"], dependencies=[Depends(get_current_active_user)])
app.include_router(Logs.router, tags=['Log Methods'], dependencies=[Depends(get_current_active_user)])
app.include_router(Settings.router,tags=["Settings Methods"], dependencies=[Depends(get_current_active_user)])
app.include_router(Auth.router,tags=["Auth Methods"])

# Create db tables if needed
@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def api_health_check():
    return {"message": "ARM API"}
