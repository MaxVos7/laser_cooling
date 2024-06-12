from src.execution.save_and_load_forces import load_forces_from_tarbut
from src.model.helpers import use_symmetry_force_curve, velocity_to_si
from src.model.molecules import BaF

import matplotlib.pyplot as plt

import numpy as np


velocities = np.array([
    0,
    0.1061419008,
    0.2051545023,
    0.3038992297,
    0.402878493,
    0.5007503152,
    0.6050973017,
    0.7038725554,
    0.8052621334,
    0.9083614884,
    1.00553705,
    1.104692092,
    1.205578729,
    1.304226467,
    1.406894346,
    1.506439833,
    1.608919075,
    1.710902396,
    1.809940246,
    1.909945374,
    2.014229267,
    2.113645235,
    2.21392439,
    2.31493455,
    2.416153132,
    2.516331367,
    2.616346627,
    2.716417552,
    2.817057021,
    2.914364462,
    3.019697945,
    3.115753565,
    3.218555633,
    3.31857878,
    3.419480484,
    3.521144532,
    4.778150995,
    6.035921883,
    7.290710506,
    8.550703851,
    9.810749643,
    11.06190102,
    12.3229471,
    13.57828218,
    14.83830872,
    16.09590861,
    17.35101147,
    18.61021787,
    19.86844661,
    21.12510923,
    22.3812792,
    23.64080449,
    24.89906973
])
forces = np.array([
    0,
    0.3694095101,
    0.6883694061,
    0.9725707263,
    1.114120879,
    1.228197082,
    1.262211739,
    1.28499495,
    1.224943784,
    1.076163252,
    0.9566081732,
    0.7738635641,
    0.6024525279,
    0.3803875186,
    0.08985652802,
    -0.104146398,
    -0.3018424881,
    -0.5587985617,
    -0.8338390097,
    -1.116313225,
    -1.251931497,
    -1.74072921,
    -1.807944151,
    -2.120389196,
    -2.229086576,
    -2.541974613,
    -2.635956705,
    -2.760590773,
    -3.015248238,
    -3.136309235,
    -3.381786996,
    -3.444854684,
    -3.505613052,
    -3.843720665,
    -4.002783484,
    -4.058846054,
    -5.227901219,
    -5.718510705,
    -5.725745027,
    -5.140736544,
    -4.618447804,
    -4.052357689,
    -3.454442176,
    -3.010472841,
    -2.671932427,
    -2.482141227,
    -2.341844027,
    -2.213337452,
    -1.878969698,
    -1.718137079,
    -1.342872976,
    -1.138197387,
    -1.161387756
])

velocities,forces = use_symmetry_force_curve(velocities,forces)

velocities /= 2.5
forces /= 1.4

print(velocity_to_si(np.array([1]), BaF))


first_doppler_start = 0
first_doppler_end = sub_doppler_start = 40
sub_doppler_end = doppler_start = 66
doppler_end = len(velocities)

plt.fill_between(velocities[first_doppler_start:first_doppler_end], np.zeros(velocities[first_doppler_start:first_doppler_end].shape), forces[first_doppler_start:first_doppler_end], color='lightgreen', alpha=0.5)
plt.fill_between(velocities[doppler_start:doppler_end], np.zeros(velocities[doppler_start:doppler_end].shape), forces[doppler_start:doppler_end], color='lightgreen', alpha=0.5)
plt.fill_between(velocities[sub_doppler_start:sub_doppler_end], np.zeros(velocities[sub_doppler_start:sub_doppler_end].shape), forces[sub_doppler_start:sub_doppler_end], color='orange', alpha=0.5)

plt.ylabel(r'acceleration ($\times 10^3 m/s^2$)')
plt.xlabel(r'velocity (m/s)')
plt.grid(True)
plt.plot(velocities, forces)

plt.savefig('example_force_curve.png',bbox_inches='tight', pad_inches=0.1)