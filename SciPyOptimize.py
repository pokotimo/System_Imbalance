import numpy as np
from scipy.optimize import minimize

# Constants
SI = -50  # System Imbalance in MW
AEP = 1.5  # Balancing energy price in €/MW
BK = [1, 0.5, 0.2, 0.1]
AEK = [2, 1, 0.4, 0.2]
previous_RL = 100  # Target value for the absolute deviation term

# Bounds for variables P1, P2, P3, P4
bounds = [(-125, 125), (-125, 125), (-150, 150), (-300, 300)]

# Define the objective function
def objective(P):
    P1, P2, P3, P4 = P
    abs_dev1 = abs(P1 - 100)
    abs_dev2 = abs(P2 - 100)
    abs_dev3 = abs(P3 - 100)
    abs_dev4 = abs(P4 - 100)
    
    RL = P1 + P2 + P3 + P4
    penalty = AEP * (np.sign(RL - SI)) * RL
    
    obj = (
        -BK[0] * P1 - (BK[0])**2 * P1**2 - AEK[0] * abs_dev1 +
        -BK[1] * P2 - (BK[1])**2 * P2**2 - AEK[1] * abs_dev2 +
        -BK[2] * P3 - (BK[2])**2 * P3**2 - AEK[2] * abs_dev3 +
        -BK[3] * P4 - (BK[3])**2 * P4**2 - AEK[3] * abs_dev4 +
        penalty
    )
    return obj

# Define constraints
def constraint1(P):
    return 250 - (P[0] - previous_RL)

def constraint2(P):
    return 25 - (P[1] - previous_RL)

def constraint3(P):
    return 15 - (P[2] - previous_RL)

def constraint4(P):
    return 2 - (P[3] - previous_RL)

# Add constraints as inequality constraints (g(x) >= 0)
constraints = [
    {"type": "ineq", "fun": constraint1},
    {"type": "ineq", "fun": constraint2},
    {"type": "ineq", "fun": constraint3},
    {"type": "ineq", "fun": constraint4},
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
