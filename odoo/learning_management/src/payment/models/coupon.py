from odoo import models, fields, api


class Coupon(models.Model):
     _name = 'payment.coupon'
     _description = 'Coupon'

     code = fields.Char(string="Coupon Code", required=True)
     discount_percent = fields.Float(string="Discount %", required=True)



