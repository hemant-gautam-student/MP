from flask import Flask, render_template, request, redirect, url_for, jsonify
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re

from Codes.LP_Graphical import solve_linear_program
from Codes.Simplex_Method import simplex
from Codes.Transportation import solve_transportation_problem

app = Flask(__name__)


# Home Page (Mathematical Programming)
@app.route("/")
def home():
    return render_template("index.html")


# Linear Programming Page
@app.route("/linear-programming")
def linear_programming():
    return render_template("linear_programming.html")


# Graphical Method Page
@app.route("/graphical-method", methods=["GET", "POST"])
def graphical_method():
    if request.method == "POST":
        equations = request.form.get("equations")
        objective = request.form.get("objective")

    return render_template("graphical_method.html")


@app.route("/submit", methods=["POST"])
def graphical_method1():
    # Check if the request is JSON
    if request.is_json:
        data = request.get_json()  # Parse JSON data
        print(data)
        c = []
        A = []
        b= []

        c.append(int(data['objectiveFunction']['x1']))
        c.append(int(data['objectiveFunction']['x2']))

        for constraint in data['constraints']:
            alist = []

            alist.append(int(constraint['x1']))
            alist.append(int(constraint['x2']))
            A.append(alist)
            b.append(int(constraint['value']))
        A.append([-1, 0])
        A.append([0, -1])
        b.append(0)
        b.append(0)
        print(f"Parsed Data: c: {c}, A: {A}, b: {b}")

        # return solve_linear_program(c, A, b)
        graph_image = solve_linear_program(c, A, b)
        # return jsonify({
        #     "message": "Data received successfully",
        #     "data": data
        # }), 200

        return jsonify({"graph": graph_image, "message": "Graph generated successfully"})


@app.route("/solve", methods=["POST"])
def simplex_method1():
    # Check if the request is JSON
    if request.is_json:
        data = request.get_json()  # Parse JSON data
        print(data)
        c = []
        A = []
        b = []
        c.extend(map(float, data['objectiveFunction']))

        for constraint in data['constraints']:
            alist = []
            alist.extend(map(float, constraint['coefficients']))
            A.append(alist)
            b.append(float(constraint['value']))
        print(f"Parsed Data: c: {c}, A: {A}, b: {b}")

        # return simplex(np.array(c), np.array(A), np.array(b))
        # Solve using the simplex method
        solution, optimal_value = simplex(np.array(c), np.array(A), np.array(b))

        # Return solution and optimal value
        return jsonify({
            "solution": solution.tolist(),
            "optimalValue": optimal_value
        })


# Simplex Method Page
@app.route("/simplex-method", methods=["GET", "POST"])
def simplex_method():
    result = None
    if request.method == "POST":
        # Dummy result for now (implement Simplex logic)
        result = "Optimal Solution: x = 3, y = 5, Z = 25"
    return render_template("simplex_method.html", result=result)


# Transportation Method Page
@app.route('/transportation_method', methods=["GET", 'POST'])
def transportation_method():
    result = None
    return render_template("transportation_method.html", result=result)


@app.route("/solve-transportation", methods=["POST"])
def solve_transportation1():
    # Check if the request is JSON
    if request.is_json:
        data = request.get_json()  # Parse JSON data
        print(data)
        cost_matrix = data['costs']
        supply = data['supply']
        demand = data['demand']

        print(f"Parsed Data: cost_matrix: {cost_matrix}, supply: {supply}, demand: {demand}")

        result = solve_transportation_problem(cost_matrix, supply, demand)
        print(result)

        solution_array = np.array(result["solution"])

        # Convert NumPy array to a Python list
        solution_list = solution_array.tolist()

        # Return solution and optimal value
        return jsonify({
            "solution": solution_list,
            "total_cost": result["total_cost"],
            "status": result["status"]
        })


if __name__ == "__main__":
    app.run(debug=True)
