# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Seuil de Validation du Manager
    manager_approval_threshold = fields.Float(
        string="Seuil de Validation Manager",
        config_parameter='bamba_corporation_custom.manager_approval_threshold',
        default=1000.0, # Valeur par défaut si rien n'est configuré
        help="Montant (en devise de la compagnie) au-delà duquel une demande de validation nécessite l'approbation du Manager (Niveau 2)."
    )

    # Note: Si vous aviez plusieurs paramètres, vous les ajouteriez ici.
    
    # Exemple de paramètre lié à l'affichage (ne sera pas sauvegardé dans ir.config_parameter)
    # group_analytic_validation_required = fields.Boolean(
    #     string="Validation Analytique Obligatoire",
    #     implied_group='analytic.group_analytic_user',
    # )

