from datetime import timedelta
from odoo import models, fields, api, _


class EduScheduleTable(models.Model):
    _name = 'edu.schedule.table'
    _description = 'Timetable'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date asc'

    name = fields.Char(string='Timetable Name', compute='_compute_name', store=True)
    group_id = fields.Many2one('edu.group', string='Group', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    lesson_start_time = fields.Float(string='Lesson Start Time', required=True)
    lesson_end_time = fields.Float(string='Lesson End Time', required=True)

    weekday_ids = fields.Many2many("edu.weekday")
    teacher_id = fields.Many2one('user.teacher', string='Teacher')
    company_id = fields.Many2one("res.company", string="Branch")
    schedule_lesson_ids = fields.One2many('edu.schedule.lesson', 'schedule_table_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled')
    ], default='draft', tracking=True)

    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)
    total_duration = fields.Float(string='Total Duration', compute='_compute_total_duration', store=True)
    first_lesson_date = fields.Date(string='First Lesson Date', compute='_compute_lesson_dates', store=True)
    last_lesson_date = fields.Date(string='Last Lesson Date', compute='_compute_lesson_dates', store=True)


    @api.depends('group_id')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.group_id.name} Schedule Table" if record.group_id else False


    @api.depends('group_id.course_id.total_lessons', 'weekday_ids', 'start_date')
    def _compute_end_date(self):
        for record in self:
            if not record.start_date or not record.weekday_ids:
                record.end_date = False
                return

            lesson_count = record.group_id.course_id.total_lessons
            weekdays = record.weekday_ids.mapped('sequence')

            current_date = record.start_date
            scheduled = 0

            while scheduled < lesson_count:
                if current_date.isoweekday() in weekdays:
                    scheduled += 1
                current_date += timedelta(days=1)

            record.end_date = current_date - timedelta(days=1)



    @api.depends('group_id.course_id.duration')
    def _compute_total_duration(self):
        for record in self:
            record.total_duration = record.group_id.course_id.duration * record.group_id.course_id.total_lessons



    @api.depends('start_date', 'end_date', 'weekday_ids')
    def _compute_lesson_dates(self):
        for record in self:
            if not record.start_date or not record.end_date or not record.weekday_ids:
                record.first_lesson_date = False
                record.last_lesson_date = False
                continue

            weekdays = record.weekday_ids.mapped('sequence')
            current = record.start_date

            first = None
            last = None

            while current <= record.end_date:
                if current.isoweekday() in weekdays:
                    first = first or current
                    last = current
                current += timedelta(days=1)

            record.first_lesson_date = first
            record.last_lesson_date = last


    # =============================
    # CREATE LESSONS AFTER CREATE
    # =============================
    def create(self, vals):
        record = super().create(vals)
        record.generate_schedule_lessons()
        return record



    def generate_schedule_lessons(self):
        schedule_lesson = self.env['edu.schedule.lesson']
        weekdays = self.weekday_ids.mapped('sequence')
        lessons = self.group_id.lesson_ids.sorted('sequence')

        if not self.start_date or not self.end_date:
            return

        current_date = self.start_date
        index = 0

        while current_date <= self.end_date and index < len(lessons):
            if current_date.isoweekday() in weekdays:

                lesson = lessons[index]

                schedule_lesson.create({
                    'schedule_table_id': self.id,
                    'name': lesson.name,
                    'sequence': lesson.sequence,
                    'date': current_date,
                    'lesson_start_time': self.lesson_start_time,
                    'lesson_end_time': self.lesson_end_time,
                    'teacher_id': self.teacher_id.id,
                    'group_id': self.group_id.id,
                })
                lesson[index].write({'date': current_date})

                index += 1

            current_date += timedelta(days=1)
