# Settings/Stats
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from crud import create_job, get_ripper_settings, update_ui_settings, get_ui_settings, get_apprise_settings, \
    get_abcde_settings
from database import get_db
from exceptions import JobException
from schemas import CreateAndUpdateJob, CreateAndUpdateUISettings, UISettingsSchemas

router = APIRouter()


# Example of Class based view
@cbv(router)
class Settings:
    session: Session = Depends(get_db)
    # API to get stats of the server
    @router.get("/settings/stats")
    def get_stats_for_server(self):
        response = {"data": "ripper_settings"}
        return response

    # Get ripper settings
    @router.get("/settings/ripper")
    def get_ripper_settings(self):
        response = {"data": get_ripper_settings()}
        return response

    # Save ripper settings
    @router.put("/settings/ripper")
    def save_ripper_settings(self, jobs_list: CreateAndUpdateJob):
        try:
            jobs_list = create_job(self.session, jobs_list)
            return jobs_list
        except JobException as cie:
            raise HTTPException(**cie.__dict__)

    # Get abcde config
    @router.get("/settings/get_abcde")
    def get_abcde(self):
        return get_abcde_settings(self.session)

    # Save abcde config
    @router.put("/settings/get_abcde")
    def save_abcde_config(self):
        return {"message": "Hello, get_abcde"}

    # Get apprise config
    @router.get("/settings/get_apprise")
    def get_apprise(self):
        return get_apprise_settings(self.session)

    # Save apprise config
    @router.put("/settings/get_apprise")
    def save_apprise_config(self):
        return {"message": "Hello, get_apprise"}

    # Get ui config
    @router.get("/settings/get_ui_conf")
    def get_ui_conf(self):
        return get_ui_settings(self.session)


# Save ui config
@router.put("/settings/get_ui_conf", response_model=UISettingsSchemas)
def save_ui_conf( new_info: CreateAndUpdateUISettings, session: Session = Depends(get_db)):
    try:
        ui_config = update_ui_settings(session, new_info)
        json_compatible_item_data = jsonable_encoder(ui_config)
        return JSONResponse(content=json_compatible_item_data)
    except JobException as cie:
        raise HTTPException(**cie.__dict__)