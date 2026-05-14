# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class BambaDocument(models.Model):
    _name = "bamba.document"
    _description = "Document Bamba"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    # ======================================================
    # IDENTITÉ DU DOCUMENT
    # ======================================================

    name = fields.Char(
        string="Nom du document",
        required=True,
        tracking=True
    )

    document_type = fields.Selection(
        [
            ("plan", "Plan"),
            ("photo", "Photo chantier"),
            ("devis", "Devis"),
            ("rapport", "Rapport"),
            ("pv", "Procès-verbal"),
            ("autre", "Autre"),
        ],
        string="Type de document",
        required=True,
        tracking=True
    )

    description = fields.Text(string="Description")

    # ======================================================
    # FICHIER
    # ======================================================

    file = fields.Binary(
        string="Fichier",
        required=True,
        attachment=True,
        tracking=True
    )

    filename = fields.Char(string="Nom du fichier")

    # ======================================================
    # LIENS MÉTIERS
    # ======================================================

    request_id = fields.Many2one(
        "bamba.request",
        string="Demande associée",
        ondelete="cascade",
        index=True
    )

    project_id = fields.Many2one(
        "project.project",
        string="Projet / Chantier",
        ondelete="cascade",
        index=True
    )
    


    # ======================================================
    # GESTION & TRAÇABILITÉ
    # ======================================================

    uploaded_by = fields.Many2one(
        "res.users",
        string="Ajouté par",
        default=lambda self: self.env.user,
        readonly=True
    )

    upload_date = fields.Datetime(
        string="Date d’ajout",
        default=fields.Datetime.now,
        readonly=True
    )

    is_confidential = fields.Boolean(
        string="Document confidentiel",
        tracking=True
    )

    active = fields.Boolean(
        default=True
    )

    # ======================================================
    # CONTRAINTES MÉTIER
    # ======================================================

    @api.constrains("request_id", "project_id")
    def _check_linked_object(self):
        """
        Un document DOIT être lié soit :
        - à une demande
        - à un projet / chantier
        """
        for doc in self:
            if not doc.request_id and not doc.project_id:
                raise UserError(
                    _("Un document doit être rattaché à une demande ou à un projet.")
                )

    # ======================================================
    # HOOKS & NOTIFICATIONS
    # ======================================================

    @api.model_create_multi
    def create(self, vals_list):
        documents = super().create(vals_list)

        for doc in documents:
            target = doc.request_id or doc.project_id
            if target:
                target.message_post(
                    body=_(
                        "📎 Un nouveau document a été ajouté : <b>%s</b> (%s)"
                    ) % (doc.name, doc.document_type)
                )

        return documents

class ProjectInherit(models.Model):
    _inherit = "project.project"

    bamba_document_ids = fields.One2many(
        "bamba.document", 
        "project_id", 
        string="Documents Bamba"
    )

class RequestInherit(models.Model):
    _inherit = "bamba.request"

    # C'est ce champ qui manque à Odoo pour valider le XML
    document_ids = fields.One2many(
        "bamba.document",
        "request_id",
        string="Documents"
    )

