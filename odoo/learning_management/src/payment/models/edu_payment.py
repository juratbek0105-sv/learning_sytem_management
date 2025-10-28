from odoo import models, fields, api


class EduPayments(models.Model):
     _name = 'payment.edu.payment'
     _description = 'Edu Payment'

     student_id = fields.Many2one("res.users")
     course_id = fields.Many2one("edu.course")
     amount = fields.Float()
     payment_type = fields.Selection([
         ('tuition', 'Course Payment'),
         ('material', 'Material Payment'),
         ('salary', 'Salary'),
         ('expense', 'Expense')
     ])
     status = fields.Selection([
         ('paid', 'Paid'),
         ('cancelled', 'Cancelled'),
         ('refunded', 'Refunded')
     ], default='paid')



