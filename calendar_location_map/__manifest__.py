{
    'name': 'Calendar Location Map',
    'summary': 'Department-wise attendee auto-assign + clickable location links for Calendar Events',
    'description': """
        Calendar Custom Suite
        ======================
        Combines two calendar customizations into a single module:

        1. Department Attendees
           Adds a Department field to Calendar Events (Meetings). Selecting
           one or more departments automatically adds all employees of
           those departments (who have a related user/partner) as
           attendees - and removes them again if the department is
           deselected.

        2. Clickable Location Link
           The standard Calendar popover shows the "Location" field as
           plain text, even if it contains a URL (e.g. a Google Maps link).
           This module makes any URL in the Location field clickable in
           the meeting popover, opening in a new tab. It also understands
           Markdown-style links, e.g.
           [https://maps.google.com/?q=MG+Road+Kochi](https://maps.google.com/?q=MG+Road+Kochi)
           and, for plain text locations, generates a Google Maps search
           link automatically.
    """,
    'version': '18.0.1.0.0',
    'category': 'Productivity/Calendar',
    'author': 'Vishnu Priya C',
    'license': 'LGPL-3',
    'depends': ['calendar', 'hr'],
    'data': [
        'views/calendar_event_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'calendar_location_map/static/src/js/calendar_location_link.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
