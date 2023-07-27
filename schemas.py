from datetime import datetime
from pydantic import BaseModel
from typing import List
from pydantic.schema import Optional, Dict


class CreateAndUpdateTrack(BaseModel):
    track_id: int
    job_id: int
    track_number: str
    length: int
    aspect_ratio: str
    fps: float
    main_feature: Optional[bool]
    basename: str
    filename: str
    orig_filename: Optional[str]
    new_filename: Optional[str]
    ripped: Optional[bool]
    status: Optional[str]
    error: Optional[str]
    source: str


class TrackSchemas(CreateAndUpdateTrack):
    track_id: int
    class Config:
        orm_mode = True


class CreateAndUpdateConfig(BaseModel):
    job_id: int
    CONFIG_ID: int
    ARM_CHECK_UDF: bool
    GET_VIDEO_TITLE: bool
    SKIP_TRANSCODE: bool
    VIDEOTYPE: str
    MINLENGTH: str
    MAXLENGTH: str
    MANUAL_WAIT: bool
    MANUAL_WAIT_TIME: int
    RAW_PATH: str
    TRANSCODE_PATH: str
    COMPLETED_PATH: str
    EXTRAS_SUB: str
    INSTALLPATH: str
    LOGPATH: str
    LOGLEVEL: str
    LOGLIFE: int
    DBFILE: str
    WEBSERVER_IP: str
    WEBSERVER_PORT: int
    SET_MEDIA_PERMISSIONS: bool
    CHMOD_VALUE: int
    SET_MEDIA_OWNER: bool
    CHOWN_USER: str
    CHOWN_GROUP: str
    RIPMETHOD: str
    MKV_ARGS: str
    DELRAWFILES: bool
    HASHEDKEYS: Optional[bool]
    HB_PRESET_DVD: str
    HB_PRESET_BD: str
    DEST_EXT: str
    HANDBRAKE_CLI: str
    MAINFEATURE: bool
    HB_ARGS_DVD: str
    HB_ARGS_BD: str
    EMBY_REFRESH: bool
    EMBY_SERVER: str
    EMBY_PORT: str
    EMBY_CLIENT: str
    EMBY_DEVICE: str
    EMBY_DEVICEID: str
    EMBY_USERNAME: str
    EMBY_USERID: str
    EMBY_PASSWORD: str
    EMBY_API_KEY: str
    NOTIFY_RIP: bool
    NOTIFY_TRANSCODE: bool
    PB_KEY: str
    IFTTT_KEY: str
    IFTTT_EVENT: str
    PO_USER_KEY: str
    PO_APP_KEY: str
    OMDB_API_KEY: str


class ConfigSchemas(CreateAndUpdateConfig):
    CONFIG_ID: int

    class Config:
        orm_mode = True


# TO support creation and update APIs
class CreateAndUpdateJob(BaseModel):
    config: ConfigSchemas
    tracks: Optional[List[TrackSchemas]]
    arm_version: str
    crc_id: Optional[str]
    logfile: str
    start_time: datetime
    stop_time: Optional[datetime]
    job_length: Optional[str]
    status: str
    stage: str
    no_of_titles: Optional[int]
    title: str
    title_auto: Optional[str]
    title_manual: Optional[str]
    year: str
    year_auto: Optional[str]
    year_manual: Optional[str]
    video_type: str
    video_type_auto: Optional[str]
    video_type_manual: Optional[str]
    imdb_id: str
    imdb_id_auto: Optional[str]
    imdb_id_manual: Optional[str]
    poster_url: str
    poster_url_auto: Optional[str]
    poster_url_manual: Optional[str]
    devpath: str
    mountpoint: str
    hasnicetitle: bool
    errors: Optional[str]
    disctype: str
    label: str
    path: Optional[str]
    ejected: bool
    updated: bool
    pid: int
    pid_hash: int


# TO support list and get APIs
class JobSchemas(CreateAndUpdateJob):
    job_id: int
    class Config:
        orm_mode = True


# To support list Jobs API
class PaginatedJobList(BaseModel):
    limit: int
    offset: int
    results: List[JobSchemas]


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
