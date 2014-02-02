from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from PIL import ImageColor

from forms import *

import image_placeholder
import text_placeholder


def image(request, **param):
    """Sends back a placeholder image.

Responds to a /sketch/iph/ or /sketch/iph.png request.

"""

    if not param:
        param = dict(request.GET.items())

    response = HttpResponse(content_type='image/png')
    image_placeholder.image_placeholder(param).save(response, 'png')
    response['Content-Length'] = len(response.content)

    return response


def text(request, **param):
    """Sends back a placeholder text.

Responds to a /sketch/blah/ or /sketch/blah.txt request.

"""

    if not param:
        param = dict(request.GET.items())

    response = HttpResponse(content_type='text/plain')
    response.write(text_placeholder.text_placeholder(param))

    return response


def demo(request, dtype):

    formclass = {'image': ImageDemoForm, 'text': TextDemoForm}[dtype]

    form = formclass(request.POST) if request.method == 'POST' else formclass()

    data = sorted(ImageColor.colormap.keys()) if dtype == 'image' else None

    return render_to_response('demo.djt', {
        'form': form,
        'type': dtype,
        'data': data,
    }, context_instance=RequestContext(request))
