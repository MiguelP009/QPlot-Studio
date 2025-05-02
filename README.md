
# QPlot-Studio

QPlot-Studio est une application graphique en Python (PySide6) qui permet de transformer les résultats de questionnaires papier en graphiques lisibles et exportables. Elle est idéale pour les présentations, rapports, ou simplement pour visualiser rapidement des statistiques de sondages ou d’enquêtes.

## ✨ Fonctionnalités

- Interface moderne en Qt (PySide6)
- Ajout manuel des questions et de leurs réponses
- Choix du type de graphique (barres, camembert, etc.)
- Affichage dynamique des résultats
- Export de chaque graphique sous forme d’image (nommé automatiquement avec la question)
- Menu latéral listant toutes les questions ajoutées
- Sauvegarde automatique des questions entre les sessions
- Possibilité de supprimer des questions précédemment ajoutées
- Redimensionnement dynamique de la zone d’affichage des graphiques

## 🖼️ Interface

> *(Insère ici des captures d’écran si tu veux)*

## 🛠️ Installation

### Prérequis

- Python 3.7 ou plus
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

**requirements.txt**
```
PySide6
matplotlib
```

### Lancer l'application

```bash
python main.py
```

## 📁 Structure du projet

```
QPlot-Studio/
│
├── main.py                  # Fichier principal
├── data.json               # Sauvegarde automatique des questions
├── requirements.txt        # Dépendances
└── README.md               # Ce fichier
```

## 📤 Export

Chaque graphique peut être enregistré en un clic, avec le nom de la question comme nom de fichier PNG.

## 📃 Licence

Ce projet est sous licence MIT. Tu peux l’utiliser librement, le modifier et le partager.

---

Développé avec ❤️ pour Jojo pour faciliter la mise en forme des résultats de questionnaires papier.
```

---
