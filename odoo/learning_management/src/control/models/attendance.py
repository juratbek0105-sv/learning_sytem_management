from odoo import models, fields, api


class Attendance(models.Model):
     _name = 'control.attendance'
     _description = 'Attendance'

     person_type = fields.Selection([
         ("student", "Student"),
         ("employee", "Employee"),
     ], required=True)
     student_id = fields.Many2one("lms.student", string="Student")
     employee_id = fields.Many2one("res.users", string="Employee")
     date = fields.Date()
     status = fields.Selection([
         ('present', 'Present'),
         ('absent', 'Absent'),
         ('late', 'Late')
     ])



