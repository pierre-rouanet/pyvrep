import time

from pypot.vrep.io import close_all_connections


class VrepXpPool(object):
    def __init__(self, xps):
        self.xps = xps

    def run(self, cpu_count):
        close_all_connections()

        running_xp = []

        for xp in self.xps:
            # Wait for an empty spot in the queue
            while len(running_xp) == cpu_count:
                time.sleep(1)
                running_xp = [rxp for rxp in running_xp if rxp.running]

            # Add the xp to the queue and start it
            running_xp.append(xp)
            xp.start()
