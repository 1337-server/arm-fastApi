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
    job_id: Optional[int]
    CONFIG_ID: Optional[int]
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
    CHOWN_USER: Optional[str]
    CHOWN_GROUP: Optional[str]
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


class CreateAndUpdateRipper(BaseModel):
    ARM_NAME: Optional[str]
    ARM_CHILDREN: Optional[str]
    PREVENT_99: int
    ARM_CHECK_UDF: int
    UMASK: str
    GET_VIDEO_TITLE: int
    ARM_API_KEY: Optional[str]
    DISABLE_LOGIN: int
    SKIP_TRANSCODE: int
    VIDEOTYPE: str
    MINLENGTH: int
    MAXLENGTH: int
    MANUAL_WAIT: int
    MANUAL_WAIT_TIME: int
    DATE_FORMAT: str
    ALLOW_DUPLICATES: int
    MAX_CONCURRENT_TRANSCODES: int
    DATA_RIP_PARAMETERS: Optional[str]
    METADATA_PROVIDER: str
    GET_AUDIO_TITLE: str
    RIP_POSTER: int
    ABCDE_CONFIG_FILE: str
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
    SET_MEDIA_PERMISSIONS: int
    CHMOD_VALUE: int
    SET_MEDIA_OWNER: int
    CHOWN_USER: Optional[str]
    CHOWN_GROUP: Optional[str]
    MAKEMKV_PERMA_KEY: Optional[str]
    RIPMETHOD: str
    RIPMETHOD_DVD: str
    RIPMETHOD_BR: str
    MKV_ARGS: Optional[str]
    DELRAWFILES: int
    HB_PRESET_DVD: str
    HB_PRESET_BD: str
    DEST_EXT: str
    HANDBRAKE_CLI: str
    HANDBRAKE_LOCAL: str
    MAINFEATURE: int
    HB_ARGS_DVD: str
    HB_ARGS_BD: str
    EMBY_REFRESH: int
    EMBY_SERVER: Optional[str]
    EMBY_PORT: int
    EMBY_CLIENT: str
    EMBY_DEVICE: str
    EMBY_DEVICEID: str
    EMBY_USERNAME: Optional[str]
    EMBY_USERID: Optional[str]
    EMBY_PASSWORD: Optional[str]
    EMBY_API_KEY: Optional[str]
    NOTIFY_RIP: int
    NOTIFY_TRANSCODE: int
    NOTIFY_JOBID: int
    PB_KEY: Optional[str]
    IFTTT_KEY: Optional[str]
    IFTTT_EVENT: Optional[str]
    PO_USER_KEY: Optional[str]
    PO_APP_KEY: Optional[str]
    OMDB_API_KEY: Optional[str]
    TMDB_API_KEY: Optional[str]
    JSON_URL: Optional[str]
    APPRISE: Optional[str]


class RipperSchemas(CreateAndUpdateRipper):
    id: int

    class Config:
        orm_mode = True
