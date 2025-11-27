from odoo import models, fields

class EducationStudent(models.Model):
    _inherit = 'user.student'

    payment_ids = fields.One2many('payment.edu.payment', 'user_id', string="Payments")
    total_paid = fields.Float(string="Total Paid", compute="_compute_total_paid")

    def _compute_total_paid(self):
        for record in self:
            record.total_paid = sum(record.payment_ids.mapped('amount'))








