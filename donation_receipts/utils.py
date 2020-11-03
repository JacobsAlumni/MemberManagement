

_NUMERAL_MAP = {
    '0': 'null',
    '1': 'eins',
    '2': 'zwei',
    '3': 'drei',
    '4': 'vier',
    '5': 'fünf',
    '6': 'sechs',
    '7': 'sieben',
    '8': 'acht',
    '9': 'neun',
    ',': 'komma',
    '.': 'komma'  # This is the German way of writing out the number
}

_DELIMITER = ' - '


def _convert_to_written(number):
    out = []

    for char in str(number):
        try:
            out.append(_NUMERAL_MAP[char])
        except KeyError:
            pass

    return "X{}X".format(" - ".join(out))
