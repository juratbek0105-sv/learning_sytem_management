from odoo import models, api

class EducationStudentWithdraw(models.Model):
    _inherit = 'res.users'  # Changed from 'user.student' to match your other model

    @api.depends('student_payment_ids.amount', 'student_payment_ids.status', 'student_payment_ids.detailed_type')
    def _compute_balance(self):
        super()._compute_balance()

        for student in self:
            withdrawals = student.student_payment_ids.filtered(
                lambda x: x.status == "paid" and x.detailed_type == "lesson_payment"
            )
            total_withdraw = sum(withdrawals.mapped('amount'))

            student.balance -= total_withdraw