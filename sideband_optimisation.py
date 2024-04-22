import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

import numpy as np
import pylcp

from model.hamiltonian import get_hamiltonian
from model.molecules import BaF, Molecule
from model.magnetic_field import get_magnetic_fields
from model.helpers import velocity_from_si, velocity_to_si, force_to_acceleration
from model.force_function import get_forces_from_equation
from equilibrium_position import x_labels


def make_laser_beams(saturation: float, center_frequency: float, eom_frequency: float,
                     sideband_ratio: list, molecule: Molecule) -> pylcp.laserBeams:
    """
    Give frequencies in MHz
    """

    laserbeams = pylcp.laserBeams()

    laserbeams += pylcp.laserBeams([
        {'kvec': np.array([1., 0., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
         'delta': (center_frequency + eom_frequency), 's': saturation * sideband_ratio[0]},
        {'kvec': np.array([-1., 0., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
         'delta': center_frequency + (eom_frequency), 's': saturation * sideband_ratio[0]},
    ], beam_type=pylcp.infinitePlaneWaveBeam)

    for index in np.arange(1, len(sideband_ratio)):
        laserbeams += pylcp.laserBeams([
            {'kvec': np.array([1., 0., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
             'delta': (center_frequency + (eom_frequency * index)),
             's': saturation * sideband_ratio[index]},
            {'kvec': np.array([-1., 0., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
             'delta': (center_frequency + (eom_frequency * index)),
             's': saturation * sideband_ratio[index]},
            {'kvec': np.array([1., 0., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
             'delta': (center_frequency - (eom_frequency * index)),
             's': saturation * sideband_ratio[index]},
            {'kvec': np.array([-1., 0., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
             'delta': (center_frequency - (eom_frequency * index)),
             's': saturation * sideband_ratio[index]},
        ], beam_type=pylcp.infinitePlaneWaveBeam)

    return laserbeams


molecule = BaF

(hamiltonian, E_X, E_A) = get_hamiltonian(molecule)

mag_field = get_magnetic_fields()

eom_freqs = np.linspace(37, 39, 20) / molecule.line_width_in_MHz
center_freqs = np.linspace(-10, 10, 20) / molecule.line_width_in_MHz
saturation = 10

max_value = 0
best_eom = None
best_center = None
best_first_sideband = None

for first_sideband in np.arange(0,1.1,.1):
    for i, center_freq in enumerate(center_freqs):
        for j, eom_freq in enumerate(eom_freqs):
            laser_beams = make_laser_beams(saturation, center_freq, eom_freq, [0, first_sideband, 1-first_sideband], molecule)

            governing_equation = pylcp.rateeq(laser_beams, mag_field, hamiltonian)

            pop = governing_equation.equilibrium_populations(np.zeros(3), np.zeros(3), 0)

            excited_pop = sum(pop[12:17])

            if excited_pop > max_value:
                max_value = excited_pop
                best_center = center_freq
                best_eom = eom_freq
                best_first_sideband = first_sideband

print(
    max_value,
    best_eom,
    best_center,
    best_first_sideband
)

plt.show()
