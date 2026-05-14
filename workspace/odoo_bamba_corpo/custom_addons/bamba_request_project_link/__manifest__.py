{
    "name": "Bamba - Lien Demandes / Projets",
    "version": "1.0.0",
    "category": "Project",
    "summary": "Création et suivi des projets depuis les demandes validées",
    "depends": [
        "bamba_request",
        "bamba_project",
        "mail",
    ],
    "data": [
        "security/project_link_rules.xml",
        "views/bamba_request_views.xml",
        "views/project_views.xml",
    ],
    "installable": True,
    "application": False,
}
