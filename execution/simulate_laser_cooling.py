import time

import numpy as np
import pylcp
from typing import Union

from src.model.helpers import velocity_from_si, velocity_to_si
from src.model.molecules import BaF, CaF
from src.execution.save_and_load_forces import save_forces

from src.model.molecules import Molecule, BaF
from src.model.hamiltonian import get_hamiltonian
from src.model.laser_beams import get_laser_beams
from src.model.magnetic_field import get_magnetic_fields

import scipy.constants as cts

'''
This file is responsible for making force-velocity diagrams. There should be no direct PyLCP usage here, 
that responsibility is elsewhere. 
'''

molecules = [CaF, BaF]


def get_forces_from_equation(velocities: np.ndarray,
                             governing_equation: Union[pylcp.obe, pylcp.rateeq],
                             velocity_in_y: bool = True) -> np.ndarray:
    if velocity_in_y:
        velocity_array = np.array([np.zeros(velocities.shape), velocities, np.zeros(velocities.shape)])
    else:
        velocity_array = np.array([velocities, np.zeros(velocities.shape), np.zeros(velocities.shape)])

    governing_equation.generate_force_profile(
        R=np.array([np.zeros(velocities.shape), np.zeros(velocities.shape), np.zeros(velocities.shape)]),
        V=velocity_array,
        name='F'
    )

    if velocity_in_y:
        return governing_equation.profile['F'].F[1]
    else:
        return governing_equation.profile['F'].F[0]


def make_governing_equation(method: str,
                            saturation: float,
                            detuning: float,
                            molecule: Molecule,
                            transitions: list[dict]) -> Union[pylcp.obe, pylcp.rateeq]:
    if method != 'obe' and method != 'rateeq':
        raise Exception('please provide valid method. ie obe or rateeq')

    (hamiltonian, E_X, E_A) = get_hamiltonian(molecule)

    laser_beams = get_laser_beams(detuning, saturation, E_X, E_A, transitions)
    magnetic_fields = get_magnetic_fields(
        mag_field_in_gauss=1,
        theta_deg=45,
        phi_deg=45
    )

    if method == 'obe':
        return pylcp.obe(laser_beams, magnetic_fields, hamiltonian)
    else:
        return pylcp.rateeq(laser_beams, magnetic_fields, hamiltonian)


def simulate(saturation, detuning):
    method = 'rateeq'
    molecule = BaF
    velocities = np.concatenate((
        velocity_from_si(np.arange(0, 1.5, .1), molecule),
        velocity_from_si(np.arange(1.5, 6, .25), molecule)
    ))
    velocity_in_y = True

    omega = 2*np.pi*(cts.c/molecule.wave_length)
    Isat = cts.hbar*omega**3*(2*np.pi*molecule.line_width_in_MHz*1e6)/(12*np.pi*cts.c**2)

    transitions = [
        {'ground': 3, 'excited': 1},  # F = 2 -> F' = 1
        {'ground': 2, 'excited': 0},  # F = 1+ -> F' = 0
        {'ground': 1, 'excited': 1},  # F = 0 -> F' = 1
        {'ground': 0, 'excited': 1},  # F = 1- -> F' = 1
    ]

    forces = get_forces_from_equation(velocities, make_governing_equation(
        method, saturation, detuning, molecule, transitions=transitions,
    ), velocity_in_y=velocity_in_y)

    save_forces(velocities, forces, method, detuning, saturation, molecule, velocity_in_y=velocity_in_y, directory='data_caf')


# start_time = time.time()
#
# simulate(1.2, -1)
#
# print('it took %d seconds' % (time.time() - start_time))
