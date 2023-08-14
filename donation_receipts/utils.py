import locale

_NUMERAL_MAP = {
    "0": "null",
    "1": "eins",
    "2": "zwei",
    "3": "drei",
    "4": "vier",
    "5": "fünf",
    "6": "sechs",
    "7": "sieben",
    "8": "acht",
    "9": "neun",
    ",": "komma",
    # Ignore '.' as indicated in https://esth.bundesfinanzministerium.de/esth/2016/C-Anhaenge/Anhang-37/I/anhang-37-I.html under point 5
}

_DELIMITER = " - "


def _convert_to_numeral(number):
    whole = int(number)
    decimal = str(round(number - whole, 2))[2:]

    whole_dotted = []

    for index, char in enumerate(reversed(str(whole))):
        if index != 0 and index % 3 == 0:
            whole_dotted.append(".")
        whole_dotted.append(char)

    out = "".join(reversed(whole_dotted))

    # only add decimal numbers if not 00
    if number - whole:
        out += "," + decimal

    return out


def _convert_to_written(number):
    number_formatted = _convert_to_numeral(number)

    out = []

    for char in number_formatted:
        try:
            out.append(_NUMERAL_MAP[char])
        except KeyError:
            pass

    return "X{}X".format(" - ".join(out))
