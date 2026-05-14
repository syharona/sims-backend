from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    bamba_department_id = fields.Many2one(
        "hr.department",
        string="Département",
        help="Département de rattachement de l'utilisateur"
    )