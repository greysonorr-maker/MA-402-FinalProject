# ksp.solve

## Function
```python
ksp.solve(b, x)
```
## Underlying PETSc Function
`KSPSolve(KSP ksp, Vec b, Vec x)`

## Description
`ksp.solve` is the method that solves the linear system defined by the KSP solver. It takes the vector `b` and computes the solution vector `x` such that the defined linear system is satisfied. This must be called after setting the solver type and operators. 

## Parameters
- `b (PETSc.Vec)`:
The right-hand side vector of the system.
- `x (PETSc.Vec)`:
The vector where the solution will be stored.

## Returns
This function does not return a value. It stores the computed solution in the vector `x`.

## Mathematical Context
Our goal is to solve `Ax=b` using the augmented least-squares system:
```
[ -I   A ] [ r ] = [ b ]

[ A^T  0 ] [ x ]   [ 0 ]
```
The solver computes both the residual vector `r` and the least squares solution `x`. The solution vector passed into `ksp.solve()` contains both components, and the least-squares solution is extracted from it. In the code, this system $Cz = d$ is solved when `ksp.solve(rhs, sol)` is called, where `rhs` represents $d$ and `sol` stores the solution vector $z$.

## Example
```python
from petsc4py import PETSc

ksp = PETSc.KSP().create()
ksp.setType(PETSc.KSP.Type.GMRES)

ksp.setOperators(C, C)

ksp.solve(rhs, sol)
```
## Notes
- This function must be called after the `ksp.setOperators()`
- This function stores the solution in the provided vector
- Convergence can be checked using:
    - `ksp.getConvergedReason()`
    - `ksp.getIterationNumber()`


## Source References
- PETSc Manual Page: https://petsc.org/release/manualpages/KSP/KSPSolve/
- PETSc C Source: src/ksp/ksp/interface/itfunc.c
