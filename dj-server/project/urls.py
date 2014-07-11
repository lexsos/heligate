from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^api/accounts_dynamic/', include('accounts_dynamic_ip.urls')),
    url(r'^auth/', include('accounts_web.urls')),

    url(r'^tmpl/(.*)$', 'django.shortcuts.render')
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
