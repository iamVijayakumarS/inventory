from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

def jwt_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        print(request)
        # Print the full headers
        print(f"Request Headers: {request.headers}")
        auth = request.headers.get('Authorization', None)
        print(auth,'auth')
        if not auth:
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)
        try:
            # Extract the token from the Authorization header
            token = auth.split()[1]  # This splits 'Bearer <token>' and takes <token>
            # Validate the token
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            request.user = jwt_auth.get_user(validated_token)  # Assign the user to request
        except (IndexError, AuthenticationFailed):
            return JsonResponse({'detail': 'Invalid token.'}, status=401)

        return func(request, *args, **kwargs)

    return wrapper
