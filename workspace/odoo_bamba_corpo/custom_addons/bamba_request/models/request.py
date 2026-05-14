# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class BambaRequestLine(models.Model):
    """Ligne de produit/service sur une demande."""
    _name = "bamba.request.line"
    _description = "Ligne de demande"
    _order = "sequence, id"

    request_id = fields.Many2one("bamba.request", ondelete="cascade", required=True)
    sequence = fields.Integer(string="N°", default=10)
    description = fields.Char(string="Libellé", required=True)
    supplier_id = fields.Many2one("res.partner", string="Fournisseur",
                                  domain=[("supplier_rank", ">", 0)])
    unit_price = fields.Float(string="Prix unitaire", digits="Product Price")
    quantity = fields.Float(string="Quantité", default=1.0)
    subtotal = fields.Float(string="Sous-total", compute="_compute_subtotal", store=True)

    @api.depends("unit_price", "quantity")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.unit_price * line.quantity


class BambaRequest(models.Model):
    _name = "bamba.request"
    _description = "Demande de validation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(
        string="Numéro", required=True, copy=False,
        readonly=True, default=lambda self: "Nouveau"
    )
    requester_id = fields.Many2one(
        "res.users", string="Demandeur",
        default=lambda self: self.env.user, tracking=True, required=True
    )
    project_id = fields.Many2one("project.project", string="Projet / Chantier", tracking=True)
    department_id = fields.Many2one("hr.department", string="Département")
    urgency = fields.Selection(
        [("1", "Faible"), ("2", "Moyenne"), ("3", "Urgente")],
        default="2", tracking=True
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Compte Analytique"
    )
    project_manager_id = fields.Many2one(
        "res.users", string="Responsable Projet",
        help="L'utilisateur assigné comme responsable du projet",
        tracking=True
    )

    # --- Lignes de produits ---
    line_ids = fields.One2many("bamba.request.line", "request_id", string="Lignes de demande")

    # --- Totaux ---
    total_price = fields.Float(
        string="Prix total", compute="_compute_total", store=True
    )

    # --- Workflow ---
    state = fields.Selection([
        ("draft", "Brouillon"),
        ("to_approve", "En cours de validation"),
        ("approved", "Approuvée"),
        ("rejected", "Rejetée"),
    ], default="draft", tracking=True)

    template_id = fields.Many2one("bamba.request.template", string="Modèle de circuit")
    validation_line_ids = fields.One2many(
        "bamba.request.validation.line", "request_id", string="Circuit de Validation"
    )
    current_validator_id = fields.Many2one(
        "res.users", string="Validateur Actuel",
        compute="_compute_current_validator", store=True
    )

    @api.depends("validation_line_ids.state", "validation_line_ids.sequence")
    def _compute_current_validator(self):
        for rec in self:
            next_line = rec.validation_line_ids.filtered(
                lambda l: l.state == "waiting"
            ).sorted("sequence")[:1]
            rec.current_validator_id = next_line.user_id if next_line else False

    @api.depends("line_ids.subtotal")
    def _compute_total(self):
        for rec in self:
            rec.total_price = sum(rec.line_ids.mapped("subtotal"))

    @api.onchange("template_id")
    def _onchange_template_id(self):
        if self.template_id:
            self.validation_line_ids = [(5, 0, 0)]
            lines = []
            for line in self.template_id.line_ids:
                lines.append((0, 0, {
                    "sequence": line.sequence,
                    "user_id": line.user_id.id,
                    "state": "waiting",
                }))
            self.validation_line_ids = lines

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nouveau") == "Nouveau":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("bamba.request") or "Nouveau"
                )
        return super().create(vals_list)

    def action_submit(self):
        for rec in self:
            if not rec.validation_line_ids:
                raise UserError(_("Veuillez configurer un circuit de validation."))
            rec.state = "to_approve"
            rec._notify_next_validator()

    def action_approve_step(self):
        for rec in self:
            if self.env.user != rec.current_validator_id:
                raise UserError(
                    _("Seul %s peut approuver cette étape.") % rec.current_validator_id.name
                )
            current_line = rec.validation_line_ids.filtered(
                lambda l: l.user_id == self.env.user and l.state == "waiting"
            )[:1]
            current_line.write({"state": "approved", "validation_date": fields.Datetime.now()})
            rec.message_post(body=_("Étape validée par %s") % self.env.user.name)

            if not rec.validation_line_ids.filtered(lambda l: l.state == "waiting"):
                rec.state = "approved"
                rec.message_post(body=_("✅ Demande approuvée. Notification envoyée aux comptables."))
                rec._notify_accounting()
            else:
                rec._notify_next_validator()

    def action_reject(self):
        for rec in self:
            rec.state = "rejected"
            rec.message_post(body=_("❌ Rejetée par %s") % self.env.user.name)

    def _notify_next_validator(self):
        self.ensure_one()
        if self.current_validator_id:
            self.activity_schedule(
                "bamba_request.activity_bamba_request_validation",
                user_id=self.current_validator_id.id,
                summary=_("Validation requise : %s") % self.name,
            )

    def _notify_accounting(self):
        group_finance = self.env.ref("bamba_base.group_bamba_finance")
        for user in group_finance.users:
            self.activity_schedule(
                "mail.mail_activity_data_todo",
                user_id=user.id,
                summary=_("💰 DÉCAISSEMENT : %s") % self.name,
                note=_("Demande validée. Prête pour paiement."),
            )


class BambaRequestValidationLine(models.Model):
    _name = "bamba.request.validation.line"
    _description = "Ligne de validation"
    _order = "sequence, id"

    request_id = fields.Many2one("bamba.request", ondelete="cascade")
    sequence = fields.Integer(string="Ordre", default=10)
    user_id = fields.Many2one("res.users", string="Validateur", required=True)
    state = fields.Selection(
        [("waiting", "En attente"), ("approved", "Validé")], default="waiting"
    )
    validation_date = fields.Datetime("Date de validation", readonly=True)


class BambaRequestTemplate(models.Model):
    _name = "bamba.request.template"
    _description = "Modèle de circuit de validation"

    name = fields.Char(string="Nom du modèle", required=True)
    line_ids = fields.One2many(
        "bamba.request.template.line", "template_id", string="Étapes", copy=True
    )


class BambaRequestTemplateLine(models.Model):
    _name = "bamba.request.template.line"
    _description = "Ligne de modèle de validation"
    _order = "sequence"

    template_id = fields.Many2one("bamba.request.template")
    sequence = fields.Integer(string="Ordre", default=10)
    user_id = fields.Many2one("res.users", string="Validateur", required=True)
