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

saturations = np.arange(2, 15.5, .5)
saturations_special = np.arange(5, 20, .5)
detunings = [-.5, -1, -1.5, -2]
mag_field = 2

areas = np.empty(saturations.shape)
areas_special = np.empty(saturations_special.shape)

width = 2 * 2
height = 2.5

fig, axs = plt.subplots(1, 2, sharey=True, figsize=(width, height))

interaction_time = 0.85
start_velocity = 4.5
end_velocity = 3.5

for j, detuning in enumerate(detunings):
    for k, saturation in enumerate(saturations_special):
        try:
            x, y = load_forces('obe', detuning, saturation, BaF, velocity_in_y=False,
                               additional_title='%.1f_%.0f' % (mag_field, 45), directory='data_grid_special')

            # areas[k] = - trapezoid(y[start:end], x[start:end])
            # areas[k] = get_start_velocity(x, y, end_velocity, interaction_time)
            areas_special[k] = get_area_under_curve(x, y, start_velocity, end_velocity)
        except Exception as e:
            areas_special[k] = None
            print(e)
            # print('no file for saturation: %.1f detuning: %.1f, mag_field: %.1f' % (saturation, detuning, detuning))
    axs[0].plot(saturations_special, areas_special, '.-', label=r'$\delta = %.1f \Gamma$' % (detuning),
                color=colors_detuning[detuning],
                linewidth=1,
                markersize=3,
                markeredgewidth=2)

    areas_special = np.empty(saturations_special.shape)

for j, detuning in enumerate(detunings):
    for k, saturation in enumerate(saturations):
        try:
            x, y = load_forces('obe', detuning, saturation, BaF, velocity_in_y=False,
                               additional_title='%.1f_%.0f' % (mag_field, 45), directory='data_grid')

            # areas[k] = - trapezoid(y[start:end], x[start:end])
            # areas[k] = get_start_velocity(x, y, end_velocity, interaction_time)
            areas[k] = get_area_under_curve(x, y, start_velocity, end_velocity)
        except Exception as e:
            areas[k] = None
            print(e)
            # print('no file for saturation: %.1f detuning: %.1f, mag_field: %.1f' % (saturation, detuning, detuning))
    axs[1].plot(saturations, areas, '.-', label=r'$\delta = %.1f \Gamma$' % (detuning),
                color=colors_detuning[detuning],
                linewidth=1,
                markersize=3,
                markeredgewidth=2)

    areas = np.empty(saturations.shape)



axs[0].set_xticks(np.arange(5, 21, 2))
axs[1].set_xticks(np.arange(3, 16, 2))
axs[0].set_xlabel(r'saturation')
axs[1].set_xlabel(r'saturation')
axs[0].grid(True, which='major', alpha=0.5)
axs[1].grid(True, which='major', alpha=0.5)

axs[1].set_title('Standard setup')
axs[0].set_title('Alternative setup')

axs[0].set_ylabel(r'area ($m/s \times m/s^2$)')

axs[0].legend(loc=3, bbox_to_anchor=(-1, -.42),
              fancybox=True, shadow=True, ncol=5)
plt.savefig('figures/special_area_3.5_4.5.png', bbox_inches='tight', pad_inches=0.1)
