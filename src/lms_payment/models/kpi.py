from odoo import models, fields, api


class KPI(models.Model):
    _name = 'payment.kpi'
    _description = 'KPI'


    employee_id = fields.Many2one("res.users", string="Employee", required=True)
    month = fields.Selection([
        ("01", "January"), ("02", "February"), ("03", "March"),
        ("04", "April"), ("05", "May"), ("06", "June"),
        ("07", "July"), ("08", "August"), ("09", "September"),
        ("10", "October"), ("11", "November"), ("12", "December"),
    ], string="Month", required=True)
    year = fields.Integer(string="Year", default=lambda self: fields.Date.today().year)
    score = fields.Float(string="KPI Score", required=True)
    bonus_amount = fields.Float(string="Bonus", compute="_compute_bonus", store=True)


