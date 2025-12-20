# Keeps database alive

from django.http import JsonResponse
from django.db import connection

def cron_ping(request):
    # Security: Check for Vercel's internal cron header (optional but recommended)
    # if request.headers.get('Authorization') != f"Bearer {os.environ.get('CRON_SECRET')}":
    #     return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        # Perform a lightweight query to wake up the DB
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            
        return JsonResponse({'status': 'success', 'message': 'Database pinged successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)