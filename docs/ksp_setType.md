# ksp.setType

## Function
```python
ksp.setType(type)
``` 
## Underlying PETSc Function

`KSPSetType(KSP ksp, KSPType type)`

## Description
`ksp.setType` sets the type of solver that will be used to solve the linear system.
PETSc provides different Krylov subspace methods, which include the Generalized Minimal Residual Method (GMRES), Conjugate Gradient Method (CG), and others.  
This function allows you to choose which method the solver will use.

## Parameters
- `ksp (PETSc.KSP)`: The solver object. In Python, this is the object you call the method on.
- `type (PETSc.KSP.Type)`: The solver method you want to use (such as GMRES).

## Mathematical Context

In this project, we solve an augmented system of the form:

[ -I   A ] [ r ] = [ b ]

[ A^T  0 ] [ x ]   [ 0 ]

The matrix in this system is not symmetric positive definite, so we cannot always use methods like Conjugate Gradient Method.

Instead, we use:

`ksp.setType(PETSc.KSP.Type.GMRES)`

GMRES is a more general solver that works for a wider class of matrices, including the augmented system used in this project.

## Example
```python
from petsc4py import PETSc

ksp = PETSc.KSP().create()

# Set the solver type
ksp.setType(PETSc.KSP.Type.GMRES)

ksp.setOperators(C, C)
ksp.solve(rhs, sol)
```

## Notes
- Must be called before ksp.solve()

## Source References
- PETSc Manual Page: https://petsc.org/release/manualpages/KSP/KSPSetType/
- PETSc C Source: src/ksp/ksp/interface/itcreate.c
