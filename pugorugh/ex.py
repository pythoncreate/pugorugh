AGES = {
    'b': list(range(0, 6)),
    'y': list(range(6, 18)),
    'a': list(range(18, 72)),
    's': list(range(72, 192))
}


def get_ages(keys='b,y,a,s'):
    """Returns age ranges in years."""
    data = []
    for key in keys.split(','):
        data.extend(AGES[key])
    return data
