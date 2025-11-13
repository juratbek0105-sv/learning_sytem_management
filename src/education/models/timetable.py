from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class Timetable(models.Model):
    _name = 'edu.timetable'
    _description = 'Timetable'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    group_id = fields.Many2one(
        "edu.group",
        string="Group",
        required=True,
        domain=lambda self: [('company_id', '=', self.env.company.id)]
    )
    course_id = fields.Many2one('edu.course', string="Course", tracking=True)
    teacher_id = fields.Many2one('user.teacher', string="Teacher", required=True, tracking=True)
    company_id = fields.Many2one('res.company', string="Branch", default=lambda self: self.env.company, tracking=True)

    start_date = fields.Date(string="Start", required=True, tracking=True)
    end_date = fields.Date(string="End", required=True, tracking=True)
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
    ], string="Status", default='draft', tracking=True)

    # ------------------ COMPUTES ------------------
    @api.depends('group_id', 'teacher_id', 'start_date', 'end_date')
    def _compute_name(self):
        for record in self:
            if record.group_id  and record.teacher_id and record.start_date and record.end_date:
                teacher_initials = ''.join([n[0] for n in record.teacher_id.name.split()])
                record.name = f"{record.group_id.name} - {teacher_initials} - {record.start_date.strftime('%d %b')} to {record.end_date.strftime('%d %b')}"

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
            lesson_count = sum(
                1 for i in range(total_days)
                if (record.start_date + timedelta(days=i)).isoweekday() in weekdays
            )
            record.total_lessons = lesson_count
            record.total_duration = lesson_count * record.lesson_duration

    # ------------------ VALIDATIONS ------------------
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
            # Get all lessons for this teacher
            existing_lessons = self.env['edu.schedule.lesson'].search([
                ('timetable_id.teacher_id', '=', record.teacher_id.id)
            ])
            new_weekdays = record.weekday_ids.mapped('sequence')
            current_date = record.start_date
            while current_date <= record.end_date:
                if current_date.isoweekday() in new_weekdays:
                    # Check overlapping lessons on this date
                    day_lessons = existing_lessons.filtered(lambda l: l.lesson_date == current_date)
                    for l in day_lessons:
                        if (record.lesson_start_time < l.lesson_end_time) and (record.lesson_end_time > l.lesson_start_time):
                            raise ValidationError(_(
                                "Teacher %s already has a lesson on %s from %.2f to %.2f"
                            ) % (record.teacher_id.name, current_date, l.lesson_start_time, l.lesson_end_time))
                current_date += timedelta(days=1)

    # ------------------ ONCHANGE ------------------
    @api.onchange('course_id')
    def _onchange_course_subject(self):
        if self.course_id:
            return {'domain': {'group_id': [('course_id', '=', self.course_id.id)]}}
        return {'domain': {'group_id': []}}

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

    # ------------------ LESSON GENERATION ------------------
    @api.model_create_multi
    def create(self, vals_list):
        records = super(Timetable, self).create(vals_list)
        for record in records:
            record._generate_schedule_lessons()
        return records

    def write(self, vals):
        res = super(Timetable, self).write(vals)
        for record in self:
            if 'start_date' in vals or 'end_date' in vals:
                record._generate_schedule_lessons()
        return res

    def _generate_schedule_lessons(self):
        lesson_model = self.env['edu.schedule.lesson']
        # Remove previous lessons of this timetable
        lesson_model.search([('timetable_id', '=', self.id)]).unlink()
        weekdays = self.weekday_ids.mapped('sequence')
        current_date = self.start_date
        while current_date <= self.end_date:
            if current_date.isoweekday() in weekdays:
                lesson_model.create({
                    'timetable_id': self.id,
                    'lesson_date': current_date,
                    'lesson_start_time': self.lesson_start_time,
                    'lesson_end_time': self.lesson_end_time,
                })
            current_date += timedelta(days=1)

    # ------------------ ACTIONS ------------------
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
            'domain': [('timetable_id', '=', self.id)],
            'context': {'default_timetable_id': self.id},
        }
