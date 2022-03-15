from datetime import timedelta
from os import getenv

from redis.commands.json.path import Path
from timeloop import Timeloop

from .redis_client import rclient
from ..handlers.dasan_handler import DasanWorkflow
from ..handlers.rtstack_handler import get_rt_stack
from ..handlers.ubiquiti_handler import UbiquitiWorkflow
from ..sql_app.fonction import get_setting
from ..sql_app.database import SessionLocal


tl = Timeloop()



@tl.job(interval=timedelta(seconds=15))
def update_cache():
    session = SessionLocal()
    dasan_workflow = DasanWorkflow(get_setting(session, "ip_olt").value)
    if dasan_workflow.is_online():
        rclient.json().set('olt-dasan', Path.rootPath(), dasan_workflow.get_olt())
        rclient.json().set('onus-dasan', Path.rootPath(), dasan_workflow.get_onus())
        rclient.json().set('onus-activity', Path.rootPath(), dasan_workflow.get_onus_active())
    else:
        rclient.json().set('olt-dasan', Path.rootPath(), "None")
        rclient.json().set('onus-dasan', Path.rootPath(), "None")
        rclient.json().set('onus-activity', Path.rootPath(), "None")


def run_cache():
    tl.start(block=False)
