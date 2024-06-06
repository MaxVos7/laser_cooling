import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
from numpy import trapz
from scipy.integrate import trapezoid

from src.model.molecules import CaF, BaF
from src.execution.save_and_load_forces import load_forces, load_forces_from_tarbut
from force_curve_integration import get_start_velocity, get_end_velocity
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

saturations = np.arange(2, 15.5, .5)
# detunings = [-.5, -1, -1.5, -2]
detunings = [-1, -1.5]
# mag_fields = [.5,1,1.5, 2, 2.5,3]
mag_fields = [2, 2.5,3]

width = 2 * len(mag_fields)
height = 2.5

fig, axs = plt.subplots(1,len(mag_fields),  sharey=True, figsize=(width, height))

interaction_time = 0.8
end_velocity = 0.25
# start_velocity = 4.5

areas = np.zeros(saturations.shape)
for i, mag_field in enumerate(mag_fields):
    axs[i].axhline(y=end_velocity, linestyle='-', linewidth=2, alpha=0.4,
                   label='exit velocity',
                   color=colors[0])
    # axs[i].axhline(y=start_velocity, linestyle='-', linewidth=2, alpha=0.4,
    #                label='enter velocity',
    #                color=colors[0])
    for j, detuning in enumerate(detunings):
        for k, saturation in enumerate(saturations):
            try:
                x, y = load_forces('obe', detuning, saturation, BaF, velocity_in_y=False,
                                   additional_title='%.1f_%.0f' % (mag_field, 45), directory='data_grid_special')

                # areas[k] = get_end_velocity(x, y, start_velocity, interaction_time)
                areas[k] = get_start_velocity(x, y, end_velocity, interaction_time)
            except Exception as e:
                print(e)
                print('saturation: %.1f detuning: %.1f, mag_field: %.1f' % (saturation, detuning, detuning))

        areas[areas == 0] = None
        areas[areas == 4.49] = None
        areas[areas == 4.5] = None
        axs[i].plot(saturations, areas, '.-', label=r'$\delta = %.1f \Gamma$' % (detuning),
                    linewidth=1,
                    markersize=3,
                    markeredgewidth=2,
                    color=colors[j + 1])
        axs[i].grid(True, which='major', alpha=0.5)
        axs[i].set_xlabel(r'saturation')

        areas = np.zeros(saturations.shape)
    axs[i].set_xticks(np.arange(3, 16, 2))
    axs[i].set_title('B = %.1fG' % mag_field)
axs[0].set_ylabel(r'enter velocity  (m/s)')
# axs[0].set_ylabel(r'exit velocity  (m/s)')

axs[1].set_xlabel(r'saturation')
axs[0].legend(loc=3, bbox_to_anchor=(0,-.42),
           fancybox=True, shadow=True, ncol=5)
# axs[0].legend(loc=3, bbox_to_anchor=(.65,-.42),
#            fancybox=True, shadow=True, ncol=5)
plt.savefig('figures/exit_speed_0.25.png',bbox_inches='tight', pad_inches=0.1)
