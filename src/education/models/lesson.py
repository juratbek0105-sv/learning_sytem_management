from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EduLesson(models.Model):
    _name = 'edu.lesson'
    _description = 'Course Lesson / Topic'
    _order = 'sequence asc'

    name = fields.Char(string='Lesson Name', required=True)
    date = fields.Date(string="Date")
    sequence = fields.Integer(string='Sequence', default=1)
    duration = fields.Float(string='Duration')
    duration_uom = fields.Many2one("uom.uom", required=True, domain=[("category_id.name", "=", "Time")])
    course_id = fields.Many2one('edu.course', string='Course', required=True)
    group_id = fields.Many2one('edu.group', string='Group')
    teacher_id = fields.Many2one('user.teacher', string='Teacher', domain=[("teacher_id", "in", "course_id.teacher_ids")])
    task_ids = fields.One2many("edu.task", "lesson_id", string="Tasks")

    def action_change_lesson_date(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Change Lesson Date'),
            'res_model': 'edu.lesson.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_lesson_id': self.id},
        }