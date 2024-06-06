import numpy as np
import pylcp

from src.model.molecules import Molecule

import scipy.constants as cts

""""
This file represents the hamiltonian used in the NL-eEDM laser cooling experiment.

By Max Vos 19/02/2024
"""


def get_hamiltonian(molecule: Molecule) -> tuple[pylcp.hamiltonian, np.ndarray, np.ndarray]:
    H0_X, Bq_X, U_X, x_basis = get_x_hamiltonian(molecule)
    H0_A, Bq_A, a_basis = get_a_hamiltonian(molecule)

    dijq = get_dipole_x_and_a_states(molecule, x_basis, a_basis, U_X)

    E_X = np.unique(np.diag(H0_X))
    E_A = np.unique(np.diag(H0_A))

    return (pylcp.hamiltonian(
        H0_X, H0_A, Bq_X, Bq_A, dijq, mass=molecule.mass
    ), E_X, E_A)


def get_x_hamiltonian(molecule) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return pylcp.hamiltonians.XFmolecules.Xstate(
        N=molecule.ground_N,
        I=molecule.nuclear_spin,
        B=molecule.ground_B / molecule.line_width_in_MHz,
        gamma=molecule.ground_gamma / molecule.line_width_in_MHz,
        b=molecule.ground_b / molecule.line_width_in_MHz,
        c=molecule.ground_c / molecule.line_width_in_MHz,
        muB=cts.value('Bohr magneton in Hz/T') / (molecule.line_width_in_MHz * 1e6),
        return_basis=True
    )


def get_a_hamiltonian(molecule) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return pylcp.hamiltonians.XFmolecules.Astate(
        J=molecule.excited_J,
        I=molecule.nuclear_spin,
        P=molecule.excited_parity,
        a=molecule.frosch_a / molecule.line_width_in_MHz,
        b=molecule.frosch_b / molecule.line_width_in_MHz,
        c=molecule.frosch_c / molecule.line_width_in_MHz,
        muB=cts.value('Bohr magneton in Hz/T') / (molecule.line_width_in_MHz * 1e6),
        return_basis=True
    )


def get_dipole_x_and_a_states(molecule, x_basis: np.ndarray, a_basis: np.ndarray, U_X: np.ndarray) -> np.ndarray:
    return pylcp.hamiltonians.XFmolecules.dipoleXandAstates(
        x_basis,
        a_basis,
        I=molecule.nuclear_spin,
        S=molecule.sigma,
        UX=U_X
    )
