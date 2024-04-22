import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from model.force_function import get_governing_equation
from model.molecules import BaF, CaF

import numpy as np

x_labels = [
    r'$\frac{-1}{1_-}$', r'$\frac{0}{1_-}$', r'$\frac{1}{1_-}$',  # F = 1-
    r'$\frac{0}{0}$',  # F = 0
    r'$\frac{-1}{1_+}$', r'$\frac{0}{1_+}$', r'$\frac{1}{1_+}$',  # F = 1+
    r'$\frac{-2}{2}$', r'$\frac{-1}{2}$', r'$\frac{0}{2}$', r'$\frac{1}{2}$', r'$\frac{2}{2}$',  # F = 1
    r'$\frac{0}{0}$',  # F = 0
    r'$\frac{-1}{1}$', r'$\frac{0}{1}$', r'$\frac{1}{1}$',  # F = 1
]
def plot_equilibrium_position():
    saturation = 2
    detuning = 0
    molecule = BaF

    fig, axs = plt.subplots(2, 1, sharex=True)

    rateeq = get_governing_equation(
        'rateeq',
        saturation,
        detuning,
        molecule,
        ground_states_targeted=[0, 1, 2, 3],
        excited_state_targeted=[0, 1])

    pop = rateeq.equilibrium_populations(
        np.zeros(3),
        np.zeros(3),
        0
    )

    axs[0].bar(np.arange(len(pop)), pop, label=r"initial population in F=1-")
    axs[0].legend()

    axs[-1].set_xticks(np.arange(len(x_labels)))
    axs[-1].set_xticklabels(x_labels)
    axs[-1].set_xlabel(r'hyperfine state: $\frac{m_f}{F}$')

    axs[-1].text(11.5, -.15, r'| $\rightarrow$ excited states', color='r')

    plt.show()
