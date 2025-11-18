from odoo import models, fields, api


class EduPayment(models.Model):
    _name = 'payment.edu.payment'
    _description = 'Edu Payment'

    user_id = fields.Many2one("res.users", string="User")
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
