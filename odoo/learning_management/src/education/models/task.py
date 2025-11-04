from odoo import models, fields, api


class Task(models.Model):
     _name = 'edu.task'
     _description = 'Task'


     name = fields.Char(string="Assignment", required=True)
     description = fields.Text(string="Task Description")
     deadline = fields.Datetime(string="Deadline")

     course_id = fields.Many2one("edu.course")
     group_id = fields.Many2one("edu.group")
     lesson_id = fields.Many2one("edu.lesson")
     student_ids = fields.Many2many("user.student", string="Assigned Students")

     state = fields.Selection([
         ('draft', 'Draft'),
         ('assigned', 'Assigned'),
         ('submitted', 'Submitted'),
         ('reviewed', 'Reviewed'),
         ('closed', 'Closed'),
     ], default='draft')

     submission_ids = fields.One2many("edu.task.submission", "homework_id")

     def action_assign(self):
         for rec in self:
             rec.state = "assigned"

     def action_close(self):
         for rec in self:
             rec.state = "closed"




