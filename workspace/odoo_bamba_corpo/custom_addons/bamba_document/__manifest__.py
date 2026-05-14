# -*- coding: utf-8 -*-
{
    "name": "Bamba Document Management",
    "version": "1.0.0",
    "category": "Operations",
    "summary": "Gestion documentaire Projets & Demandes",
    "depends": [
        "base",
        "mail",
        "project",
        "bamba_request",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/rules.xml",
        "views/document_views.xml",
        "views/project_views.xml",
        "views/request_views.xml",
    ],
    "installable": True,
}


