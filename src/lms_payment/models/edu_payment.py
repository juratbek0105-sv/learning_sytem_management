from odoo import models, fields, api


class EduPayments(models.Model):
    _name = 'payment.edu.payment'
    _description = 'Edu Payment'
    _rec_name = "student_id"

    student_id = fields.Many2one("res.users", domain=[("user_type", "=", "student")],)
    amount = fields.Float(string="Amount")
    payment_date = fields.Date(string="Payment Date", default=fields.Date.today)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded')
    ], default='paid')
    note = fields.Text()



