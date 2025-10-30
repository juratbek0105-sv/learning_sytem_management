from odoo import models, fields, api


class Group(models.Model):
     _name = 'edu.group'
     _description = 'Group'

     name = fields.Char(required=True)
     course_id = fields.Many2one("edu.course")
     student_ids = fields.Many2many("lms.student", string="Students")
     teacher_id = fields.Many2one("lms.teacher")
     timetable_id = fields.One2many("edu.timetable", "group_id", string="Timetable")
     lesson_ids = fields.One2many("edu.lesson", "group_id")
     state = fields.Selection([
         ('active', 'Active'),
         ('frozen', 'Frozen'),
         ('completed', 'Completed')
     ], default='active')



