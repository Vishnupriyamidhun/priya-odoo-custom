# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MetaApiLog(models.Model):
    _name = 'meta.lead.ads.api.log'
    _description = 'Meta Lead Ads API Log'
    _order = 'create_date desc, id desc'

    name = fields.Char(required=True)
    config_id = fields.Many2one('meta.lead.ads.config', required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one('res.company', required=True, index=True)
    method = fields.Char()
    endpoint = fields.Char(index=True)
    url = fields.Char()
    request_payload = fields.Text()
    response_payload = fields.Text()
    status_code = fields.Integer()
    state = fields.Selection([
        ('success', 'Success'),
        ('error', 'Error'),
        ('pending', 'Pending'),
    ], default='pending', index=True, required=True)
    duration_ms = fields.Integer(string='Duration (ms)')
    error_message = fields.Text()
    user_id = fields.Many2one('res.users')
    res_model = fields.Char()
    res_id = fields.Integer()

    def action_retry(self):
        for rec in self:
            if not rec.config_id:
                continue
            ok, _data, _log = rec.config_id._api_request(rec.method or 'GET', rec.endpoint or 'me')
            pass
        return True

    @api.model
    def _cron_cleanup(self, days=90):
        from datetime import timedelta
        limit = fields.Datetime.now() - timedelta(days=days)
        old = self.search([('create_date', '<', limit)])
        count = len(old)
        old.unlink()
        return count
