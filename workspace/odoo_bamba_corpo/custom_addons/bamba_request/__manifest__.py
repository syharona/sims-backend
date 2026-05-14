# -*- coding: utf-8 -*-
{
    "name": "Bamba - Demandes & Validations",
    "version": "2.0",
    "category": "Operations",
    "depends": [
        "bamba_base",
        "mail",
        "hr",
        "account",
        "analytic",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/request_rules.xml",
        "data/sequences.xml",
        "data/mail_activity_type.xml",
        "views/request_views.xml",
        "views/request_menu.xml",
    ],
    "application": True,
}
