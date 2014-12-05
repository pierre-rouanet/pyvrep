import os
import time
import signal
import platform

from subprocess import Popen, PIPE


if 'VREP_PATH' not in os.environ:
    raise SystemError('Please set the VREP_PATH variable in your environment!')

vrep_path = os.environ['VREP_PATH']
vrep_bin_folder = os.path.join(vrep_path,
                               ('vrep.app/Contents/MacOS'
                                if platform.system() == 'Darwin' else ''))
vrep_bin = os.path.join(vrep_bin_folder, 'vrep')


class Vrep(object):
    def __init__(self, scene, gui):
        args = []

        if not gui:
            args.append('-h')

        args.append(os.path.join(os.getcwd(), scene))
        args.append('-s')

        self.p = Popen([vrep_bin] + args, stdout=PIPE)
        time.sleep(10)

    def terminate(self):
        self.p.terminate()


class AvakasVrep(object):
    def __init__(self, scene, num_proc=99):
        self.num_proc = num_proc
        self.p = Popen(['xvfb-run', '--server-num={}'.format(self.num_proc),
                        vrep_bin, '-h', scene, '-s'])
        time.sleep(20)

    def terminate(self):
        with open('/tmp/.X{}-lock'.format(self.num_proc)) as f:
            pid = int(f.read().strip())

        os.kill(pid, signal.SIGINT)
