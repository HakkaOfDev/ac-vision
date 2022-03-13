from datetime import timedelta
from os import getenv

from redis.commands.json.path import Path
from timeloop import Timeloop

from .redis_client import rclient
from ..handlers.dasan_handler import DasanWorkflow
from ..handlers.rtstack_handler import get_rt_stack
from ..handlers.ubiquiti_handler import UbiquitiWorkflow
from ..sql_app.database import SessionLocal
from ..sql_app.fonction import get_oltip

tl = Timeloop()

session = SessionLocal()
ip = get_oltip(session).ip

@tl.job(interval=timedelta(seconds=15))
def update_cache():

    dasan_workflow = DasanWorkflow(ip)
    rclient.json().set('olt-dasan', Path.rootPath(), dasan_workflow.get_olt())
    rclient.json().set('onus-dasan', Path.rootPath(), dasan_workflow.get_onus())
    rclient.json().set('onus-activity', Path.rootPath(), dasan_workflow.get_onus_active())

    #ubiquiti_workflow = UbiquitiWorkflow('c4a201ea-ffba-4c25-8d71-161c06917464', getenv('API_UNMS_TOKEN'))
    #rclient.json().set('olt-ubiquiti', Path.rootPath(), ubiquiti_workflow.get_olt())
    #rclient.json().set('onus-ubiquiti', Path.rootPath(), ubiquiti_workflow.get_onus())

    rclient.json().set('rt-stack', Path.rootPath(), get_rt_stack())

@tl.job(interval=timedelta(seconds=1))
def update_cache():
    dasan_workflow = DasanWorkflow(ip)

def run_cache():
    tl.start(block=False)
