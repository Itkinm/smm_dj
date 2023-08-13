
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
	path('shtab/', include('socnet.urls')),
	path('platform/', include('socnet.urls')),
	path('', include('socnet.urls')),
    path('admin/', admin.site.urls),
    url(r'^', include('django_telegrambot.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
