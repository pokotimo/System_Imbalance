import pyomo.environ as pyo
from pyomo.environ import ConcreteModel, Var, Objective, Constraint, SolverFactory, NonNegativeReals, Binary, minimize

# Define the model
model = ConcreteModel()

# Define variables for each asset at time 1
model.P1 = Var(domain=NonNegativeReals)
model.P2 = Var(domain=NonNegativeReals)
model.P3 = Var(domain=NonNegativeReals)
model.P4 = Var(domain=NonNegativeReals)

# Constants
SI = -50  # System Imbalance (SI) in timestep t in MW
AEP = 1.5  # Balancing energy price in €/MW
BK = [1, 0.5, 0.2, 0.1]
AEK = [2, 1, 0.4, 0.2]
previous_RL = 100  # Target value for the absolute deviation term

# Calculate RL (Reserve Load) as the sum of all P values
RL = model.P1 + model.P2 + model.P3 + model.P4

# Define auxiliary variables for absolute values |P[i] - target_power|
model.abs_dev1 = Var(domain=NonNegativeReals)
model.abs_dev2 = Var(domain=NonNegativeReals)
model.abs_dev3 = Var(domain=NonNegativeReals)
model.abs_dev4 = Var(domain=NonNegativeReals)

model.Constraint1 = pyo.Constraint(expr = model.P1 >= -125)
model.Constraint2 = pyo.Constraint(expr = model.P1 <= 125)
model.Constraint3 = pyo.Constraint(expr = model.P2 >= -125)
model.Constraint4 = pyo.Constraint(expr = model.P2 <= 125)
model.Constraint5 = pyo.Constraint(expr = model.P3 >= -150)
model.Constraint6 = pyo.Constraint(expr = model.P3 <= 150)
model.Constraint7 = pyo.Constraint(expr = model.P4 >= -300)
model.Constraint8 = pyo.Constraint(expr = model.P4 <= 300)

model.Constraint9 = pyo.Constraint(expr = model.P1 - previous_RL <= 250)
model.Constraint10 = pyo.Constraint(expr = model.P2 - previous_RL <= 25)
model.Constraint11 = pyo.Constraint(expr = model.P3 - previous_RL <= 15)
model.Constraint11 = pyo.Constraint(expr = model.P4 - previous_RL <= 2)

# Binary variable for sign handling in the objective function
model.sign_RL = Var(domain=Binary)

# Constraint for sign_RL: it determines whether RL > SI or not
# model.sign_constraint = Constraint(expr=(RL - SI) >= 0 if model.sign_RL == 1 else (RL - SI) <= 0)

# Objective function
# model.OBJ = Objective(
#     expr=(
#         -BK[0] * model.P1 - BK[0] ** 2 * model.P1 ** 2 - AEK[0] * model.abs_dev1
#         - BK[1] * model.P2 - BK[1] ** 2 * model.P2 ** 2 - AEK[1] * model.abs_dev2
#         - BK[2] * model.P3 - BK[2] ** 2 * model.P3 ** 2 - AEK[2] * model.abs_dev3
#         - BK[3] * model.P4 - BK[3] ** 2 * model.P4 ** 2 - AEK[3] * model.abs_dev4
#         + AEP * (2 * model.sign_RL - 1) * RL  # (2 * sign_RL - 1) simulates sign function
#     ),
#     sense=minimize
# )

model.OBJ = pyo.Objective(expr=-BK[0]*model.P1+-(BK[0])**2*model.P1**2
                          + (-AEK[0]*abs(model.P1-100))
                          + -BK[1]*model.P2+-(BK[1])**2*model.P2**2
                          + (-AEK[1]*abs(model.P2-100))
                          + -BK[2]*model.P3+-(BK[2])**2*model.P3**2
                          + (-AEK[2]*abs(model.P3-100))
                          + -BK[3]*model.P4+-(BK[3])**2*model.P4**2
                          + (-AEK[3]*abs(model.P4-100))
)
                        #   + AEP*sign(-SI+RL)*RL)


# Solve the model
solver = SolverFactory('ipopt')
solver.solve(model)

# Display results
for i in range(1, 5):
    print(f"P{i} = {pyo.value(getattr(model, f'P{i}'))}")
print(f"Objective = {pyo.value(model.OBJ)}")
