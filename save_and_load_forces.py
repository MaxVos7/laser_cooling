from typing import Optional

import numpy as np

from laser_cooling_simulations.model.helpers import velocity_to_si, force_to_acceleration
from model.molecules import Molecule


def save_forces(velocities: np.ndarray, forces: np.ndarray, method: str, detuning: float, saturation: float,
                molecule: Molecule,
                additional_title: str = ''
                ):
    velocity_force_array = np.stack((velocities, forces), axis=1)

    np.savetxt(make_title(method, detuning, saturation, molecule.get_name(), additional_title), velocity_force_array,
               fmt='%.4e', delimiter=',')


def load_forces(method: str, detuning: float, saturation: float, molecule: Molecule, additional_title: str = '') -> \
        Optional[tuple[np.ndarray, np.ndarray]]:
    title = make_title(method, detuning, saturation, molecule.get_name(), additional_title)
    try:
        velocity_force_array = np.genfromtxt(title, delimiter=',')
    except:
        print('No data found for %s' % title)
        return

    velocities = velocity_to_si(velocity_force_array[:, 0], molecule)
    forces = force_to_acceleration(velocity_force_array[:, 1], molecule)

    return velocities, forces


def make_title(method: str, detuning: float, saturation: float, molecule_name: str,
               additional_title: Optional[str] = None) -> str:
    return 'data/%s_%.2f_%.2f_%s%s.txt' % (
        method, detuning, saturation, molecule_name, '_' + additional_title if additional_title else '')
