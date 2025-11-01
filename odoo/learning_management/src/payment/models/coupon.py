from odoo import models, fields, api


class Coupon(models.Model):
    _name = 'payment.coupon'
    _description = 'Coupon'

    code = fields.Char(string="Coupon Code", required=True)
    discount_percent = fields.Float(string="Discount %", required=True)

    valid_from = fields.Date(default=fields.Date.context_today)
    valid_to = fields.Date()
    usage_limit = fields.Integer(default=1)


    status = fields.Selection([
            ("valid", "Valid"),
            ("expired", "Expired"),
            ("used_up", "Used Up"),
        ],compute="_compute_status",store=True)

    _sql_constraints = [
        ("unique_coupon_code", "unique(code)", "Coupon code must be unique!")
    ]

