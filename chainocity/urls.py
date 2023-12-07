from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Chainocity Admin"
admin.site.site_title = "Chainocity Admin Portal"
admin.site.index_title = "Welcome to Chainocity Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("myapp.urls")),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

