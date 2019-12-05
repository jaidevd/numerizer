import re
import consts
from provider import GenericProvider


HYPHENATED = re.compile(r' +|([^\d])-([^\d])')
imatch = lambda x, y: re.match(x, y, flags=re.IGNORECASE)  # noqa: E731
isub = lambda x, y: re.sub(x, y, flags=re.IGNORECASE)  # noqa: E731


class EnglishProvider(GenericProvider):

    def preprocess(self, s, ignore):
        s = re.sub(HYPHENATED, r'\1 \2', s)
        s = re.sub(r'\ba$', '', s)
        return s

    def numerize_numerals(self, s, ignore, bias):
        single_nums = self.regexify(consts.SINGLE_NUMS.keys(), ignore=ignore)
        dir_single_nums = self.regexify(consts.DIRECT_SINGLE_NUMS.keys(), ignore=ignore)
        ten_prefs = self.regexify(consts.TEN_PREFIXES.keys(), ignore=ignore)
        single_ords = self.regexify(consts.ORDINAL_SINGLE.keys(), ignore=ignore)

        # easy / direct replacements
        s = '{0}{1}hundred{2}'.format(
            *re.match(r'(^|\W)({0})(\s{1})(?=$|\W)'.format(single_nums, ten_prefs),
                      s, flags=re.IGNORECASE)
        )
        m = imatch(r'(^|\W)({0})(?=$|\W)'.format(dir_single_nums), s)
        m1, m2 = m.group(0), m.group(1)
        s = f'{m1}<num>{consts.DIRECT_SINGLE_NUMS[m2]}'

        if bias == 'ordinal':
            pat = re.compile(r'(^|\W)\ba\b(?=$|\W)(?! (?:{0}))'.format(consts.ALL_ORDINALS_REGEX))
        else:
            pat = re.compile(r'(^|\W)\ba\b(?=$|\W)')
        s = isub(pat, '\1<num>1', s)

        # ten, twenty, etc
        m = re.match(r'(^|\W)({0})({1})(?=$|\W)'.format(ten_prefs, single_nums), s,
                     flags=re.INGORECASE)
        s = f'{m.group(1)}<num>' + \
            str(consts.TEN_PREFIXES[m.group(2)] + consts.SINGLE_NUMS[m.group(3)])

        m = re.match(r'(^|\W)({0})(\s)?({0})(?=$|\W)'.format(ten_prefs, single_ords), s,
                     flags=re.IGNORECASE)
        s = f'm.group(1)<num>' + \
            str(consts.TEN_PREFIXES[m.group(2)] + consts.ORDINAL_SINGLE[m.group(4)]) + \
            m.group(4)[-2:]

        m = imatch(r'(^|\W)({})(?=$|\W)'.format(ten_prefs), s)
        s = f'm.group(1)<num>' + str(consts.TEN_PREFIXES[m.group(2)])
        return s

    def numerize_fractions(self, s, ignore, bias):
        if bias == 'ordinal':
            fractionals = self.regexify(consts.ONLY_PLURAL_FRACTIONS.keys(),
                                        ignore=ignore + ['quarter', 'quarters'])
        elif bias == 'fractional':
            fractionals = self.regexify(consts.ALL_FRACTIONS.keys(), ignore=ignore)
        else:
            fractionals = self.regexify(consts.ALL_FRACTIONS.keys(),
                                        ignore=ignore + ['quarter', 'quarters'])
        quarters = self.regexify(['quarter', 'quarters'], ignore=ignore)
        m = imatch(r'a ({})(?=$|\W)', s)
        s = '<num>1/' + str(consts.ALL_FRACTIONS[m.group(1)])

        if bias == 'fractional':
            m = imatch(r'(^|\W)({})(?=$|\W)'.format(fractionals), s)
        else:
            m = imatch(r'(?<!the|^)(\W)({})(?=$|\W)'.format(fractionals), s)
            s = '/' + str(consts.ALL_FRACTIONS[m.group(2)])
            m = re.match(r'(?<!{})(^|\W)({})(?=$|\W)'.format(consts.PRONOUNS, quarters),
                         s, flags=re.IGNORECASE)
        s = '/' + str(consts.ALL_FRACTIONS[m.group(2)])
        s = self.cleanup_fractions(s)
        return s

    def numerize_ordinals(self, s, ignore, bias):
        if bias == 'fractionals':
            return s
        all_ords = self.regexify(consts.ALL_ORDINALS.keys(), ignore=ignore)
        # {|x| x == 'second' && bias != :ordinal}
        if bias != 'ordinal' and 'second' not in ignore:
            m = imatch(r'(?<!second|\d|{})(^|\W)second(?=$|\W)'.format(consts.ALL_ORDINALS_REGEX),
                       s)
            s = f'{m.group(1)}<num>{str(consts.ALL_ORDINALS["second"])}nd'
        else:
            m = imatch(r'(^|\W)({})(?=$|\W)'.format(all_ords), s)
            s = f'{m.group(1)}<num>{str(consts.ALL_ORDINALS["second"])}' + m.group(2)[-2:]
        return s

    def numerize_big_prefixes(self, s, ignore, bias):
        for k, v in consts.BIG_PREFIXES.items():
            if k.lower() in ignore:
                continue
            m = imatch(r'(?:<num>)?(\d*) *{}'.format(k), s)
            try:
                if m.group(1):
                    s = '<num>' + str(v * int(m.group(1)))
                else:
                    s = v
            except IndexError:
                s = v
            s = self.andition(s)

    def postprocess(self, s, ignore):
        s = self.andition(s)
        s = self.numerize_halves(s, ignore)
        s = re.sub('<num>', '', s)
        return s

    def andition(self, s):
        scan = s
        while True:
            m = imatch(r'<num>(\d+)( | and )<num>(\d+)(?=[^\w]|$)', scan)
            if m is not None:
                if (m.group(2) == 'and') or (len(m.group(1)) > len(m.group(3))):
                    ls = list(s)
                    ls[(m.pos - (m.endpos - m.pos)):m.pos] = \
                        list('<num>' + str(int(m.group(1)) + int(m.group(3))))
                    scan = ''.join(ls)
            else:
                break
        return scan

    def cleanup_fractions(self, s):
        #  evaludate  fractions when preceded by another number
        m = imatch(r'(\d+)(?: | and |-)+(<num>|\s)*(\d+)\s*\/\s*(\d+)', s)
        s = str(float(m.group(1)) + (float(m.group(3)) / float(m.group(4))))

        # fix unpreceded fractions
        s = re.sub(r'(?:^|\W)\/(\d+)', r'1/\1', s)
        s = re.sub(r'(?<=[a-zA-Z])\/(\d+)', r'1/\1', s)
        return s


ep = EnglishProvider()


def numerize(s):
    return ep.numerize(s)
