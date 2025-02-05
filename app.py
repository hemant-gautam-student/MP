from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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

        # Dummy solver for demonstration (replace with an actual solver)
        x_vals = np.linspace(0, 10, 100)
        y_vals = 10 - x_vals  # Example constraint line

        # Plot graph
        plt.figure(figsize=(6, 6))
        plt.plot(x_vals, y_vals, label="x + y ≤ 10")
        plt.fill_between(x_vals, y_vals, 10, color='gray', alpha=0.3)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Feasible Region")
        plt.legend()
        
        # Save image in memory
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close()

        return render_template("graphical_method.html", result=img_str)

    return render_template("graphical_method.html")

# Simplex Method Page
@app.route("/simplex-method", methods=["GET", "POST"])
def simplex_method():
    result = None
    if request.method == "POST":
        # Dummy result for now (implement Simplex logic)
        result = "Optimal Solution: x = 3, y = 5, Z = 25"
    return render_template("simplex_method.html", result=result)

# Transportation Method Page
@app.route("/transportation-method", methods=["GET", "POST"])
def transportation_method():
    result = None
    if request.method == "POST":
        # Dummy result for now (implement Transportation logic)
        result = "Optimal Transportation Cost: 120"
    return render_template("transportation_method.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
