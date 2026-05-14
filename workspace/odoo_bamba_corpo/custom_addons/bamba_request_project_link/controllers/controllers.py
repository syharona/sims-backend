# -*- coding: utf-8 -*-
# from odoo import http


# class BambaRequestProjectLink(http.Controller):
#     @http.route('/bamba_request_project_link/bamba_request_project_link', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bamba_request_project_link/bamba_request_project_link/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bamba_request_project_link.listing', {
#             'root': '/bamba_request_project_link/bamba_request_project_link',
#             'objects': http.request.env['bamba_request_project_link.bamba_request_project_link'].search([]),
#         })

#     @http.route('/bamba_request_project_link/bamba_request_project_link/objects/<model("bamba_request_project_link.bamba_request_project_link"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bamba_request_project_link.object', {
#             'object': obj
#         })

