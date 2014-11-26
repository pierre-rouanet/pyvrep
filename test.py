import os
import time

from pyvrep.xp import PoppyVrepXp

import poppytools

from poppytools.primitive.walking import WalkingGaitFromMat


class MyWalkingXP(PoppyVrepXp):
    def run(self):
        cpg_filename = os.path.join(os.path.dirname(poppytools.__file__),
                                    'behavior', 'IROS_Normal_Gait.mat')

        walk = WalkingGaitFromMat(self.robot, cpg_filename)
        walk.start()

        time.sleep(30)

        walk.stop()


if __name__ == '__main__':
    xp = MyWalkingXP('../pypot/samples/notebooks/poppy-standing.ttt', gui=True)
    xp2 = MyWalkingXP('../pypot/samples/notebooks/poppy-sitting.ttt', gui=True)
    xp3 = MyWalkingXP('../pypot/samples/notebooks/poppy-sitting.ttt', gui=True)

    xp.start()
    xp2.start()

    xp.wait()
    xp2.wait()
