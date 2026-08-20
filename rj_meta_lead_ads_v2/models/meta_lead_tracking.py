# -*- coding: utf-8 -*-
from odoo import fields, models


class MetaLeadAdsLead(models.Model):
    _name = 'meta.lead.ads.lead'
    _description = 'Meta Lead Ads - Imported Lead Tracking'
    _order = 'create_date desc'

    name = fields.Char(compute='_compute_name', store=True)
    meta_id = fields.Char(string='Meta Lead ID', required=True, index=True, copy=False)
    form_id = fields.Many2one('meta.lead.ads.form', string='Lead Form', ondelete='cascade', index=True)
    config_id = fields.Many2one(related='form_id.config_id', store=True, index=True)
    crm_lead_id = fields.Many2one('crm.lead', string='CRM Lead', ondelete='set null')
    company_id = fields.Many2one(related='form_id.company_id', store=True)
    raw_data = fields.Text(string='Raw Meta Data')

    _sql_constraints = [
        ('meta_id_uniq', 'unique(meta_id)', 'This Meta lead has already been imported.'),
    ]

    def _compute_name(self):
        for rec in self:
            rec.name = (rec.crm_lead_id.name if rec.crm_lead_id else False) or rec.meta_id
