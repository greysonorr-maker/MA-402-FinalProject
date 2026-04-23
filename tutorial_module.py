"""
lsq_augmented.py
================
Solves a small least-squares problem   min ‖Ax - b‖₂
using the augmented-system (saddle-point) formulation from PETSc's ex27.c.

Augmented system
----------------
Instead of solving A x ≈ b directly, we introduce the residual vector r = b - Ax
and write the equivalent block system:

    [ -I   A ] [ r ]   [ b ]
    [ Aᵀ   0 ] [ x ] = [ 0 ]

Solving this 2x2 block system gives the least-squares solution x* and the
optimal residual r* = b - Ax* simultaneously.

Hard-coded example (overdetermined, 4 equations in 3 unknowns)
--------------------------------------------------------------
    A = [ 1  1  0 ]      b = [ 2 ]
        [ 1  0  1 ]          [ 3 ]
        [ 0  1  1 ]          [ 3 ]
        [ 1  1  1 ]          [ 4 ]

Exact least-squares solution: x ≈ [1, 1, 2]ᵀ  (residual = 0 here — system
is consistent, so ‖r‖ should be essentially machine zero).
"""

import sys
import numpy as np

# ---------------------------------------------------------------------------
# PETSc / petsc4py bootstrap
# ---------------------------------------------------------------------------
import petsc4py
petsc4py.init(sys.argv)
from petsc4py import PETSc

Print = PETSc.Sys.Print   # MPI-aware print (only rank-0 speaks)

# ---------------------------------------------------------------------------
# 1.  Define A  (m×n = 4×3) and b  (length m = 4)
# ---------------------------------------------------------------------------
#
# We store A as a PETSc AIJ matrix.  For a serial script we own every row.

m, n = 4, 3   # rows, columns of A

# Dense description of A — convert to sparse COO triples
A_dense = np.array([
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 1],
], dtype=PETSc.ScalarType)

b_vals = np.array([2, 3, 3, 4], dtype=PETSc.ScalarType)

# Build the PETSc Mat for A
A = PETSc.Mat().createAIJ([m, n], comm=PETSc.COMM_WORLD)
A.setFromOptions()
A.setUp()
for i in range(m):
    for j in range(n):
        if A_dense[i, j] != 0:
            A.setValue(i, j, A_dense[i, j])
A.assemblyBegin(); A.assemblyEnd()

Print("\n=== Matrix A ===")
A.view()

# ---------------------------------------------------------------------------
# 2.  Build the augmented block matrix  C = [ -I   A ]
#                                            [ Aᵀ   0 ]
#
#  Size: (m+n) × (m+n)
#  Blocks:
#    (0,0)  –I  shape m×m   (top-left)
#    (0,1)   A  shape m×n   (top-right)
#    (1,0)  Aᵀ  shape n×m   (bottom-left)
#    (1,1)   0  shape n×n   (bottom-right, omitted / zero)
# ---------------------------------------------------------------------------

N_total = m + n   # = 7 for our example

C = PETSc.Mat().createAIJ([N_total, N_total], comm=PETSc.COMM_WORLD)
C.setFromOptions()
C.setUp()

# Block (0,0): -I  (rows 0..m-1, cols 0..m-1)
for i in range(m):
    C.setValue(i, i, -1.0)

# Block (0,1): A  (rows 0..m-1, cols m..m+n-1)
for i in range(m):
    for j in range(n):
        v = A_dense[i, j]
        if v != 0:
            C.setValue(i, m + j, v)

# Block (1,0): Aᵀ  (rows m..m+n-1, cols 0..m-1)
for j in range(n):
    for i in range(m):
        v = A_dense[i, j]
        if v != 0:
            C.setValue(m + j, i, v)

# Block (1,1): zero — no entries needed

C.assemblyBegin(); C.assemblyEnd()

Print("\n=== Augmented matrix C ===")
C.view()

# ---------------------------------------------------------------------------
# 3.  Build the right-hand side vector  rhs = [ b ]
#                                              [ 0 ]
# ---------------------------------------------------------------------------

rhs = PETSc.Vec().createSeq(N_total, comm=PETSc.COMM_WORLD)
rhs.setFromOptions()
for i in range(m):
    rhs.setValue(i, b_vals[i])
# entries m..m+n-1 default to 0
rhs.assemblyBegin(); rhs.assemblyEnd()

# ---------------------------------------------------------------------------
# 4.  Create the initial guess vector  sol = [ 0 ]
#                                             [ 0 ]
# ---------------------------------------------------------------------------

sol = rhs.duplicate()
sol.set(0.0)

# ---------------------------------------------------------------------------
# 5.  Set up and run the KSP solver
#
#  The augmented system is indefinite (it has both positive and negative
#  eigenvalues), so CG is not appropriate.  We use GMRES with no
#  preconditioner (PCNONE) to keep the example self-contained.
#  In production you would use -pc_type fieldsplit as ex27.c does.
# ---------------------------------------------------------------------------

ksp = PETSc.KSP().create(comm=PETSc.COMM_WORLD)
ksp.setOperators(C, C)
ksp.setType(PETSc.KSP.Type.GMRES)

pc = ksp.getPC()
pc.setType(PETSc.PC.Type.NONE)

# Allow command-line overrides, e.g. -ksp_monitor -ksp_view
ksp.setFromOptions()
ksp.setTolerances(rtol=1e-10, atol=1e-12, max_it=500)

ksp.solve(rhs, sol)

reason = ksp.getConvergedReason()
n_iter = ksp.getIterationNumber()
Print(f"\nKSP converged reason : {reason}")
Print(f"Iterations           : {n_iter}")

# ---------------------------------------------------------------------------
# 6.  Extract and display results
# ---------------------------------------------------------------------------

sol_array = sol.getArray()
r_star = sol_array[:m]          # optimal residual  r* = b - Ax*
x_star = sol_array[m:]          # least-squares solution  x*

Print("\n=== Least-squares solution  x* ===")
for i, xi in enumerate(x_star):
    Print(f"  x[{i}] = {xi:.10f}")

# Verify: compute Ax* and compare with b
Ax = np.zeros(m, dtype=complex if np.iscomplexobj(x_star) else float)
for i in range(m):
    for j in range(n):
        Ax[i] += A_dense[i, j] * x_star[j]

residual_check = b_vals - Ax
res_norm = np.linalg.norm(residual_check)

Print("\n=== Verification ===")
Print(f"  b - A x*  (should be ≈ r*)        : {residual_check}")
Print(f"  ‖b - Ax*‖ (least-squares residual) : {res_norm:.6e}")
Print(f"  r* from augmented sol              : {r_star}")
Print(f"  ‖r* - (b-Ax*)‖                    : {np.linalg.norm(r_star - residual_check):.6e}")

# ---------------------------------------------------------------------------
# 7.  Clean up
# ---------------------------------------------------------------------------

ksp.destroy(); C.destroy(); A.destroy()
rhs.destroy(); sol.destroy()