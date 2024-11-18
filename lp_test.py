from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, value

# Define the initial system imbalance in MW
initial_imbalance = 500

# Define the problem
model = LpProblem("System_Imbalance_Minimization", LpMinimize)

# Define control variables for each asset with their respective control ranges
A = LpVariable("Asset_A_Control", lowBound=-300, upBound=300)
B = LpVariable("Asset_B_Control", lowBound=-150, upBound=150)
C = LpVariable("Asset_C_Control", lowBound=-125, upBound=125)
D = LpVariable("Asset_D_Control", lowBound=-125, upBound=125)

# Define the remaining imbalance as an expression
remaining_imbalance = initial_imbalance - (A + B + C + D)

# Define a variable for the absolute value of the remaining imbalance
RemainingImbalanceAbs = LpVariable("Remaining_Imbalance_Abs", lowBound=0)

# Add constraints to ensure RemainingImbalanceAbs is the absolute value of remaining_imbalance
model += RemainingImbalanceAbs >= remaining_imbalance
model += RemainingImbalanceAbs >= -remaining_imbalance

# Add speed of change limits as constraints
model += A <= 2
model += A >= -2
model += B <= 15
model += B >= -15
model += C <= 25
model += C >= -25
model += D <= 250
model += D >= -250

# Define the objective function to minimize the absolute remaining imbalance
model += RemainingImbalanceAbs, "Minimize_System_Imbalance"

# Solve the problem
model.solve()

# Output results
print("Status:", LpStatus[model.status])
print("Optimal Control for Asset A:", A.varValue)
print("Optimal Control for Asset B:", B.varValue)
print("Optimal Control for Asset C:", C.varValue)
print("Optimal Control for Asset D:", D.varValue)
print("Remaining Imbalance:", value(remaining_imbalance))
print("Absolute Remaining Imbalance:", value(RemainingImbalanceAbs))
