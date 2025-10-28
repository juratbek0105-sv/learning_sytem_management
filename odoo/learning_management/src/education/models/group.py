from odoo import models, fields, api


class Group(models.Model):
     _name = 'edu.group'
     _description = 'Group'

     name = fields.Char(required=True)
     course_id = fields.Many2one("edu.course")
     student_ids = fields.Many2many("lms.student", string="Students")
     teacher_id = fields.Many2one("lms.teacher")
     schedule_ids = fields.One2many("edu.schedule", "group_id", string="Schedule")
     state = fields.Selection([
         ('active', 'Active'),
         ('frozen', 'Frozen'),
         ('completed', 'Completed')
     ], default='active')



