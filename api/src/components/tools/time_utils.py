intervals = (
    ('d', 86400),  # 60 * 60 * 24
    ('h', 3600),  # 60 * 60
    ('m', 60),
    ('s', 1),
)


def format_uptime(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append(f"{value}{name}")
    return ' '.join(result[:granularity])


def format_dasan_olt_uptime(time):
    x = time.split(':')
    return f'{x[0]}d {x[1]}h {x[2]}m {x[3][:2]}s'
