from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'adme.views.home', name='home'),
    # url(r'^adme/', include('adme.foo.urls')),

    url(r'^sign-up','adme.adme_app.views.auth_sign_up'),
    url(r'^log-in','adme.adme_app.views.auth_log_in'),
    url(r'^log-out','adme.adme_app.views.auth_log_out'),
    
    url(r'^hello-world/(.*)','adme_app.views.hello_world'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
