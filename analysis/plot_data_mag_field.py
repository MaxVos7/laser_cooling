import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from src.model.molecules import CaF, BaF
from scipy.integrate import trapezoid
from src.model.helpers import velocity_to_si
from src.execution.save_and_load_forces import load_forces, load_forces_from_tarbut
from scipy.integrate import simpson
from force_curve_integration import get_start_velocity, get_end_velocity, get_area_under_curve
import scipy.constants as cts
from numpy import trapz
import numpy as np

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

import numpy as np

molecules = [CaF, BaF]

detuning = -1.5
# angles = np.arange(1,91,1)
saturation = 10
molecule = BaF
interaction_time = .8
start_velocity = 1
end_velocity = 0.5

width = 2 * 3
height = 2.5

fig, axs = plt.subplots(1, 2, sharey=True, figsize=(width, height))
fig.tight_layout()

mag_fields = np.arange(.2, 5.2, .2)
angle = 45
areas = np.empty(mag_fields.shape)
for i, mag_field in enumerate(mag_fields):
    try:
        velocities, forces = load_forces('obe', detuning, saturation, molecule,
                                         velocity_in_y=False, additional_title='%.1f_%.0f' % (mag_field, angle),
                                         directory='data_mag_field')

        areas[i] = get_area_under_curve(velocities, forces, start_velocity, end_velocity)
        # areas[i] = get_end_velocity(velocities,forces,start_velocity, interaction_time)
    except Exception as e:
        print(e)

axs[0].plot(mag_fields, areas, '.-', color=colors[1])

angles = np.arange(1, 91, 1)
areas2 = np.empty(angles.shape)
mag_field = 1
for i, angle in enumerate(angles):
    try:
        velocities, forces = load_forces('obe', detuning, saturation, molecule,
                                         velocity_in_y=False, additional_title='%.1f_%.0f' % (mag_field, angle),
                                         directory='data_mag_field')

        areas2[i] = get_area_under_curve(velocities, forces, start_velocity, end_velocity)
        # areas2[i] = get_end_velocity(velocities,forces,start_velocity, interaction_time)
    except Exception as e:
        print(e)

# axs[0].axhline(y=start_velocity, color=colors[0], linestyle='-', linewidth=2, alpha=.4,
#                label='start velocity')
# axs[1].axhline(y=start_velocity, color=colors[0], linestyle='-', linewidth=2, alpha=.4,
#                label='start velocity')
axs[1].plot(angles, areas2, '.-', color=colors[1])

axs[0].grid(True, which='both')
axs[1].grid(True, which='both')
axs[0].set_title('magnetic field angle 45 deg')
axs[1].set_title('magnetic field strength 1G')
axs[0].set_xlabel(r'magnetic field strength (G)')
axs[0].set_xticks(np.arange(0, 5.5, .5))
axs[0].set_xticklabels([0, None, 1, None, 2, None, 3, None, 4, None, 5])

axs[1].set_xticks(np.arange(0, 91, 5))
axs[1].set_xticklabels([0, None, 10, None, 20, None, 30, None, 40, None, 50, None, 60, None, 70, None, 80, None, 90])

axs[1].set_xlabel(r'magnetic field angle (deg)')
# plt.xlabel(r'magnetic field strength (G)')
# axs[0].set_ylabel(r'exit velocity (m/s)')
axs[0].set_ylabel(r'area ($m/s \times m/s^2$)')

# axs[0].legend(loc=3, bbox_to_anchor=(-.5,-.42),
#            fancybox=True, shadow=True, ncol=4)
# axs[1].legend(loc='lower center', bbox_to_anchor=(.5,-.25),
#            fancybox=True, shadow=True, ncol=3)

plt.savefig('figures/mag_field_area_0.25_1.png', bbox_inches='tight', pad_inches=0.1)
