from django.urls import path

from . import views

app_name = 'spots'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:surfspot_id>/', views.detail, name='detail'),
]