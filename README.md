# simplex_py
Two-phase Simplex implementation in Python with numpy

## Not yet implemented
1. Identify unbounded solutions.
2. Identify when there is no feasible solution.
3. Edge cases with only equalities.
4. Only output the optimal solution with no slack or artificial variables.

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

## Input from files
Use the same format from the `input_example/` directory
to write your problems in files, then redirect the file contents to the script.

### Example
First `chmod +x two_phase_simplex.py` if you want to run it as a program. Then

```./two_phase_simplex < input_examples/min_example3.txt```

will output

```
...
The optimal solution is:
x_1 = 0
x_2 = 0
x_3 = 0.19999999999999996
x_4 = 0.5999999999999999
x_5 = 0
x_6 = 3.0000000000000018
x_7 = 30.0
x_8 = 40.00000000000001
x_9 = 0
With an optimal Z value of 12.999999999999996
```
where `x_5` to `x_9` are slack and artificial variables.
