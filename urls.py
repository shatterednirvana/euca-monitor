from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^addkeypair$', 'monitor.euca.views.addkeypair'),
    (r'^addkeypairpost$', 'monitor.euca.views.addkeypairpost'),
    (r'^$', 'monitor.euca.views.viewrunning'),
    (r'^viewpost$', 'monitor.euca.views.viewrunningpost'),
    (r'^run$', 'monitor.euca.views.runinstance'),
    (r'^runpost$', 'monitor.euca.views.runinstancepost'),
    (r'^terminate$', 'monitor.euca.views.terminstance'),
    (r'^terminatepost$', 'monitor.euca.views.terminstancepost'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),

    # Example:
    # (r'^monitor/', include('monitor.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
