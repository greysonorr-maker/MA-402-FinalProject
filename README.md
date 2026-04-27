# MA-402 Final Project
# PETSc Least Squares Project 

## Overview

This project focuses on solving linear least-squares problems using PETSc and petsc4py. The goal of this project is to translate and understand the PETSc example "ex27.c", which demonstrates different methods for solving least-squares problems. In this project, the focus is specifically on the **augmented system approach**, rather than implementing all methods from the original example.

The core mathematical problem is:


min_x ||Ax - b||_2


Typically, one could compute this using the Normal Equation:  


A^T A x = A^T b


However, solving the least-squares problem this way can be numerically unstable. As an alternative, PETSc uses more stable solving approaches, including iterative and augmented system solvers. This project focuses on understanding and implementing the augmented system approach in Python using petsc4py.

## Mathematical Background

A least-squares problem occurs when solving an overdetermined system \( Ax = b \), where the exact solution may not exist. The goal is to find the vector \(x\) that minimizes the residual:  


||Ax - b||_2


While the normal equation provides a direct method of solving this system, it can create significant numerical errors. Most modern libraries, like PETSc, use more stable numerical techniques, such as LSQR or the augmented system method, to solve these problems.

The augmented system used in this project is:


[ -I A ] [ r ] = [ b ]

[ A^T 0 ] [ x ] [ 0 ]


This formulation solves for both the least-squares solution \(x\) and the residual vector \(r = b - Ax\) at the same time.

## AI Translation Experience

AI tools, such as ChatGPT and Claude, were used to assist in translating the PETSc C example `ex27.c` into Python using petsc4py. Since I do not have experience with PETSc or C, AI was helpful for getting an initial version of the code running and understanding how the different parts of the solver were structured. The goal of this project was not to produce a perfect code translation, but to understand the structure of the original code and create a simplified version that highlights the augmented system method for solving a least-squares problem. 

AI was helpful in identifying the main steps in the code, such as creating matrices, setting up the KSP solver, and solving the system. It also helped convert some of the C-style PETSc functions into their Python equivalents. However, the code generated was not completely correct, so I had to debug several issues. For example, some function calls did not match the petsc4py API exactly, and I ran into errors when printing outputs such as the convergence reason. I had to test the code, fix these errors, and make sure everything ran correctly in my environment.

After debugging, I verified the solution by checking that the solver converged and that the residual was approximately zero. This confirmed that the augmented system method was working correctly. Overall, AI was very useful for getting started and understanding the structure of the code, but it was not enough on its own. I still had to go through the code, fix mistakes, and make sure I understood what each part of the code was doing. 

## Summary

This project demonstrates how PETSc solves least-squares problems using a numerically stable augmented system approach and highlights the challenges of translating scientific computing code between programming languages.
