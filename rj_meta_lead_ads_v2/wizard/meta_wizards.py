# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class MetaImportWizard(models.TransientModel):
    _name = 'meta.lead.ads.import.wizard'
    _description = 'Meta Lead Ads Import Wizard'

    config_id = fields.Many2one('meta.lead.ads.config', required=True)
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    result_message = fields.Text(readonly=True)

    def action_import(self):
        self.ensure_one()
        if not self.config_id:
            raise UserError(_('Select a configuration.'))
        self.config_id.action_sync_import()
        self.result_message = _('Import finished. Open records to review.')
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }


class MetaExportWizard(models.TransientModel):
    _name = 'meta.lead.ads.export.wizard'
    _description = 'Meta Lead Ads Export Wizard'

    config_id = fields.Many2one('meta.lead.ads.config', required=True)
    result_message = fields.Text(readonly=True)

    def action_export(self):
        self.ensure_one()
        records = self.env['meta.lead.ads.form'].search([
            ('config_id', '=', self.config_id.id),
            ('sync_state', 'in', ('draft', 'error', 'pending')),
        ], limit=100)
        if records:
            records.action_sync_to_meta()
            self.result_message = _('Exported / synced %s record(s).') % len(records)
        else:
            self.result_message = _('No draft/error records to export.')
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
