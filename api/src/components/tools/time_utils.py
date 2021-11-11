from datetime import timedelta

def formatUptime(s):
    if s is not None:
        x = str(timedelta(seconds=s)).split(':')
        s = f"{x[0]}h, {x[1]}m, {x[2]}s"
        return s
