class AlumniSearch:
    search_fields = [
        'firstName', 'middleName', 'lastName', 'email',
        'existingEmail', 'approval__gsuite', 'payment__customer'
    ]
