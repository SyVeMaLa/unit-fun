

class RovarSprak(object):

    _CONSONANTS = 'bcdfghjklmnpqrstvxz'

    def __init__(self, text=''):
        self._text = text

    @property
    def text(self):
        return self.rovar_decode(self._text)

    @text.setter
    def text(self, value):
        self._text = value

    def rovar_decode(self, text_to_decode):
        decoded = []
        for c in text_to_decode:
            if self.is_consonant(c):
                decoded.append('%so%s' % (c, c.lower()))
            else:
                decoded.append(c)
        return ''.join(decoded)

    def is_consonant(self, char):
        return char.lower() in self._CONSONANTS


def main():

    rs = RovarSprak('koko')
    print(rs.text)

    rs.text='muha !'

    print(rs.text)

# main()