# -*- coding: utf-8 -*-
import json
import logging
import time
from datetime import datetime

import requests

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)
GRAPH_VERSION = 'v21.0'


class MetaConfig(models.Model):
    _name = 'meta.lead.ads.config'
    _description = 'Meta Lead Ads Configuration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name, id'

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company, index=True)
    active = fields.Boolean(default=True)
    enabled = fields.Boolean(string='Enabled', default=True, tracking=True)

    # Meta credentials (module-owned)
    access_token = fields.Char(string='Access Token', copy=False)
    app_id = fields.Char(string='App ID')
    ad_account_id = fields.Char(string='Ad Account ID', help='act_XXXXXXXX')
    pixel_id = fields.Char(string='Pixel / Dataset ID')
    page_id = fields.Char(string='Page ID')
    catalog_id = fields.Char(string='Catalog ID')
    waba_id = fields.Char(string='WhatsApp Business Account ID')
    graph_version = fields.Char(string='Graph API Version', default=GRAPH_VERSION)
    test_event_code = fields.Char(string='Test Event Code')
    api_base_url = fields.Char(string='API Base', default='https://graph.facebook.com')

    last_connection_state = fields.Selection([
        ('unknown', 'Not Tested'),
        ('success', 'Connected'),
        ('failed', 'Failed'),
    ], default='unknown', readonly=True)
    last_connection_date = fields.Datetime(readonly=True)
    log_count = fields.Integer(compute='_compute_counts')
    success_count = fields.Integer(compute='_compute_counts')
    error_count = fields.Integer(compute='_compute_counts')
    record_count = fields.Integer(compute='_compute_counts')

    def _compute_counts(self):
        Log = self.env['meta.lead.ads.api.log']
        Biz = self.env['meta.lead.ads.form']
        for rec in self:
            domain = [('config_id', '=', rec.id)]
            rec.log_count = Log.search_count(domain)
            rec.success_count = Log.search_count(domain + [('state', '=', 'success')])
            rec.error_count = Log.search_count(domain + [('state', '=', 'error')])
            rec.record_count = Biz.search_count([('config_id', '=', rec.id)])

    def _graph_url(self, path):
        self.ensure_one()
        ver = (self.graph_version or GRAPH_VERSION).strip()
        if not ver.startswith('v'):
            ver = f'v{ver}'
        base = (self.api_base_url or 'https://graph.facebook.com').rstrip('/')
        return f'{base}/{ver}/{path.lstrip("/")}'

    def _api_request(self, method, path, params=None, json_body=None, timeout=30):
        """Call Meta Graph API and write a log line. Returns (success, response_dict|None, log)."""
        self.ensure_one()
        if not self.access_token and not self._meta_no_api_required():
            raise UserError(_('Please configure the Access Token on %s.') % self.display_name)
        params = dict(params or {})
        if self.access_token:
            params.setdefault('access_token', self.access_token)
        url = self._graph_url(path)
        started = time.time()
        state = 'error'
        status_code = 0
        resp_text = ''
        data = None
        error = False
        try:
            response = requests.request(
                method.upper(), url, params=params, json=json_body, timeout=timeout
            )
            status_code = response.status_code
            resp_text = (response.text or '')[:4000]
            if status_code in (200, 201):
                state = 'success'
                try:
                    data = response.json()
                except Exception:
                    data = {'raw': resp_text}
            else:
                error = resp_text[:500]
        except requests.RequestException as exc:
            error = str(exc)
            resp_text = error
            _logger.exception('Meta API error %s %s', method, path)

        duration = int((time.time() - started) * 1000)
        log = self.env['meta.lead.ads.api.log'].sudo().create({
            'name': f'{method.upper()} {path}',
            'config_id': self.id,
            'company_id': self.company_id.id,
            'method': method.upper(),
            'endpoint': path,
            'url': url.split('?')[0],
            'request_payload': json.dumps(json_body or params, default=str)[:4000],
            'response_payload': resp_text,
            'status_code': status_code,
            'state': state,
            'duration_ms': duration,
            'error_message': error or False,
            'user_id': self.env.user.id,
        })
        return state == 'success', data, log


    def _meta_no_api_required(self):
        """Return True if this module works without Meta Graph credentials."""
        return False

    def action_test_connection(self):
        self.ensure_one()
        if self._meta_no_api_required():
            self.write({
                'last_connection_state': 'success',
                'last_connection_date': fields.Datetime.now(),
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('OK'),
                    'message': _('This module works without Meta API credentials.'),
                    'type': 'success',
                },
            }
        ok, data, _log = self._api_request('GET', 'me', params={'fields': 'id,name'})
        self.write({
            'last_connection_state': 'success' if ok else 'failed',
            'last_connection_date': fields.Datetime.now(),
        })
        if ok:
            self.message_post(body=_('Connection successful: %s') % (data or {}))
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Connection successful') if ok else _('Connection failed'),
                'message': _('Meta API test completed.'),
                'type': 'success' if ok else 'danger',
            },
        }


    def action_open_logs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('API Logs'),
            'res_model': 'meta.lead.ads.api.log',
            'view_mode': 'list,graph,pivot,form',
            'domain': [('config_id', '=', self.id)],
            'context': {'default_config_id': self.id},
        }

    def action_open_records(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Lead Ads Forms'),
            'res_model': 'meta.lead.ads.form',
            'view_mode': 'list,form',
            'domain': [('config_id', '=', self.id)],
            'context': {'default_config_id': self.id},
        }

    def action_sync_import(self):
        """Discover Lead Ads forms on the configured Page, then fetch real
        lead submissions for each form and create CRM leads."""
        self.ensure_one()
        if self._meta_no_api_required():
            raise UserError(_('Import via Meta API is not required for this module.'))
        if not self.page_id:
            raise UserError(_('Set the Page ID before importing lead forms.'))

        ok, data, log = self._api_request(
            'GET', f'{self.page_id}/leadgen_forms', params={'fields': 'id,name,status'}
        )
        if not ok:
            raise UserError(_('Could not fetch lead forms from Meta. Check API logs.'))

        Form = self.env['meta.lead.ads.form']
        forms_to_sync = Form
        for f in (data or {}).get('data', []):
            form_meta_id = f.get('id')
            if not form_meta_id:
                continue
            existing = Form.search([('form_id', '=', form_meta_id), ('config_id', '=', self.id)], limit=1)
            if existing:
                existing.write({'name': f.get('name') or existing.name})
                forms_to_sync |= existing
            else:
                forms_to_sync |= Form.create({
                    'name': f.get('name') or form_meta_id,
                    'config_id': self.id,
                    'company_id': self.company_id.id,
                    'form_id': form_meta_id,
                    'page_id': self.page_id,
                    'sync_state': 'pending',
                })

        if forms_to_sync:
            forms_to_sync.action_fetch_leads()

        self.message_post(body=_('Import completed: %s form(s) processed.') % len(forms_to_sync))
        return self.action_open_records()

    @api.model
    def _cron_sync_all_leads(self):
        """Called periodically by ir.cron to pull new leads for every enabled config."""
        configs = self.search([('enabled', '=', True)])
        for config in configs:
            try:
                config.action_sync_import()
            except Exception:
                _logger.exception('Meta Lead Ads: scheduled sync failed for config %s', config.id)

    def action_open_import_wizard(self):
        self.ensure_one()
        # wizard model is sibling of config model: *.import.wizard
        wiz_model = self._name.rsplit('.', 1)[0] + '.import.wizard' if self._name.endswith('.config') else self._name + '.import.wizard'
        # fix: config is meta.X.config -> import is meta.X.import.wizard
        parts = self._name.split('.')
        if parts[-1] == 'config':
            wiz_model = '.'.join(parts[:-1] + ['import', 'wizard'])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import',
            'res_model': wiz_model,
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_config_id': self.id},
        }

    def action_open_export_wizard(self):
        self.ensure_one()
        parts = self._name.split('.')
        if parts[-1] == 'config':
            wiz_model = '.'.join(parts[:-1] + ['export', 'wizard'])
        else:
            wiz_model = self._name + '.export.wizard'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Export',
            'res_model': wiz_model,
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_config_id': self.id},
        }

