from mip import Model, xsum, MAXIMIZE, CONTINUOUS, BINARY
from collections import deque

def load_input_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        num_variables = int(lines[0][0])
        objective_coefficients = list(map(int, lines[1].split()))
        constraints = [list(map(int, line.split())) for line in lines[2:]]

        return num_variables, objective_coefficients, constraints
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

def solve_MIP_problem(num_variables, objective_coefficients, constraints):
    model = Model(name="MIP_Solution", solver_name="CBC", sense=MAXIMIZE)

    x = [model.add_var(var_type=BINARY, name=f'x_{i+1}') for i in range(num_variables)]
    model.objective += xsum(objective_coefficients[i] * x[i] for i in range(num_variables))

    for constraint in constraints:
        model += xsum(constraint[i] * x[i] for i in range(num_variables)) <= constraint[-1]

    model.optimize()

    return model.objective_value, model

def branch_and_bound_solver(num_variables, objective_coefficients, constraints):
    queue = deque()
    best_solution = float('-inf')
    best_model = None

    model = Model(solver_name="CBC", sense=MAXIMIZE)
    x = [model.add_var(var_type=CONTINUOUS, lb=0, ub=1, name=f'x_{i+1}') for i in range(num_variables)]
    model.objective += xsum(objective_coefficients[i] * x[i] for i in range(num_variables))

    for constraint in constraints:
        model += xsum(constraint[i] * x[i] for i in range(num_variables)) <= constraint[-1]

    queue.append(model)

    while queue:
        model = queue.popleft()
        model.optimize()

        if model.objective_value and model.objective_value > best_solution:
            fractional_vars = [(var, abs(var.x - 0.5)) for var in model.vars if not var.x.is_integer()]
            fractional_vars.sort(key=lambda x: x[1])

            if not fractional_vars:
                best_solution = model.objective_value
                best_model = model
            else:
                var, _ = fractional_vars[0]
                idx = var.idx

                model1 = model.copy()
                model2 = model.copy()

                model1 += model1.vars[idx] == 1
                model2 += model2.vars[idx] == 0

                queue.append(model1)
                queue.append(model2)

    return best_solution, best_model


instance_name = "teste2.txt"
data = load_input_file(instance_name)

if data:
    num_variables, objective_coefficients, constraints = data

    best_solution, best_model = branch_and_bound_solver(num_variables, objective_coefficients, constraints)

    if best_model:
        best_model.name = instance_name
        best_model.write(f"{instance_name}.lp")

        print(f"Best solution found (BB): {best_solution}")

        print("Variables (BB):")
        for var in best_model.vars:
            print(f"{var.name} = {var.x}")

        print("Solving with MIP...")
        best_solution_mip, best_model_mip = solve_MIP_problem(num_variables, objective_coefficients, constraints)
        print(f"Best solution found (MIP): {best_solution_mip}")
        print("Variables (MIP):")
        for var in best_model_mip.vars:
            print(f"{var.name} = {var.x}")


