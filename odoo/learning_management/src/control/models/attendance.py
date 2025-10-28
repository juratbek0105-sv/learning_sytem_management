from odoo import models, fields, api


class Attendance(models.Model):
     _name = 'control.attendance'
     _description = 'Attendance'

     user_id = fields.Many2one("res.users")
     date = fields.Date()
     status = fields.Selection([
         ('present', 'Present'),
         ('absent', 'Absent'),
         ('late', 'Late')
     ])



