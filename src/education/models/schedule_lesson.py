from odoo import models, fields, api, _

class ScheduleLesson(models.Model):
    _name = "edu.schedule.lesson"
    _description = "Schedule Lesson"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "lesson_date asc"

    name = fields.Char(string="Name", required=True, copy=False, readonly=True)
    sequence_number = fields.Integer(string="Lesson Number", readonly=True)
    active = fields.Boolean(default=True)

    timetable_id = fields.Many2one("edu.timetable", string="Timetable", required=True, ondelete="cascade")
    lesson_id = fields.Many2one("edu.lesson", string="Lesson", ondelete="cascade")

    lesson_date = fields.Date(string="Lesson Date", required=True)
    lesson_start_time = fields.Float(string="Start Time", required=True)
    lesson_end_time = fields.Float(string="End Time", required=True)

    teacher_id = fields.Many2one(related="timetable_id.teacher_id", string="Teacher", store=True)
    group_id = fields.Many2one(related="timetable_id.group_id", string="Group", store=True)
    course_id = fields.Many2one(related="timetable_id.course_id", string="Course", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            group_id = vals.get('group_id')
            timetable_id = vals.get('timetable_id')

            # If group not in vals, derive from timetable
            if not group_id and timetable_id:
                timetable = self.env['edu.timetable'].browse(timetable_id)
                group_id = timetable.group_id.id
                vals['group_id'] = group_id

            # Determine the next lesson number for the group
            next_number = 1
            if group_id:
                last_lesson = self.search(
                    [('group_id', '=', group_id)],
                    order='sequence_number desc',
                    limit=1
                )
                if last_lesson:
                    next_number = last_lesson.sequence_number + 1

            vals['sequence_number'] = next_number

            # Fetch group name for naming
            group = self.env['edu.group'].browse(group_id)
            group_name = group.name or 'Group'

            vals['name'] = f"{group_name}-Lesson{next_number}"

        return super(ScheduleLesson, self).create(vals_list)

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
