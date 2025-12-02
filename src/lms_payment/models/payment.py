from odoo import models, fields, api


class EduPayment(models.Model):
    _name = 'payment.edu.payment'
    _description = 'Edu Payment'
    _rec_name = "name"

    name = fields.Char(string="Payment Name", copy=False, readonly=True)
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
    ],  default='top_up_balance', string='Payment Category')
    student_id = fields.Many2one("res.partner", string="Student")
    branch_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


    def action_paid(self):
        self.write({'status': 'paid'})

    def action_cancelled(self):
        self.write({'status': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'status': 'draft'})

    @api.model
    def create(self, vals):
        """Automatically generate a descriptive name for the payment"""
        if not vals.get('name'):
            today_str = fields.Date.today().strftime('%Y-%m-%d')
            dt = vals.get('detailed_type')
            if dt == 'top_up_balance' and vals.get('student_id'):
                student = self.env['res.partner'].browse(vals['student_id'])
                vals['name'] = f"Top-up for {student.name} on {today_str}"
            elif dt == 'lesson_payment' and vals.get('student_id') and vals.get('group_id'):
                student = self.env['res.partner'].browse(vals['student_id'])
                group = self.env['edu.group'].browse(vals['group_id'])
                vals['name'] = f"Lesson payment for {student.name} ({group.name}) on {today_str}"
            elif dt == 'teacher_salary' and vals.get('teacher_id') and vals.get('group_id'):
                teacher = self.env['res.partner'].browse(vals['teacher_id'])
                group = self.env['edu.group'].browse(vals['group_id'])
                vals['name'] = f"Teacher salary for {teacher.name} ({group.name}) - {today_str}"
            else:
                vals['name'] = f"Payment {today_str}"
        return super(EduPayment, self).create(vals)

