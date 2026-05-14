# -*- coding: utf-8 -*-
"""
Migration 1.0 -> 2.0
- Adds project_manager_id column if missing (was declared in Python but never migrated)
- Migrates existing description/unit_price/quantity/supplier_id data into bamba.request.line rows
  (handled automatically by Odoo ORM on upgrade; old columns are left in place and
   will be ignored by the ORM once removed from the model definition)
"""

import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    # Fix missing project_manager_id column that caused the crash
    cr.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'bamba_request'
          AND column_name = 'project_manager_id'
    """)
    if not cr.fetchone():
        _logger.info("bamba_request: adding missing project_manager_id column")
        cr.execute("""
            ALTER TABLE bamba_request
            ADD COLUMN project_manager_id INTEGER
            REFERENCES res_users(id) ON DELETE SET NULL
        """)

    # Migrate old single-line data into the new bamba_request_line table
    # Only run if the old columns still exist AND new table is empty
    cr.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'bamba_request' AND column_name = 'description'
    """)
    old_desc_exists = cr.fetchone()

    if old_desc_exists:
        cr.execute("SELECT COUNT(*) FROM bamba_request_line")
        already_migrated = cr.fetchone()[0] > 0

        if not already_migrated:
            _logger.info("bamba_request: migrating old single-line data to bamba_request_line")
            cr.execute("""
                INSERT INTO bamba_request_line
                    (request_id, sequence, description, supplier_id, unit_price, quantity)
                SELECT
                    id,
                    10,
                    COALESCE(description, 'Ligne migrée'),
                    supplier_id,
                    COALESCE(unit_price, 0),
                    COALESCE(quantity, 1)
                FROM bamba_request
                WHERE description IS NOT NULL OR unit_price IS NOT NULL
            """)
            _logger.info("bamba_request: migration complete")
