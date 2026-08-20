# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    meta_panel_enabled = fields.Boolean(related='website_id.meta_panel_enabled', readonly=False)
    meta_panel_position = fields.Selection(related='website_id.meta_panel_position', readonly=False)
    meta_panel_label = fields.Char(related='website_id.meta_panel_label', readonly=False)
    meta_panel_open_mode = fields.Selection(related='website_id.meta_panel_open_mode', readonly=False)
    meta_panel_default_screen = fields.Selection(related='website_id.meta_panel_default_screen', readonly=False)
    meta_url_business_suite = fields.Char(related='website_id.meta_url_business_suite', readonly=False)
    meta_url_ads_manager = fields.Char(related='website_id.meta_url_ads_manager', readonly=False)
    meta_url_events_manager = fields.Char(related='website_id.meta_url_events_manager', readonly=False)
    meta_url_commerce = fields.Char(related='website_id.meta_url_commerce', readonly=False)
    meta_url_whatsapp = fields.Char(related='website_id.meta_url_whatsapp', readonly=False)
    meta_url_custom = fields.Char(related='website_id.meta_url_custom', readonly=False)
    meta_panel_show_on_mobile = fields.Boolean(related='website_id.meta_panel_show_on_mobile', readonly=False)
    meta_panel_require_editor = fields.Boolean(related='website_id.meta_panel_require_editor', readonly=False)

    has_meta_common_panel = fields.Boolean(
        string='Meta Website Panel',
        compute='_compute_has_meta_common_panel',
        inverse='_inverse_has_meta_common_panel',
    )

    @api.depends('meta_panel_enabled')
    def _compute_has_meta_common_panel(self):
        for rec in self:
            rec.has_meta_common_panel = bool(rec.meta_panel_enabled)

    def _inverse_has_meta_common_panel(self):
        for rec in self:
            rec.meta_panel_enabled = bool(rec.has_meta_common_panel)
