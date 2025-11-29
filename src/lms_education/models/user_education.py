from odoo import models, fields, api



class User(models.Model):
    _inherit = "res.users"

    group_ids = fields.Many2many("edu.group")
    course_ids = fields.Many2many("edu.course")

