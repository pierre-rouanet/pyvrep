import os
import json

import poppytools

from pypot.vrep import from_vrep

from spawn import Vrep, AvakasVrep


class VrepXp(object):
    def __init__(self, creature, scene):
        if creature not in ('poppy', ):
            raise ValueError('Creature should be one of ("poppy", )!')

        if creature == 'poppy':
            configfile = os.path.join(os.path.dirname(poppytools.__file__),
                                      'configuration', 'poppy_config.json')

            with open(configfile) as f:
                self.robot_config = json.load(f)

        if not os.path.exists(scene):
            raise ValueError('{} does not exist!'.format(scene))

        self.scene = scene if os.path.isabs(scene) else os.path.join(os.getcwd(), scene)

    def spawn(self, log=None, gui=False, avakas=False):
        try:
            vrep = AvakasVrep(self.scene) if avakas else Vrep(self.scene, gui)
            self.robot = from_vrep(self.robot_config, '127.0.0.1', 19997)

            self.run()

            if log:
                with open(log, 'w') as f:
                    self.save(f)
        except:
            raise
        finally:
            if hasattr(self, 'robot'):
                self.robot.close()
            vrep.terminate()

        # if log:
        #     with open(log, 'w') as f:
        #         self.save(f)

    def run(self):
        raise NotImplementedError

    def save(self, f):
        raise NotImplementedError
