from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AssignmentResult(models.Model):
    _name = 'edu.result'
    _description = 'AssignmentResult'

    student_id = fields.Many2one("user.student", string="Student", required=True)
    assignment_id = fields.Many2one("edu.assignment")
    submission_file = fields.Binary(string="Submission File")
    submit_date = fields.Datetime(string="Submitted On")


    score = fields.Float(string="Score", required=True)
    passed = fields.Boolean(string="Passed", compute="_compute_passed", store=True)
    teacher_feedback = fields.Text(string="Teacher Feedback")
    graded_date = fields.Datetime(string="Graded On")

    state = fields.Selection([
        ('draft', 'Pending Submission'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ], default='draft')


    @api.depends('score', 'assignment_id.pass_score')
    def _compute_passed(self):
        for record in self:
            record.passed = bool(record.assignment_id and record.score >= record.assignment_id.pass_score)

    def action_submit(self):
        for record in self:
            if not record.submission_file:
                raise ValidationError(_("You must upload your submission file before submitting."))
            record.submit_date = fields.Datetime.now()
            record.state = 'submitted'

    def action_grade(self):
        for record in self:
            if record.score < 0 or record.score > record.assignment_id.max_score:
                raise ValidationError(_("Score must be between 0 and the maximum score."))
            record.graded_date = fields.Datetime.now()
            record.state = 'graded'