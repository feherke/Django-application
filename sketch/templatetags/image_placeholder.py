from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.conf import settings

import os
import re
import hashlib

from .. import image_placeholder

register = template.Library()


@register.filter(name='imgplace', is_safe=True)
@stringfilter
def imgplace_filter(value, param=None):
    """Handles imgplace template filter.

Syntax :
    {{ tag | imgplace[:"attribute=value [...]"] }}

Parameters :
    tag  - Text containing HTML img tag definition.
    attribute=value  - Parameters to override the attributes of the img tag.

Example :
    {{ document.logo | imgplace }}  - img tag from template variable.
    {{ '<img src="whatever.png" width=320 height=200 front=red>' | imgplace }}  - Fixed img tag string.
    {{ document.logo | imgplace:'front=red back=yellow' }}  - img tag from template variable; override some attributes.

"""

    tpparam = [(one[0], one[2] + one[3]) for one in re.findall('\\b(\\w+)=(?:([\'"])?(.+?)\\2|(\w+))', value)]

    if param:
        tpparam = dict(tpparam)
        tpparam.update([(one[0], one[2] + one[3]) for one in re.findall('\\b(\\w+)=(?:([\'"])?(.+?)\\2|(\w+))', param)])
        tpparam = tpparam.items()

    return ImagePlaceholderNode(tpparam).render(None)


@register.tag(name='imgplace')
def imgplace_tag(value, token):
    """Handles imgplace template tag.

Syntax :
    {% imgplace [width=number] [height=number] [front=color] [back=color] [text=message] %}

Parameters :
    width  - Width of the image.
    height  - Height of the image.
    front  - Color of the displayed text.
    back  - Background color of the image.
    text  - Text to display.

Example :
    {% imgplace width=320 height=200 %}  - Image of size 320x200; with default colors and default text.
    {% imgplace width=320 height=200 front=red text=something %}  - Image of size 320x200; with red text; displaying "something".

"""

    param = token.split_contents()[1:]

    param = [one[1:-1] if one[0] == one[-1] and one[0] in ('"', "'") else one for one in param]

    param = [one.split('=', 1) for one in param]

    param = [(key, val[1:-1]) if val[0] == val[-1] and val[0] in ('"', "'") else (key, val) for key, val in param]

    return ImagePlaceholderNode(param)



class ImagePlaceholderNode(template.Node):
    """Helper class to generate a Node for the iph template tag.
"""

    def __init__(self, param):
        self.param = param


    def render(self, context):
        equiv = [('width', 'width'), ('height', 'height'), ('front', None), ('back', None), ('text', 'alt')]
        imageequiv = dict([(val or key, key) for key, val in equiv])
        htmlequiv = dict([(key, val) for key, val in equiv])

        imageparam = [(imageequiv[key], val) if key in imageequiv else (key, val) for key, val in self.param if key in imageequiv or key in imageequiv.values()]
        htmlparam = [(htmlequiv[key], val) if key in htmlequiv else (key, val) for key, val in self.param if key not in htmlequiv or htmlequiv[key]]

        imageparamdict = dict(imageparam)

        md5 = hashlib.md5()
        md5.update(' '.join(sorted(imageparamdict.values())))
        filename = md5.hexdigest() + '.png'
        filepath = os.path.join(settings.STATIC_ROOT, filename)
        fileurl = os.path.join(settings.STATIC_URL, filename)

        found = False
        for idx, one in enumerate(htmlparam):
           if one[0] == 'src':
                found = True
                htmlparam[idx] = ('src', fileurl)
                break

        if not found:
            htmlparam.insert(0, ('src', fileurl))

        if not os.path.isfile(filepath):
            image_placeholder.image_placeholder(imageparamdict).save(filepath)

        tag = '<img ' + ' '.join(['%s="%s"' % (escape(key), escape(val)) for key, val in htmlparam]) + '>'

        print tag

        return tag
