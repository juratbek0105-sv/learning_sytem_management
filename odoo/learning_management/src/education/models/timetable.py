from odoo import models, fields, api


class Timetable(models.Model):
     _name = 'edu.timetable'
     _description = 'Timetable'
     _inherit = ['mail.thread', 'mail.activity.mixin']

     name = fields.Char(string="Schedule Name", required=True, tracking=True)
     start_time = fields.Float(string="Start Time (hours)")
     end_time = fields.Float(string="End Time (hours)")
     duration = fields.Float(string="Duration (hours)", compute="_compute_duration", store=True)
     topic = fields.Char(string="Topic")


     group_id = fields.Many2one("edu.group")



     weekday = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
     ], string="Weekday", required=True)

     @api.depends('start_time', 'end_time')
     def _compute_duration(self):
         for record in self:
             record.duration = max(record.end_time - record.start_time, 0.0)
