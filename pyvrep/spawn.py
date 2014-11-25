import os
import time
import shutil
import platform

from subprocess import Popen, PIPE
from multiprocessing import Lock

from _env import VREP_PATH

vrep_processes = []
vrep_bin_folder = os.path.join(VREP_PATH,
                               ('vrep.app/Contents/MacOS'
                                if platform.system() == 'Darwin' else ''))
vrep_bin = os.path.join(vrep_bin_folder, 'vrep')

config = os.path.join(vrep_bin_folder, 'remoteApiConnections.txt')
bkp_config = config + '.bkp'

vrep_config_template = """
portIndex1_port                 = {}
portIndex1_debug                = false
portIndex1_syncSimTrigger       = true
"""

_spawn_lock = Lock()


def spawn_vrep(port=19997, gui=False,
               scene=None, start=False):

    if not os.path.exists(bkp_config):
        shutil.move(config, bkp_config)

    args = []
    if not gui:
        args.append('-h')
    if scene is not None:
        args.append(scene)

        if start:
            args.append('-s')

    with _spawn_lock:
        with open(config, 'w') as f:
            f.write(vrep_config_template.format(port))

        p = Popen([vrep_bin] + args, stdout=PIPE)
        vrep_processes.append(p)

        # Just give enough time for vrep to actually starts
        # The remote API server
        time.sleep(2)


def killall_vrep():
    while vrep_processes:
        p = vrep_processes.pop()
        p.terminate()
