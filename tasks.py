from robocorp.tasks import task

from app.process import Process
import app.scrape as scrape

@task
def run():
    proces = Process()
    proces.before_run_process()
    proces.run_process()
    proces.after_run_process()

