# -*- coding: utf-8 -*-
from odoo import models, fields

class BambaPartner(models.Model):
    _name = "bamba.partner"
    _description = "Bamba Partner"
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Pour messagerie interne et log

    name = fields.Char(string="Nom du client", required=True, tracking=True)
    phone = fields.Char(string="Téléphone")
    email = fields.Char(string="Email")
    crm_id = fields.Many2one("res.partner", string="Client lié")
    client_type = fields.Selection([('pro','Professionnel'),('part','Particulier')], string="Type de client")
    segment = fields.Selection([('vip','VIP'),('standard','Standard')], string="Segment client")