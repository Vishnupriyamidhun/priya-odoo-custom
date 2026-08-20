# -*- coding: utf-8 -*-
{
    'name': 'Meta Common — Website Panel & Shared Tools',
    'version': '18.0.1.2.0',
    'author': 'Recent Technologies',
    'website': 'mailto:rajodoodevelop@gmail.com',
    'support': 'rajodoodevelop@gmail.com',
    'category': 'Website/Website',
    'summary': 'Shared Meta side panel snippet (OWL), console links, and API helpers for all Meta suite modules',
    'depends': ['website', 'web', 'mail'],
    'data': ['security/meta_common_security.xml', 'views/website_views.xml', 'views/res_config_settings_views.xml', 'views/meta_dashboard_views.xml', 'views/menus.xml', 'data/website_snippet_data.xml'],
    'assets': {'web.assets_frontend': ['rj_meta_common_v2/static/src/scss/meta_side_panel.scss', 'rj_meta_common_v2/static/src/xml/meta_side_panel.xml', 'rj_meta_common_v2/static/src/js/meta_side_panel_core.js', 'rj_meta_common_v2/static/src/js/meta_side_panel.js'], 'web.assets_backend': ['rj_meta_common_v2/static/src/scss/meta_side_panel.scss', 'rj_meta_common_v2/static/src/xml/meta_side_panel.xml', 'rj_meta_common_v2/static/src/js/meta_side_panel_core.js', 'rj_meta_common_v2/static/src/js/meta_side_panel_backend.js', 'rj_meta_common_v2/static/src/scss/meta_dashboard.scss', 'rj_meta_common_v2/static/src/xml/meta_dashboard.xml', 'rj_meta_common_v2/static/src/js/meta_dashboard.js']},
    'images': ['static/description/banner.gif', 'static/description/img/banner.png', 'static/description/img/step_snippet.png', 'static/description/img/step_side_panel.png', 'static/description/img/step_settings.png', 'static/description/img/step_dual_screen.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': '',
}
