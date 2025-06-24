from django.urls import path
from .views import user_dashboard, staff_dashboard, user_applications, user_payments, new_application
from django.conf import settings
from django.conf.urls.static import static


app_name = "iniyathalaimurai"
urlpatterns = [
    path('dashboard/', user_dashboard, name="user_dashboard"),
    path('staff/dashboard/', staff_dashboard, name="staff_dashboard"),
    path('applications/', user_applications, name="user_applications"),
    path('payments/', user_payments, name="user_payments"),
    path('applications/new/', new_application, name='new_application'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)