
def get_ip(request):
    ip = request.META.get('REMOTE_ADDR', '')[:255]
    ip_forward = request.META.get('X-FORWARDED-FOR', '')[:255]
    return ip_forward if ip_forward else ip
        

    