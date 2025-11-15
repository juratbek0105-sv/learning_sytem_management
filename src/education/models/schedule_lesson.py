from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ScheduleLesson(models.Model):
    _name = 'edu.schedule.lesson'
    _description = 'Scheduled Lesson'

    name = fields.Char(string="Name", required=True, copy=False, readonly=True)
    sequence = fields.Integer(string="Lesson Number", readonly=True)
    schedule_table_id = fields.Many2one('edu.schedule.table', string='Timetable', required=True)
    date = fields.Date(string='Lesson Date', required=True)
    lesson_start_time = fields.Float(string='Start Time', required=True)
    lesson_end_time = fields.Float(string='End Time', required=True)
    teacher_id = fields.Many2one('user.teacher', string='Teacher', related='group_id.teacher_id', store=True)
    group_id = fields.Many2one('edu.group', string='Group', related='schedule_table_id.group_id', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], string='Status', default='draft')

    def action_mark_done(self):
        self.state = "done"

    def action_reset_draft(self):
        self.state = "draft"
