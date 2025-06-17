from django.urls import path
from .views import index

app_name = "iniyathalaimurai"
urlpatterns = [
    path('', index, name="home"),
]