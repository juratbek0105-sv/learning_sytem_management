from odoo import models, fields, api, _
from datetime import timedelta, datetime, time
from odoo.exceptions import UserError

from odoo.odoo.exceptions import ValidationError


class LessonDateWizard(models.TransientModel):
    _name = 'edu.lesson.date.wizard'
    _description = 'Change Lesson Date Wizard'

    schedule_lesson_id = fields.Many2one('edu.schedule.lesson', string='Lesson', required=True)
    option = fields.Selection([
        ('manual', 'Select Specific Date'),
        ('auto', 'Set Date After Last Lesson'),
        ('skip', 'Skip the lesson')
    ], string='Change Option', required=True, default='manual')

    lesson_start_time = fields.Float(string='Start Time')
    lesson_end_time = fields.Float(string='End Time')
    new_date = fields.Date(string='New Lesson Date')

    @api.onchange('lesson_start_time')
    def _onchange_lesson_start_time(self):
        if self.lesson_start_time and self.schedule_lesson_id:
            duration = self.schedule_lesson_id.group_id.course_id.duration
            self.lesson_end_time = self.lesson_start_time + duration

    def reschedule_lessons(self, start_from_lesson):
        schedule_table = start_from_lesson.schedule_table_id
        weekdays = schedule_table.weekday_ids.mapped('sequence')
        if not weekdays:
            raise UserError(_("No weekdays defined in timetable."))

        lessons = self.env['edu.schedule.lesson'].search(
            [('schedule_table_id', '=', schedule_table.id)],
            order='sequence asc'
        )

        index = lessons.ids.index(start_from_lesson.id)
        lessons_to_reschedule = lessons[index:]

        previous_date = start_from_lesson.date

        if previous_date <  datetime.today().date():
            raise ValidationError("You can not do operations on past lessons!")

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


    def action_apply_change(self):
        self.ensure_one()
        lesson = self.schedule_lesson_id
        old_date = lesson.date
        old_start = lesson.lesson_start_time
        old_end = lesson.lesson_end_time

        if self.option == 'manual':
            if not self.new_date or self.lesson_start_time is None or self.lesson_end_time is None:
                raise UserError(_("Please set a new date, start time and end time for manual option."))

            if self.lesson_start_time >= self.lesson_end_time:
                raise UserError(_("Start time must be before end time."))

            if lesson.date < datetime.today().date():
                raise ValidationError("You can not do operations on past lessons!")

            lesson.write({
                'date': self.new_date,
                'lesson_start_time': self.lesson_start_time,
                'lesson_end_time': self.lesson_end_time
            })

            try:
                lesson._check_conflict()
            except ValueError as e:
                raise UserError(_("Lesson conflict detected: %s") % e)

            if self.new_date > old_date:
                schedule_table = lesson.schedule_table_id
                weekdays = schedule_table.weekday_ids.mapped('sequence')
                if not weekdays:
                    raise UserError(_("No weekdays defined in timetable."))

                lessons = self.env['edu.schedule.lesson'].search(
                    [('schedule_table_id', '=', schedule_table.id)],
                    order='sequence asc'
                )

                index = lessons.ids.index(lesson.id)
                lessons_to_reschedule = lessons[index + 1:]

                previous_date = lesson.date

                for l in lessons_to_reschedule:
                    next_date = previous_date
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
            return


        elif self.option == 'auto':
            schedule_table = lesson.schedule_table_id
            last_lesson = self.env['edu.schedule.lesson'].search(
                [('schedule_table_id', '=', schedule_table.id)],
                order='date desc', limit=1
            )
            if not last_lesson:
                raise UserError(_("No previous lessons found."))
            if last_lesson.date < datetime.today().date():
                raise ValidationError("You can not do operations on past lessons!")

            weekdays = schedule_table.weekday_ids.mapped('sequence')
            next_date = last_lesson.date + timedelta(days=1)
            for _ in range(7):
                if next_date.isoweekday() in weekdays:
                    break
                next_date += timedelta(days=1)

            lesson.with_context(skip_reschedule=True).write({'date': next_date})
            try:
                lesson._check_conflict()
            except ValueError as e:
                raise UserError(_("Lesson conflict detected: %s") % e)

        elif self.option == 'skip':
            schedule_table = lesson.schedule_table_id
            weekdays = schedule_table.weekday_ids.mapped('sequence')
            if not weekdays:
                raise UserError(_("No weekdays defined in timetable."))
            lessons = self.env['edu.schedule.lesson'].search(
                [('schedule_table_id', '=', schedule_table.id)],
                order='sequence asc')

            index = lessons.ids.index(lesson.id)

            if index > 0:
                start_from_lesson = lessons[index - 1]
            else:
                start_from_lesson = lesson

            self.reschedule_lessons(start_from_lesson=start_from_lesson)

        else:
                    raise UserError(_("Unknown option selected"))

        return {'type': 'ir.actions.act_window_close'}
