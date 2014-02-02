from PIL import Image, ImageColor, ImageDraw, ImageFont


def image_placeholder(param):
    fontfile = '/usr/share/fonts/X11/TTF/arialbd.ttf'
    minsize = 5
    maxsize = 500

    try:
        param['width'] = int(param['width'])
    except:
        param['width'] = 640

    try:
        param['height'] = int(param['height'])
    except:
        param['height'] = 480

    try:
        ImageColor.getrgb(param['front'])
    except:
        param['front'] = '#666'

    try:
        ImageColor.getrgb(param['back'])
    except:
        param['back'] = '#999'

    if not param.get('text'):
        param['text'] = '%(width)s x %(height)s'

    try:
        param['text'] = param['text'] % param
    except:
        param['text'] = 'placeholder'

    img = Image.new('RGB', (param['width'], param['height']))
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, 0), (param['width'], param['height'])), fill=param['back'])

    size = (maxsize + minsize) / 2
    while size != minsize and size != maxsize:
        font = ImageFont.truetype(fontfile, size)
        textsize = draw.textsize(param['text'], font=font)

        if (textsize[0] == param['width'] and textsize[1] <= param['height']) \
        or (textsize[0] <= param['width'] and textsize[1] == param['height']):
            break

        if textsize[0] > param['width'] or textsize[1] > param['height']:
            maxsize = size
        else:
            minsize = size

        size = (maxsize + minsize) / 2

    if size:
        font = ImageFont.truetype(fontfile, size)
        textsize = draw.textsize(param['text'], font=font)

        draw.text((param['width'] / 2 - textsize[0] / 2, param['height'] / 2 - textsize[1] / 2), param['text'], fill=param['front'], font=font)

    return img
