from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from banking import views

urlpatterns = [   
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='Banking API', description='RESTful API for Banking Project')),
    url(r'^$', views.api_root),
    url(r'', include(('restservice.urls', 'restservice'), namespace='restservice')),
]
