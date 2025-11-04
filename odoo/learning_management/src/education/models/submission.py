from odoo import models, fields

class EduHomeworkSubmission(models.Model):
    _name = "edu.task.submission"
    _description = "Homework Submission"
    _order = "submit_date desc"

    task_id = fields.Many2one("edu.task", string="Homework", required=True)
    student_id = fields.Many2one("user.student", string="Student", required=True)
    submit_date = fields.Datetime(default=fields.Datetime.now)
    attachment = fields.Binary(string="Attachment")
    file_name = fields.Char(string="Filename")
    note = fields.Text(string="Comment")
    mark = fields.Float(string="Mark", tracking=True)
    feedback = fields.Text(string="Feedback from Teacher")

    state = fields.Selection([
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('returned', 'Returned'),
    ], default="submitted", tracking=True)

    def action_review(self):
        for rec in self:
            rec.state = "reviewed"

    def action_return(self):
        for rec in self:
            rec.state = "returned"
