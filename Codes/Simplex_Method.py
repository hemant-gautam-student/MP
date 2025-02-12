import numpy as np


def simplex(c, A, b):
    """
    Solves the Linear Programming problem using the Simplex Method:
    Maximize: Z = c^T * x
    Subject to: A * x <= b, x >= 0

    Parameters:
    - c: Objective function coefficients (1D array)
    - A: Coefficient matrix of constraints (2D array)
    - b: Right-hand side values of constraints (1D array)

    Returns:
    - Optimal solution and value of the objective function if feasible, otherwise infeasibility.
    """
    num_constraints, num_variables = A.shape

    # Add slack variables to convert inequalities to equalities
    slack_vars = np.eye(num_constraints)
    tableau = np.hstack((A, slack_vars, b.reshape(-1, 1)))

    # Add the objective function row to the tableau
    obj_row = np.hstack((-c, np.zeros(num_constraints + 1)))
    tableau = np.vstack((tableau, obj_row))

    # Number of total variables (original + slack)
    num_total_vars = num_variables + num_constraints

    # Start Simplex iterations
    while True:
        # Step 1: Check for optimality (no negative values in the objective row)
        if all(tableau[-1, :-1] >= 0):
            break

        # Step 2: Determine the entering variable (most negative in the objective row)
        pivot_col = np.argmin(tableau[-1, :-1])

        # Step 3: Determine the leaving variable (smallest positive ratio of RHS / pivot column)
        ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
        ratios[ratios <= 0] = np.inf  # Ignore non-positive ratios
        pivot_row = np.argmin(ratios)

        if np.all(ratios == np.inf):
            raise ValueError("The problem is unbounded.")

        # Step 4: Perform the pivot operation
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_element

        for i in range(tableau.shape[0]):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

    # Extract the solution
    solution = np.zeros(num_total_vars)
    for i in range(num_constraints):
        basic_var_index = np.where(tableau[i, :-1] == 1)[0]
        if len(basic_var_index) == 1 and basic_var_index[0] < num_total_vars:
            solution[basic_var_index[0]] = tableau[i, -1]

    # Objective function value
    optimal_value = tableau[-1, -1]
    return solution[:num_variables], optimal_value



# Example usage
if __name__ == "__main__":
    c = np.array([9,10,7])  # Coefficients of the objective function
    A = np.array([
        [1,3,2],
        [4,1,3],
       [2, 4, 1]
    ])  # Coefficient matrix of constraints
    b = np.array([12,16,14])  # Right-hand side values of constraints

    solution, optimal_value = simplex(c, A, b)
    print("Optimal Solution:", solution)
    print("Optimal Value:", optimal_value)