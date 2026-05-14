# -*- coding: utf-8 -*-
# from odoo import http


# class BambaRequest(http.Controller):
#     @http.route('/bamba_request/bamba_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bamba_request/bamba_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bamba_request.listing', {
#             'root': '/bamba_request/bamba_request',
#             'objects': http.request.env['bamba_request.bamba_request'].search([]),
#         })

#     @http.route('/bamba_request/bamba_request/objects/<model("bamba_request.bamba_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bamba_request.object', {
#             'object': obj
#         })

