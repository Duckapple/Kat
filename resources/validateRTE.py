import os
generator = "generator.py"
solution = "../problemName.py"
iterations = 1000

solutionOut = "problemName.ans"

print(f"Running {iterations} iterations")
for i in range(1, iterations):
    print(i)
    os.system(f"python {generator} > test.in")
    code = os.system(f"python {solution} < test.in > {solutionOut}")
    if code != 0:
        print("Error found")
        break