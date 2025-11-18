# -*- coding: utf-8 -*-
# from odoo import http


# class Control(http.Controller):
#     @http.route('/control/control', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/control/control/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('control.listing', {
#             'root': '/control/control',
#             'objects': http.request.env['control.control'].search([]),
#         })

#     @http.route('/control/control/objects/<model("control.control"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('control.object', {
#             'object': obj
#         })

