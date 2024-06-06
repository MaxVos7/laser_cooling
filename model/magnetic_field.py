import numpy as np
import pylcp

"""
This file represents the magnetic fields in the NL-eEDM laser cooling experiment.

By Max Vos 19/02/2024
"""


def get_magnetic_fields(
        mag_field_in_gauss: float = 1,
        theta_deg: float = 45,
        phi_deg: float = 45
):
    phi = 2 * np.pi / 360 * phi_deg
    theta = 2 * np.pi / 360 * theta_deg

    return pylcp.constantMagneticField(
        mag_field_in_gauss * 1e-4 * np.array(
            [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)]))
