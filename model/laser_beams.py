import numpy as np
import pylcp

""""
This file represents the laser beams in the NL-eEDM laser cooling experiment.

By Max Vos 19/02/2024
"""

WAVE_LENGTH = 860e-9


def get_laser_beams(
        detuning: float,
        saturation: float,
        E_X: np.ndarray,
        E_A: np.ndarray,
        ground_levels_to_target: list = [1, 2, 3, 4],
        excited_levels_to_target: list = [0, 1]
) -> pylcp.laserBeams:
    # Selects only some F states to target laser on.

    laserbeams = pylcp.laserBeams()
    for freq in get_frequencies(ground_levels_to_target, excited_levels_to_target, E_X, E_A, detuning):
        laserbeams += pylcp.laserBeams([
            # x direction
            {'kvec': np.array([1., 0., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
             'delta': freq, 's': saturation},
            {'kvec': np.array([-1., 0., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
             'delta': freq, 's': saturation},

            # y direction
            {'kvec': np.array([0., 1., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
             'delta': freq, 's': saturation},
            {'kvec': np.array([0., -1., 0.]), 'pol': np.array([0., 0., 1.]), 'pol_coord': 'cartesian',
             'delta': freq, 's': saturation},
        ], beam_type=pylcp.infinitePlaneWaveBeam)
    return laserbeams


def get_frequencies(
        ground_levels_to_target: list,
        excited_levels_to_target: list,
        E_X: np.ndarray,
        E_A: np.ndarray,
        detuning: float
) -> np.ndarray:
    freqs = []
    for ground in ground_levels_to_target:
        for excited in excited_levels_to_target:
            freqs.append(E_A[excited] - E_X[ground] + detuning)

    return freqs
