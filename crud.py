import os
import re
from typing import List

import psutil
from sqlalchemy.orm import Session, joinedload

from exceptions import JobAlreadyExistError, JobNotFoundError, UISettingsNotFoundError
from models import Job, Notifications, UISettings
from schemas import CreateAndUpdateJob, CreateAndUpdateUISettings
import requests
import json


# Function to get list of jobs
def get_all_jobs(session: Session, limit: int, offset: int) -> List[Job]:
    return session.query(Job).offset(offset).limit(limit).all()


# Function to  get info of a particular job
def get_job_info_by_id(session: Session, _id: int) -> Job:
    job_info = session.query(Job).get(_id)
    if job_info is None:
        raise JobNotFoundError
    return job_info


# Function to add a new job info to the database
def create_job(session: Session, job_info: CreateAndUpdateJob) -> Job:
    job_details = session.query(Job).filter(Job.pid_hash == job_info.pid_hash).first()
    if job_details is not None:
        raise JobAlreadyExistError
    print(job_details)
    print(job_info.dict())
    new_job_info = Job(**job_info.dict())
    session.add(new_job_info)
    session.commit()
    session.refresh(new_job_info)
    return new_job_info


# Function to update details of the job
def update_job_info(session: Session, _id: int, info_update: CreateAndUpdateJob) -> Job:
    job_info = get_job_info_by_id(session, _id)

    if job_info is None:
        raise JobNotFoundError

    job_info.title = job_info.title_manual = info_update.title  # clean_for_filename(title)
    job_info.year = job_info.year_manual = info_update.year
    job_info.video_type = job_info.video_type_manual = info_update.video_type
    job_info.imdb_id = job_info.imdb_id_manual = info_update.imdb_id
    job_info.poster_url = job_info.poster_url_manual = info_update.poster_url
    job_info.hasnicetitle = True

    session.commit()
    session.refresh(job_info)

    return job_info


def abandon_job_crud(session: Session, _id: int, ) -> dict:
    job_info = get_job_info_by_id(session, _id)
    json_return = {}
    try:
        job_info.status = "fail"
        job_process = psutil.Process(job_info.pid)
        job_process.terminate()  # or p.kill()
        notification = Notifications(title=f"Job: {job_info.job_id} was Abandoned!",
                                     message=f'Job with id: {job_info.job_id} was successfully abandoned. No files were deleted!')
        session.add(notification)
        session.commit()
    except psutil.NoSuchProcess:
        session.rollback()
        json_return['Error'] = f"Couldn't find job.pid - {job_info.pid}! Reverting db changes."
        print(f"Couldn't find job.pid - {job_info.pid}! Reverting db changes.")
    except psutil.AccessDenied:
        session.rollback()
        json_return['Error'] = f"Access denied abandoning job: {job_info.pid}! Reverting db changes."
        print(f"Access denied abandoning job: {job_info.pid}! Reverting db changes.")
    except Exception as error:
        session.rollback()
        print(f"Job {job_info.job_id} couldn't be abandoned. - {error}")
        json_return["Error"] = str(error)
    if 'Error' in json_return:
        notification = Notifications(title=f"Job ERROR: {job_info.job_id} couldn't be abandoned",
                                     message=json_return["Error"])
        session.add(notification)
        session.commit()
    session.commit()
    session.refresh(job_info)
    if job_info is None:
        raise JobNotFoundError
    return json_return


# Function to delete a job info from the db
def delete_job_info(session: Session, _id: int):
    job_info = get_job_info_by_id(session, _id)

    if job_info is None:
        raise JobNotFoundError

    session.delete(job_info)
    session.commit()

    return


def send_job_to_remote_api(session: Session, _id: int):
    job = get_job_info_by_id(session, _id)
    return_dict = {}
    api_key = 'ARM_API_KEY'

    # This allows easy updates to the API url
    base_url = "https://1337server.pythonanywhere.com"
    url = f"{base_url}/api/v1/?mode=p&api_key={api_key}&crc64={job.crc_id}&t={job.title}" \
          f"&y={job.year}&imdb={job.imdb_id}" \
          f"&hnt={job.hasnicetitle}&l={job.label}&vt={job.video_type}"
    response = requests.get(url)
    req = json.loads(response.text)
    job_dict = job.get_d().items()
    return_dict['config'] = job.config.get_d()
    for key, value in iter(job_dict):
        return_dict[str(key)] = str(value)
    if req['success']:
        return_dict['status'] = "success"
    else:
        return_dict['error'] = req['Error']
        return_dict['status'] = "fail"
    return return_dict


def search(session: Session, search_query: str):
    """ Queries ARMui db for the movie/show matching the query"""
    safe_search = re.sub(r'[^a-zA-Z\d]', '', search_query)
    safe_search = f"%{safe_search}%"
    print('-' * 30)

    posts = session.query(Job).filter(Job.title.like(safe_search)).all()
    search_results = {}
    i = 0
    for jobs in posts:
        search_results[i] = {}
        try:
            search_results[i]['config'] = jobs.config.get_d()
        except AttributeError:
            search_results[i]['config'] = "config not found"
            print("couldn't get config")

        for key, value in iter(jobs.get_d().items()):
            if key != "config":
                search_results[i][str(key)] = str(value)
            # app.logger.debug(str(key) + "= " + str(value))
        i += 1
    return {'success': True, 'mode': 'search', 'results': search_results}


def get_jobs_by_status(session: Session, job_status: str)-> List[Job]:
    if job_status in ("success", "fail"):
        jobs = session.query(Job).filter_by(status=job_status).all()
    else:
        print("Get running jobs")
        jobs = session.query(Job).filter(Job.status.notin_(['fail', 'success'])).all()
    if jobs:
        print("jobs  - we have jobs", jobs)
    return jobs


################################ logs #####################################################
def get_all_logs():
    return None


def delete_log(logfile):
    print(logfile)
    return None


################################# Settings ################################################
def get_ripper_settings():
    # TODO Read from file
    return None


def update_ripper_settings():
    # TODO Read from file
    return None


def get_ui_settings(session: Session) -> UISettings:
    """
    Update/create the ui settings if needed
    :param session: Current db session
    :return: The ui settings
    """
    ui_settings = session.query(UISettings).first()
    if ui_settings is None:
        ui_settings = UISettings(**{'use_icons': False, 'save_remote_images': False, 'bootstrap_skin': 'spacelab',
                                    'language': 'en', 'index_refresh': 2000,
                                    'database_limit': 20, 'notify_refresh': 2000})
        session.add(ui_settings)
        session.commit()
    return session.query(UISettings).first()


def update_ui_settings(session: Session, info_update: CreateAndUpdateUISettings) -> UISettings:
    """
    Update/create the ui settings if needed
    :param session:
    :param info_update:
    :return:
    """
    ui_settings = session.query(UISettings).first()
    # If none found in ui settings create and add it to db
    if ui_settings is None:
        ui_settings = UISettings(**info_update.dict())
        session.add(ui_settings)
    ui_settings.use_icons = info_update.use_icons
    ui_settings.save_remote_images = info_update.save_remote_images
    ui_settings.bootstrap_skin = info_update.bootstrap_skin
    ui_settings.language = info_update.language
    ui_settings.index_refresh = info_update.index_refresh
    ui_settings.database_limit = info_update.database_limit
    ui_settings.notify_refresh = info_update.notify_refresh

    session.commit()
    session.refresh(ui_settings)

    return ui_settings


def get_abcde_settings(session: Session) -> UISettings:
    """
    Update/create the ui settings if needed
    :param session: Current db session
    :return: The ui settings
    """
    # TODO Read from file
    return session.query(UISettings).first()


def get_apprise_settings(session: Session) -> UISettings:
    """
    Update/create the ui settings if needed
    :param session: Current db session
    :return: The ui settings
    """
    # TODO Read from file
    return session.query(UISettings).first()
