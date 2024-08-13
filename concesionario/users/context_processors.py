# users/context_processors.py

def user_status(request):
    """Proporciona información sobre el estado del usuario."""
    if request.user.is_authenticated:
        return {
            'is_authenticated': True,
            'is_staff': request.user.is_staff,
            'user_name': request.user.username,
        }
    else:
        return {
            'is_authenticated': False,
        }
