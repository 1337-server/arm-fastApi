from datetime import datetime
from pydantic import BaseModel
from typing import List


# TO support creation and update APIs
class CreateAndUpdateJob(BaseModel):
    arm_version: str
    crc_id: str
    logfile: str
    start_time: datetime
    stop_time: datetime
    job_length: str
    status: str
    stage: str
    no_of_titles: int
    title: str
    title_auto: str
    title_manual: str
    year: str
    year_auto: str
    year_manual: str
    video_type: str
    video_type_auto: str
    video_type_manual: str
    imdb_id: str
    imdb_id_auto: str
    imdb_id_manual: str
    poster_url: str
    poster_url_auto: str
    poster_url_manual: str
    devpath: str
    mountpoint: str
    hasnicetitle: bool
    errors: str
    disctype: str
    label: str
    path: str
    ejected: bool
    updated: bool
    pid: int
    pid_hash: int


# TO support list and get APIs
class JobSchemas(CreateAndUpdateJob):
    id: int
    class Config:
        orm_mode = True


# To support list Jobs API
class PaginatedJobList(BaseModel):
    limit: int
    offset: int
    data: List[JobSchemas]

class CreateAndUpdateUISettings(BaseModel):
    use_icons: bool
    save_remote_images: bool
    bootstrap_skin: str
    language: str
    index_refresh: int
    database_limit: int
    notify_refresh: int

class UISettingsSchemas(CreateAndUpdateUISettings):
    id: int
    class Config:
        orm_mode = True


class CreateAndUpdateUser(BaseModel):
    user_id: int
    username: str
    password: str
    hash: str
    disabled: bool

class UserSchemas(CreateAndUpdateUser):
    id: int
    class Config:
        orm_mode = True
