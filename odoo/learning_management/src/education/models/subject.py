from odoo import models, fields, api


class Subject(models.Model):
    _name = 'edu.subject'
    _description = 'Subject'


    name = fields.Char(string="Subject Name", required=True)
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")

    course_ids = fields.Many2many("lms.course", string="Courses")
