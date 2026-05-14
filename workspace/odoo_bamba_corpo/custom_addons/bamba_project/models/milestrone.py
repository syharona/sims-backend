from odoo import models, fields


class BambaProjectMilestone(models.Model):
    _name = "bamba.project.milestone"
    _description = "Jalon de projet"
    _inherit = ["mail.thread"]

    name = fields.Char(required=True)
    project_id = fields.Many2one("project.project", required=True)
    date_planned = fields.Date(required=True)
    date_done = fields.Date()
    state = fields.Selection(
        [
            ("pending", "À faire"),
            ("done", "Terminé"),
        ],
        default="pending",
        tracking=True
    )