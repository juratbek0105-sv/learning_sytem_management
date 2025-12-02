from datetime import timedelta, datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class ScheduleLesson(models.Model):
    _name = 'edu.schedule.lesson'
    _description = 'Scheduled Lesson'

    name = fields.Char(string="Name", required=True, copy=False, readonly=True)
    sequence = fields.Integer(string="Lesson Number", readonly=True)
    schedule_table_id = fields.Many2one('edu.schedule.table', string='Timetable', required=True, ondelete='cascade')
    date = fields.Date(string='Lesson Date', required=True)
    lesson_start_time = fields.Float(string='Start Time', required=True)
    lesson_end_time = fields.Float(string='End Time', required=True)
    teacher_id = fields.Many2one('res.users', domain=[("user_type", "=", "teacher")], string='Teacher', related='group_id.teacher_id', store=True)
    group_id = fields.Many2one('edu.group', string='Group', related='schedule_table_id.group_id', store=True)
    group_lesson_id = fields.Many2one('edu.group.lesson', string='Group Lesson')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], string='Status', default='draft')
    schedule_student_lesson_ids = fields.One2many('edu.schedule.student.lesson', 'schedule_lesson_id',
                                                  string='Student Lessons')
    schedule_student_lesson_count = fields.Integer(string='Student Lesson Count',
                                                   compute="_compute_schedule_student_lesson_count")

    @api.onchange('lesson_start_time')
    def _onchange_lesson_start_time(self):
        if self.lesson_start_time:
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
            'name': 'Schedule Student Lessons',
            'type': 'ir.actions.act_window',
            'res_model': 'edu.schedule.student.lesson',
            'view_mode': 'list,form',
            'domain': [('schedule_lesson_id', '=', self.id)],
            'context': {'default_schedule_lesson_id': self.id}
        }

    @api.constrains("lesson_start_time", "lesson_end_time", "date", "teacher_id")
    def _check_conflict(self):
        """
        Check if the lesson time conflicts with another lesson for the same teacher on the same date
        """
        for record in self:
            conflicting_lessons = self.env["edu.schedule.lesson"].search([
                ('id', '!=', record.id),  # Exclude current record
                ('date', '=', record.date),
                ('teacher_id', '=', record.teacher_id.id),
                '|',
                '&',
                ('lesson_start_time', '<', record.lesson_start_time),
                ('lesson_end_time', '>', record.lesson_start_time),
                '&',
                ('lesson_start_time', '<', record.lesson_end_time),
                ('lesson_end_time', '>', record.lesson_end_time),
            ])

            if conflicting_lessons:
                raise ValidationError(
                    _("Lesson time conflict detected for teacher %s on %s. "
                      "Conflicting lesson(s): %s") % (
                        record.teacher_id.name,
                        record.date,
                        ', '.join(conflicting_lessons.mapped('name'))
                    )
                )

    def unlink(self):
        lessons_to_delete = self.sorted('sequence')

        for lesson in lessons_to_delete:
            if lesson.date < datetime.today().date():
                raise ValidationError(_("You cannot delete past lessons!"))

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

            # Delete student lessons first (cascade should handle this, but being explicit)
            lesson.schedule_student_lesson_ids.unlink()

            # Delete the lesson
            super(ScheduleLesson, lesson).unlink()

            # Reschedule following lessons
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
        _logger.info("=" * 80)
        _logger.info("STARTING LESSON CREATE METHOD")
        _logger.info(f"Number of lessons to create: {len(vals_list)}")

        # Create the lessons first
        lessons = super().create(vals_list)

        _logger.info(f"✔ Created {len(lessons)} lessons successfully")

        # Collect all student lesson records to create in batch
        all_student_lesson_vals = []

        for lesson in lessons:
            _logger.info("-" * 60)
            _logger.info(f"Processing lesson: ID={lesson.id}, Name={lesson.name}")

            # Check schedule_table_id
            if not lesson.schedule_table_id:
                _logger.warning(f"❌ Lesson {lesson.id} has NO schedule_table_id - skipping")
                continue

            _logger.info(f"  Schedule Table: {lesson.schedule_table_id.name} (ID: {lesson.schedule_table_id.id})")

            # Check group_id
            if not lesson.schedule_table_id.group_id:
                _logger.warning(f"❌ Schedule table {lesson.schedule_table_id.id} has NO group_id - skipping")
                continue

            group = lesson.schedule_table_id.group_id
            _logger.info(f"  Group: {group.name} (ID: {group.id})")

            # Get students
            students = group.student_ids
            _logger.info(f"  Students in group: {len(students)}")

            if not students:
                _logger.warning(f"⚠️ Group '{group.name}' has NO students - skipping")
                continue

            _logger.info(f"  Student names: {', '.join(students.mapped('name'))}")

            # Create student lesson entries
            for student in students:
                student_lesson_vals = {
                    'schedule_lesson_id': lesson.id,
                    'student_id': student.id,
                }
                all_student_lesson_vals.append(student_lesson_vals)
                _logger.info(f"    → Adding student: {student.name} (ID: {student.id})")

        # Create all student lessons in one batch operation
        _logger.info("=" * 80)
        _logger.info(f"TOTAL student lessons to create: {len(all_student_lesson_vals)}")

        if all_student_lesson_vals:
            try:
                created_student_lessons = self.env['edu.schedule.student.lesson'].create(all_student_lesson_vals)
                _logger.info(f"✔✔✔ Successfully created {len(created_student_lessons)} student lesson records")
                _logger.info(f"Student lesson IDs: {created_student_lessons.ids}")
            except Exception as e:
                _logger.error(f"❌❌❌ ERROR creating student lessons: {str(e)}")
                _logger.exception(e)
                raise
        else:
            _logger.warning("⚠️⚠️⚠️ No student lessons to create - check if groups have students!")

        _logger.info("=" * 80)
        return lessons