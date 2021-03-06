import os
import time
import shutil
import platform

from subprocess import Popen, PIPE
from multiprocessing import Lock

from _env import VREP_PATH

vrep_processes = {}
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


def spawn_vrep(gui=False, scene=None, start=False):

    if not os.path.exists(bkp_config):
        shutil.move(config, bkp_config)

    args = []
    if not gui:
        args.append('-h')
    if scene is not None:
        args.append(os.path.join(os.getcwd(), scene))

        if start:
            args.append('-s')

    with _spawn_lock:
        port = 29997
        while port in vrep_processes:
            port += 1

        with open(config, 'w') as f:
            f.write(vrep_config_template.format(port))

        p = Popen([vrep_bin] + args, stdout=PIPE)
        vrep_processes[port] = p

        # Just give enough time to vrep to
        # actually starts the remote API server
        time.sleep(10 if gui else 2)

    return p, port


def stop_vrep(port):
    vrep_processes.pop(port).terminate()


def killall_vrep():
    [stop_vrep(port) for port in vrep_processes]
