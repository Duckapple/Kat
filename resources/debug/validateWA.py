import filecmp
import os
generator = "generator.py"
solution = "../problemName.py"
bruteForce = "bruteforce.py"
iterations = 1000

solutionOut = "problemName.ans"
bruteOut = "test.ans"

print(f"Running {iterations} iterations")
for i in range(1, iterations):
    print(i)
    os.system(f"python {generator} > test.in")
    os.system(f"python {solution} < test.in > {solutionOut}")
    os.system(f"python {bruteForce} < test.in > {bruteOut}")
    if not filecmp.cmp(solutionOut, bruteOut):
        print("Error found")
        break