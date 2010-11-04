from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^addkeypair$', 'euca-monitor.euca.views.addkeypair'),
    (r'^addkeypairpost$', 'euca-monitor.euca.views.addkeypairpost'),
    (r'^$', 'euca-monitor.euca.views.viewrunning'),
    (r'^viewpost$', 'euca-monitor.euca.views.viewrunningpost'),
    (r'^run$', 'euca-monitor.euca.views.runinstance'),
    (r'^runpost$', 'euca-monitor.euca.views.runinstancepost'),
    (r'^terminate$', 'euca-monitor.euca.views.terminstance'),
    (r'^terminatepost$', 'euca-monitor.euca.views.terminstancepost'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),

    # Example:
    # (r'^euca-monitor/', include('euca-monitor.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
