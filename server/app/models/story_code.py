import re
from google.appengine.ext import ndb
import json
import wordcode

NON_ALPHA = r'[^a-z]'


class StoryCode(ndb.Model):
    story_uid = ndb.StringProperty(required=True)
    word_string = ndb.StringProperty(required=True)
    uid = ndb.ComputedProperty(lambda s: StoryCode.gen_key(s.word_string))
    used = ndb.BooleanProperty(default=False)
    single_use = ndb.BooleanProperty(default=False)

    @staticmethod
    def gen_key(words):
        return re.sub(NON_ALPHA, '', ''.join(words).lower())

    @classmethod
    def build_key(cls, words):
        code = StoryCode.gen_key(words)
        return ndb.Key(cls, code)

    @classmethod
    def from_words(cls, words, **kwargs):
        return cls(key=cls.build_key(words), word_string=words, **kwargs)

    def use(self):
        if self.single_use:
            self.used = True
            self.put()

    def toJSON(self):
        return {'word_string': self.word_string,
                'used': str(self.used).lower(),
                'single_use': str(self.single_use).lower(),
                'story_uid': self.story_uid}


def generate_codes(story_uid, amount, single_use):
    codes = []
    while len(codes) < amount:
        words = wordcode.gen(3)
        key = StoryCode.build_key(words)
        if not key.get():
            code = StoryCode.from_words(words, story_uid=story_uid, single_use=single_use)
            codes.append(code)
            code.put()
    return codes