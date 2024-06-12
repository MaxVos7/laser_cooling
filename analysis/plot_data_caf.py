import matplotlib
import matplotlib.pyplot as plt



matplotlib.use('TkAgg')

from src.model.molecules import CaF, BaF
from src.execution.save_and_load_forces import load_forces, load_forces_from_tarbut
from src.model.helpers import velocity_to_si

import numpy as np

molecules = [CaF, BaF]

saturations = [1.56, 3.81, 7.79, 15.51]
detuning = -0.64
molecule = CaF
vibrational_compensation = [1.16, 1.32, 1.48, 1.65]
intensities = [46, 112, 229, 456]
mag_fields = [0, 6]

fig, axs = plt.subplots(2, 2, figsize=[6, 5], sharex=True, sharey='row')
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

axs = [axs[0,0], axs[0,1], axs[1,0],axs[1,1]]

velocity_end = 56

for i, saturation in enumerate(saturations):
    ax = axs[i]


    ax.grid(True, which='major', alpha=0.5)

    ax.set_title(r'%.1f $mW/cm^2$' % intensities[i])


    for j, mag_field in enumerate(mag_fields):
        if saturation == 0 and mag_field == 0:
            continue

        try:
            velocities, forces = load_forces('obe', detuning, saturation, molecule,
                                             additional_title='%.1f_%.0f' % (mag_field, 45), directory='data_caf')

            forces /= 1000
            forces /= vibrational_compensation[i]
            ax.plot(velocities[0:velocity_end], forces[0:velocity_end], '.-', label=r'%.1f G' % mag_field,
                          linewidth=1,
                          markersize=3,
                          markeredgewidth=2,
                            color=colors[j + 1])
        except:
            print('no data found')

    velocities_tarbut, forces_tarbut = load_forces_from_tarbut(intensities[i])

    ax.plot(velocities_tarbut[0:velocity_end], forces_tarbut[0:velocity_end], '-', label=r'Devlin and Tarbutt (2018)',
            linewidth=2,
            markersize=3,
            markeredgewidth=2, color='black')

    ax.axvline(x=velocity_to_si(np.array([-detuning]), molecule)[0], color='purple', linestyle='-', linewidth=2, alpha=0.4,
                   label='resonant velocity')


axs[0].set_ylabel(r'$10^3 a (m/s^2)$')
axs[2].set_ylabel(r'$10^3 a (m/s^2)$')
axs[2].set_xlabel('v (m/s)')
axs[3].set_xlabel('v (m/s)')
plt.legend(loc='lower center', bbox_to_anchor=(-.1,-.45),
           fancybox=True, shadow=True, ncol=5)
plt.show()
