import random
import re


def text_placeholder(param):
    """Convenience function to instantiate BlahBlah and call one of its methods.

"""

    sample = None
    entity = 'text'
    length = None

    if 'sample' in param:
        sample = param['sample']

    if 'entity' in param and param['entity'] in ('word', 'sentence', 'paragraph', 'text'):
        entity = param['entity']

    if 'length' in param and param['length'] and param['length'].isdigit():
        length = int(param['length'])

    if entity == 'text' and length is None:
        length = 5

    return getattr(BlahBlah(sample=sample), entity)(length)



class BlahBlah:
    """Generates various amounts of random strings based on a sample.

"""

    sample = '''
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''

    vowel = 'aeiou'
    consonant = 'cbdgfhkjmlnqpsrtwvyxz'
    punctuation = '.!?'
    delimiter = ',;:'


    def __init__(self, sample=None, complete=0, group=False):
        """Initializes a random text generator instance.

sample: sample text from which to calculate frequencies ( The Zen of Python )
complete: add missing values to the sets ( 0 )
    - 0: do not complete
    - -1: complete with the average of the other values
    - 1..100: complete with this percent of other values
group: use letter groups instead of just letters ( False )

"""
        def extract(charset, default):
            result = re.findall(r'[' + charset + ']' + ('+' if group else ''), sample)

            if complete:
                if complete == -1:
                    count = max(int(round(len(result) / float(len(set(result))))), 1)
                else:
                    count = max(int(round(len(result) * complete / 100.0)), 1)

                result.extend(list(''.join([i * count for i in charset if i not in result])))

            if not result:
                result = default

            return result

        if not sample:
            sample = BlahBlah.sample

        sample = re.sub(r'[^' + BlahBlah.vowel + BlahBlah.consonant + BlahBlah.punctuation + BlahBlah.delimiter + ']+', ' ', sample.lower()).strip()

        self.vowelset = extract(BlahBlah.vowel, ('a', 'o'))
        self.consonantset = extract(BlahBlah.consonant, ('d', 'j', 'n', 'g'))
        self.punctuationset = extract(BlahBlah.punctuation, ('.',))
        self.delimiterset = extract(BlahBlah.delimiter, (',',))

        self.wordset = [len(word) for word in re.sub(r'[' + BlahBlah.punctuation + BlahBlah.delimiter + ' ]+', ' ', sample).split()]
        self.sentenceset = [len(sentence.split()) for sentence in re.split(r'[' + BlahBlah.punctuation + ']', sample.strip(BlahBlah.punctuation))]
        self.paragraphset = range(int(round(len(self.sentenceset) / 2.0)), int(round(len(self.sentenceset) / 2.0 * 3)))


    def word(self, length=None):
        """Generates a random word.

length: number of letters ( randomly chosen from analyzed data )
returns: the generated word

"""

        if not length:
            length = random.choice(self.wordset)

        letter = True # True vowel, False consonant
        hasvowel = False
        if length > 1:
            letter = random.randint(0, 1) == 0

        result = ''
        while len(result) < length:
            new = random.choice(self.vowelset if letter else self.consonantset)

            if len(result + new) == length and not letter and not hasvowel:
                continue

            if len(result + new) <= length:
                result += new

                if letter:
                    hasvowel = True

                letter = not letter

        return result


    def sentence(self, length=None):
        """Generates a random sentence.

length: number of words ( randomly chosen from analyzed data )
returns: the generated sentence

"""

        if not length:
            length = random.choice(self.sentenceset)

        list = [self.word() for i in range(length)]

        list[0] = list[0].capitalize()

        result = ' '.join(list)

        result += random.choice(self.punctuationset)

        return result


    def paragraph(self, length=None):
        """Generates a random paragraph.

length: number of sentences ( randomly chosen from analyzed data )
returns: the generated paragraph

"""
        if not length:
            length = random.choice(self.paragraphset)

        result = '  '.join([self.sentence() for i in range(length)])

        return result


    def text(self, length=5, wrap=None):
        """Generates a random text.

length: number of paragraphs ( 5 )
wrap: HTML tag name to wrap each paragraphs in ( None )
returns: the generated text

Note that the wrap is only the tag name, optionally with attribute, not including the tag delimiters.

"""

        begin = end = ''
        if wrap:
            begin = '<' + wrap + '>'
            end = '</' + wrap.split()[0] + '>'

        result = '\n\n'.join([begin + self.paragraph() + end for i in range(length)])

        return result



if __name__ == '__main__':
    bb = BlahBlah(group=True)
    print bb.word(), "\n"
    print bb.sentence(), "\n"
    print bb.paragraph(), "\n"
    print bb.text(3), "\n"
    print bb.text(3, 'p'), "\n"
    print bb.text(3, 'p class="blahblah"'), "\n"
