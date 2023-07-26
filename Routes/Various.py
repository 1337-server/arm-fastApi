# Various
@app.get("/read_notification")
async def read_notification(notify_id: str):
    return {"message": f"Hello, {notify_id}"}

@app.get("/notify_timeout")
async def notify_timeout(notify_timeout: str,):
    return {"message": f"Hello, {notify_timeout}"}


@app.get("/search_remote")
async def search_remote(job_id: str, title: str, year: str,):
    return {"message": f"Hello, {job_id} - {title} - {year}"}


@app.get("/enable_dev_mode")
async def enable_dev_mode():
    return {"message": "Hello, {job_id}"}