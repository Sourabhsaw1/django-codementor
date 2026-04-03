from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from submissions import views as sub_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sub_views.home, name='home'),
    path('dashboard/', sub_views.dashboard, name='dashboard'),
    path('users/', include('users.urls')),
    path('submissions/', include('submissions.urls')),
    path('leaderboard/', include('leaderboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
