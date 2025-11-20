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

                try:
                    l._check_conflict()
                except ValueError as e:
                    raise UserError(_("Conflict for lesson %s: %s") % (l.name, e))

                previous_date = next_date

        return True
