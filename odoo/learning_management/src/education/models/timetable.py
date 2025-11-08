from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class Timetable(models.Model):
    _name = 'edu.timetable'
    _description = 'Timetable'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, tracking=True)
    group_id = fields.Many2one(
        "edu.group",
        string="Group",
        required=True,
        domain=lambda self: [('company_id', '=', self.env.company.id)]
    )

    course_id = fields.Many2one('edu.course', string="Course", tracking=True)
    teacher_id = fields.Many2one('user.teacher',string="Teacher",required=True,tracking=True)
    company_id = fields.Many2one('res.company', string="Branch", default=lambda self: self.env.company, tracking=True)

    start_date = fields.Datetime(string="Start", required=True, tracking=True)
    end_date = fields.Datetime(string="End", required=True, tracking=True)
    first_lesson_date = fields.Date(string="First Lesson", compute="_compute_lesson_dates", store=True)
    last_lesson_date = fields.Date(string="Last Lesson", compute="_compute_lesson_dates", store=True)
    lesson_start_time = fields.Float(string="Lesson Start", required=True, help="Use 24h format, e.g. 13.5 for 13:30")
    lesson_end_time = fields.Float(string="Lesson End", required=True)

    weekday_ids = fields.Many2many("edu.weekday", string="Weekdays")

    lesson_duration = fields.Float(string="Lesson Duration (hours)", compute="_compute_duration", store=True)
    total_lessons = fields.Integer(string="Total Lessons", compute="_compute_totals", store=True)
    total_duration = fields.Float(string="Total Duration (hours)", compute="_compute_totals", store=True)

    notes = fields.Text(string="Notes")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
    ], string="Status", default='draft', tracking=True) \

    @api.depends('lesson_start_time', 'lesson_end_time')
    def _compute_duration(self):
        for record in self:
            record.lesson_duration = max(record.lesson_end_time - record.lesson_start_time, 0.0)

    @api.depends('start_date', 'end_date', 'weekday_ids')
    def _compute_lesson_dates(self):
        for record in self:
            if not (record.start_date and record.end_date and record.weekday_ids):
                record.first_lesson_date = False
                record.last_lesson_date = False
                continue

            weekdays = record.weekday_ids.mapped('sequence')
            current_date = record.start_date
            first, last = None, None

            while current_date <= record.end_date:
                if current_date.isoweekday() in weekdays:
                    first = first or current_date
                    last = current_date
                current_date += timedelta(days=1)

            record.first_lesson_date = first
            record.last_lesson_date = last

    @api.depends('start_date', 'end_date', 'weekday_ids', 'lesson_duration')
    def _compute_totals(self):
        for record in self:
            if not (record.start_date and record.end_date and record.weekday_ids):
                record.total_lessons = 0
                record.total_duration = 0.0
                continue

            weekdays = record.weekday_ids.mapped('sequence')
            total_days = (record.end_date - record.start_date).days + 1
            lesson_count = 0

            for i in range(total_days):
                current_date = record.start_date + timedelta(days=i)
                if current_date.isoweekday() in weekdays:
                    lesson_count += 1

            record.total_lessons = lesson_count
            record.total_duration = lesson_count * record.lesson_duration

    # ------------------- CONSTRAINTS -------------------

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

    @api.constrains('teacher_id', 'start_date', 'end_date', 'lesson_start_time', 'lesson_end_time', 'weekday_ids')
    def _check_conflicts(self):
        for record in self:
            if not record.teacher_id or not record.weekday_ids:
                continue

            overlaps = self.search([
                ('id', '!=', record.id),
                ('teacher_id', '=', record.teacher_id.id),
                ('weekday_ids', 'in', record.weekday_ids.ids),
                ('start_date', '<=', record.end_date),
                ('end_date', '>=', record.start_date),
            ])
            if overlaps:
                raise ValidationError(_("Teacher %s already has classes in this period.") % record.teacher_id.name)

    @api.onchange('course_id')
    def _onchange_course_subject(self):
        if self.course_id:
            return {'domain': {'subject_id': [('course_id', '=', self.course_id.id)]}}
        return {'domain': {'subject_id': []}}


    @api.onchange('company_id')
    def _onchange_company_teacher_group(self):
        if self.company_id:
            return {
                'domain': {
                    'teacher_id': [('company_id', '=', self.company_id.id)],
                    'group_id': [('company_id', '=', self.company_id.id)],
                }
            }
        return {'domain': {'teacher_id': [], 'group_id': []}}


    def action_activate(self):
        self.write({'state': 'active'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
