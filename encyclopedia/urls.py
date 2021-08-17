from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:name>", views.entries, name="entries"),
    path("add", views.add, name="add"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("save/<str:title>", views.save, name="save"),
    path("random", views.random, name="random")
]
