from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EduLesson(models.Model):
    _name = 'edu.lesson'
    _description = 'Course Lesson / Topic'
    _order = 'sequence asc'

    name = fields.Char(string='Lesson Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    duration = fields.Float(string='Duration')
    duration_uom = fields.Many2one("uom.uom", required=True, domain=[("category_id.name", "=", "Time")])
    course_id = fields.Many2one('edu.course', string='Course', required=True)
    teacher_ids = fields.Many2many('res.users', domain=[("user_type", "=", "teacher")], string='Teachers', related="course_id.teacher_ids")

