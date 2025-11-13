from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError


class LessonDateWizard(models.TransientModel):
    _name = 'edu.lesson.date.wizard'
    _description = 'Change Lesson Date Wizard'

    lesson_id = fields.Many2one('edu.schedule.lesson', string='Lesson', required=True)
    option = fields.Selection([
        ('manual', 'Select Specific Date'),
        ('auto', 'Set Date After Last Lesson'),
    ], string='Change Option', required=True, default='manual')

    new_date = fields.Date(string='New Lesson Date')

    def action_apply_change(self):
        self.ensure_one()
        lesson = self.lesson_id

        if self.option == 'manual':
            if not self.new_date:
                raise UserError(_("Please select a new date."))
            lesson.lesson_date = self.new_date

        elif self.option == 'auto':
            # get all lessons of the timetable
            timetable = lesson.timetable_id
            lessons = self.env['edu.schedule.lesson'].search([
                ('timetable_id', '=', timetable.id)
            ], order='lesson_date desc')

            if not lessons:
                raise UserError(_("No previous lessons found in this timetable."))

            last_lesson_date = lessons[0].lesson_date
            weekdays = timetable.weekday_ids.mapped('sequence')  # e.g., 1=Mon, 2=Tue, ...

            # find the next date after last lesson that matches timetable weekdays
            next_date = last_lesson_date + timedelta(days=1)
            while next_date.isoweekday() not in weekdays:
                next_date += timedelta(days=1)

            lesson.lesson_date = next_date

        return {'type': 'ir.actions.act_window_close'}
