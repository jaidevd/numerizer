from numerize import numerize


def test_init():
    assert numerize('forty two') == '42'


def test_hyenated():
    assert numerize('forty-two') == '42'


def test_hundreds():
    assert numerize('four hundred and forty two') == '442'


def test_fraction():
    assert numerize('half') == '1/2'
    assert numerize('quarter') == '1/4'
    assert numerize('two and a half') == '2.5'
    assert numerize('three quarters') == '3/4'
    assert numerize('two and three eighths') == '2.375'


def test_straight_parsing():
    strings = {
        1: 'one',
        5: 'five',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'fourteen',
        15: 'fifteen',
        16: 'sixteen',
        17: 'seventeen',
        18: 'eighteen',
        19: 'nineteen',
        20: 'twenty',
        27: 'twenty seven',
        31: 'thirty-one',
        37: 'thirty-seven',
        41: 'forty one',
        42: 'fourty two',
        59: 'fifty nine',
        100: ['one hundred', 'a hundred'],
        150: ['one hundred and fifty', 'one fifty'],
        200: 'two-hundred',
        500: '5 hundred',
        999: 'nine hundred and ninety nine',
        1_000: 'one thousand',
        1_200: ['twelve hundred', 'one thousand two hundred'],
        17_000: 'seventeen thousand',
        21_473: 'twentyone-thousand-four-hundred-and-seventy-three',
        74_002: 'seventy four thousand and two',
        99_999: 'ninety nine thousand nine hundred ninety nine',
        100_000: '100 thousand',
        250_000: 'two hundred fifty thousand',
        1_000_000: 'one million',
        1_250_007: 'one million two hundred fifty thousand and seven',
        1_000_000_000: 'one billion',
        1_000_000_001: 'one billion and one'
    }
    for k, v in strings.items():
        if isinstance(v, list):
            for s in v:
                assert numerize(s) == str(k)
        else:
            assert numerize(v) == str(k)
#
#     strings.sort.each do |key, value|
#       Array(value).each do |value|
#         assert_equal key, Numerizer.numerize(value).to_i
#       end
#     end
#
#     assert_equal "1/2", Numerizer.numerize("half")
#     assert_equal "1/4", Numerizer.numerize("quarter")
#   end
#
#   def test_combined_double_digets
#     assert_equal "21", Numerizer.numerize("twentyone")
#     assert_equal "37", Numerizer.numerize("thirtyseven")
#   end
#
#   def test_fractions_in_words
#     assert_equal "1/2", Numerizer.numerize("one half")
#
#     assert_equal "1/4", Numerizer.numerize("1 quarter")
#     assert_equal "1/4", Numerizer.numerize("one quarter")
#     assert_equal "1/4", Numerizer.numerize("a quarter")
#     assert_equal "1/8", Numerizer.numerize("one eighth")
#
#     assert_equal "3/4", Numerizer.numerize("three quarters")
#     assert_equal "2/4", Numerizer.numerize("two fourths")
#     assert_equal "3/8", Numerizer.numerize("three eighths")
#     assert_equal "7/10", Numerizer.numerize("seven tenths")
#   end
#
#   def test_fractional_addition
#     assert_equal "1.25", Numerizer.numerize("one and a quarter")
#     assert_equal "2.375", Numerizer.numerize("two and three eighths")
#     assert_equal "2.5", Numerizer.numerize("two and a half")
#     assert_equal "3.5 hours", Numerizer.numerize("three and a half hours")
#   end
#
#   def test_word_with_a_number
#     assert_equal "pennyweight", Numerizer.numerize("pennyweight")
#   end
#
#   def test_edges
#     assert_equal "27 Oct 2006 7:30am", Numerizer.numerize("27 Oct 2006 7:30am")
#   end
#
#   def test_multiple_slashes_should_not_be_evaluated
#     assert_equal '11/02/2007', Numerizer.numerize('11/02/2007')
#   end
#
#   def test_compatability
#     assert_equal '1/2', Numerizer.numerize('1/2')
#     assert_equal '05/06', Numerizer.numerize('05/06')
#     assert_equal "3.5 hours", Numerizer.numerize("three and a half hours")
#     assert_equal "1/2 an hour", Numerizer.numerize("half an hour")
#   end
#
#   def test_ordinal_strings
#     {
#       'first' => '1st',
#       'second' => '2nd',
#       'third' => '3rd',
#       'fourth' => '4th',
#       'fifth' => '5th',
#       'seventh' => '7th',
#       'eighth' => '8th',
#       'tenth' => '10th',
#       'eleventh' => '11th',
#       'twelfth' => '12th',
#       'thirteenth' => '13th',
#       'sixteenth' => '16th',
#       'twentieth' => '20th',
#       'twenty-third' => '23rd',
#       'thirtieth' => '30th',
#       'thirty-first' => '31st',
#       'fourtieth' => '40th',
#       'fourty ninth' => '49th',
#       'fiftieth' => '50th',
#       'sixtieth' => '60th',
#       'seventieth' => '70th',
#       'eightieth' => '80th',
#       'ninetieth' => '90th',
#       'hundredth' => '100th',
#       'thousandth' => '1000th',
#       'millionth' => '1000000th',
#       'billionth' => '1000000000th',
#       'trillionth' => '1000000000000th',
#       'first day month two' => '1st day month 2'
#     }.each do |key, val|
#       assert_equal val, Numerizer.numerize(key)
#     end
#   end
#
#   def test_ambiguous_cases
#     # Quarter ( Coin ) is Untested
#     # Second ( Time / Verb ) is Untested
#     assert_equal 'the 4th', Numerizer.numerize('the fourth')
#     assert_equal '1/3 of', Numerizer.numerize('a third of')
#     assert_equal '4th', Numerizer.numerize('fourth')
#     assert_equal '2nd', Numerizer.numerize('second')
#     assert_equal 'I quarter', Numerizer.numerize('I quarter')
#     assert_equal 'You quarter', Numerizer.numerize('You quarter')
#     assert_equal 'I want to quarter', Numerizer.numerize('I want to quarter')
#     assert_equal 'the 1st 1/4', Numerizer.numerize('the first quarter')
#     assert_equal '1/4 pound of beef', Numerizer.numerize('quarter pound of beef')
#     assert_equal 'the 2nd second', Numerizer.numerize('the second second')
#     assert_equal 'the 4th second', Numerizer.numerize('the fourth second')
#     assert_equal '1 second', Numerizer.numerize('one second')
#
#   # TODO: Find way to distinguish this verb
#   # assert_equal 'I peel and quarter bananas', Numerizer.numerize('I peel and quarter bananas')
#   end
#
#   def test_ignore
#     assert_equal 'the second day of march', Numerizer.numerize('the second day of march',
#                                                                ignore: ['second'])
#     assert_equal 'quarter', Numerizer.numerize('quarter', ignore: ['quarter'])
#     assert_equal 'the five guys', Numerizer.numerize('the five guys', ignore: ['five'])
#     assert_equal 'the fifty 2', Numerizer.numerize('the fifty two', ignore: ['fifty'])
#   end
#
#   def test_bias_ordinal
#     assert_equal '4th', Numerizer.numerize('fourth', bias: :ordinal)
#     assert_equal '12th', Numerizer.numerize('twelfth', bias: :ordinal)
#     assert_equal '2nd', Numerizer.numerize('second', bias: :ordinal)
#     assert_equal 'the 4th', Numerizer.numerize('the fourth', bias: :ordinal)
#     assert_equal '2.75', Numerizer.numerize('two and three fourths', bias: :ordinal)
#     assert_equal '3/5', Numerizer.numerize('three fifths', bias: :ordinal)
#     assert_equal 'a 4th of', Numerizer.numerize('a fourth of', bias: :ordinal)
#     assert_equal 'I quarter your home', Numerizer.numerize('I quarter your home', bias: :ordinal)
#     assert_equal 'the 1st 2nd 3rd',  Numerizer.numerize('the first second third', bias: :ordinal)
#   end
#
#   def test_bias_fractional
#     assert_equal '1/4', Numerizer.numerize('fourth', bias: :fractional)
#     assert_equal '1/12', Numerizer.numerize('twelfth', bias: :fractional)
#     assert_equal '2nd', Numerizer.numerize('second', bias: :fractional)
#     assert_equal 'the 1/4', Numerizer.numerize('the fourth', bias: :fractional)
#     assert_equal '2.75', Numerizer.numerize('two and three fourths', bias: :fractional)
#     assert_equal '3/5', Numerizer.numerize('three fifths', bias: :fractional)
#     assert_equal '1/4 of', Numerizer.numerize('a fourth of', bias: :fractional)
#     assert_equal 'I 1/4 your home', Numerizer.numerize('I quarter your home',
#                                                        bias: :fractional)
#     assert_equal 'the 1st second 1/3',  Numerizer.numerize('the first second third',
#                                                            bias: :fractional)
#   end
# end
