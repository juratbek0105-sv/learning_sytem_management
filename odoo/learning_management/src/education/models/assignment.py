from odoo import models, fields, api


class Assignment(models.Model):
     _name = 'edu.assignment'
     _description = 'Assignment'

     course_id = fields.Many2one("edu.course")
     group_id = fields.Many2one("edu.group")





