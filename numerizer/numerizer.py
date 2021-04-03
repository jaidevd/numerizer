import re
from . import consts
try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
    SPACY_INSTALLED = True
except ImportError:
    SPACY_INSTALLED = False


HYPHENATED = re.compile(r' +|([^\d])-([^\d])')
isub = lambda x, y, s: re.sub(x, y, s, flags=re.IGNORECASE)  # noqa: E731
SPACY_ENT_LABELS = ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL', 'ORDINAL']


# Replacement regular expressions - to be used only in `re.sub`
def _repl_single_digit(m):
    m1 = m.group(1)
    m2 = consts.DIRECT_SINGLE_NUMS[m.group(2).lower()]
    return f'{m1}<num>{m2}'


def _repl_ten_prefixes(m):
    m1 = m.group(1)
    m2 = consts.TEN_PREFIXES[m.group(2).lower()]
    m3 = consts.SINGLE_NUMS[m.group(3).lower()]
    return f'{m1}<num>{m2 + m3}'


def _repl_ten_prefs_single_ords(m):
    m2, m4 = m.group(2), m.group(4)
    repl = f'{m.group(1)}<num>' \
        + str(consts.TEN_PREFIXES[m2.lower()] + consts.ORDINAL_SINGLE[m4.lower()]) \
        + m4[-2:]
    return repl


def _repl_ten_prefs(m):
    return f'{m.group(1)}<num>' + str(consts.TEN_PREFIXES[m.group(2).lower()])


def _repl_all_fractions(m):
    return f'<num>{m.group(1)}' + str(consts.ALL_FRACTIONS[m.group(1).lower()])


# Public

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
        s = re.sub(pat, _repl_single_digit, s)

    if bias == 'ordinal':
        pat = re.compile(r'(^|\W)\ba\b(?=$|\W)(?! (?:{}))'.format(consts.ALL_ORDINALS_REGEX),
                         flags=re.IGNORECASE)
    else:
        pat = re.compile(r'(^|\W)\ba\b(?=$|\W)', flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        s = re.sub(pat, r'\1<num>1', s, count=1)

    # ten, twenty, etc
    pat = re.compile(r'(^|\W)({0})({1})(?=$|\W)'.format(ten_prefs, single_nums),
                     flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        s = re.sub(pat, _repl_ten_prefixes, s)

    #
    pat = re.compile(r'(^|\W)({0})(\s)?({1})(?=$|\W)'.format(ten_prefs, single_ords),
                     flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        try:
            s = re.sub(pat, _repl_ten_prefs_single_ords, s)
        except TypeError:
            from ipdb import set_trace; set_trace()  # NOQA

    #
    pat = re.compile(r'(^|\W)({})(?=$|\W)'.format(ten_prefs), flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
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
        s = re.sub(pat, _repl_all_fractions, s)

    #
    if bias == 'fractional':
        pat = re.compile(r'(^|\W)({})(?=$|\W)'.format(fractionals), flags=re.IGNORECASE)
        m = re.search(pat, s)
    else:
        # Terrible hack below for variable negative lookbehind.
        pat = re.compile(r'(?<!the)(\W)({})(?=$|\W)'.format(fractionals),
                         flags=re.IGNORECASE)
        pat2 = re.compile(r'(?<!^)(\W)({})(?=$|\W)'.format(fractionals),
                          flags=re.IGNORECASE)
        m = re.search(pat, s)
        m2 = re.search(pat2, s)
        if not(m and m2):
            m = None
        if m is not None:
            s = re.sub(pat, lambda m: '/' + str(consts.ALL_FRACTIONS[m.group(2).lower()]),
                       s, count=1)
        pat = re.compile(r'(^|\W)({})(?=$|\W)'.format(quarters), flags=re.IGNORECASE)
        m = re.search(pat, s)
    if m is not None:
        s = re.sub(pat, lambda m: '/' + str(consts.ALL_FRACTIONS[m.group(2).lower()]), s, count=1)
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
        pat = re.compile(r'(?!second|\d|{})(^|\W)second(?=$|\W)'.format(consts.ALL_ORDINALS_REGEX),
                         flags=re.IGNORECASE)
        m = re.search(pat, s)
        if m is not None:
            def _repl_ordinal(m):
                m1 = m.group(1)
                m2 = str(consts.ALL_ORDINALS['second'.lower()])
                return f'{m1}<num>{m2}nd'
            s = re.sub(pat, _repl_ordinal, s, count=1)
    pat = re.compile(r'(^|\W)({})(?=$|\W)'.format(all_ords), flags=re.IGNORECASE)
    m = re.search(pat, s)
    if m is not None:
        def _repl_ordinal(m):
            m1 = m.group(1)
            m2 = str(consts.ALL_ORDINALS[m.group(2).lower()])
            return f'{m1}<num>{m2}' + m.group(2)[-2:]
        s = re.sub(pat, _repl_ordinal, s, count=1)
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
            s = re.sub(pat, _repl_big_prefixes, s)
        s = andition(s)
    return s


def numerize_halves(s, ignore=None):
    if ignore is None:
        ignore = []
    if 'half' in ignore:
        return s
    return isub(r'\bhalf\b', '1/2', s)


def postprocess(s, ignore=None):
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


def _span_numerize(span):
    return numerize(span.text)


def spacy_numerize(doc, labels='all', retokenize=False):
    """Numerize a spacy document.

    Parameters
    ----------
    doc : spacy.tokens.Doc
        The SpaCy document to be numerized
    labels : str / list, optional
        The list of entity labels to be processed for numerization.
        By default, all numeric tokens
        (['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL', 'ORDINAL'])
        are numerized. Any subset of this list can be specified to restrict
        the types of entities to be numerized.
    retokenize: bool, optional
        If True, the original document is retokenized such that the span corresponding
        to each numerized entity becomes a single token.

    Examples
    --------
    >>> from spacy import load
    >>> nlp = load('en_core_web_sm')
    >>> spacy_numerize(nlp('The Hogwarts Express is at platform nine and three quarters.'))
    {nine and three quarters: '9.75'}
    >>> spacy_numerize(
    ...    nlp('Their revenue has been a billion dollars, as of six months ago.'),
    ...    labels=['MONEY']
    ... )
    {a billion dollars: '1000000000 dollars'}
    >>> doc = nlp('The Hogwarts Express is at platform nine and three quarters.')
    >>> spacy_numerize(doc, retokenize=True)
    >>> [(c.text, c._.numerized) for c in doc]
    [('The', 'The'),
     ('Hogwarts', 'Hogwarts'),
     ('Express', 'Express'),
     ('is', 'is'),
     ('at', 'at'),
     ('platform', 'platform'),
     ('nine and three quarters', '9.75'),
     ('.', '.')]
    """
    if not SPACY_INSTALLED:
        import warnings
        warnings.warn('SpaCy is not installed. Please pip install spacy.')
        return
    if labels == 'all':
        labels = SPACY_ENT_LABELS
    elif not labels:
        return numerize(doc.text)
    numerized_spans = {span: span._.numerize() for span in doc.ents if span.label_ in labels}
    if not retokenize:
        return numerized_spans
    with doc.retokenize() as retokenizer:
        for span, numerized in numerized_spans.items():
            retokenizer.merge(span, attrs={'_': {'numerized': numerized}})
    return doc


def _span_setter(token, numerized): return  # NOQA: E704


def register_extension():
    if SPACY_INSTALLED:
        spacy.tokens.Token.set_extension(
            'numerized', getter=_span_numerize,
            setter=_span_setter)
        spacy.tokens.Span.set_extension('numerize', method=_span_numerize)
        spacy.tokens.Doc.set_extension('numerize', method=spacy_numerize)


register_extension()
