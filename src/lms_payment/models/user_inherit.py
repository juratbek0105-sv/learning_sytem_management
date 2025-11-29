from odoo import models, fields, api

class EducationStudent(models.Model):
    _inherit = 'res.users'

    payment_ids = fields.One2many('payment.edu.payment', 'student_id', string="Payments")
    total_paid = fields.Float(string="Total Paid", compute="_compute_total_paid")
    balance = fields.Float("Balance", compute="_compute_balance")

    def _compute_total_paid(self):
        for record in self:
            record.total_paid = sum(record.payment_ids.mapped('amount'))

    def _compute_balance(self):
        for record in self:
            top_up_balances = record.payment_ids.filtered(
                lambda x: x.status == "paid" and x.detailed_type == "top_up_balance"
            )
            record.balance = sum(top_up_balances.mapped('amount'))
    def action_balance(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': ' Balance',
            'res_model': 'payment.edu.payment',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('student_id', '=', self.id),('status', '=', 'paid')],
            'context': {
                'default_student_id': self.id,
            }
        }





