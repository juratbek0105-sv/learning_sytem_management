from odoo import models, fields, api


class WorkHours(models.Model):
     _name = 'control.work.hours'
     _description = 'Work Hours'

     employee_id = fields.Many2one("res.users", required=True)
     date = fields.Date(default=fields.Date.today)
     start_time = fields.Datetime(string="Start Time")
     end_time = fields.Datetime(string="End Time")
     total_hours = fields.Float(compute="_compute_total_hours", store=True)
     status = fields.Selection([
         ("working", "Working"),
         ("completed", "Completed"),
         ("absent", "Absent"),
     ], string="Status", default="working")

     @api.depends("start_time", "end_time")
     def _compute_total_hours(self):
         for rec in self:
             if rec.start_time and rec.end_time:
                 rec.total_hours = (rec.end_time - rec.start_time).total_seconds() / 3600
             else:
                 rec.total_hours = 0




