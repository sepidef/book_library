from datetime import timezone
from books.models import Books
from django.db import models
from users.models import CustomUser
import datetime


class Reservation(models.Model):
    check_in = models.DateField(default=datetime.datetime.now())
    check_out = models.DateField()
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'


class BookSchedule(models.Model):
    reservation_date = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    book_name = models.ForeignKey(Books, on_delete=models.CASCADE)
