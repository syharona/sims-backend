# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class BambaProject(models.Model):
    _inherit = 'project.project'

    # Champs spécifiques au Chantier (Conformité 2.1.4)
    
    x_is_chantier = fields.Boolean(
        string="Est un Chantier", 
        default=False,
        help="Cochez pour activer les champs et les règles métier spécifiques aux chantiers."
    )
    
    x_localisation = fields.Char(
        string="Localisation",
        help="Adresse physique ou zone géographique du chantier."
    )
    
    # 1. Suivi Budgétaire (Allocation)
    x_budget_alloue = fields.Monetary(
        string="Budget Alloué",
        currency_field='company_currency_id',
        tracking=True,
        help="Le budget total approuvé pour ce chantier."
    )
    
    # Devise de la compagnie (référence pour les champs Monetary)
    company_currency_id = fields.Many2one(
        'res.currency', 
        related='company_id.currency_id', 
        string="Devise"
    )

    # 2. Suivi des Coûts (Calculé)
    x_depenses_en_cours = fields.Monetary(
        string="Dépenses en Cours",
        compute='_compute_couts_chantier',
        currency_field='company_currency_id',
        store=True,
        help="Total des coûts engagés et enregistrés sur le compte analytique du chantier."
    )

    x_budget_restant = fields.Monetary(
        string="Budget Restant",
        compute='_compute_couts_chantier',
        currency_field='company_currency_id',
        store=True,
        help="Budget Alloué moins les Dépenses en Cours."
    )

    # 3. Logique de Calcul des Coûts
    @api.depends('analytic_account_id.line_ids.amount', 'x_budget_alloue')
    def _compute_couts_chantier(self):
        """ 
        Calcule les dépenses en cours et le budget restant en utilisant
        les lignes du compte analytique lié au projet.
        """
        for project in self:
            total_depenses = 0.0
            
            # Vérification de l'existence d'un compte analytique (crucial)
            if project.analytic_account_id:
                # Les dépenses sont généralement enregistrées comme des montants négatifs
                # sur les lignes analytiques (dépenses, salaires, notes de frais).
                # On somme les montants négatifs et on prend la valeur absolue.
                total_depenses = sum(
                    line.amount for line in project.analytic_account_id.line_ids if line.amount < 0
                )
            
            # Stockage des dépenses (valeur absolue)
            project.x_depenses_en_cours = abs(total_depenses)
            
            # Calcul du budget restant
            project.x_budget_restant = project.x_budget_alloue - project.x_depenses_en_cours

    # 4. Affectation du Chantier (Règle de gestion 3)
    # Le champ 'user_id' (Responsable du projet) est déjà dans le modèle parent.
    # Vous pouvez ajouter ici une contrainte pour garantir qu'il est toujours rempli
    # si le projet est marqué comme un chantier.
    # @api.constrains('user_id', 'x_is_chantier')
    # def _check_project_manager_required(self):
    #     for project in self:
    #         if project.x_is_chantier and not project.user_id:
    #             raise UserError(_("La règle de gestion exige qu'un Chef de Projet soit affecté à chaque Chantier."))

