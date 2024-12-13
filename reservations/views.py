from datetime import datetime
from rest_framework import status
from .models import Books
from .models import Reservation
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class BookReservation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if pk:
            invalid_dates = False
            book = Books.objects.get(pk=pk)
            user_id = request.user
            check_in = request.data.get('check_in')
            check_out = request.data.get('check_out')
            if not check_in or not check_out:
                return Response(
                    {"error": "Both check_in and check_out are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
                check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Please use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            case_1 = Reservation.objects.filter(book=book, check_in__lte=check_in, check_out__gte=check_in).exists()

            case_2 = Reservation.objects.filter(book=book, check_in__lte=check_out, check_out__gte=check_out).exists()

            case_3 = Reservation.objects.filter(book=book, check_in__gte=check_in, check_out__lte=check_out).exists()

            if case_1 or case_2 or case_3:
                return Response(
                    {"error": "This book is not available on your selected dates."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            reservations = Reservation(
                check_in=check_in,
                check_out=check_out,
                user=user_id,
                book=book
            )

            reservations.save()

            reservation_data = {
                "id": reservations.id,
                "check_in": reservations.check_in,
                "check_out": reservations.check_out,
                "user_id": reservations.user.id,
                "book_id": reservations.book.id
            }

            return Response(
                {"message": "Reservation created successfully.", "reservation": reservation_data},
                status=status.HTTP_201_CREATED
            )
