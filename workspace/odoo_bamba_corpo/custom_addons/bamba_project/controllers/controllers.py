# -*- coding: utf-8 -*-
# from odoo import http


# class BambaProject(http.Controller):
#     @http.route('/bamba_project/bamba_project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bamba_project/bamba_project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bamba_project.listing', {
#             'root': '/bamba_project/bamba_project',
#             'objects': http.request.env['bamba_project.bamba_project'].search([]),
#         })

#     @http.route('/bamba_project/bamba_project/objects/<model("bamba_project.bamba_project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bamba_project.object', {
#             'object': obj
#         })

