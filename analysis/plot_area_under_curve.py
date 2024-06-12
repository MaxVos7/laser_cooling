import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
from numpy import trapz
from scipy.integrate import trapezoid

from src.model.molecules import CaF, BaF
from src.execution.save_and_load_forces import load_forces, load_forces_from_tarbut
from force_curve_integration import get_start_velocity, get_end_velocity, get_area_under_curve

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

colors_detuning = {
    -.5: colors[1],
    -1: colors[2],
    -1.5: colors[3],
    -2: colors[4],
}

saturations = np.arange(5, 20.5, .5)
detunings = [-.5, -1, -1.5, -2]
# detunings = [-.5, -1, -1.5]
mag_fields = [.5, 1, 1.5, 2, 2.5, 3]
# mag_fields = [1.5, 2, 2.5]

areas = np.empty(saturations.shape)

width = 2 * len(mag_fields)
height = 2.5

fig, axs = plt.subplots(1, len(mag_fields), sharey=True, figsize=(width, height))

interaction_time = 0.85
start_velocity = 4.5
end_velocity = 3.5
velocities, y = load_forces('obe', detunings[0], saturations[0], BaF, velocity_in_y=False,
                            additional_title='%.1f_%.0f' % (mag_fields[0], 45), directory='data_grid_special')

for i, mag_field in enumerate(mag_fields):
    for j, detuning in enumerate(detunings):
        for k, saturation in enumerate(saturations):
            try:
                x, y = load_forces('obe', detuning, saturation, BaF, velocity_in_y=False,
                                   additional_title='%.1f_%.0f' % (mag_field, 45), directory='data_grid_special')

                # areas[k] = - trapezoid(y[start:end], x[start:end])
                # areas[k] = get_start_velocity(x, y, end_velocity, interaction_time)
                areas[k] = get_area_under_curve(x, y, start_velocity, end_velocity)
            except Exception as e:
                areas[k] = None
                print(e)
                # print('no file for saturation: %.1f detuning: %.1f, mag_field: %.1f' % (saturation, detuning, detuning))
        axs[i].plot(saturations, areas, '.-', label=r'$\delta = %.1f \Gamma$' % (detuning),
                    color=colors_detuning[detuning],
                    linewidth=1,
                    markersize=3,
                    markeredgewidth=2)

        areas = np.empty(saturations.shape)
    axs[i].grid(True, which='major', alpha=0.5)
    axs[i].set_xticks(np.arange(3, 16, 2))
    # axs[i].set_xticklabels([3, None, 5, None, 7, None, 9, None, 11, None, 13, None, 15])
    axs[i].set_title('B = %.1fG' % mag_field)
    axs[i].set_xlabel(r'saturation')

axs[0].set_ylabel(r'area ($m/s \times m/s^2$)')

axs[0].legend(loc=3, bbox_to_anchor=(1.3, -.42),
              fancybox=True, shadow=True, ncol=5)
# plt.show()
plt.savefig('figures/area_0.25_1_full.png', bbox_inches='tight', pad_inches=0.1)
