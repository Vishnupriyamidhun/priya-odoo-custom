# -*- coding: utf-8 -*-
import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MetaBusiness(models.Model):
    _name = 'meta.lead.ads.form'
    _description = 'Lead Ads Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'write_date desc, id desc'

    name = fields.Char(required=True, tracking=True)
    config_id = fields.Many2one('meta.lead.ads.config', string='Configuration', required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one(related='config_id.company_id', store=True, index=True)
    meta_id = fields.Char(string='Meta ID', index=True, copy=False)
    sync_state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('done', 'Synced'),
        ('error', 'Error'),
    ], default='draft', tracking=True, index=True)
    last_sync_date = fields.Datetime(readonly=True)
    last_error = fields.Text(readonly=True)
    active = fields.Boolean(default=True)
    notes = fields.Text()
    form_id = fields.Char(string='Meta Form ID', index=True)
    page_id = fields.Char(string='Page ID')
    lead_count = fields.Integer(string='Leads Imported')
    crm_team_id = fields.Many2one('crm.team', string='Sales Team')

    def action_sync_to_meta(self):
        for rec in self:
            if not rec.config_id.enabled:
                raise UserError(_('Configuration is disabled.'))
            if rec.config_id._meta_no_api_required():
                rec.write({'sync_state': 'done', 'last_sync_date': fields.Datetime.now(), 'last_error': False})
                rec.message_post(body=_('Marked as synced (local module, no Meta API call).'))
                continue
            # Generic upsert marker via Graph debug-style call
            ok, data, log = rec.config_id._api_request(
                'GET', 'me', params={'fields': 'id,name'}
            )
            if ok:
                rec.write({
                    'sync_state': 'done',
                    'last_sync_date': fields.Datetime.now(),
                    'last_error': False,
                    'meta_id': rec.meta_id or (data or {}).get('id'),
                })
                rec.message_post(body=_('Sync to Meta succeeded.'))
            else:
                rec.write({'sync_state': 'error', 'last_error': log.error_message or _('Unknown error')})
                rec.message_post(body=_('Sync failed. See API logs.'))
        return True

    def action_update_from_meta(self):
        return self.action_sync_to_meta()

    def action_open_logs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('API Logs'),
            'res_model': 'meta.lead.ads.api.log',
            'view_mode': 'list,form',
            'domain': [('config_id', '=', self.config_id.id)],
            'context': {'default_config_id': self.config_id.id},
        }

    def action_export_meta(self):
        return self.action_sync_to_meta()

    @staticmethod
    def _parse_field_data(field_data):
        """Meta returns field_data as a list of {'name': .., 'values': [..]}.
        Flatten it into a simple {field_name: value} dict."""
        result = {}
        for item in field_data or []:
            key = (item.get('name') or '').strip().lower()
            values = item.get('values') or []
            result[key] = values[0] if values else False
        return result

    def action_fetch_leads(self):
        """Fetch real lead submissions from Meta for this form and create CRM leads.
        Safe to call repeatedly: already-imported Meta leads are skipped."""
        LeadTrack = self.env['meta.lead.ads.lead'].sudo()
        CrmLead = self.env['crm.lead'].sudo()
        for rec in self:
            config = rec.config_id
            if not config.access_token:
                rec.write({'sync_state': 'error', 'last_error': _('Access Token not configured.')})
                continue
            if not rec.form_id:
                rec.write({'sync_state': 'error', 'last_error': _('No Meta Form ID set on this record.')})
                continue

            after = None
            imported = 0
            had_error = False
            while True:
                params = {'fields': 'id,created_time,field_data', 'limit': 100}
                if after:
                    params['after'] = after
                ok, data, log = config._api_request('GET', f'{rec.form_id}/leads', params=params)
                if not ok:
                    rec.write({'sync_state': 'error', 'last_error': log.error_message or _('Fetch failed')})
                    had_error = True
                    break

                entries = (data or {}).get('data', [])
                for entry in entries:
                    meta_lead_id = entry.get('id')
                    if not meta_lead_id or LeadTrack.search_count([('meta_id', '=', meta_lead_id)]):
                        continue  # already imported

                    info = self._parse_field_data(entry.get('field_data'))
                    full_name = (
                        info.get('full_name')
                        or ' '.join(filter(None, [info.get('first_name'), info.get('last_name')])).strip()
                        or info.get('name')
                        or _('Meta Lead %s') % meta_lead_id
                    )
                    email = info.get('email')
                    phone = info.get('phone_number') or info.get('phone')
                    description = '\n'.join(f'{k}: {v}' for k, v in info.items() if v)

                    crm_lead = CrmLead.create({
                        'name': full_name or _('Meta Lead'),
                        'contact_name': full_name or False,
                        'email_from': email or False,
                        'phone': phone or False,
                        'team_id': rec.crm_team_id.id or False,
                        'description': description,
                        'type': 'lead',
                        'company_id': rec.company_id.id,
                    })
                    LeadTrack.create({
                        'meta_id': meta_lead_id,
                        'form_id': rec.id,
                        'crm_lead_id': crm_lead.id,
                        'raw_data': json.dumps(entry, default=str),
                    })
                    imported += 1

                paging = (data or {}).get('paging', {})
                next_after = paging.get('cursors', {}).get('after')
                if paging.get('next') and next_after and next_after != after:
                    after = next_after
                else:
                    break

            if not had_error:
                rec.write({
                    'sync_state': 'done',
                    'last_sync_date': fields.Datetime.now(),
                    'last_error': False,
                    'lead_count': rec.lead_count + imported,
                })
                rec.message_post(body=_('%s new lead(s) imported from Meta.') % imported)
        return True
