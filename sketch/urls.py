from django.conf.urls import patterns, url
from django.conf import settings


urlpatterns = patterns('your_django_project.sketch.views',

    url(r'^iph\.png\b', 'image', name='iph'),
    url(r'^iph(?:/(?P<width>\d+))?(?:/(?P<height>\d+))?(?:/(?P<front>\w+))?(?:/(?P<back>\w+))?(?:/(?P<text>.+))?', 'image'),

    url(r'^blah\.txt\b', 'text', name='blah'),
    url(r'^blah(?:/(?P<entity>word|sentence|paragraph|text))?(?:/?(?P<length>\d+))?', 'text'),

# demo
    url(r'^(?P<dtype>image|text)-demo/', 'demo'),

) + patterns('',

    url(r'^$', 'django.views.static.serve', {'path': 'sketch.html', 'document_root': settings.STATIC_ROOT}),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

)
