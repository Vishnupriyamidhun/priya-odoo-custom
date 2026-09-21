from odoo import models, fields, api


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    department_ids = fields.Many2many(
        'hr.department',
        string='Departments',
        help='Select one or more departments to automatically add/remove '
             'their employees as attendees.',
    )

    # Technical/tracking field (not stored in DB) - keeps track of which
    # attendees were auto-added because of the selected departments, so
    # that removing a department can also remove its employees again.
    department_employee_partner_ids = fields.Many2many(
        'res.partner',
        string='Department Attendees (technical)',
        store=False,
    )

    @api.onchange('department_ids')
    def _onchange_department_ids_add_attendees(self):
        """Keep the attendee list in sync with the selected departments:
        - Employees of newly selected departments are added.
        - Employees of departments that were selected before but are no
          longer selected are removed again (unless they belong to another
          still-selected department).
        """
        # Employees that SHOULD be attendees based on the current selection
        employees = self.env['hr.employee'].search([
            ('department_id', 'in', self.department_ids.ids),
            ('user_id', '!=', False),
        ])
        new_department_partners = employees.mapped('user_id.partner_id')

        # Partners that were auto-added previously but are no longer needed
        partners_to_remove = self.department_employee_partner_ids - new_department_partners
        if partners_to_remove:
            self.partner_ids = [(3, p.id) for p in partners_to_remove]

        # Partners that need to be added now
        partners_to_add = new_department_partners - self.partner_ids
        if partners_to_add:
            self.partner_ids = [(4, p.id) for p in partners_to_add]

        # Update our tracking field for the next time this onchange runs
        self.department_employee_partner_ids = [(6, 0, new_department_partners.ids)]