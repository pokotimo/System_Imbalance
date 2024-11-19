import numpy as np
from scipy.optimize import minimize

# Constants
SI = -50  # System Imbalance in MW
AEP = 0.5  # Balancing energy price in €/MW
BK = [0.75, 0.5, 0.2, 0.1]
BK = np.array(BK).T
AEK = [2, 1, 0.4, 0.2]
AEK = np.array(AEK).T
previous_RL = [100,100,100,100]  # Target value for the absolute deviation term
previous_RL = np.array(previous_RL)
max_delta = [250,25,15,2]
max_delta = np.array(max_delta)

# Bounds for variables P1, P2, P3, P4
bounds = [(-125, 125), (-125, 125), (-150, 150), (-300, 300)]

# Define the objective function
def objective(P):
    [P1, P2, P3, P4] = P
    P = np.array(P)
    abs_dev = abs(P - previous_RL)
    
    RL = sum(P)
    penalty = AEP * (np.sign(RL - SI)) * RL
    # @ Zeichen für Matrixmultiplikation, damit Skalarer Wert herauskommt
    obj = (
        -BK @ P - (BK)**2 @ P**2 - AEK @ abs_dev + penalty
    )
    return obj

# Define constraints
def constraint(P):
    # Calculate the absolute difference between current and previous values
    abs_delta = np.abs(P - previous_RL)
    # Ensure the absolute difference is within the allowed range
    return max_delta - abs_delta


# Add constraints as inequality constraints (g(x) >= 0)
constraints = [
    {"type": "ineq", "fun": constraint},
]

# Initial guess
initial_guess = [0, 0, 0, 0]

# Solve the problem
result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)

# Output results
if result.success:
    print("Optimization successful!")
    for i, value in enumerate(result.x, 1):
        print(f"P{i} = {value}")
    print(f"Objective value = {result.fun}")
else:
    print("Optimization failed!")
    print(result.message)
