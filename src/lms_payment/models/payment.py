from odoo import models, fields, api


class EduPayment(models.Model):
    _name = 'payment.edu.payment'
    _description = 'Edu Payment'

    user_id = fields.Many2one("res.users", string="User", default=lambda self: self.env.user)
    amount = fields.Float(string="Amount")
    payment_date = fields.Date(string="Payment Date", default=fields.Date.today(), required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded')
    ], default='draft')
    payment_type = fields.Selection([
        ("card", "Card"),
        ("cash", "Cash"),
        ("online", "Online"),
    ], string="Payment Type", required=True, default="card")
    note = fields.Text()
    detailed_type = fields.Selection([
        ('top_up_balance', 'Top Up Balance')
    ], required=True,  default='top_up_balance', string='Payment Category', ondelete={'top_up_balance': 'set default'} )
    student_id = fields.Many2one("res.users", string="Student")


    def action_paid(self):
        self.write({'status': 'paid'})

    def action_cancelled(self):
        self.write({'status': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'status': 'draft'})

