from odoo import models, fields, api


class Timetable(models.Model):
     _name = 'edu.timetable'
     _description = 'Timetable'

     name = fields.Char(string="Schedule Name", required=True)
     group_id = fields.Many2one("edu.group")
     start_time = fields.Float(string="Start Time (hours)")
     end_time = fields.Float(string="End Time (hours)")
     topic = fields.Char(string="Topic")


     weekday = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
     ], string="Weekday", required=True)
