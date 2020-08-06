from unicodedata import name
from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/new/", views.new_page, name="new_page"),
    path("wiki/random/", views.random_page, name="random_page"),
    path("wiki/edit/<str:title>", views.edit_page, name="edit_page"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
]
