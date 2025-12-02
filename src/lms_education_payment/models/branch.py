from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = "res.company"

    balance = fields.Float(string="Company Balance", compute="_compute_balance")

    @api.depends("balance")
    def _compute_balance(self):
        for company in self:
            lesson_payments = self.env["payment.edu.payment"].search([
                ("branch_id", "=", company.id), ('detailed_type' , '=','lesson_payment')
            ])
            lesson_payments_amount = sum(lesson_payments.mapped("amount"))
            teacher_salaries = self.env["payment.edu.payment"].search([
                ("branch_id", "=", company.id), ('detailed_type' , '=','teacher_salary')
            ])
            teacher_salaries_amount = sum(teacher_salaries.mapped("amount"))

            company.balance = lesson_payments_amount - teacher_salaries_amount


    def open_company_balance(self):
        self.ensure_one()
        return {
            "name": "Company Payments",
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "payment.edu.payment",
            "domain": [("branch_id", "=", self.id), ('detailed_type', 'in', ['lesson_payment','teacher_salary'])],
            "context": {"default_branch_id": self.id},
        }