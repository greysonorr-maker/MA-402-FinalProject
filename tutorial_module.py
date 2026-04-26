"""
lsq_augmented.py
================
Solves a least-squares problem   min ||Ax - b||_2
using the augmented-system formulation from PETSc's ex27.c.

Also includes a reusable function for solving general systems.
"""

import sys
import numpy as np

import petsc4py
petsc4py.init(sys.argv)
from petsc4py import PETSc

Print = PETSc.Sys.Print


# ============================================================
# GENERAL FUNCTION 
# ============================================================
def solve_augmented_least_squares(A_dense, b_vals):
    """
    Solves min ||Ax - b|| using the augmented system method.

    Parameters:
        A_dense (np.ndarray): m x n matrix
        b_vals (np.ndarray): length m vector

    Returns:
        x_star, r_star, residual_norm
    """

    m, n = A_dense.shape
    N_total = m + n

    # Build augmented matrix C
    C = PETSc.Mat().createAIJ([N_total, N_total])
    C.setUp()

    # -I block
    for i in range(m):
        C.setValue(i, i, -1.0)

    # A block
    for i in range(m):
        for j in range(n):
            if A_dense[i, j] != 0:
                C.setValue(i, m + j, A_dense[i, j])

    # A^T block
    for j in range(n):
        for i in range(m):
            if A_dense[i, j] != 0:
                C.setValue(m + j, i, A_dense[i, j])

    C.assemblyBegin(); C.assemblyEnd()

    # RHS
    rhs = PETSc.Vec().createSeq(N_total)
    for i in range(m):
        rhs[i] = b_vals[i]

    sol = PETSc.Vec().createSeq(N_total)
    sol.set(0.0)

    # Solver
    ksp = PETSc.KSP().create()
    ksp.setOperators(C, C)
    ksp.setType(PETSc.KSP.Type.GMRES)
    ksp.getPC().setType(PETSc.PC.Type.NONE)
    ksp.solve(rhs, sol)

    sol_array = sol.getArray()
    r_star = sol_array[:m]
    x_star = sol_array[m:]

    residual_norm = np.linalg.norm(A_dense @ x_star - b_vals)

    return x_star, r_star, residual_norm


# ============================================================
#  EXAMPLE 
# ============================================================

m, n = 4, 3

A_dense = np.array([
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 1],
], dtype=PETSc.ScalarType)

b_vals = np.array([2, 3, 3, 4], dtype=PETSc.ScalarType)

Print("\n===  Example Problem ===")

x_star, r_star, res_norm = solve_augmented_least_squares(A_dense, b_vals)

Print("\n=== Least-squares solution x* ===")
for i, xi in enumerate(x_star):
    Print(f"x[{i}] = {xi:.10f}")

Print("\n=== Verification ===")
Print(f"Residual norm ||Ax - b|| = {res_norm:.6e}")
Print(f"Residual vector r*      = {r_star}")