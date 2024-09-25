#!/usr/bin/python
import numpy as np
np.set_printoptions(suppress=True, linewidth=500)

def main():
	maximize, c, A, b, A_eq = lp_input()

	# CREATE PRE-TABLEU
	Ab = np.hstack((A, b))
#	W = np.zeros(c.shape[0])
	A_columns_without_artificials = A.shape[1]

	print("The original problem is:")
	print(np.insert(Ab, 0, np.hstack((c,np.zeros(1))), axis=0))
	print()
	
	# CREATE ARTIFICIAL VARIABLES FOR >= INEQUALITIES
	mask = b < 0
	unmasked = np.sum(mask)
	artificials = np.empty((0, b.shape[0]))
	for i, value in enumerate(mask):
		if value:
			arr = np.zeros((1, b.shape[0]))
			if i < b.shape[0]:
				arr[0, i] = -1
			artificials = np.vstack((artificials, arr))

	if artificials.size != 0:
		# TO DO: CHANGE W_basis_rows name
		# TO DO: DO NOT TRANSPOSE
		# ADD ARTIFICIAL VARIABLES
		AA = np.hstack((A, np.transpose(artificials)))
		AAb = np.hstack((AA,b))

		W_basis_rows = list()
		for i in range(A_eq.shape[0]):
			W_basis_rows.append(A.shape[0]-i)
		for i, value in enumerate(mask):
			if value:
				# i+1 constraint row index (after Z row)
				W_basis_rows.append(i+1)
				AAb[i] = -AAb[i]

#		print(AAb)
#		print(W_basis)

		W = np.hstack((np.zeros(A_columns_without_artificials-1), np.full(A_eq.shape[0]+artificials.shape[0], -1)))
		W = np.hstack((W, np.zeros(1)))
#		print(AAb)
#		print(W)
		table = np.insert(AAb, 0, W, axis=0)

		print("The uninitialized phase 1 tableu is:")
		print(table)
		print()

		# INITIALIZING PHASE 1 TABLEU
		for row in W_basis_rows:
			table[0] += table[row]

		print("The phase 1 tableu is:")
		print(table)
		print()

		basis = simplex(table, maximize, iterations=200)

		# PREPARING PHASE 2 TABLEU
		# delete non basic variables
		to_delete = list()
		for j, value in enumerate(table[0]):
			if j not in [element[1] for element in basis] and j in range(A.shape[1]-A_eq.shape[1], A.shape[1] + artificials.shape[0]):
				to_delete.append(j)
		table = np.delete(table, to_delete, axis=1)

		table[0] = np.hstack((c,np.zeros(table.shape[1] - c.shape[0])))
		print("The uninitialized phase 2 tableu is:")
		print(table)
		print()

		for element in basis:
			if table[0, element[1]] != 0:
				table[0] -= table[element[0]]*table[0, element[1]]
	
		print("The phase 2 tableu is:")
	else:
		Ab = np.hstack((A, b))
		Z = np.hstack((c, np.zeros(1)))
		print(Ab)
		print(Z)
		table = np.insert(Ab, 0, Z, axis=0)
		print("The tableu is:")

	if maximize:
		print("Maximize")
	else:
		print("Minimize")
	print(table)
	print()

	# SIMPLEX ORIGINAL PROBLEM
	basis = simplex(table, maximize, iterations=200)

	# get the first len(c) basic columns
	solution_indexes = list()
	columns = np.transpose(table)[:len(c)]
	for j, column in enumerate(columns):
		is_basic = sum(column) == 1 and 1 in column
		if is_basic:
			solution_indexes.append(j)
	
	# get the x index and value of the solutions
	x_values = list()
	for j, column in enumerate(columns):
		if j in solution_indexes:
			for i in range(len(table)):
				if table[i,j] == 1:
					x_values.append((j, float(table[i,-1])))
	
	print("The optimal solution is:")
	for index in range(len(c)):
		if index in [x[0] for x in x_values]:
			for x in x_values:
				if x[0] == index:
					print(f"x_{x[0]+1} = {x[1]}")
		else:
			print(f"x_{index+1} = 0")

	print(f"With an optimal Z value of {table[0, -1]}")

def iteration(table: np.array, maximize: bool):
	pivot_rule = np.argmin if maximize else np.argmax
	pivot_j = pivot_rule(table[0,:-1])

	# FIND MINIMUM QUOTIENT IN TABLE
	quotients = list()
	for row in table[1:]:
		if row[pivot_j] <= 0:
			quotients.append(np.inf)
		else:
			quotients.append(row[-1]/row[pivot_j])
	quotients = np.array(quotients)
	pivot_i = quotients.argmin()+1
	if pivot_i == np.inf:
		return

	# PIVOT
	table[pivot_i] /= table[pivot_i][pivot_j]

	for i, row in enumerate(table):
		if i != pivot_i:
			row -= table[pivot_i]*row[pivot_j]

	return pivot_i, pivot_j

def has_no_negative(row: np.array) -> bool:
	for j in row:
		if j < 0:
			return False
	return True

def has_no_positive(row: np.array) -> bool:
	for j in row:
		if j > 0:
			return False
	return True

def simplex(table: np.array, maximize: bool, iterations: int):
	k = 0
	basis = list()
	columns = np.transpose(table)
	for j, column in enumerate(columns):
		is_basic = sum(column) == 1 and 1 in column
		if is_basic:
			for i in range(table.shape[0]):
				if table[i, j] == 1:
					basis.append((i, j))
	print("The initial basis is:")
	for element in basis:
		print(f"x_{element[1]+1}")
	print()

	halting_condition = has_no_negative if maximize else has_no_positive
	
	while True:
		if halting_condition(table[0,:-1]):
			break
		k += 1
		print(f"Iteration {k}")
		pivot_row, pivot_column = iteration(table, maximize)
		# replace basic variable
		print(f"x_{pivot_column+1} enters")
		for i, variable in enumerate(basis):
			if variable[0] == pivot_row:
				print(f"x_{variable[1]+1} exits")
				basis[i] = (int(pivot_row), int(pivot_column))
#		if pivot_column == variable[1]:
#			break
		print(table)
		print("The current basis is:")
		for element in basis:
			print(f"x_{element[1]+1}")
		print()
		if k == iterations: #or pivot_column == pivot_row:
			print(f"simplex halted at {k} iterations")
			print()
			return basis
	print("Optimal solution reached.")
	print()
	return basis

def lp_input():
	print("For maximization enter 1, for minimization write 0, then press Enter again:")
	if input().strip() == "1":
		maximize = True
	else:
		maximize = False
	input()

	print("Enter the c vector values separated by spaces:")
	c = list(map(lambda x: -float(x) if True else float(x), input().split(" ")))
	print("Press Enter again.")
	input()
	c = np.array(c)

	A = list()
	print("Write the INEQUALITY rows for the A matrix line by line")
	print("with values separated by spaces and press Enter again:")
	line = str()
	i = 0
	while True:
		line = input()
		if line == "":
			break
		numbers = line.split(" ")

		if len(numbers) != len(c):
			print("The length of an A row should be the length of c.")
			return

		row = list(map(lambda x: float(x), numbers))
		A.append(row)

		if len(A) > 1 and len(A[len(A) - 1]) != len(A[len(A) - 2]):
			print("Err: All rows should have equal size.")
			return
	A = np.array(A)

	print("Write the b values of INEQUALITY restrictions:")
	b = np.array(list(map(lambda x: float(x), input().split(" "))))
	b = np.transpose([b])
	print("Press Enter again:")
	input()
	print()

#	print("If the problem has equality restrictions, write 1, else 0:")
#	has_eq = input().strip() == "1"
#	print("Press enter again.")
#	input()
	
	A_eq = list()
	print("Write the EQUALITY rows of A line by line with values")
	print("separated by spaces, and press Enter again:")
	line = str()
	i = 0
	while True:
		line = input()
		if line == "":
			break
		numbers = line.split(" ")

		if len(numbers) != len(c):
			print("The length of an A row should be the length of c.")
			return

		row = list(map(lambda x: float(x), numbers))
		A_eq.append(row)

		if len(A_eq) > 1 and len(A_eq[len(A_eq) - 1]) != len(A_eq[len(A_eq) - 2]):
			print("Err: All rows should have equal size.")
			return
	A_eq = np.array(A_eq)

	print("Write the b EQUALITY values:")
	line = input().strip()
	if line != "":
		b_eq = np.array(list(map(lambda x: float(x), line.split(" "))))
		b_eq = np.transpose([b_eq])
	print()

	if A_eq.size != 0:
		A = np.vstack((A, A_eq))
		A = np.hstack((A, np.identity(len(A))))
		b = np.vstack((b, b_eq))
		c = np.hstack((c, np.zeros(A.shape[1] - c.shape[0])))
	else:
		A = np.hstack((A, np.identity(len(A))))
		c = np.hstack((c, np.zeros(A.shape[1] - c.shape[0])))

	return maximize, c, A, b, A_eq

main()
