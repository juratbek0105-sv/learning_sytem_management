from odoo import models, fields, api



class Student(models.Model):
    _inherit = "user.student"

    group_ids = fields.Many2many("edu.group")
    course_ids = fields.Many2many("edu.course")


class Teacher(models.Model):
    _inherit = "user.teacher"

    subjects = fields.Many2many("edu.subject")
    group_ids = fields.Many2many("edu.group", string="Groups")
    course_ids = fields.Many2many("edu.course", string="Courses")
