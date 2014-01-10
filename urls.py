from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'adme.views.home', name='home'),
    # url(r'^adme/', include('adme.foo.urls')),

    

    url(r'^test-module','adme_app.views.test_module'),
    url(r'^contract-create/','adme_app.views.contract_create'),
    url(r'^contract_create_action','adme_app.views.contract_create_action'),
    url(r'^activate/(.*)/','adme_app.views.link_activate'),
    url(r'^link_activate_action/','adme_app.views.link_activate_action'),
    url(r'^link/(.*)-(.*)','adme_app.views.view_link'),
    url(r'^business_signup_action/','adme_app.views.business_signup_action'),
    url(r'^business/contracts/','adme_app.views.business_contracts'),
    url(r'^contract/(.*)/clicks/','adme_app.views.contract_clicks'),
    url(r'^contract/(.*)/links/','adme_app.views.contract_links'),
    url(r'^home/','adme_app.views.home'),

    url(r'^t/(.*)/edit','adme_app.views.edit_target'),
    url(r'^t/(.*)/','adme_app.views.show_target'),
    url(r'^target/create','adme_app.views.create_target'),
    url(r'^t/new','adme_app.views.target_create_form'),
    url(r'^new-target','adme_app.views.new_target'),
    url(r'^create_target_json','adme_app.views.create_target_json'),

    url(r'^user/stats','adme_app.views.user_stats'),
    url(r'^user/(.*)/confirm','adme_app.views.auth_user_confirm'),

    url(r'^sign-up','adme_app.views.auth_sign_up'),
    url(r'^log-in','adme_app.views.auth_log_in'),
    url(r'^log-out','adme_app.views.auth_log_out'),
    
    url(r'^hello-world/(.*)','adme_app.views.hello_world'),
    
    url(r'^$','adme_app.views.index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # cant get this to work 
    url(r'^admin/', include(admin.site.urls)),
)
