from odoo import models, fields, api


class Schedule(models.Model):
     _name = 'edu.schedule'
     _description = 'Schedule'

     group_id = fields.Many2one("edu.group")
     date = fields.Datetime(string="Lesson Time")
     topic = fields.Char(string="Topic")



