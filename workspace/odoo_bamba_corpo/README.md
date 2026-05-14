# odoo_bamba_corpo 
---

# 🚀 Quick Start – Odoo Bamba Corp

1. Pré-requis macOS

* Homebrew installé
* Python 3.11 (via Homebrew)
* PostgreSQL (via Homebrew)
* Virtualenv
* Xcode Command Line Tools (`xcode-select --install`) pour compiler certains modules
 

```bash
# Installer PostgreSQL
brew install postgresql

# Installer Python 3.11
brew install python@3.11

# Installer wkhtmltopdf (pour les rapports PDF)
brew install wkhtmltopdf

# Installer virtualenv
python3.11 -m pip install --user virtualenv
```

2. Télécharger Odoo 17 ZIP : [https://nightly.odoo.com/](https://nightly.odoo.com/) → 17.0 → Source → `odoo_17.0.latest.zip`
3. Extraire le ZIP dans `~/workspace/odoo-17`
4.  Adapter le fichier requirement.txt
> ⚠️ macOS peut poser problème avec `psycopg2` si les headers de PostgreSQL ne sont pas trouvés.
> Solution :
> dans odoo/requirement.txt
> remplacer psycopg2==2.9.5 ; python_version == '3.11' 
> par 
> psycopg2-binary==2.9.5 ; python_version == '3.11' 

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install wheel
pip install -r odoo/requirements.txt
```

5. Installer PostgreSQL et créer l’utilisateur Odoo :

```bash
 # Créer l’utilisateur et la base
createuser -s odoo
createdb odoo_bamba
psql -c "ALTER USER odoo WITH PASSWORD 'odoo';"
```

6. Cloner le projet custom :

```bash
git clone https://gitlab.com/bamba_corpo/odoo_bamba_corpo.git
```

6. Structure finale :

```
workspace/
   odoo-17/
   odoo_bamba_corpo/
       custom_addons/
       odoo.conf
```

7. Mettre à jour `odoo.conf` avec les chemins addons :

```
addons_path = ~/workspace/odoo-17/addons, ~/workspace/odoo_bamba_corpo/custom_addons
```

8. Lancer Odoo :

```bash
python3 odoo-17/odoo-bin -c odoo_bamba_corpo/odoo.conf
```

9. Accéder à l’interface : [http://localhost:8069](http://localhost:8069)
10. Créer une base de dev et commencer à travailler sur les modules.
 
