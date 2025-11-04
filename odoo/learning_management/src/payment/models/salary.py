from odoo import models, fields, api


class Salary(models.Model):
    _name = "payment.salary"
    _description = "Employee Salary"

    employee_id = fields.Many2one("res.users", string="Employee", required=True)
    month = fields.Selection([
        ("01", "January"), ("02", "February"), ("03", "March"),
        ("04", "April"), ("05", "May"), ("06", "June"),
        ("07", "July"), ("08", "August"), ("09", "September"),
        ("10", "October"), ("11", "November"), ("12", "December"),
    ], required=True)
    year = fields.Integer(string="Year", default=lambda self: fields.Date.today().year)
    base_salary = fields.Float(string="Base Salary", required=True)
    bonus = fields.Float(string="Bonus", default=0)
    total_salary = fields.Float(string="Total Salary", compute="_compute_total", store=True)
    status = fields.Selection([
        ("draft", "Draft"),
        ("paid", "Paid"),
        ("hold", "On Hold"),
    ], string="Status", default="draft")


    @api.depends("base_salary", "bonus")
    def _compute_total(self):
        for record in self:
            record.total_salary = record.base_salary + record.bonus





