DIRECT_NUMS = {
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "ninteen": "19",
    "zero": "0",
    "ten": "10",
}

SINGLE_NUMS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

TEN_PREFIXES = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fourty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}

BIG_PREFIXES = {
    "hundred": 100,
    "thousand": 1000,
    "million": 1_000_000,
    "billion": 1_000_000_000,
    "trillion": 1_000_000_000_000,
}

FRACTIONS = {"half": 2, "halves": 2, "quarter": 4, "quarters": 4}

ORDINALS = {"first": 1, "second": 2}

SINGLE_ORDINAL_FRACTIONALS = {
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
}

DIRECT_ORDINAL_FRACTIONALS = {
    "tenth": "10",
    "eleventh": "11",
    "twelfth": "12",
    "thirteenth": "13",
    "fourteenth": "14",
    "fifteenth": "15",
    "sixteenth": "16",
    "seventeenth": "17",
    "eighteenth": "18",
    "nineteenth": "19",
    "twentieth": "20",
    "thirtieth": "30",
    "fourtieth": "40",
    "fiftieth": "50",
    "sixtieth": "60",
    "seventieth": "70",
    "eightieth": "80",
    "ninetieth": "90",
}

ALL_ORDINALS = ORDINALS.copy()
ALL_ORDINALS.update(SINGLE_ORDINAL_FRACTIONALS)
ALL_ORDINALS.update(DIRECT_ORDINAL_FRACTIONALS)

opf = SINGLE_ORDINAL_FRACTIONALS.copy()
opf.update(DIRECT_ORDINAL_FRACTIONALS)
opf.update(FRACTIONS)
ONLY_PLURAL_FRACTIONS = {k + "s": v for k, v in opf.items() if not k.endswith('s')}
ONLY_PLURAL_FRACTIONS.update({k: v for k, v in opf.items() if k.endswith('s')})

ALL_FRACTIONS = ONLY_PLURAL_FRACTIONS.copy()
ALL_FRACTIONS.update(SINGLE_ORDINAL_FRACTIONALS)
ALL_FRACTIONS.update(DIRECT_ORDINAL_FRACTIONALS)
ALL_FRACTIONS.update(opf)

DIRECT_SINGLE_NUMS = DIRECT_NUMS.copy()
DIRECT_SINGLE_NUMS.update(SINGLE_NUMS)

ORDINAL_SINGLE = ORDINALS.copy()
ORDINAL_SINGLE.update(SINGLE_ORDINAL_FRACTIONALS)

ALL_ORDINALS_REGEX = "|".join(ALL_ORDINALS.keys())
PRONOUNS = "|".join(["i", "you", "he", "she", "we", "it", "you", "they", "to", "the"])
