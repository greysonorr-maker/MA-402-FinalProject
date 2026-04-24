# MA-402 Final Project
# PETsc Least Squares Project 

## Overview

This project focuses on soliving linear least-squares problems using PETSc and petsc4py. The goal of this project is to translate and understand the PETsc example "ex27.c", which demonstrates different methods for solving least-squares problems. 

The core mathematical problem is:


min_x ||Ax - b||_2


Typically, one could compute this using the Normal Equation: 
A^T A x = A^T b.

However, solving the least squares solution this way can be numerically unstable. As an alternative, PETSc uses more stable solving approaches, which includes iterative and augmented system solvers. This project focuses on understanding and implementing the augmented system approach in Python. 

## Mathematical Background

A least-squares problem is when we are solving an overdetermined system \( Ax = b \), where the exact solution may not exist. The goal of these problems is to find the vector \(x\) that minimizes the residual: 
||Ax - b||_2

While the normal equation provides a direct method of solving this system, it can create major numerican errors. Most modern libraries, like PETSc, use more stable numerical techniques, such as LSQR or the augmented systems method, to solve these problems. 

## AI Translation Experience
AI tools, such as ChatGPT and Claude, were used to assist in translating the PETSc C example `ex27.c` into Python using petsc4py. Since I don't have experience with PETSc or C, these AI tools were helpful for getting an initial version of the code running and understanding how the different parts of this solver were structured. The goal of this project was not to produce a perfect code translation from this example, but to understand the structure of the original code and create a simplified version of this C script that highlighted the core mathematical idea of the augmented system method of solving a least-squares problem. 

AI was helpful in helping me identify the main steps in the code, such as creating matrices, setting up the KSP slver, and solving the system. It also helped convert some of the C-style PETSc functions into the Python equivalent functions. However, the code that Claude generated was not completely correct, so I had to go through and debug several issues. For example, some function calls didn't match the petsc4py API exactly, and I ran into errors trying to print certain outputs like the convergence reason. I had to test the code, fix these errors, and make sure everything ran correctly in my environment.

After debugging, I verified the solution by checking that the solver converged and that the residual was approximately zero. This confirmed that the augmented system method was working. Overall, AI was very useful for getting started with this project and helping me understand the structure of the code. However, it was not enough on its own, as I had to go through the code, fix mistakes, and make sure I understood what wach part of the code was doing. 


## Summary
This project demonstrates how PETSc solves least-squares problems using numerically stable methods and highlights the challenges of translatning scientific computing between coding languages. 


