import numpy as np
import pylcp

""""
This file represents the laser beams in the NL-eEDM laser cooling experiment.

By Max Vos 19/02/2024
"""

from model.molecules import CaF


def get_laser_beams(
        detuning: float,
        saturation: float,
        E_X: np.ndarray,
        E_A: np.ndarray,
        transitions: list[dict],
) -> pylcp.laserBeams:
    laserbeams = pylcp.laserBeams()

    for i, freq in enumerate(get_frequencies(transitions, E_X, E_A, detuning)):
        laserbeams += pylcp.laserBeams([
            # X direction
            # beam one
            {'kvec': np.array([1., 0., 0.]), 'pol': np.array([0., 0., 1.]),
             'pol_coord': 'cartesian',
             'delta': freq, 's': saturation, 'wb': 10e-3},
            # beam one
            {'kvec': np.array([-1., 0., 0.]), 'pol': np.array([0., 0., 1.]),
             'pol_coord': 'cartesian',
             'delta': freq, 's': saturation, 'wb': 10e-3},

            # Y direction
            # beam one
            {'kvec': np.array([0., 1., 0.]), 'pol': np.array([0., 0., 1.]),
             'pol_coord': 'cartesian',
             'delta': freq, 's': saturation, 'wb': 10e-3},
            # beam one
            {'kvec': np.array([0., -1., 0.]), 'pol': np.array([0., 0., 1.]),
             'pol_coord': 'cartesian',
             'delta': freq, 's': saturation, 'wb': 10e-3},
        ], beam_type=pylcp.gaussianBeam)

    return laserbeams


def get_frequencies(
        transitions: list[dict],
        E_X: np.ndarray,
        E_A: np.ndarray,
        detuning: float
) -> np.ndarray:
    freqs = []

    # freqs = np.array([
    #     -2.9,
    #     24.15,
    #     72.29,
    #     146
    # ])
    #
    # freqs /= CaF.line_width_in_MHz
    # freqs += E_A[1] - E_X[3]
    #
    # return freqs

    freqs = []
    for i, transition in enumerate(transitions):
        freqs.append(E_A[transition['excited']] - E_X[transition['ground']] + detuning)

    return freqs
