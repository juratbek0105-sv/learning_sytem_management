from odoo import models, fields, api


class Timetable(models.Model):
     _name = 'edu.timetable'
     _description = 'Timetable'

     name = fields.Char(string="Schedule Name", required=True)
     group_id = fields.Many2one("edu.group")
     date = fields.Datetime(string="Lesson Time")
     topic = fields.Char(string="Topic")



