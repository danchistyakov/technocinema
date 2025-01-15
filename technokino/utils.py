from django.http import JsonResponse

def api_error(message, status=500):
    return JsonResponse({'status': 'error', 'message': message}, status=status)
