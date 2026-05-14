from odoo import models, fields


class BambaProjectCost(models.Model):
    _name = "bamba.project.cost"
    _description = "Coûts du projet"

    project_id = fields.Many2one("project.project", required=True)
    description = fields.Char(required=True)
    amount = fields.Float(required=True)
    date = fields.Date(default=fields.Date.today)
    employee_id = fields.Many2one("hr.employee", string="Responsable")