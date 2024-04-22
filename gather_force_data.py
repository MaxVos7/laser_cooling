import time
from multiprocessing import Pool

import numpy as np

from laser_cooling_simulations.model.helpers import velocity_from_si
from model.force_function import get_forces, get_governing_equation, get_forces_from_equation
from model.molecules import BaF, CaF
from save_and_load_forces import save_forces

'''
This file is responsible for making force-velocity diagrams. There should be no direct PyLCP usage here, 
that responsibility is elsewhere. 
'''

molecules = [CaF, BaF]


def simulate(saturation):
    method = 'rateeq'
    molecule = BaF
    velocities = velocity_from_si(np.arange(0, 10, 1), molecule)
    detuning = 0

    print('start of simulation for detuning %s' % detuning)
    forces = get_forces_from_equation(velocities, get_governing_equation(
        method, saturation, detuning, molecule, excited_state_targeted=[1]
    ))

    save_forces(velocities, forces, method, detuning, saturation, molecule)


if __name__ == '__main__':
    """
    Simulation parameters
    """

    saturations = [2]

    start_time = time.time()

    """
    Simulation
    """

    p = Pool(len(saturations))

    p.map(simulate, saturations)

    print('it took %d seconds' % (time.time() - start_time))
