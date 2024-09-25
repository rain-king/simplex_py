# simplex_py
Two-phase Simplex implementation in Python with numpy

## Not yet implemented
1. Identify unbounded solutions.
2. Identify when there is no feasible solution.
3. Edge cases with only equalities.

## Usage
Needs numpy installed.

When running the scripts, it asks for the problem information.
Exactly, the script will ask:
1. If it is a maximization (write 1) or minimization problem (write 0).
2. For $c$ vector, $A$ matrix, $b$ vector, $A_{eq}$ matrix, $b_{eq}$ vector, from the following problem description: Maximize (or minimize) the $Z$ function of vector $x$ subject to

$$Z = c\cdot x$$

$$Ax\leq b$$

$$A_{eq}x = b_{eq}$$

$$x \geq 0$$

Notice that $b$ is not restricted to be of only positive values. So the inequalities $Ax\geq b$ with $b>0$
can be transformed into $-Ax \leq -b$ by multiplying by $-1$, and the program will take the input for processing the equivalent problem.
