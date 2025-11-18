from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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

    @api.depends('schedule_lesson_ids', 'schedule_lesson_ids.lesson_start_time', 'schedule_lesson_ids.lesson_end_time')
    def _compute_total_duration(self):
        for record in self:
            total = 0
            for lesson in record.schedule_lesson_ids:
                total += lesson.lesson_end_time - lesson.lesson_start_time
            record.total_duration = total

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

    def action_activate(self):
        self.write({'state': 'active'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_view_schedule_lessons(self):
        self.ensure_one()
        return {
            'name': _('Lesson Schedules'),
            'type': 'ir.actions.act_window',
            'res_model': 'edu.schedule.lesson',
            'view_mode': 'list,form',
            'domain': [('schedule_table_id', '=', self.id)],
            'context': {
                           'default_schedule_table_id': self.id,
                           'search_default_group_by_group_id': 0,
                       }
        }

    @api.model_create_multi
    def create(self, vals_list):
        record = super().create(vals_list)
        record.generate_schedule_lessons()
        return record

    def generate_schedule_lessons(self):
        if self.state == "active":

            self.ensure_one()
            Lesson = self.env['edu.schedule.lesson']
            weekdays = self.weekday_ids.mapped('sequence')
            lessons = self.group_id.group_lesson_ids.sorted('sequence')

            if not self.start_date or not self.end_date or not lessons:
                return

            lesson_index = 0
            total = len(lessons)
            days_count = (self.end_date - self.start_date).days + 1
            for i in range(days_count):

                if lesson_index >= total:
                    break

                current_date = self.start_date + timedelta(days=i)

                if current_date.isoweekday() not in weekdays:
                    continue
                gl = lessons[lesson_index]

                Lesson.create({
                    'schedule_table_id': self.id,
                    'group_lesson_id': gl.id,
                    'name': gl.name,
                    'sequence': gl.sequence,
                    'date': current_date,
                    'lesson_start_time': self.lesson_start_time,
                    'lesson_end_time': self.lesson_end_time,
                    'teacher_id': self.teacher_id.id,
                    'group_id': self.group_id.id,
                })

                lesson_index += 1
        else:
            raise ValidationError("Please activate the schedule table first, to generate schedule lessons!")

    @api.constrains('lesson_start_time', 'lesson_end_time')
    def _check_time_validity(self):
        for record in self:
            if record.lesson_end_time <= record.lesson_start_time:
                raise ValidationError(_("Lesson end time must be after start time."))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError(_("End date cannot be earlier than start date."))
