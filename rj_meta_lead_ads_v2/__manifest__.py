# -*- coding: utf-8 -*-
{
    'name': 'Meta Lead Ads',
    'version': '18.0.1.0.0',
    'author': 'Recent Technologies',
    'website': 'mailto:rajodoodevelop@gmail.com',
    'support': 'rajodoodevelop@gmail.com',
    'category': 'Sales/CRM',
    'summary': 'Import Facebook and Instagram Lead Ads into Odoo CRM',
    'depends': ['rj_meta_common_v2', 'crm', 'mail'],
    'data': ['security/meta_lead_ads_security.xml', 'security/ir.model.access.csv', 'data/ir_cron_data.xml', 'views/meta_lead_ads_views.xml'],
    'images': ['static/description/banner.gif'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
    'description': '',
}
