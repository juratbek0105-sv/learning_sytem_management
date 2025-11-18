from odoo import models, fields

class EducationStudent(models.Model):
    _inherit = 'res.users'

    payment_ids = fields.One2many('payment.edu.payment', 'user_id', string="Payments")
    total_paid = fields.Monetary(string="Total Paid", compute="_compute_total_paid", currency_field="currency_id")
    currency_id = fields.Many2one('res.currency')

    def _compute_total_paid(self):
        for record in self:
            record.total_paid = sum(record.payment_ids.mapped('amount'))