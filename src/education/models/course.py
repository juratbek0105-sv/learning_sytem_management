from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EduCourse(models.Model):
    _name = 'edu.course'
    _description = 'Course / Program'

    name = fields.Char(string='Course Name', required=True)
    price = fields.Float(string="Price per month")

    total_lessons = fields.Integer(string='Total Lessons', required=True)
    duration = fields.Float(string='Lesson Duration')
    duration_uom = fields.Many2one("uom.uom", domain=[("category_id.name", "=", "Time")])

    course_lesson_ids = fields.One2many('edu.course.lesson', 'course_id', string="Default Lessons")

    lesson_ids = fields.One2many('edu.lesson', 'course_id', string='Lessons / Topics')
    group_ids = fields.One2many('edu.group', 'course_id', string='Groups')
    teacher_ids = fields.Many2many("user.teacher", string="Teachers")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed')
    ], default='draft', string="State")
    active = fields.Boolean(string="Active", default=True)

    def action_open_course(self):
        self.state = "open"

    def action_close_course(self):
        self.state = "closed"

    def action_reset_draft_course(self):
        self.state = "draft"

    def action_create_group(self):
        self.ensure_one()
        if self.state == "open":
            return {
                "type": "ir.actions.act_window",
                "res_model": "edu.group",
                "view_mode": "form",
                "view_id": self.env.ref("education.view_group_form").id,
                "target": "current",
                "context": {
                    "default_course_id": self.id,
                }
            }
        else:
            raise ValidationError("For create group, open the course first, please")

    @api.model_create_multi
    def create(self, vals_list):
        courses = super().create(vals_list)
        courses.create_default_lessons()
        return courses

    def create_default_lessons(self):
        for course in self:
            if course.course_lesson_ids or not course.total_lessons:
                continue

            lines = []
            for i in range(1, course.total_lessons + 1):
                lines.append((0, 0, {
                    'name': f"{course.name} Lesson {i}",
                    'sequence': i,
                    'duration': course.duration,
                    'duration_uom': course.duration_uom.id,
                }))
            course.course_lesson_ids = lines


class EduCourseLesson(models.Model):
    _name = 'edu.course.lesson'
    _description = 'Course Default Lesson'
    _order = 'sequence asc'

    name = fields.Char(string="Lesson Name", required=True)
    sequence = fields.Integer(string="Sequence")
    duration = fields.Float(string="Duration")
    duration_uom = fields.Many2one("uom.uom", string="Duration UoM")

    course_id = fields.Many2one('edu.course', string="Course", required=True)
