from datetime import timedelta
from os import getenv

from redis.commands.json.path import Path
from timeloop import Timeloop

from .redis_client import rclient
from ..handlers.dasan_handler import DasanWorkflow
from ..handlers.rtstack_handler import get_rt_stack
from ..handlers.ubiquiti_handler import UbiquitiWorkflow

tl = Timeloop()


@tl.job(interval=timedelta(minutes=1))
def update_cache():
    dasan_workflow = DasanWorkflow('10.59.10.20')
    rclient.json().set('olt-dasan', Path.rootPath(), dasan_workflow.get_olt())
    rclient.json().set('onus-dasan', Path.rootPath(), dasan_workflow.get_onus())

    ubiquiti_workflow = UbiquitiWorkflow('c4a201ea-ffba-4c25-8d71-161c06917464', getenv('API_UNMS_TOKEN'))
    rclient.json().set('olt-ubiquiti', Path.rootPath(), ubiquiti_workflow.get_olt())
    rclient.json().set('onus-ubiquiti', Path.rootPath(), ubiquiti_workflow.get_onus())

    rclient.json().set('rt-stack', Path.rootPath(), get_rt_stack())


def run_cache():
    tl.start(block=False)
