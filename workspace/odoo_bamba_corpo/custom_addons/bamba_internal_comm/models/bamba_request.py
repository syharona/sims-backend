from odoo import models, fields


class BambaRequest(models.Model):
    _inherit = "bamba.request"

    message_ids = fields.One2many(
        "bamba.internal.message",
        "request_id",
        string="Communications internes"
    )
