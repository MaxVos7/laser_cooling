from src.model.molecules import BaF, Molecule
import scipy.constants as cts


def get_capture_velocity(molecule: Molecule, length: float) -> float:
    k = 2 * cts.pi / molecule.wave_length
    l = molecule.mass * molecule.line_width_in_MHz * 1e6 / cts.hbar / (k ** 3)
    saturation = 1

    return molecule.line_width_in_MHz * 1e6 / k * (3 * length * saturation / l) ** (1 / 4)


print(get_capture_velocity(BaF, .01))


sat_i = cts.pi * cts.h * cts.c * BaF.line_width_in_MHz * 1e6 / 3 / BaF.wave_length**3
print(sat_i)