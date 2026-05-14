# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class bamba_request(models.Model):
#     _name = 'bamba_request.bamba_request'
#     _description = 'bamba_request.bamba_request'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

