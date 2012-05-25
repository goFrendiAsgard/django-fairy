from django.conf.urls import patterns, include, url

# Comment the next two lines to disable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # (DON'T CHANGE THE NEXT ONE LINE !!!)  
    ##[include_app_url]## 
      
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^django_project/', include('django_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
