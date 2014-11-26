import os
import json

from threading import Thread, Event

import poppytools

from pypot.vrep import from_vrep
from pypot.vrep.io import VrepConnectionError

from spawn import spawn_vrep, stop_vrep


class VrepXp(object):

    def __init__(self, robot_config, scene, tracked_collisions=[], gui=False):

        self.robot_config = robot_config
        self.scene = scene
        self.gui = gui
        self.tracked_collisions = tracked_collisions
        self._running = Event()

    def start(self):
        self._running.set()
        Thread(target=self._target).start()

    def setup(self):
        done = False
        self.port = 2000

        while not done and (1024 < self.port < 65535):
            try:
                self._vrep_proc, self.port = spawn_vrep(self.gui, self.scene, start=True)
                self.robot = from_vrep(
                    self.robot_config, '127.0.0.1', self.port, tracked_collisions=self.tracked_collisions)
                done = True

            except VrepConnectionError:
                print 'Error connecting to port:', self.port
                stop_vrep(self.port)
                self.port += 1

    def run(self):
        raise NotImplementedError

    @property
    def running(self):
        return self._running.is_set()

    def wait(self):
        self._running.wait()

    def teardown(self):
        if hasattr(self, 'robot'):
            self.robot.close()
        stop_vrep(self.port)
        self._running.clear()

    def _target(self):
        try:
            self.setup()
            self.run()
        except:
            raise
        finally:
            if hasattr(self, 'port'):
                self.teardown()


class PoppyVrepXp(VrepXp):

    def __init__(self, scene, tracked_collisions=[], gui=False):
        configfile = os.path.join(os.path.dirname(poppytools.__file__),
                                  'configuration', 'poppy_config.json')

        with open(configfile) as f:
            poppy_config = json.load(f)

        VrepXp.__init__(self, poppy_config, scene, tracked_collisions, gui)
