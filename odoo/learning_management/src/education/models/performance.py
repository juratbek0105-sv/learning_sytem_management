from odoo import models, fields, api


class Performance(models.Model):
    _name = 'edu.performance'
    _description = 'Performance'

    student_id = fields.Many2one("lms.student", string="Student", required=True)

    assignment_id = fields.Many2one("edu.exam", string="Exam", required=True)
    score = fields.Float(string="Score", required=True)
    passed = fields.Boolean(string="Passed", compute="_compute_passed", store=True)

    @api.depends('score', 'exam_id.pass_score')
    def _compute_passed(self):
        for record in self:
            record.passed = record.score >= record.exam_id.pass_score
