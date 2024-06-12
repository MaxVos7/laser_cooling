import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from src.execution.simulate_laser_cooling import make_governing_equation
from src.model.molecules import BaF, CaF

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

    rateeq = make_governing_equation(
        'rateeq',
        saturation,
        detuning,
        molecule,
        transitions=[
            {'ground': 3, 'excited': 1},
            {'ground': 2, 'excited': 1},
            {'ground': 1, 'excited': 1},
            {'ground': 0, 'excited': 1},
        ]
    )

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


plot_equilibrium_position()