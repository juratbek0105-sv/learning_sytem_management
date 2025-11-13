from datetime import date
from odoo import models, fields, api


class Group(models.Model):
    _name = 'edu.group'
    _description = 'Group'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, string="Name", tracking=True)
    active = fields.Boolean(default=True, string="Active")
    state = fields.Selection([
        ('active', 'Active'),
        ('frozen', 'Frozen'),
        ('completed', 'Completed')
    ], default='active', string="State")

    course_id = fields.Many2one("edu.course")
    student_ids = fields.Many2many("user.student", string="Students")
    teacher_ids = fields.Many2many("user.teacher")
    timetable_id = fields.One2many("edu.timetable", "group_id", string="Timetable")
    lesson_ids = fields.One2many("edu.lesson", "group_id")
    company_id = fields.Many2one('res.company', string="Branch", default=lambda self: self.env.company)

    # Optional: store the year if you want to use it in naming
    year = fields.Integer(default=lambda self: date.today().year, string="Year")

    def action_toggle_group(self):
        for record in self:
            record.active = not record.active

    def action_create_timetable(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Timetable',
            'res_model': 'edu.timetable',
            'view_mode': 'form',
            'context': {
                'default_group_id': self.id,
                'default_course_id': self.course_id.id if self.course_id else False,
                'default_teacher_ids': self.teacher_ids.ids,
                'default_company_id': self.company_id.id if self.company_id else False,
            },
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['active'] = True
            if 'course_id' in vals:
                course = self.env['edu.course'].browse(vals['course_id'])
                year = vals.get('year', date.today().year)

                existing_groups = self.search([
                    ('course_id', '=', course.id),
                    ('year', '=', year)
                ], order='id asc')

                sequence = 1
                if existing_groups:
                    last_group = existing_groups[-1]
                    try:
                        sequence = int(last_group.name.split('-')[-1]) + 1
                    except:
                        sequence = len(existing_groups) + 1

                vals['name'] = f"{course.name}{year}-{sequence}"

        return super(Group, self).create(vals_list)
