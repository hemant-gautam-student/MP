import base64
import io

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull


def plot_constraints(constraints, bounds, feasible_region=None, optimal_vertex=None):
    """Plots the constraints, feasible region, and optimal solution."""
    x = np.linspace(bounds[0], bounds[1], 400)
    plt.figure(figsize=(10, 8))

    # Plot constraints as lines
    for coeff, b in constraints:
        if coeff[1] != 0:  # Plot lines with a slope
            y = (b - coeff[0] * x) / coeff[1]
            plt.plot(x, y, label=f"{coeff[0]}x1 + {coeff[1]}x2 ≤ {b}")
        else:  # Vertical line
            x_val = b / coeff[0]
            plt.axvline(x_val, color='r', linestyle='--', label=f"x1 = {x_val}")

    # Highlight feasible region
    if feasible_region is not None and len(feasible_region) > 0:
        hull = ConvexHull(feasible_region)
        polygon = Polygon(feasible_region[hull.vertices], closed=True, color='lightgreen', alpha=0.5, label='Feasible Region')
        plt.gca().add_patch(polygon)

    # Highlight corner points
    if feasible_region is not None:
        for point in feasible_region:
            plt.plot(point[0], point[1], 'bo')  # Mark corners

    # Highlight the optimal solution
    if optimal_vertex is not None:
        plt.plot(optimal_vertex[0], optimal_vertex[1], 'ro', label='Optimal Solution')

    plt.xlim(bounds)
    plt.ylim(bounds)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Linear Programming: Graphical Method")
    plt.legend()
    plt.grid()
    # plt.show()

    # ✅ Convert plot to Base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')  # Save figure to buffer
    img.seek(0)  # Move to the beginning of the buffer
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')  # Convert to Base64
    img.close()
    plt.close()  # Close the plot to free memory

    return graph_url  # ✅ Return Base64-encoded image


def solve_linear_program(c, A, b):
    """Solve the linear programming problem and plot."""
    bounds = [0, max(b)]  # Define a reasonable range for visualization
    constraints = list(zip(A, b))

    # Solve using vertices of the feasible region
    vertices = []
    num_constraints = len(A)
    for i in range(num_constraints):
        for j in range(i + 1, num_constraints):
            # Find intersection of two lines
            A_ = np.array([A[i], A[j]])
            b_ = np.array([b[i], b[j]])
            try:
                vertex = np.linalg.solve(A_, b_)
                if all(np.dot(A, vertex) <= b) and all(vertex >= 0):  # Ensure non-negativity and feasibility
                    vertices.append(vertex)
            except np.linalg.LinAlgError:
                continue

    # Filter unique vertices
    feasible_vertices = np.unique(vertices, axis=0)

    # Evaluate the objective function at each vertex
    if len(feasible_vertices) > 0:
        z_values = [np.dot(c, v) for v in feasible_vertices]
        optimal_value = max(z_values)
        optimal_vertex = feasible_vertices[np.argmax(z_values)]

        print("Optimal Point:", optimal_vertex)
        print("Optimal Value:", optimal_value)

        # Plot the constraints and feasible region
        return plot_constraints(constraints, bounds, feasible_region=feasible_vertices, optimal_vertex=optimal_vertex)
    else:
        print("No feasible region found.")

# Example Inputs for the Given Problem
# c = [5,4]  # Coefficients of the objective function Z = 50x + 18y
# A = [[1, 2], [3, 1], [-1, 0], [0, -1]]  # Coefficients of the inequalities
# b = [20, 30, 0, 0]  # Right-hand side values of the inequalities
# Max z= 7x1+6x2
# Subject to 2x1+4x2 <= 80
# 3x1+2x2 <= 100
# x1,x2>=0

# c = [7, 6]
# A = [[2, 4], [3, 2], [-1, 0], [0, -1]]
# b = [80, 100, 0, 0]

# c = [7, 6]  # Coefficients of the objective function Z = 7x1 + 6x2
# A = [[2, 4], [3, 2], [-1, 0], [0, -1]]  # Coefficients of the inequalities
# b = [80, 100, 0, 0]  # Right-hand side values of the inequalities
#
#
# solve_linear_program(c, A, b)
