from odoo import models, fields, api


class Group(models.Model):
    _inherit = "edu.group"

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    balance = fields.Monetary(currency_field='currency_id', compute="_compute_balance")
    total_paid_students_amount = fields.Monetary(currency_field='currency_id',
                                                 compute='_compute_total_paid_students_amount')

    def _compute_total_paid_students_amount(self):
        for group in self:
            payments = self.env["payment.edu.payment"].search([
                ('detailed_type', '=', 'lesson_payment'),
                ('schedule_student_lesson_id.group_id', '=', group.id),
                ('status', '=', 'paid')
            ])
            group.total_paid_students_amount = sum(payments.mapped('amount'))

    def _compute_balance(self):
        for group in self:
            teacher_salary_payments = self.env["payment.edu.payment"].search([
                ('detailed_type', '=', 'teacher_salary'),
                ('status', '=', 'paid'),
                ('schedule_student_lesson_id.group_id', '=', group.id)])
            salary_paid_sum = sum(teacher_salary_payments.mapped('amount'))
            group.balance = group.total_paid_students_amount - salary_paid_sum

    def action_view_balance(self):
        self.ensure_one()
        return {
            'name': f'Balance Details for {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'payment.edu.payment',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('schedule_student_lesson_id.group_id', '=', self.id)],
            'context': {'default_detailed_type': 'lesson_payment'}
        }
