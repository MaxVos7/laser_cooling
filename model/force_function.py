import time
from typing import Union

import numpy as np
import pylcp

from model.hamiltonian import get_hamiltonian
from model.laser_beams import get_laser_beams
from model.magnetic_field import get_magnetic_fields
from model.molecules import BaF, Molecule
from model.helpers import get_estimated_end_time

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

'''
This method provides force in x direction based on velocity in x direction. Provide an array of velocities.
'''


def get_forces(velocity_in_x: np.ndarray,
               method: str,
               saturation: float = 1,
               detuning: float = 0,
               molecule: Molecule = BaF) -> np.ndarray:
    governing_equation = get_governing_equation(method, saturation, detuning, molecule)

    return get_forces_from_equation(velocity_in_x, governing_equation)


def get_forces_from_equation(velocities_in_x: np.ndarray,
                             governing_equation: Union[pylcp.obe, pylcp.rateeq]) -> np.ndarray:
    force_in_x = np.zeros(len(velocities_in_x))
    time_start = time.time()

    for i, v_x in enumerate(velocities_in_x):
        if type(governing_equation) is pylcp.obe:
            governing_equation.generate_force_profile(
                R=np.array([0, 0, 0]),
                V=np.array([v_x, 0, 0]),
                name='F',
                debug=True,
                abs=1e-9
            )
        else:
            governing_equation.generate_force_profile(
                R=np.array([0, 0, 0]),
                V=np.array([v_x, 0, 0]),
                name='F'
            )

        force_in_x[i] = governing_equation.profile['F'].F[0]

        if type(governing_equation) is pylcp.obe:
            print('%d / %d, estimated end at %s' % ((i + 1), len(velocities_in_x),
                                                    get_estimated_end_time(time_start, i, len(velocities_in_x)))
                  )

    return force_in_x


def get_governing_equation(method: str,
                           saturation: float = 1,
                           detuning: float = 0,
                           molecule: Molecule = BaF,
                           ground_states_targeted: list = [0, 1, 2, 3],
                           excited_state_targeted: list = [0, 1]) -> Union[pylcp.obe, pylcp.rateeq]:
    if method != 'obe' and method != 'rateeq':
        raise Exception('please provide valid method. ie obe or rateeq')

    (hamiltonian, E_X, E_A) = get_hamiltonian(molecule)
    laser_beams = get_laser_beams(detuning, saturation, E_X, E_A, ground_states_targeted, excited_state_targeted)
    magnetic_fields = get_magnetic_fields()

    if method == 'obe':
        return pylcp.obe(laser_beams, magnetic_fields, hamiltonian)
    else:
        return pylcp.rateeq(laser_beams, magnetic_fields, hamiltonian)
