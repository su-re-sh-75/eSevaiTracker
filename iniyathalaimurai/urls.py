from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "iniyathalaimurai"
urlpatterns = [
    # customer
    path('dashboard/', views.user_dashboard, name="user_dashboard"),
    path('applications/', views.user_applications, name="user_applications"),
    path('payments/', views.user_payments, name="user_payments"),
    path('applications/new/', views.new_application, name='new_application'),

    # staff
    path('staff/dashboard/', views.staff_dashboard, name="staff_dashboard"),
    path('customers/new/', views.new_customer, name='new_customer'),
    path('customers/manage/', views.manage_customers, name='manage_customers'),
    path('customers/manage/edit/<int:user_id>/', views.edit_customer, name='edit_customer'),
    path('customers/manage/delete/<int:user_id>/', views.delete_customer, name='delete_customer'),
    path('customers/manage/activate/<int:user_id>/', views.activate_customer, name='activate_customer'),
    path('customers/manage/deactivate/<int:user_id>/', views.deactivate_customer, name='deactivate_customer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)