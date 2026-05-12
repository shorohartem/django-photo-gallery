from django.urls import path

from . import views

urlpatterns = [
    path('', views.new_page, name='new_page'),
    path("reception", views.reception, name="reception"),
    path('append', views.append, name="append"),
    path('delete/', views.delete, name="delete"),
    path('all/', views.all_photo, name='all_photo')
]
