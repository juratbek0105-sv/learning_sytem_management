from datetime import date
from email.policy import default

from odoo import models, fields, api, _


class Group(models.Model):
    _name = 'edu.group'
    _description = 'Student Group / Class'

    name = fields.Char(string='Group Name', required=True, default="New")
    active = fields.Boolean(default=True, string="Active")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('frozen', 'Frozen'),
        ('completed', 'Completed')
    ], default='draft', string="State")

    course_id = fields.Many2one('edu.course', string='Course', required=True)
    teacher_id = fields.Many2one('user.teacher', string='Teacher')
    group_lesson_ids = fields.One2many('edu.group.lesson',"group_id", string='Lessons')
    group_lesson_count = fields.Integer(string="Lessons", compute="_compute_group_lesson_count")
    student_ids = fields.Many2many("edu.group.student", string="Students")
    student_count = fields.Integer(string="Students", compute="_compute_student_count")
    schedule_table_ids = fields.One2many('edu.schedule.table', 'group_id', string=  'Timetables')
    schedule_table_count = fields.Integer(string="Schedule Tables", compute="_compute_schedule_table_count")
    company_id = fields.Many2one("res.company", string="Branch")

    def _compute_group_lesson_count(self):
        for record in self:
            record.group_lesson_count = len(record.group_lesson_ids)

    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids)

    def _compute_schedule_table_count(self):
        for record in self:
            record.schedule_table_count = len(record.schedule_table_ids)

    def action_reset_draft(self):
        self.state = 'draft'

    def action_set_active(self):
        self.state = 'active'

    def action_set_frozen(self):
        self.state = 'frozen'

    def action_set_completed(self):
        self.state = 'completed'

    def action_view_group_lessons(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Group Lessons'),
            'res_model': 'edu.group.lesson',
            'view_mode': 'list,form',
            'domain': [('group_id', '=', self.id)],
        }

    def action_create_schedule_table(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Schedule Table',
            'res_model': 'edu.schedule.table',
            'view_mode': 'form',
            'context': {
                'default_group_id': self.id,
                'default_teacher_id': self.teacher_id.id,
                'default_company_id': self.company_id.id if self.company_id else False,
            },
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            year = vals.get('year', date.today().year)
            self = self.with_context(year=year)

            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('edu.group.sequence')

        groups = super(Group, self).create(vals_list)

        for group in groups:
            group.copy_course_lessons()

        return groups

    def copy_course_lessons(self):
        for group in self:
            if not group.course_id.lesson_ids:
                continue
            lessons_to_add = []
            for lesson in group.course_id.lesson_ids:
                lessons_to_add.append((0, 0, {
                    'name':  lesson.name,
                    'sequence': lesson.sequence,
                    'duration': lesson.duration,
                    'duration_uom': lesson.duration_uom.id if lesson.duration_uom else False,
                    'group_id': group.id,
                    'teacher_id': group.teacher_id.id,
                }))

            group.write({'group_lesson_ids': lessons_to_add})


class GroupLesson(models.Model):
    _name= "edu.group.lesson"

    name = fields.Char(string='Lesson Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    duration = fields.Float(string='Duration')
    duration_uom = fields.Many2one("uom.uom", required=True, domain=[("category_id.name", "=", "Time")])
    teacher_id = fields.Many2one('user.teacher', string='Teacher',
                                 domain=[("teacher_id", "in", "course_id.teacher_ids")])
    task_ids = fields.One2many("edu.task", "lesson_id", string="Tasks")
    group_id = fields.Many2one("edu.group")
    schedule_lesson_id = fields.One2many("edu.schedule.lesson", "group_lesson_id")


class GroupStudent(models.Model):
    _name = "edu.group.student"
    _description = "Group Student"

    group_id = fields.Many2one("edu.group", string="Group", required=True)
    student_id = fields.Many2one("user.student", string="Student", required=True)
    status = fields.Selection([
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("frozen", "Frozen")
    ], string="Status", required=True, default="inactive")
    active = fields.Boolean(default=True)