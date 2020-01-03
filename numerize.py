import re
import consts


HYPHENATED = re.compile(r' +|([^\d])-([^\d])')
imatch = lambda x, y: re.search(x, y, flags=re.IGNORECASE)  # noqa: E731
isub = lambda x, y, s: re.sub(x, y, s, flags=re.IGNORECASE)  # noqa: E731


def preprocess(s):
    s = re.sub(HYPHENATED, r'\1 \2', s)
    s = re.sub(r'\ba$', '', s)
    return s


def numerize(s, ignore=None, bias=None):
    if ignore is None:
        ignore = []
    s = preprocess(s)
    s = numerize_numerals(s, ignore, bias)
    s = numerize_fractions(s, ignore, bias)
    s = numerize_ordinals(s, ignore, bias)
    s = numerize_big_prefixes(s, ignore, bias)
    s = postprocess(s, ignore)
    return s


def regexify(words, ignore=None):
    if ignore is None:
        ignore = []
    return '|'.join([c for c in words if c not in ignore])


def numerize_numerals(s, ignore=None, bias=None):
    single_nums = regexify(consts.SINGLE_NUMS.keys(), ignore=ignore)
    dir_single_nums = regexify(consts.DIRECT_SINGLE_NUMS.keys(), ignore=ignore)
    ten_prefs = regexify(consts.TEN_PREFIXES.keys(), ignore=ignore)
    single_ords = regexify(consts.ORDINAL_SINGLE.keys(), ignore=ignore)

    # easy / direct replacements
    pat = re.compile(r'(^|\W)({0})(\s({1}))(?=$|\W)'.format(single_nums, ten_prefs),
                     flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        s = re.sub(pat, lambda m: f'{m.group(1)}{m.group(2)} hundred{m.group(3)}', s)

    #
    pat = re.compile(r'(^|\W)({0})(?=$|\W)'.format(dir_single_nums), flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        def _repl_single_digit(m):
            m1 = m.group(1)
            m2 = consts.DIRECT_SINGLE_NUMS[m.group(2)]
            return f'{m1}<num>{m2}'
        s = re.sub(pat, _repl_single_digit, s)

    if bias == 'ordinal':
        pat = r'(^|\W)\ba\b(?=$|\W)(?! (?:{0}))'.format(consts.ALL_ORDINALS_REGEX)
    else:
        pat = r'(^|\W)\ba\b(?=$|\W)'
    s = isub(pat, r'\1<num>1', s)

    # ten, twenty, etc
    pat = re.compile(r'(^|\W)({0})({1})(?=$|\W)'.format(ten_prefs, single_nums),
                     flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        def _repl_ten_prefixes(m):
            m1 = m.group(1)
            m2 = consts.TEN_PREFIXES[m.group(2)]
            m3 = consts.SINGLE_NUMS[m.group(3)]
            return f'{m1}<num>{m2 + m3}'
        s = re.sub(pat, _repl_ten_prefixes, s)

    #
    pat = re.compile(r'(^|\W)({0})(\s)?({1})(?=$|\W)'.format(ten_prefs, single_ords),
                     flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        def _repl_ten_prefs_single_ords(m):
            m2, m4 = m.group(2), m.group(4)
            repl = r'\1<num>' + str(
                consts.TEN_PREFIXES[m2] + consts.ORDINAL_SINGLE[m4] + m4[-2:])
            return repl
        s = re.sub(pat, _repl_ten_prefs_single_ords, s)

    #
    pat = re.compile(r'(^|\W)({})(?=$|\W)'.format(ten_prefs), flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        def _repl_ten_prefs(m):
            return f'{m.group(1)}<num>' + str(consts.TEN_PREFIXES[m.group(2)])
        s = re.sub(pat, _repl_ten_prefs, s)

    return s


def numerize_fractions(s, ignore=None, bias=None):
    if ignore is None:
        ignore = []
    if bias == 'ordinal':
        fractionals = regexify(consts.ONLY_PLURAL_FRACTIONS.keys(),
                               ignore=ignore + ['quarter', 'quarters'])
    elif bias == 'fractional':
        fractionals = regexify(consts.ALL_FRACTIONS.keys(), ignore=ignore)
    else:
        fractionals = regexify(consts.ALL_FRACTIONS.keys(),
                               ignore=ignore + ['quarter', 'quarters'])
    quarters = regexify(['quarter', 'quarters'], ignore=ignore)

    #
    pat = re.compile(r'a ({})(?=$|\W)'.format(fractionals), flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        def _repl_all_fractions(m):
            return f'<num>{m.group(1)}' + str(consts.ALL_FRACTIONS[m.group(1)])
        s = re.sub(pat, _repl_all_fractions, s)

    #
    if bias == 'fractional':
        pat = re.compile(r'(^|\W)({})(?=$|\W)'.format(fractionals), flags=re.IGNORECASE)
        m = re.search(pat, s)
    else:
        pat = re.compile(r'(?!the|^)(\W)({})(?=$|\W)'.format(fractionals),
                         flags=re.IGNORECASE)
        m = re.search(pat, s)
        if m is not None:
            s = re.sub(pat, lambda m: '/' + str(consts.ALL_FRACTIONS[m.group(2)]), s)
        pat = re.compile(r'(^|\W)({})(?=$|\W)'.format(quarters), flags=re.IGNORECASE)
        m = re.search(pat, s)
        if m is not None:
            s = re.sub(pat, lambda m: '/' + str(consts.ALL_FRACTIONS[m.group(2)]), s)
    s = cleanup_fractions(s)
    return s


def numerize_ordinals(s, ignore=None, bias=None):
    if bias == 'fractionals':
        return s
    if ignore is None:
        ignore = []
    all_ords = regexify(consts.ALL_ORDINALS.keys(), ignore=ignore)
    # {|x| x == 'second' && bias != :ordinal}
    if bias != 'ordinal' and 'second' not in ignore:
        m = imatch(r'(?!second|\d|{})(^|\W)second(?=$|\W)'.format(consts.ALL_ORDINALS_REGEX),
                   s)
        if m is not None:
            s = f'{m.group(1)}<num>{str(consts.ALL_ORDINALS["second"])}nd'
    else:
        m = imatch(r'(^|\W)({})(?=$|\W)'.format(all_ords), s)
        if m is not None:
            s = f'{m.group(1)}<num>{str(consts.ALL_ORDINALS["second"])}' + m.group(2)[-2:]
    return s


def numerize_big_prefixes(s, ignore=None, bias=None):
    if ignore is None:
        ignore = []
    for k, v in consts.BIG_PREFIXES.items():
        if k.lower() in ignore:
            continue
        pat = re.compile(r'(?:<num>)?(\d*) *{}'.format(k.lower()), flags=re.IGNORECASE)
        m = re.search(pat, s)
        if m is not None:
            def _repl_big_prefixes(m):
                try:
                    if m.group(1):
                        repl = '<num>' + str(v * int(m.group(1)))
                    else:
                        repl = str(v)
                except IndexError:
                    repl = str(v)
                return repl
            s = re.sub(pat, _repl_big_prefixes, s, count=1)
        s = andition(s)
    return s


def numerize_halves(s, ignore=None):
    if ignore is None:
        ignore = []
    if 'half' in ignore:
        return s
    return isub(r'\bhalf\b', '1/2', s)


def postprocess(s, ignore):
    s = andition(s)
    s = numerize_halves(s, ignore)
    s = re.sub(r'<num>', '', s)
    return s


def andition(s):
    pat = re.compile(r'<num>(\d+)( | and )<num>(\d+)(?=[^\w]|$)', flags=re.IGNORECASE)
    while True:
        m = re.search(pat, s)
        if m is not None:
            if (m.group(2) == 'and') or (len(m.group(1)) > len(m.group(3))):
                s = re.sub(pat, lambda m: '<num>' + str(int(m.group(1)) + int(m.group(3))),
                           s, count=1)
            else:
                break

        else:
            break
    return s


def cleanup_fractions(s):
    #  evaludate  fractions when preceded by another number
    pat = re.compile(r'(\d+)(?: | and |-)+(<num>|\s)*(\d+)\s*\/\s*(\d+)',
                     flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        def _repl_frac_cleanup(m):
            return str(float(m.group(1)) + (float(m.group(3)) / float(m.group(4))))
        s = re.sub(pat, _repl_frac_cleanup, s)

    # fix unpreceded fractions
    s = re.sub(r'(?:^|\W)\/(\d+)', r'1/\1', s)
    s = re.sub(r'(?<=[a-zA-Z])\/(\d+)', r'1/\1', s)
    return s


def main():
    print(numerize('three quarters'))


if __name__ == "__main__":
    main()
