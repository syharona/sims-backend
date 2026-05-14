# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class bamba_request_project_link(models.Model):
#     _name = 'bamba_request_project_link.bamba_request_project_link'
#     _description = 'bamba_request_project_link.bamba_request_project_link'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

