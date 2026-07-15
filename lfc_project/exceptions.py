from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        return response

    data = {
        "status": False,
        "message": "",
        "errors": None,
    }

    if response.status_code == status.HTTP_400_BAD_REQUEST:

        if "detail" in response.data:
            data["message"] = response.data["detail"]
        else:
            data["message"] = "Validation failed."
            data["errors"] = response.data

    elif response.status_code == status.HTTP_401_UNAUTHORIZED:
        data["message"] = "Authentication credentials were not provided."

    elif response.status_code == status.HTTP_403_FORBIDDEN:
        data["message"] = "Permission denied."

    elif response.status_code == status.HTTP_404_NOT_FOUND:
        data["message"] = "Resource not found."

    elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        data["message"] = "Too many requests."

    else:
        data["message"] = response.data.get(
            "detail",
            "An unexpected error occurred."
        )

    response.data = data

    return response

