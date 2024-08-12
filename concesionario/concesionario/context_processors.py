def dealership_info(request):
    """Proporciona información general del concesionario."""
    return {
        'dealership_name': 'Concesionario Didier',
        'opening_hours': 'Mon-Fri 9am-6pm',
        'contact_email': 'contact@concesionario.com',
        'contact_phone': '+1-800-555-1234',
    }