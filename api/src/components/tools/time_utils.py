import datetime


def formatUptime(time, dasan=False):
    if time is not None:
        x = str(datetime.timedelta(seconds=(time, (time / 100))[dasan])).split(':')
        time = f"{str(datetime.timedelta(seconds=(time, (time / 100))[dasan])).split(' ')[0]}d {x[0][:2]}h {x[1]}m {round(float(x[2]), 0)}s"
    return time
