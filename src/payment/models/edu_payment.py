from odoo import models, fields, api


class EduPayments(models.Model):
    _name = 'payment.edu.payment'
    _description = 'Edu Payment'

    student_id = fields.Many2one("res.users")
    amount = fields.Float()
    payment_date = fields.Date()
    status = fields.Selection([
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded')
    ], default='paid')
    note = fields.Text()


    @api.onchange('group_id')
    def _onchange_group_id(self):
        if self.group_id:
            return {
                'domain': {'student_id': [('group_id', '=', self.group_id.id)]}
            }
        else:
            return {
                'domain': {'student_id': []}
            }
