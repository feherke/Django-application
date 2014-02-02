from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.conf import settings

import re

from .. import text_placeholder

register = template.Library()


@register.filter(name='blahblah', is_safe=True)
@stringfilter
def blahblah_filter(value, param=None):
    """Handles blahblah template filter.

Syntax :
    {{ sample | blahblah[:"entity length"] }}

Parameters :
    sample  - sample text to analyze, provides base values for the random properties of the text
    entity  - one of "word", "sentence", "paragraph", "text"
    length  - integer indicating how many sub-entities should the generated entity contain

Example :
    {{ document.title | blahblah:"sentence 10" }}  - One sentence of 10 words; using template variable for sample.
    {{ "Hello World" | blahblah:"word" }}  - One word; letter count chosen randomly based on analyzed sample; using fixed sample.
    {{ "" | blahblah }}  - One text of 5 paragraphs; using default sample.

"""

    tpparam = {'sample': value or None}
    if param:
        match = re.match(r'(?P<entity>word|sentence|paragraph|text)s?(?:\s*(?P<length>\d+))?$', param)
        if match:
            tpparam.update(match.groupdict())

    return text_placeholder.text_placeholder(tpparam)


@register.tag(name='blahblah')
def blahblah_tag(parser, token):
    """Handles blahblah template tag.

Syntax :
    {% blahblah [entity [length]] %}

Parameters :
    entity  - one of "word", "sentence", "paragraph", "text"
    length  - integer indicating how many sub-entities should the generated entity contain

Example :
    {% blahblah "sentence" 10 %}  - One sentence of 10 words.
    {% blahblah "word" %}  - One word; letter count chosen randomly based on analyzed sample.
    {% blahblah %}  - One text of 5 paragraphs.

"""

    param = token.split_contents()
    tag = param.pop(0)

    if len(param) > 2:
        raise template.TemplateSyntaxError("%r tag requires 0, 1 or 2 arguments" % tag)

    return BlahBlahNode(param)



class BlahBlahNode(template.Node):
    """Helper class to generate a Node for blahblah template tag.
"""

    def __init__(self, param):

        self.param = param

        for i, one in enumerate(self.param):
            if one[0] == one[-1] and one[0] in ('"', "'"):
                self.param[i] = one[1:-1]
            elif not one.isdigit():
                self.param[i] = template.Variable(one)


    def render(self, context):

        for i, one in enumerate(self.param):
            if isinstance(one, template.Variable):
                try:
                    self.param[i] = one.resolve(context)
                except template.VariableDoesNotExist:
                    pass # will handle in text_placeholder

        tpparam = {}
        if self.param:
            tpparam = dict(zip(('entity', 'length'), self.param))

        return text_placeholder.text_placeholder(tpparam)


@register.tag(name='blahblock')
def blahblock_tag(parser, token):
    """Handles blahblock template tag.

Syntax :
    {% blahblock [entity [length]] %}
        sample
    {% endblahblock %}

Parameters :
    sample  - sample text to analyze, provides base values for the random properties of the text
    entity  - one of "word", "sentence", "paragraph", "text"
    length  - integer indicating how many sub-entities should the generated entity contain

Example :
    {% blahblock "sentence" 10 %}{{ document.title }}{% endblahblock %}  - One sentence of 10 words; using template variable for sample.
    {% blahblock "word" %}Hello World{% endblahblock %} - One word; letter count chosen randomly based on analyzed sample; using fixed sample.
    {% blahblock %}{% endblahblock %}  - One text of 5 paragraphs; using default sample.

"""

    param = token.split_contents()
    tag = param.pop(0)

    if len(param) > 2:
        raise template.TemplateSyntaxError("%r tag requires 0, 1 or 2 arguments" % tag)

    nodelist = parser.parse(('end' + tag,))
    parser.delete_first_token()

    return BlahBlockNode(param, nodelist)



class BlahBlockNode(template.Node):
    """Helper class to generate a Node for blahblah template tag.
"""

    def __init__(self, param, nodelist):

        self.param = param
        self.nodelist = nodelist

        for i, one in enumerate(self.param):
            if one[0] == one[-1] and one[0] in ('"', "'"):
                self.param[i] = one[1:-1]
            elif not one.isdigit():
                self.param[i] = template.Variable(one)


    def render(self, context):

        for i, one in enumerate(self.param):
            if isinstance(one, template.Variable):
                try:
                    self.param[i] = one.resolve(context)
                except template.VariableDoesNotExist:
                    pass # will handle in text_placeholder

        tpparam = {'sample': self.nodelist.render(context)}
        if self.param:
            tpparam.update(zip(('entity', 'length'), self.param))

        return text_placeholder.text_placeholder(tpparam)
