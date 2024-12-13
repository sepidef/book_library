from django.urls import path
from .views import AddBook, ModifyBook

urlpatterns = [
    path("create/book/", AddBook.as_view()),
    path("modify/book/<int:pk>", ModifyBook.as_view())
]
