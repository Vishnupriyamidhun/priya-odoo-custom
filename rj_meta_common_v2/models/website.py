# -*- coding: utf-8 -*-
import json

from odoo import api, fields, models, _


class Website(models.Model):
    _inherit = 'website'

    # --- Side panel / embed ---
    meta_panel_enabled = fields.Boolean(
        string='Enable Meta Side Panel',
        default=False,
        help='Show the Meta control panel on every website page (floating button + drawer).',
    )
    meta_panel_position = fields.Selection(
        [
            ('right', 'Right'),
            ('left', 'Left'),
        ],
        string='Panel Position',
        default='right',
    )
    meta_panel_label = fields.Char(
        string='Button Label',
        default='Meta',
        help='Short label on the floating button.',
    )
    meta_panel_open_mode = fields.Selection(
        [
            ('drawer', 'Side drawer (recommended)'),
            ('embed', 'Try embed iframe'),
            ('new_tab', 'Open links in new tab only'),
        ],
        string='Open Mode',
        default='drawer',
        help='Meta may block iframes; drawer with quick links always works.',
    )
    meta_panel_default_screen = fields.Selection(
        [
            ('business', 'Business Suite'),
            ('ads', 'Ads Manager'),
            ('events', 'Events Manager'),
            ('commerce', 'Commerce Manager'),
            ('whatsapp', 'WhatsApp Manager'),
            ('custom', 'Custom URL'),
        ],
        string='Default Screen',
        default='business',
    )

    # Meta console URLs (overridable per website)
    meta_url_business_suite = fields.Char(
        string='Business Suite URL',
        default='https://business.facebook.com/',
    )
    meta_url_ads_manager = fields.Char(
        string='Ads Manager URL',
        default='https://www.facebook.com/adsmanager/manage/campaigns',
    )
    meta_url_events_manager = fields.Char(
        string='Events Manager URL',
        default='https://www.facebook.com/events_manager2/list',
    )
    meta_url_commerce = fields.Char(
        string='Commerce Manager URL',
        default='https://business.facebook.com/commerce',
    )
    meta_url_whatsapp = fields.Char(
        string='WhatsApp Manager URL',
        default='https://business.facebook.com/wa/manage/',
    )
    meta_url_custom = fields.Char(
        string='Custom Meta URL',
        help='Optional custom console URL used when Default Screen is Custom.',
    )
    meta_panel_show_on_mobile = fields.Boolean(
        string='Show on Mobile',
        default=True,
    )
    meta_panel_require_editor = fields.Boolean(
        string='Only for Website Editors',
        default=False,
        help='If enabled, only users who can edit the website see the panel.',
    )

    def _meta_panel_urls(self):
        self.ensure_one()
        return {
            'business': self.meta_url_business_suite or 'https://business.facebook.com/',
            'ads': self.meta_url_ads_manager or 'https://www.facebook.com/adsmanager/manage/campaigns',
            'events': self.meta_url_events_manager or 'https://www.facebook.com/events_manager2/list',
            'commerce': self.meta_url_commerce or 'https://business.facebook.com/commerce',
            'whatsapp': self.meta_url_whatsapp or 'https://business.facebook.com/wa/manage/',
            'custom': self.meta_url_custom or self.meta_url_business_suite or 'https://business.facebook.com/',
        }

    def get_meta_panel_frontend_config(self):
        """JSON-serializable config for the Meta side panel (SSR + OWL)."""
        self.ensure_one()
        if not self.meta_panel_enabled:
            return {'enabled': False}
        # Editor-only visibility (leave OFF so public visitors also see the button)
        if self.meta_panel_require_editor:
            user = self.env.user
            if user._is_public() or not user.has_group('website.group_website_restricted_editor'):
                return {'enabled': False}
        urls = self._meta_panel_urls()
        default_key = self.meta_panel_default_screen or 'business'
        return {
            'enabled': True,
            'position': self.meta_panel_position or 'right',
            'label': self.meta_panel_label or 'Meta',
            'openMode': self.meta_panel_open_mode or 'drawer',
            'showOnMobile': bool(self.meta_panel_show_on_mobile),
            'defaultScreen': default_key,
            'defaultUrl': urls.get(default_key) or urls['business'],
            'screens': [
                {'key': 'business', 'title': _('Business Suite'), 'url': urls['business'], 'icon': 'fa-briefcase'},
                {'key': 'ads', 'title': _('Ads Manager'), 'url': urls['ads'], 'icon': 'fa-bullhorn'},
                {'key': 'events', 'title': _('Events Manager'), 'url': urls['events'], 'icon': 'fa-line-chart'},
                {'key': 'commerce', 'title': _('Commerce'), 'url': urls['commerce'], 'icon': 'fa-shopping-bag'},
                {'key': 'whatsapp', 'title': _('WhatsApp'), 'url': urls['whatsapp'], 'icon': 'fa-whatsapp'},
            ] + (
                [{'key': 'custom', 'title': _('Custom'), 'url': urls['custom'], 'icon': 'fa-link'}]
                if self.meta_url_custom else []
            ),
            'websiteId': self.id,
            'websiteName': self.name,
        }

    def get_meta_panel_frontend_config_json(self):
        self.ensure_one()
        return json.dumps(self.get_meta_panel_frontend_config())

    @api.model
    def get_backend_meta_panel_config(self):
        """Fetch config for the backend OWL component. Uses default company's website or first found."""
        website = self.env['website'].search([('company_id', '=', self.env.company.id)], limit=1)
        if not website:
            website = self.env['website'].search([], limit=1)
        
        if website:
            return website.get_meta_panel_frontend_config()
        return {'enabled': False}
