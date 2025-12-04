from odoo import models, fields, api

class EducationStudent(models.Model):
    _inherit = 'res.users'

    student_payment_ids = fields.One2many('payment.edu.payment', 'student_id', string="Student Payments")
    teacher_payment_ids = fields.One2many('payment.edu.payment', 'teacher_id', string="Teacher Payments")
    total_paid_student = fields.Float(string="Total Paid Student", compute="_compute_total_paid")
    total_paid_teacher = fields.Float(string="Total Paid Student", compute="_compute_total_paid")
    balance = fields.Float("Balance", compute="_compute_balance")

    def _compute_total_paid(self):
        for record in self:
            teacher_paid_payments = record.teacher_payment_ids.filtered(lambda p: p.status == 'paid')
            record.total_paid_teacher = sum(teacher_paid_payments.mapped('amount'))
            student_paid_payments = record.teacher_payment_ids.filtered(lambda p: p.status == 'paid')
            record.total_paid_student = sum(student_paid_payments.mapped('amount'))

    def _compute_balance(self):
        for record in self:
            if record.user_type == "student":
                top_up_balances = record.student_payment_ids.filtered(
                    lambda x: x.detailed_type == "top_up_balance" and x.status == "paid"
                )
                record.balance = sum(top_up_balances.mapped('amount'))
            elif record.user_type == "teacher":
                salaries = record.teacher_payment_ids.filtered(lambda x: x.detailed_type == "teacher_salary" and
                                                               x.status == "paid")
                record.balance = sum(salaries.mapped('amount'))

    def action_balance(self):
        self.ensure_one()

        if self.user_type == 'student':
            domain = [
                ('student_id', '=', self.id),
                ('status', '=', 'paid'),
                ('detailed_type', '=', 'top_up_balance')
            ]
        else:
            domain = [
                ('teacher_id', '=', self.id),
                ('status', '=', 'paid'),
                ('detailed_type', '=', 'teacher_salary')
            ]

        return {
            'type': 'ir.actions.act_window',
            'name': f'{self.name} Balance',
            'res_model': 'payment.edu.payment',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': domain,
        }
