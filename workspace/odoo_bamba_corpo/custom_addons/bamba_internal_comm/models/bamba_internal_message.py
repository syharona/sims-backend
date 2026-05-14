from odoo import models, fields, api


class BambaInternalMessage(models.Model):
    _name = "bamba.internal.message"
    _description = "Message interne"
    _order = "create_date desc"

    name = fields.Char(
        string="Sujet",
        required=True
    )

    body = fields.Text(
        string="Message",
        required=True
    )

    message_type = fields.Selection([
        ('internal', 'Interne'),
        ('user_notification', 'Notification'),
    ], string="Type", default='internal')

    author_id = fields.Many2one(
        "res.users",
        string="Auteur",
        default=lambda self: self.env.user,
        readonly=True
    )

    request_id = fields.Many2one(
        "bamba.request",
        string="Demande liée",
        ondelete="cascade"
    )

    project_id = fields.Many2one(
        "project.project",
        string="Projet lié",
        ondelete="cascade"
    )

    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("sent", "Envoyé"),
            ("archived", "Archivé"),
        ],
        default="draft",
        string="Statut"
    )

    active = fields.Boolean(default=True)

    # --- Actions workflow ---
    def action_send(self):
        self.write({"state": "sent"})

    def action_archive(self):
        self.write({
            "state": "archived",
            "active": False
        })
