from odoo import models, fields, api


class EduPayment(models.Model):
    _name = 'payment.edu.payment'
    _description = 'Edu Payment'
    _rec_name = "name"

    name = fields.Char(string="Payment Name", readonly=True, copy=False)
    user_id = fields.Many2one("res.users", string="User", default=lambda self: self.env.user)
    amount = fields.Monetary(string="Amount", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
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
    ],  default='top_up_balance', string='Payment Category')
    student_id = fields.Many2one("res.partner", string="Student", domain=[('user_type', '=', 'student')])
    teacher_id = fields.Many2one("res.users", domain=[('user_type', '=', 'teacher')])
    branch_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


    def action_paid(self):
        self.write({'status': 'paid'})

    def action_cancelled(self):
        self.write({'status': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'status': 'draft'})

    @api.model
    def _generate_payment_name(self, vals):
        dt = vals.get('detailed_type')

        if dt == 'teacher_salary':
            return self.env['ir.sequence'].next_by_code('payment.teacher.salary')

        if dt == 'top_up_balance':
            return self.env['ir.sequence'].next_by_code('payment.student.topup')

        return self.env['ir.sequence'].next_by_code('payment.edu.payment')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self._generate_payment_name(vals)

        return super().create(vals_list)