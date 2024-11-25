def dealership_info(request):
    """Proporciona información general del concesionario."""
    return {
        'dealership_name': 'Saez&Saez Car Dealership',
        'opening_hours': 'Mon-Fri 9am-6pm',
        'contact_email': 'contact@concesionario.com',
        'contact_phone': '+54-0358-462-5361',
    }