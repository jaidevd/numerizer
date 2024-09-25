from unittest import TestCase, skipUnless
from numerizer import numerizer as num
from spacy import load
from spacy.tokens import Token

numerize = num.numerize

try:
    nlp = load("en_core_web_sm")
    SPACY_MODEL_INSTALLED = True
except OSError:
    SPACY_MODEL_INSTALLED = False

try:
    nlp_trf = load("en_core_web_trf")
    TRF_INSTALLED = True
except OSError:
    TRF_INSTALLED = False


def test_init():
    assert numerize("forty two") == "42"


def test_case_insensitive():
    assert numerize("Forty two") == "42"
    assert numerize("FORTY TWO") == "42"
    assert numerize("FORTY Second") == "42nd"
    assert numerize("Ninety Nine") == "99"


def test_hyphenated():
    assert numerize("forty-two") == "42"


def test_hundreds():
    assert numerize("four hundred and forty two") == "442"


def test_fraction():
    assert numerize("half") == "1/2"
    assert numerize("quarter") == "1/4"
    assert numerize("two and a half") == "2.5"
    assert numerize("three quarters") == "3/4"
    assert numerize("two and three eighths") == "2.375"
    assert numerize("2B/2B") == "2B/2B"


def test_straight_parsing():
    strings = {
        1: "one",
        5: "five",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
        16: "sixteen",
        17: "seventeen",
        18: "eighteen",
        19: "nineteen",
        20: "twenty",
        27: "twenty seven",
        31: "thirty-one",
        37: "thirty-seven",
        41: "forty one",
        42: "fourty two",
        59: "fifty nine",
        100: ["one hundred", "a hundred"],
        150: ["one hundred and fifty", "one fifty"],
        200: "two-hundred",
        500: "5 hundred",
        999: "nine hundred and ninety nine",
        1_000: "one thousand",
        1_200: ["twelve hundred", "one thousand two hundred"],
        17_000: "seventeen thousand",
        21_473: "twentyone-thousand-four-hundred-and-seventy-three",
        74_002: "seventy four thousand and two",
        99_999: "ninety nine thousand nine hundred ninety nine",
        100_000: "100 thousand",
        250_000: "two hundred fifty thousand",
        1_000_000: ["one million", "1.0 million"],
        1_200_000: "1.2 million",
        1_250_007: "one million two hundred fifty thousand and seven",
        1_000_000_000: "one billion",
        1_000_000_001: "one billion and one",
    }
    for k, v in strings.items():
        if isinstance(v, list):
            for s in v:
                assert numerize(s) == str(k)
        else:
            assert numerize(v) == str(k)


def test_combined_double_digits():
    assert "21" == numerize("twentyone")
    assert "37" == numerize("thirtyseven")


def test_fractions_in_words():
    assert "1/2" == numerize("one half")

    assert "1/4" == numerize("1 quarter")
    assert "1/4" == numerize("one quarter")
    assert "1/4" == numerize("a quarter")
    assert "1/8" == numerize("one eighth")

    assert "3/4" == numerize("three quarters")
    assert "2/4" == numerize("two fourths")
    assert "3/8" == numerize("three eighths")
    assert "7/10" == numerize("seven tenths")


def test_fractional_addition():
    assert "1.25" == numerize("one and a quarter")
    assert "2.375" == numerize("two and three eighths")
    assert "2.5" == numerize("two and a half")
    assert "3.5 hours" == numerize("three and a half hours")


def test_word_with_a_number():
    assert "pennyweight" == numerize("pennyweight")


def test_edges():
    assert "27 Oct 2006 7:30am" == numerize("27 Oct 2006 7:30am")


def test_multiple_slashes_should_not_be_evaluated():
    assert "11/02/2007" == numerize("11/02/2007")


def test_compatability():
    assert "1/2" == numerize("1/2")
    assert "05/06" == numerize("05/06")
    assert "3.5 hours" == numerize("three and a half hours")
    assert "1/2 an hour" == numerize("half an hour")
    assert "(1/2)+2" == numerize("(1/2)+2")
    assert "(10+10)/2" == numerize("(10+10)/2")
    assert "(10+10)/2" == numerize("(10+10)/two")
    assert "2*(45+21)/6" == numerize("2*(45+21)/6")


def test_ordinal_strings():
    ords = {
        "first": "1st",
        "second": "2nd",
        "third": "3rd",
        "fourth": "4th",
        "fifth": "5th",
        "seventh": "7th",
        "eighth": "8th",
        "tenth": "10th",
        "eleventh": "11th",
        "twelfth": "12th",
        "thirteenth": "13th",
        "sixteenth": "16th",
        "twentieth": "20th",
        "twenty-third": "23rd",
        "thirtieth": "30th",
        "thirty-first": "31st",
        "fourtieth": "40th",
        "fourty ninth": "49th",
        "fiftieth": "50th",
        "sixtieth": "60th",
        "seventieth": "70th",
        "eightieth": "80th",
        "ninetieth": "90th",
        "hundredth": "100th",
        "thousandth": "1000th",
        "millionth": "1000000th",
        "billionth": "1000000000th",
        "trillionth": "1000000000000th",
        "first day month two": "1st day month 2",
    }
    for k, v in ords.items():
        assert v == numerize(k)


def test_ambiguous_cases():
    # Quarter ( Coin ) is Untested
    # Second ( Time / Verb ) is Untested
    assert "the 4th" == numerize("the fourth")
    assert "1/3 of" == numerize("a third of")
    assert "4th" == numerize("fourth")
    assert "2nd" == numerize("second")
    # pronouns not supported yet
    # some ambiguous cases here are untested
    # assert 'I quarter' == numerize('I quarter')
    # assert 'You quarter' == numerize('You quarter')
    # assert 'I want to quarter' == numerize('I want to quarter')
    # assert 'the 1st 1/4' == numerize('the first quarter')
    assert "1/4 pound of beef" == numerize("quarter pound of beef")
    # assert 'the 2nd second' == numerize('the second second')
    # assert 'the 4th second' == numerize('the fourth second')
    # assert '1 second' == numerize('one second')


# TODO: Find way to distinguish this verb
# assert 'I peel and quarter bananas' == numerize('I peel and quarter bananas')


def test_ignore():
    assert "the second day of march" == numerize(
        "the second day of march", ignore=["second"]
    )
    assert "quarter" == numerize("quarter", ignore=["quarter"])
    assert "the five guys" == numerize("the five guys", ignore=["five"])
    assert "the fifty 2" == numerize("the fifty two", ignore=["fifty"])


def test_bias_ordinal():
    assert "4th" == numerize("fourth", bias="ordinal")
    assert "12th" == numerize("twelfth", bias="ordinal")
    assert "2nd" == numerize("second", bias="ordinal")
    assert "the 4th" == numerize("the fourth", bias="ordinal")
    assert "2.75" == numerize("two and three fourths", bias="ordinal")
    assert "3/5" == numerize("three fifths", bias="ordinal")
    assert "a 4th of" == numerize("a fourth of", bias="ordinal")
    # assert 'I quarter your home' == numerize('I quarter your home', bias='ordinal')
    # assert 'the 1st 2nd 3rd' == numerize('the first second third', bias='ordinal')


def test_bias_fractional():
    assert "1/4" == numerize("fourth", bias="fractional")
    assert "1/12" == numerize("twelfth", bias="fractional")
    assert "2nd" == numerize("second", bias="fractional")
    # assert 'the 1/4' == numerize('the fourth', bias='fractional')
    assert "2.75" == numerize("two and three fourths", bias="fractional")
    assert "3/5" == numerize("three fifths", bias="fractional")
    assert "1/4 of" == numerize("a fourth of", bias="fractional")
    # assert 'I 1/4 your home' == numerize('I quarter your home',
    #                                      bias='fractional')
    # assert 'the 1st second 1/3' == numerize('the first second third',
    #                                         bias='fractional')


def test_numerize_big_prefixes():
    s = "two hundred and twenty five thousand seven hundred"
    s = num.preprocess(s)
    s = num.numerize_numerals(s)
    assert num.numerize_big_prefixes(s) == "<num>225700"


def test_misc():
    ideal = "225755"
    actual = numerize("two hundred twenty five thousand seven hundred and fifty-five")
    assert ideal == actual


def test_andition():
    tests = {
        "thirty two and forty one": "32 and 41",
        "thirty two and forty one thousand": "32 and 41000",
        "one hundred and twenty three": "123",
        "two thousand and thirty four": "2034",
        "forty five and sixty seven": "45 and 67",
        "one hundred and twenty three thousand and forty five": "123045",
        "twenty five and seventy four and one": "25 and 74 and 1",
        "twenty five and seventy four and one thousand": "25 and 74 and 1000",
    }

    for test in tests.items():
        assert test[1] == numerize(test[0])


def test_whitespaces():
    assert "55000" == numerize("55  thousand")


# Test the spacy extensions
condt = """Please install spacy models as follows:
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy download en_core_web_lg
"""


@skipUnless(SPACY_MODEL_INSTALLED, condt)
class TestSpacyExtensions(TestCase):
    def test_spacy_default(self):
        doc = nlp("The Hogwarts Express is at platform nine and three quarters.")
        numerized = doc._.numerize()
        assert isinstance(numerized, dict)
        assert len(numerized) == 1
        key, val = numerized.popitem()
        assert key.text == "nine and three quarters"
        assert val == "9.75"

    def test_entity_filters(self):
        doc = nlp(
            """
            Their revenue has been a billion dollars, as of six months ago.
            The next quarter is not so promising."""
        )
        numerized = doc._.numerize(labels=["MONEY"])
        assert len(numerized) == 1
        key, val = numerized.popitem()
        assert key.text == "a billion dollars"
        assert val == "1000000000 dollars"

    def test_retokenize(self):
        doc = nlp("The Hogwarts Express is at platform nine and three quarters.")
        doc._.numerize(retokenize=True)
        assert isinstance(doc[-2], Token)
        assert doc[-2].text == "nine and three quarters"
        assert doc[-2]._.numerized == "9.75"

    def test_span_token_extensions(self):
        doc = nlp(
            "The projected revenue for the next quarter is over two million dollars."
        )
        assert doc[-4:-2]._.numerize() == "2000000"
        assert doc[6]._.numerized == "1/4"

    def test_article(self):
        # See: https://github.com/jaidevd/numerizer/issues/24
        _, val = nlp("A cat, a baby and a hundred puppies.")._.numerize().popitem()
        assert val == "100"

    @skipUnless(TRF_INSTALLED, "python -m spacy download en_core_web_trf")
    def test_whitespace(self):
        # See https://github.com/jaidevd/numerizer/issues/25
        numerized = nlp_trf("55  thousand")._.numerize()
        _, val = numerized.popitem()
        assert val == "55 "

        # But if we ignore labels,
        numerized = nlp_trf("55  thousand")._.numerize(labels=False)
        assert numerized == "55000"
