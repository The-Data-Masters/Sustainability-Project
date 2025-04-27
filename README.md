# 📊 Projet Power BI - Déploiement Git

Bienvenue dans ce projet Power BI versionné avec Git et organisé pour un déploiement structuré.

## 📁 Structure du projet

Voici la structure des dossiers utilisée :

PowerBI_Project/
├── pbix/            # Fichiers Power BI Desktop (.pbix) versionnés avec Git LFS
├── scripts_DAX/     # Fichiers JSON des mesures extraites avec Tabular Editor 3
├── scripts_M/       # Scripts M (Power Query) extraits manuellement
├── README.md        # Documentation du projet
├── .gitignore       # Fichiers et extensions ignorés par Git

---

## ✍️ Contenu

- **`pbix/`** : Fichiers .pbix principaux (rapports Power BI).
- **`scripts_DAX/`** : Scripts DAX (mesures, colonnes calculées) exportés en JSON.
- **`scripts_M/`** : Scripts M issus de Power Query pour les transformations de données.

---

## 🚀 Règles de Contribution

- Utiliser des branches séparées :
  - `feature/nom-fonctionnalité` pour de nouvelles fonctionnalités
  - `bugfix/nom-bug` pour corriger des problèmes
- Soumettre les changements via **Pull Request** pour revue avant de fusionner dans `main`.

---

## 🔒 Sécurité

- Aucune donnée sensible ne doit être stockée dans le dépôt (mots de passe, clés API, etc.).
- Utilisation de **Git LFS** pour gérer les gros fichiers `.pbix`.

---

## ✅ Déploiement

1. Cloner le projet :
    ```bash
    git clone https://github.com/TonNomUtilisateur/PowerBI_Project.git
    ```

2. Installer Git LFS si ce n’est pas déjà fait :
    ```bash
    git lfs install
    ```

3. Travailler dans des branches dédiées et effectuer des Pull Requests pour toutes modifications.

---

## 📄 Licence

Projet interne. Tous droits réservés.

---
