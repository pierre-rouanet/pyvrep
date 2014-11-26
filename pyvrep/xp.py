import os
import json
import logging

from threading import Thread, Event

import poppytools

from pypot.vrep import from_vrep

from spawn import spawn_vrep


class VrepXp(object):
    def __init__(self, robot_config,
                 port, scene, gui=False):

        self.robot_config = robot_config
        self.port = port
        self.scene = scene
        self.gui = gui

        self._running = Event()

    def start(self):
        self._running.set()
        Thread(target=self._target).start()

    def setup(self):
        self._vrep_proc = spawn_vrep(self.port, self.gui, self.scene, start=True)
        self.robot = from_vrep(self.robot_config, '127.0.0.1', self.port)

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
        self._vrep_proc.terminate()
        self._running.clear()

    def _target(self):
        try:
            self.setup()
            self.run()
        except:
            raise
        finally:
            self.teardown()


class PoppyVrepXp(VrepXp):
    def __init__(self, port, scene, gui=False):
        configfile = os.path.join(os.path.dirname(poppytools.__file__),
                                  'configuration', 'poppy_config.json')

        with open(configfile) as f:
            poppy_config = json.load(f)

        VrepXp.__init__(self, poppy_config, port, scene, gui)
