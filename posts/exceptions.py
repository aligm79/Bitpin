from rest_framework import status
from rest_framework.exceptions import APIException


class PointBetween0And5(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "point should be between 0 and 5"
    default_code = "Value error"