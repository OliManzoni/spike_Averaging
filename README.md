# ⚡ Pipeline d'Excitabilité & Morphométrie - Manzoni Lab

![Manzoni Lab](https://img.shields.io/badge/Manzoni_Lab-Neurosciences-purple)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)

Une suite d'applications web (Streamlit) conçue pour l'extraction biophysique, le traitement par lots (batch processing) et l'analyse statistique d'enregistrements électrophysiologiques en patch-clamp (format `.abf`).

## 🧠 Philosophie du Projet
Cette pipeline a été développée pour standardiser l'analyse de la plasticité synaptique et de l'excitabilité intrinsèque. Elle garantit :
- **La Rigueur Biologique :** Détection des potentiels d'action via seuil de dérivée ($dV/dt$), extraction de l'AHP relative au seuil, et calcul rigoureux de la capacitance ($C_m$) et du *Decay time*.
- **La Traçabilité :** Le nom de chaque fichier originel sert de `Cell_ID` tout au long de la chaîne d'analyse.
- **Le Standard de Publication :** Génération automatique de graphiques avec bandes d'erreur (SEM ou Intervalle de Confiance à 95%) et application stricte de modèles statistiques avancés (ANOVA à mesures répétées) exigés par des journaux comme *Science* ou *Nature*.

---

## 🛠️ Installation & Prérequis

Assurez-vous d'avoir Python 3.9 (ou supérieur) installé. Il est recommandé de créer un environnement virtuel.

1. Clonez ce dépôt ou téléchargez les scripts dans un dossier.
2. Installez les dépendances requises :

```bash
pip install streamlit pyabf pandas numpy matplotlib seaborn scipy statsmodels
