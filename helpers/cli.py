def yes(defaultToYes = False):
    answer = input(f"{'(Y/n)' if defaultToYes else '(y/N)'}: ").lower()
    if answer not in ["n", "y", "no", "yes"]:
        return defaultToYes
    return answer == "y" or answer == "yes"

def getch():
    """
    This method waits for any key to continue (except modifiers, apperently).
    Lifted from https://stackoverflow.com/a/1394994 by John Millikin.
    """
    try:
        # Win32
        from msvcrt import getch
        getch()
    except ImportError:
        # UNIX
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
