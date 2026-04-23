# MA-402-FinalProject
# PETsc Least Squares Project 

## Overview

This project focuses on soliving linear least-squares problems using PETSc and petsc4py. The goal of this project is to translate and understand the PETsc example "ex27.c", which demonstrates different methods for solving least-squares problems. 

The core mathematical problem is:

\[
\min_x \|Ax - b\|_2
\]


Typically, one could compute this using the Normal Equation: 
\[
A^T A x = A^T b.
\]

However, solving the least squares solution this way can be numerically unstable. As an alternative, PETSc uses more stable solving approaches, which includes iterative and augmented system solvers. This project focuses on understanding and implementing the augmented system approach in Python. 

## Mathematical Background

A least-squares problem is when we are solving an overdetermined system \( Ax = b \), where the exact solution may not exist. The goal of these problems is to find the vector \(x\) that minimizes the residual: 
\[
\|Ax - b\|_2
\]

While the normal equation provides a direct method of solving this system, it can create major numerican errors. Most modern libraries, like PETSc, use more stable numerical techniques, such as LSQR or the augmented systems method, to solve these problems. 

## AI Translation Experience
** Will be added after translation


## Summary
This project demonstrates how PETSc solves least-squares problems using numerically stable methods and highlights the challenges of translatning scientific computing between coding languages. 


