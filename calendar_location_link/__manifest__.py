{
    'name': 'Calendar Location Clickable Link',
    'version': '18.0.1.0.0',
    'summary': 'Makes URLs in the Calendar event Location field clickable in the meeting popover',
    'description': """
Calendar Location Clickable Link
=================================
The standard Odoo Calendar popover shows the "Location" field as plain
text, even if you put a URL (e.g. a Google Maps link) in it.

This module watches the calendar popover in the browser and automatically
converts any URL found in the Location text into a clickable hyperlink
that opens in a new tab.

It also understands markdown-style links typed as:
    [https://maps.google.com/?q=MG+Road+Kochi](https://maps.google.com/?q=MG+Road+Kochi)
and renders them as a single clean clickable link instead of showing the
brackets and the URL twice.

This is implemented purely on the frontend (JS) by watching for the
popover element in the DOM, so it does NOT depend on Odoo's internal
popover template structure and is unlikely to break across minor
version updates.
""",
    'category': 'Calendar',
    'author': 'Custom',
    'depends': ['calendar'],
    'assets': {
        'web.assets_backend': [
            'calendar_location_link/static/src/js/calendar_location_link.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
