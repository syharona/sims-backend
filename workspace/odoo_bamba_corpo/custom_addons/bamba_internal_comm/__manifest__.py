{
    "name": "Bamba - Communication interne",
    "version": "1.0",
    "category": "Internal",
    "summary": "Communication interne liée aux demandes et projets",
    "depends": [
        "bamba_request",   # ton module Demande
        "project"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/bamba_communication_rules.xml",
        "views/bamba_internal_message_views.xml",
        "views/bamba_request_views.xml",
    ],
    "installable": True,
    "application": False,
}
