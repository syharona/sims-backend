{
    "name": "Bamba - Gestion des Projets & Chantiers",
    "version": "1.0.0",
    "category": "Project",
    "summary": "Gestion métier des projets et chantiers",
    "depends": [
        "project",
        "mail",
        "bamba_base",
        "bamba_document",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/project_rules.xml",
        "data/project_sequence.xml",
        "views/project_views.xml",
        "views/project_menu.xml",
    ],
    "application": True,
    "installable": True,
}
