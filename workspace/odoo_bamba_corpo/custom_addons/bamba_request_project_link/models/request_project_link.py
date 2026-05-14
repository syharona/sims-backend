# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BambaRequest(models.Model):
    _inherit = "bamba.request"

    project_id = fields.Many2one(
        "project.project",
        string="Projet / Chantier lié",
        readonly=True,
        copy=False
    )

    project_count = fields.Integer(
        compute="_compute_project_count"
    )

    # ======================================================
    # COMPUTE
    # ======================================================

    def _compute_project_count(self):
        for req in self:
            req.project_count = 1 if req.project_id else 0

    # ======================================================
    # ACTION : CRÉER PROJET
    # ======================================================

    def action_create_project(self):
        self.ensure_one()

        if self.state != "approved":
            raise ValidationError(
                _("Seules les demandes validées peuvent créer un projet.")
            )

        if self.project_id:
            raise ValidationError(
                _("Un projet est déjà lié à cette demande.")
            )

        # On définit le responsable : soit celui choisi, soit le demandeur par défaut
        pm_id = self.project_manager_id.id or self.requester_id.id

        project = self.env["project.project"].sudo().create({
            "name": self.description or self.name,
            "project_manager_id": pm_id,  # CORRECTION ICI
            "budget_allocated": self.total_price,
            "department_id": self.department_id.id,
            "date_start_planned": fields.Date.today(),
            "description": self.description,
        })

        self.project_id = project.id
        self.message_post(body=_("📁 Projet <b>%s</b> créé.") % project.name)
        
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "view_mode": "form",
            "res_id": project.id,
            "target": "current",
        }

    
    # ======================================================
    # ACTION DU SMART BUTTON (NAVIGATION)
    # ======================================================

    def action_view_project(self):
        """ Ouvre la vue formulaire du projet lié """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "res_id": self.project_id.id,
            "view_mode": "form",
            "target": "current",
        }
