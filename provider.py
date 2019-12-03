import re


class GenericProvider(object):

    def numerize(self, s, ignore=None, bias=None):
        if ignore is None:
            ignore = []
        self.numerize_numerals(s, ignore, bias)
        self.numerize_fractions(s, ignore, bias)
        self.numerize_ordinals(s, ignore, bias)
        self.numerize_big_prefixes(self, s, ignore, bias)
        self.postprocess(self, s, ignore)

    def preprocess(self, s, ignore):
        raise NotImplementedError

    def numerize_numerals(self, s, ignore, bias):
        raise NotImplementedError

    def numerize_fractions(self, s, ignore, bias):
        raise NotImplementedError

    def numerize_ordinals(self, s, ignore, bias):
        raise NotImplementedError

    def numerize_big_prefixes(self, s, ignore, bias):
        raise NotImplementedError

    def postprocess(self, s, ignore):
        raise NotImplementedError

    def regexify(self, words, ignore=None):
        if ignore is None:
            ignore = []
        return re.compile('|'.join([c for c in words if c not in ignore]))
