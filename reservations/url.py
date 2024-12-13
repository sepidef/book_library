from django.urls import path
from .views import BookReservation

urlpatterns = [
    path("reservation/<int:pk>", BookReservation.as_view()),
]
