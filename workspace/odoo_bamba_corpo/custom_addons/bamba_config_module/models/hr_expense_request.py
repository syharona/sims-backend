# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError

class BambaExpenseRequest(models.Model):
    _inherit = 'hr.expense'
    
    # Ajout du nouveau statut 'Validé Chef de Projet' pour le workflow
    state = fields.Selection(
        selection_add=[
            ('validated_chef_projet', 'Validé Chef de Projet'),
        ],
        ondelete={'validated_chef_projet': 'set default'},
    )

    # ===============================================
    # 1. Champs du Cahier des Charges
    # ===============================================
    
    # Numérotation (correspond à 'Numéro de la demande')
    x_numero_demande = fields.Char(
        string="Numéro de la Demande",
        readonly=True, 
        copy=False,
        default=lambda self: _('Nouveau')
    )
    
    # Type et Catégorie de la Demande
    x_demande_category_id = fields.Many2one(
        'hr.expense.category', # Utilise le modèle standard des catégories de frais
        string="Type et Catégorie",
        required=True
    )
    
    # Fournisseur
    x_fournisseur_id = fields.Many2one(
        'res.partner', 
        string="Fournisseur",
        domain=[('supplier_rank', '>', 0)]
    )
    
    # Imputation Budgétaire (Chantier)
    x_imputation_budgetaire_id = fields.Many2one(
        'account.analytic.account', 
        string="Imputation Budgétaire (Chantier)",
        required=True,
        help="Lien vers le compte analytique du chantier ou du département."
    )
    
    # Niveau d'Urgence
    x_niveau_urgence = fields.Selection([
        ('bas', 'Bas'),
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
    ], string="Niveau d'Urgence", default='normal')
    
    # Département (lecture seule)
    x_departement_id = fields.Many2one(
        'hr.department', 
        string="Département du Demandeur",
        related='employee_id.department_id',
        store=True,
        readonly=True
    )
    
    # Le champ 'unit_amount' du modèle hr.expense correspond au Prix Unitaire
    # Le champ 'quantity' correspond à la Quantité
    # Le champ 'amount' correspond au Montant total à décaisser (calculé)
    
    # ===============================================
    # 2. Logique de Séquence (Numérotation)
    # ===============================================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('x_numero_demande', _('Nouveau')) == _('Nouveau'):
                # Assurez-vous que la séquence 'demande.validation.sequence' existe dans data/bamba_sequences.xml
                vals['x_numero_demande'] = self.env['ir.sequence'].next_by_code('demande.validation.sequence') or _('Nouveau')
        return super().create(vals_list)

    # ===============================================
    # 3. Logique de Workflow (Validation à 2 Niveaux)
    # ===============================================
    
    # Récupération du seuil (doit être implémenté via res.config.settings)
        @api.model
    def _get_manager_approval_threshold(self):
        """ Récupère le seuil de validation du Manager depuis les paramètres globaux. """
        # Clé définie dans res_config_settings.py
        seuil = self.env['ir.config_parameter'].sudo().get_param(
            'bamba_corporation_custom.manager_approval_threshold', 
            default=1000.0 # Seuil par défaut si le paramètre n'existe pas encore
        )
        # Convertir en float car get_param renvoie une chaîne de caractères
        return float(seuil) 


    def action_validate_chef_projet(self):
        """ 
        Validation Niveau 1.
        Décide si la validation s'arrête ici ou passe au Manager.
        """
        self.ensure_one()
        # Sécurité vérifiée via le groupe 'group_bamba_chef_projet' dans le XML
        
        seuil = self._get_manager_approval_threshold()

        if self.amount > seuil: 
            # Dépassement du seuil -> Validation Manager requise
            self.write({'state': 'validated_chef_projet'}) 
            
            # Notification (Chatter)
            self.message_post(body=_("Validé par le Chef de Projet. **En attente de validation du Manager** (Montant de %.2f supérieur au seuil de %.2f).") % (self.amount, seuil))
        else:
            # Sous le seuil -> Validation Finale par le Chef de Projet
            # Utilise la fonction de validation finale du modèle parent (hr.expense)
            self.action_done() 
            
            # Notification (Chatter)
            self.message_post(body=_("Validé par le Chef de Projet (Validation Finale). Montant total: %.2f.") % self.amount)

    def action_validate_manager(self):
        """ Validation Niveau 2 (Manager). """
        self.ensure_one()
        # Sécurité vérifiée via le groupe 'group_bamba_manager' dans le XML
        
        if self.state not in ['submit', 'validated_chef_projet']:
             raise UserError(_("La demande n'est pas dans un état en attente de validation Manager."))

        # Utilise la fonction de validation finale du modèle parent (hr.expense)
        self.action_done() 
        self.message_post(body=_("Validé par le Manager (Validation Finale). La demande est complète."))

    def action_refuse(self):
        """ Réutilisation de la fonction de refus du modèle parent. """
        self.ensure_one()
        self.message_post(body=_("La demande a été refusée."))
        return super(BambaExpenseRequest, self).action_refuse()

