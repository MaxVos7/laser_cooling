import numpy as np
import pylcp

"""
This file represents the magnetic fields in the NL-eEDM laser cooling experiment.

By Max Vos 19/02/2024
"""


def get_magnetic_fields():
    theta = 2 * np.pi / 360 * 45

    return pylcp.constantMagneticField(1e-4 * np.array([0, np.sin(theta), np.cos(theta)]))
