def yes(defaultToYes = False):
    answer = input("(y/N): ").lower()
    if defaultToYes:
        return answer == "n" or answer == "no"
    else:
        return answer == "y" or answer == "yes"
