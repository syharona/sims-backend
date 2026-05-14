# -*- coding: utf-8 -*-
{
    "name": "Bamba Configuration",
    "version": "1.0.0",
    "summary": "Configuration module for Bamba Corporation (fields, groups, workflows, templates)",
    "description": "Centralized configuration: custom fields, groups, templates.",
    "category": "Hidden",
    "author": "Bamba Corp",
    "depends": ["base", "contacts", "crm", "sale_management", "project", "hr", "account"],
    "data": [
        "security/bamba_groups.xml",
        "security/ir.model.access.csv",
        "data/custom_fields_bamba.xml",
        "data/bamba_sequences.xml",
        "data/crm_pipeline.xml",
        "data/project_templates.xml",
        "views/res_partner_views.xml",
        "views/project_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}