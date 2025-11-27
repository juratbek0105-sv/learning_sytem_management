from datetime import timedelta, datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

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
    group_lesson_id = fields.Many2one('edu.group.lesson', string='Group Lesson')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], string='Status', default='draft')
    schedule_student_lesson_ids = fields.One2many('edu.schedule.student.lesson', 'schedule_lesson_id')
    schedule_student_lesson_count = fields.Integer(compute="_compute_schedule_student_lesson_count")

    @api.onchange('lesson_start_time')
    def _onchange_lesson_start_time(self):
        if self.lesson_start_time :
            duration = self.group_id.course_id.duration
            self.lesson_end_time = self.lesson_start_time + duration

    @api.depends('schedule_student_lesson_ids')
    def _compute_schedule_student_lesson_count(self):
        for record in self:
            record.schedule_student_lesson_count = len(record.schedule_student_lesson_ids)

    def action_mark_done(self):
        self.state = "done"

    def action_reset_draft(self):
        self.state = "draft"

    def action_change_lesson_date(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Change Lesson Date'),
            'res_model': 'edu.lesson.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_schedule_lesson_id': self.id,
                'default_new_date': self.date
            },
        }

    def action_view_schedule_student_lessons(self):
        self.ensure_one()
        return {
            'name': 'Schedule student lessons',
            'type': 'ir.actions.act_window',
            'res_model': 'edu.schedule.student.lesson',
            'view_mode': 'list,form',
            'domain': [('schedule_lesson_id', '=', self.id)],
        }


    @api.constrains("lesson_start_time", "lesson_end_time", "date", "teacher_id")
    def _check_conflict(self):
        """
        Joriy dars kuni joriy o'qituvchiga dars vaqti konflikt bo'lib qolmasligi tekshirildi
        """
        for record in self:
            if self.env["edu.schedule.lesson"].sudo().search_count([
                "&",
                ("date", "=", record.date),
                "&",
                ("teacher_id", "=", record.teacher_id.id),
                "|",
                "&",
                ("lesson_start_time", "<", record.lesson_start_time),
                ("lesson_end_time", ">", record.lesson_start_time),
                "&",
                ("lesson_start_time", "<", record.lesson_end_time),
                ("lesson_end_time", ">", record.lesson_end_time),
            ]) > 0:
                raise ValueError("Lesson Conflict")

    def unlink(self):
        lessons_to_delete = self.sorted('sequence')
        if self.date <  datetime.today().date():
            raise ValidationError("You can not do operations on past lessons!")
        for lesson in lessons_to_delete:
            schedule_table = lesson.schedule_table_id
            weekdays = schedule_table.weekday_ids.mapped('sequence')
            if not weekdays:
                raise UserError(_("No weekdays defined in timetable."))

            all_lessons = self.env['edu.schedule.lesson'].search(
                [('schedule_table_id', '=', schedule_table.id)],
                order='sequence asc'
            )

            index = all_lessons.ids.index(lesson.id)
            lessons_to_reschedule = all_lessons[index + 1:]

            previous_date = lesson.date
            super(ScheduleLesson, lesson).unlink()


            for l in lessons_to_reschedule:
                next_date = previous_date + timedelta(days=1)
                for _ in range(7):
                    if next_date.isoweekday() in weekdays:
                        break
                    next_date += timedelta(days=1)

                l.write({'date': next_date})


                previous_date = next_date

        return True

    @api.model_create_multi
    def create(self, vals_list):
        lessons= super().create(vals_list)

        for lesson in lessons:
            students = lesson.group_id.student_ids
            if not students:
                continue

            student_lesson_vals = []
            for student in students:
                student_lesson_vals.append({
                    'schedule_lesson_id': lesson.id,
                    'student_id': student.id,
                })
            self.env['edu.schedule.student.lesson'].create(student_lesson_vals)
        return lessons
