# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BambaProject(models.Model):
    _inherit = "project.project"

    code = fields.Char(string="Code projet", readonly=True, copy=False)
    description = fields.Text(string="Description détaillée")
    location = fields.Char(string="Localisation")
    department_id = fields.Many2one("hr.department", string="Département")
    project_manager_id = fields.Many2one("res.users", string="Chef de projet", required=True)

    budget_allocated = fields.Monetary(string="Budget alloué", currency_field="currency_id")
    cost_spent = fields.Monetary(string="Dépenses engagées", currency_field="currency_id", compute="_compute_costs", store=True)
    budget_remaining = fields.Monetary(string="Budget restant", currency_field="currency_id", compute="_compute_costs", store=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    date_start_planned = fields.Date(string="Date début prévisionnelle")
    date_end_planned = fields.Date(string="Date fin prévisionnelle")

    state = fields.Selection([
        ("draft", "Brouillon"),
        ("in_progress", "En cours"),
        ("on_hold", "En attente"),
        ("done", "Terminé"),
        ("cancelled", "Annulé"),
    ], string="Statut", default="draft", tracking=True)

    document_ids = fields.One2many("bamba.document", "project_id", string="Documents")

    @api.depends("budget_allocated", "cost_spent")
    def _compute_costs(self):
        for project in self:
            project.budget_remaining = project.budget_allocated - project.cost_spent

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("code") or vals.get("code") == "/":
                vals["code"] = self.env["ir.sequence"].next_by_code("bamba.project") or "/"
        return super().create(vals_list)

    def action_start(self):
        self.write({"state": "in_progress"})

    def action_done(self):
        self.write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    @api.constrains("date_start_planned", "date_end_planned")
    def _check_dates(self):
        for project in self:
            if project.date_start_planned and project.date_end_planned and project.date_end_planned < project.date_start_planned:
                raise ValidationError(_("La date de fin ne peut pas être antérieure à la date de début."))
