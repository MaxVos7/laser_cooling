import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from src.model.molecules import CaF, BaF
from src.model.helpers import velocity_to_si
from src.execution.save_and_load_forces import load_forces, load_forces_from_tarbut
from scipy.integrate import simpson
import scipy.constants as cts
from numpy import trapz
import numpy as np

import numpy as np

molecules = [CaF, BaF]

saturations = [5,10,19]
detunings = [-.5, -1.5,-2]
mag_fields = [1.5,2,2.5]
molecule = BaF

omega = 2 * np.pi * (cts.c / molecule.wave_length)
Isat = cts.hbar * omega ** 3 * (2 * np.pi * molecule.line_width_in_MHz * 1e6) / (12 * np.pi * cts.c ** 2)

fig, axs = plt.subplots(len(detunings),len(mag_fields), sharex=True, sharey='row')

for j, mag_field in enumerate(mag_fields):
    for i, detuning in enumerate(detunings):
        axs[i][j].axvline(x=velocity_to_si(np.array([-detuning]), molecule)[0], color='purple', linestyle='-',
                          linewidth=2, alpha=0.4,
                          label='resonant velocity')
        for k, saturation in enumerate(saturations):
            try:
                velocities, forces = load_forces('obe', detuning, saturation, molecule, velocity_in_y=False,
                                                 additional_title='%.1f_%.0f' % (mag_field, 45),
                                                 directory='data_grid_special')

                forces /= 1000
                axs[i][j].plot(velocities, forces, '.-', label=r'saturation = %.0f' % saturation,
                               linewidth=1,
                               markersize=3,
                               markeredgewidth=2)
            except:
                print('no data found')

        axs[i][j].grid(True, which='major', alpha=0.5)

        # Only set y-axis label for the first column
        if j == 0:
            axs[i][j].set_ylabel(r'$10^3$ a ($m/s^2$)')

        # Only set x-axis label for the last row
        if i == len(mag_fields) - 1:
            axs[i][j].set_xlabel(r'v (m/s)')

        if j == len(detunings) - 1:
            if i == 0:
                axs[i][j].set_ylabel(r'$\delta$ = %.1f $\Gamma$' % detunings[i], fontsize=12)
            else:
                axs[i][j].set_ylabel(r'$\delta$ = %.1f $\Gamma$' % detunings[i], fontsize=12)
            axs[i][j].yaxis.set_label_position("right")
            axs[i][j].yaxis.tick_right()

# row_labels = [r'B = $%.1f G$' % mag_field for mag_field in mag_fields]
# for i, label in enumerate(row_labels):
#     fig.text(0.91, 0.5 / len(mag_fields) + (len(mag_fields) - 1 - i) / len(mag_fields), label,
#              va='center', ha='left', rotation=90, transform=fig.transFigure)


axs[0][0].set_title('B = %.1f G' % mag_fields[0])
axs[0][1].set_title('B = %.1f G' % mag_fields[1])
axs[0][2].set_title('B = %.0f G' % mag_fields[2])

plt.legend(loc='lower center', bbox_to_anchor=(-0.7, -1),
           fancybox=True, shadow=True, ncol=3)
plt.savefig('figures/force_curves_alternative', bbox_inches='tight', pad_inches=0.1)
