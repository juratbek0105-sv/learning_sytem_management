from odoo import models, fields, api


class Group(models.Model):
     _name = 'edu.group'
     _description = 'Group'
     _inherit = ['mail.thread', 'mail.activity.mixin']

     name = fields.Char(required=True, tracking=True)
     active = fields.Boolean(default=True)
     state = fields.Selection([
         ('active', 'Active'),
         ('frozen', 'Frozen'),
         ('completed', 'Completed')
     ], default='active')

     course_id = fields.Many2one("edu.course")
     student_ids = fields.Many2many("user.student", string="Students")
     teacher_id = fields.Many2many("user.teacher")
     timetable_id = fields.One2many("edu.timetable", "group_id", string="Timetable")
     lesson_ids = fields.One2many("edu.lesson", "group_id")


     def action_toggle_group(self):
         for record in self:
             record.active = not record.active



