import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
from numpy import trapz

from src.model.molecules import CaF, BaF
from src.execution.save_and_load_forces import load_forces, load_forces_from_tarbut

from scipy.integrate import trapezoid
from scipy.interpolate import interp1d
from typing import Union

def get_acceleration(velocities:np.ndarray, accelerations: np.ndarray, velocity:Union[np.ndarray, float])->Union[np.ndarray, float]:
    # Create an interpolation function
    interpolation_function = interp1d(velocities, accelerations, kind='linear', fill_value="extrapolate")

    return interpolation_function(velocity)



def get_interaction_time_ms(x: np.ndarray, y: np.ndarray, start: float, end: float) -> float:
    # Ensure the data points are numpy arrays for easy manipulation
    x = np.array(x)
    y = np.array(y)


    # Generate the x values for integration, including the boundaries
    x_values = np.sort(np.unique(np.append(x, [start, end])))

    # Interpolate y values at the boundaries
    y_values = get_acceleration(x,y,x_values)

    # Filter the data points within the range [x_a, x_b]
    mask = (x_values <= start) & (x_values >= end)
    x_filtered = x_values[mask]
    y_filtered = y_values[mask]

    # Use scipy's trapz function to integrate the data points
    interaction_time = - trapezoid(1 / y_filtered, x_filtered)

    return interaction_time * 1000

def get_area_under_curve(x: np.ndarray, y: np.ndarray, enter_velocity: float, exit_velocity: float) -> float:
    # Ensure the data points are numpy arrays for easy manipulation
    x = np.array(x)
    y = np.array(y)


    # Generate the x values for integration, including the boundaries
    x_values = np.sort(np.unique(np.append(x, [enter_velocity, exit_velocity])))

    # Interpolate y values at the boundaries
    y_values = get_acceleration(x,y,x_values)

    # Filter the data points within the range [x_a, x_b]
    mask = (x_values <= enter_velocity) & (x_values >= exit_velocity)
    x_filtered = x_values[mask]
    y_filtered = y_values[mask]

    # Use scipy's trapz function to integrate the data points
    interaction_time = - trapezoid(y_filtered, x_filtered)

    return interaction_time


def get_start_velocity(velocities: np.ndarray, accelerations: np.ndarray, end_velocity: float,
                       interaction_time_ms: float, step_size: float = 0.01) -> float | None:
    if get_acceleration(velocities,accelerations, end_velocity) > 0:
        raise Exception('End velocity cannot be reached: it is at positive acceleration.')
        return None

    local_interaction_time_ms = 0
    start = end_velocity
    while local_interaction_time_ms < 0 or (local_interaction_time_ms < interaction_time_ms and start <= velocities[-1]):
        start += step_size
        local_interaction_time_ms = get_interaction_time_ms(velocities, accelerations, start, end_velocity)

    if (get_interaction_time_ms(velocities, accelerations, start, start - step_size) > 0 and
            abs(get_interaction_time_ms(velocities, accelerations, start, start - step_size) - interaction_time_ms) < abs(local_interaction_time_ms - interaction_time_ms)):
        start -= step_size

    return start


def get_end_velocity(velocities: np.ndarray, accelerations: np.ndarray, start_velocity: float,
                       interaction_time_ms: float, step_size: float = 0.01) -> float:

    local_interaction_time_ms = 0
    end = start_velocity
    while local_interaction_time_ms < 0 or (local_interaction_time_ms < interaction_time_ms and end <= velocities[-1]):
        end -= step_size
        local_interaction_time_ms = get_interaction_time_ms(velocities, accelerations, start_velocity, end)

    if (get_interaction_time_ms(velocities, accelerations, end, end - step_size) > 0 and
            abs(get_interaction_time_ms(velocities, accelerations, end, end - step_size) - interaction_time_ms) < abs(local_interaction_time_ms - interaction_time_ms)):
        end += step_size

    return end


# saturation = 2
# detuning = -.5
# mag_field = 1
#
# x, y = load_forces('obe', detuning, saturation, BaF, velocity_in_y=False,
#                    additional_title='%.1f_%.0f' % (mag_field, 45), directory='data_grid')
#
#
# end_velocity = .1
# interaction_time = 2
# start_velocity = get_start_velocity(
#     x, y, end_velocity, interaction_time, step_size=.001
# )
#
# print('start velocity: %.3f m/s' % start_velocity)
#
# print(get_interaction_time_ms(x,y,start_velocity, end_velocity))
#
# plt.plot(x,y)
# plt.show()