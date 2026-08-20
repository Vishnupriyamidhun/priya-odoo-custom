# Copyright 2019 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "hr.timesheet.time_control.mixin"]

    approval_state = fields.Selection(
        [
            ("none", "No Approval Needed"),
            ("pending", "Pending Approval"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="none",
        string="Approval State",
    )

    is_being_worked_on = fields.Boolean(
        compute="_compute_running_employee_ids",
        string="Currently Running",
    )

    start_button_color = fields.Char(
        compute="_compute_start_button_color",
    )

    @api.depends("timesheet_ids.unit_amount", "timesheet_ids.date_time")
    def _compute_running_employee_ids(self):
        for task in self:
            running_lines = task.sudo().timesheet_ids.filtered(
                lambda line: line.date_time and not line.unit_amount
            )
            task.is_being_worked_on = bool(running_lines)

    @api.depends("is_being_worked_on")
    def _compute_start_button_color(self):
        is_privileged = (
                self.env.user.has_group("project.group_project_manager")
                or self.env.user.has_group("hr_timesheet.group_hr_timesheet_approver")
                or self.env.user.has_group("base.group_system")
        )
        for task in self:
            if is_privileged and task.is_being_worked_on:
                task.start_button_color = "text-warning"
            else:
                task.start_button_color = "text-success"

    @api.constrains("date_deadline", "parent_id")
    def _check_deadline(self):
        for task in self:
            if not task.parent_id and not task.date_deadline:
                raise ValidationError(
                    _("Deadline is required before saving the task.")
                )

    @api.model
    def _relation_with_timesheet_line(self):
        return "task_id"

    @api.depends(
        "project_id.allow_timesheets",
        "timesheet_ids.employee_id",
        "timesheet_ids.unit_amount",
    )
    def _compute_show_time_control(self):
        result = super()._compute_show_time_control()
        for task in self:
            if not task.project_id.allow_timesheets:
                task.show_time_control = False
        return result

    def button_start_work(self):
        for task in self:
            if self.env.user not in task.user_ids:
                raise UserError(
                    _(
                        "Only the Employees assigned to this task can "
                        "start the timer"
                    )
                )
            employee = self.env["hr.employee"].search(
                [("user_id", "=", self.env.user.id)], limit=1
            )

            if not employee:
                raise UserError(_("No employee record found for your account."))

            today = fields.Date.today()

            attendance = self.env["hr.attendance"].search(
                [
                    ("employee_id", "=", employee.id),
                    ("check_in", ">=", fields.Datetime.to_datetime(today)),
                    ("check_out", "=", False),
                ],
                limit=1,
            )

            if attendance:
                task.approval_state = "none"

            else:
                work_location = employee.work_location_id.location_type

                if work_location == "home":
                    if task.approval_state == "approved":
                        task.approval_state = "none"

                    elif task.approval_state == "pending":
                        raise UserError(
                            _(
                                "Approval request already sent. "
                                "Please wait for manager approval."
                            )
                        )

                    elif task.approval_state == "rejected":
                        raise UserError(
                            _(
                                "Your request was rejected by manager. "
                                "Please contact your manager."
                            )
                        )

                    else:
                        task.approval_state = "pending"
                        task._send_approval_request()
                        return {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': _('Approval Requested'),
                                'message': _(
                                    'You are not checked in. Approval request sent to your manager. Work will start after approval.'),
                                'type': 'warning',
                                'sticky': True,
                            }
                        }

                else:
                    raise UserError(
                        _(
                            "You are currently checked out. "
                            "Please check in before starting work."
                        )
                    )

        result = super().button_start_work()
        if isinstance(result, dict):
            result.setdefault("context", {})
            result["context"].update({"default_project_id": self[0].project_id.id})
        return result

    def button_end_work(self):
        if not self.env.context.get("skip_assignee_check"):
            for task in self:
                if self.env.user not in task.user_ids:
                    raise UserError(
                        _(
                            "Only the Employees assigned to this task can "
                            "Stop the timer"
                        )
                    )
        return super().button_end_work()

    def _send_approval_request(self):
        for task in self:
            employee = self.env["hr.employee"].search(
                [("user_id", "=", self.env.user.id)], limit=1
            )

            if not employee:
                raise UserError(_("No employee record found for your account."))

            manager = employee.parent_id.user_id
            admins = self.env.ref("base.group_system").users

            if not manager and not admins:
                raise UserError(
                    _(
                        "No manager or admin available to approve. "
                        "Please contact HR."
                    )
                )

            approver_partners = (manager.partner_id if manager else self.env['res.partner']) | admins.partner_id

            task.message_post(
                body=_(
                    "<b>%s</b> is not checked in today and has requested "
                    "approval to start work on task: <b>%s</b>.<br/>"
                    "Please <b>Approve</b> or <b>Reject</b> the request."
                ) % (self.env.user.name, task.name),
                partner_ids=approver_partners.ids,
                message_type="comment",
                subtype_xmlid="mail.mt_comment",
            )

            activity_type = self.env.ref("mail.mail_activity_data_todo")

            if manager:
                task.activity_schedule(
                    activity_type_id=activity_type.id,
                    user_id=manager.id,
                    note=_(
                        "Employee %s has requested approval to start work on task '%s'. "
                        "Please review and approve or reject the request."
                    ) % (employee.name, task.name),
                )

            for admin in admins:
                if admin != manager:
                    task.activity_schedule(
                        activity_type_id=activity_type.id,
                        user_id=admin.id,
                        note=_(
                            "Employee %s has requested approval to start work on task '%s'."
                        ) % (employee.name, task.name),
                    )

    def button_approve_work(self):
        activity_type = self.env.ref("mail.mail_activity_data_todo")
        for task in self:
            employee = self.env["hr.employee"].search(
                [("user_id", "=", self.env.user.id)], limit=1
            )

            # ടാസ്ക് ക്രിയേറ്റ് ചെയ്ത ആളുടെ അല്ലെങ്കിൽ Assignee പ്രൊഫൈലിലെ മാനേജരെ എടുക്കുന്നു
            task_employee = self.env["hr.employee"].search([("user_id", "in", task.user_ids.ids)], limit=1)
            manager = task_employee.parent_id.user_id if task_employee else False

            if (
                    self.env.user != manager
                    and not self.env.user.has_group("base.group_system")
            ):
                raise UserError(
                    _("Only Manager or Administrator can approve this request.")
                )

            task.approval_state = "approved"

            task.activity_ids.filtered(
                lambda a: a.activity_type_id == activity_type
            ).action_feedback(feedback=_("Approved"))

            if task_employee and task_employee.user_id:
                task.message_post(
                    body=_(
                        "Your work start request has been <b>approved</b> by %s."
                    ) % self.env.user.name,
                    partner_ids=[task_employee.user_id.partner_id.id],
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )

    def button_reject_work(self):
        activity_type = self.env.ref("mail.mail_activity_data_todo")
        for task in self:
            task_employee = self.env["hr.employee"].search([("user_id", "in", task.user_ids.ids)], limit=1)
            manager = task_employee.parent_id.user_id if task_employee else False

            if (
                    self.env.user != manager
                    and not self.env.user.has_group("base.group_system")
            ):
                raise UserError(
                    _("Only Manager or Administrator can reject this request.")
                )

            task.approval_state = "rejected"

            task.activity_ids.filtered(
                lambda a: a.activity_type_id == activity_type
            ).action_feedback(feedback=_("Rejected"))

            if task_employee and task_employee.user_id:
                task.message_post(
                    body=_(
                        "Your work start request has been <b>rejected</b> by %s."
                    ) % self.env.user.name,
                    partner_ids=[task_employee.user_id.partner_id.id],
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )