import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from model.hamiltonian import get_hamiltonian
from model.laser_beams import get_frequencies
from model.molecules import CaF, BaF

from math import pow, exp

matplotlib.use('TkAgg')


def model(x: np.ndarray, position: float, width: float, height: float) -> np.ndarray:
    return height * np.sqrt(2 * np.pi) * width * norm.pdf(x, position, width)


def get_broadened_line_width(line_width, saturation):
    return line_width * (1 + saturation) ** (1 / 2) / 2


molecule = BaF
detunings = [0]
lasers_in_use = [0]
names = ['F=1+', 'F=0', 'F=1-', 'F=2']
saturations = [1]

(hamiltonian, E_X, E_A) = get_hamiltonian(molecule)

# freq_E_X = np.array(get_frequencies([0, 1, 2, 3], [0,1], E_X, E_A, 0)) * molecule.line_width_in_MHz
freq_E_X = E_A[0] - E_X

x_axis = np.arange(freq_E_X[-1] - 10, freq_E_X[1] + 10, .1)

plt.vlines(freq_E_X, 0, 1, linestyles='dashed', colors='C5')
for i in np.arange(len(freq_E_X)):
    plt.text(freq_E_X[i] + .1, .9, names[i], c='C5')

eom_freq = 14.03
center_freq = 1.325

print(eom_freq * molecule.line_width_in_MHz, center_freq * molecule.line_width_in_MHz)

freqs = np.array([-2 * eom_freq, - eom_freq, eom_freq, 2 * eom_freq]) + center_freq

saturations = [10 * .4, 10 * .6, 10 * .6, 10 * .4]

laser_structure = np.zeros(shape=x_axis.shape)
for index, freq in enumerate(freqs):
    laser_structure += model(x_axis, freq, get_broadened_line_width(1, saturations[index]), 1)

plt.plot(x_axis, laser_structure)

# for saturation in saturations:
#     for detuning in detunings:
#         freqs = get_frequencies(lasers_in_use, E_X, detuning, 0) * molecule.line_width_in_MHz
#
#         laser_structure = np.zeros(shape=x_axis.shape)
#         for laser in freqs:
#             laser_structure += model(x_axis, laser, get_broadened_line_width(molecule.line_width_in_MHz, saturation), 1)
#
#         plt.plot(x_axis, laser_structure, label=r'det=%.1f $\Gamma$, sat=%.1f' % (detuning, saturation))

plt.xlabel(r'$\Gamma$')
plt.legend()

plt.show()
