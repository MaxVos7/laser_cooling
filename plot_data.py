import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from model.molecules import CaF, BaF
from save_and_load_forces import load_forces
from laser_cooling_simulations.model.helpers import velocity_to_si
import numpy as np

molecules = [CaF, BaF]

velocities, forces = load_forces('obe', -2.61, 50, CaF, 'both_excited_levels_short')
plt.plot(velocities, forces, 'X-',label=r'sat=50')
velocities, forces = load_forces('obe', -2.61, 100, CaF, 'both_excited_levels_short')
plt.plot(velocities, forces, 'X-',label=r'sat=100')

plt.grid(True, which='both')
plt.legend()

plt.xlabel('v (m/s)')
plt.ylabel(r'a ($m/s^2$)')

plt.show()
