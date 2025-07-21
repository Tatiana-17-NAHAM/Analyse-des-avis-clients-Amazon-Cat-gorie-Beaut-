![Statut](https://img.shields.io/badge/🔥_Projet-Actif-EA4C4C.svg)
![Auteur](https://img.shields.io/badge/Auteur-Tatiana%20SANGUEAL%20NAHAM-blue)

# Analyse-des-avis-clients-Amazon-Catégorie-Beauté

## 📚 Sommaire

- [🧭 Présentation du projet](#🧭-présentation-du-projet)
- [🎯 Objectifs du projet](#🎯-objectifs-du-projet)
- [🛠️ Technologies utilisées](#️-technologies-utilisées)
- [📊 Visualisations](#📊-visualisations)
- [🔍 Étapes de l’analyse](#🔍-étapes-de-lanalyse)
- [🧾 Conclusion & recommandations](#🧾-conclusion--recommandations)
- [🚀 Pistes d’évolution du projet](#🚀-pistes-dévolution-du-projet)



## 🧭 Présentation du projet
Ce projet vise à analyser les commentaires des clients sur Amazon dans la section produits de beauté, afin de mieux saisir les perceptions, les aspects positifs et les domaines nécessitant des améliorations identifiés par les utilisateurs.

 Le jeu de données utilisé provient d'Amazon Reviews 2023, publié par le McAuley : https://github.com/McAuley-Lab  et accessible sans frais sur la plateforme Hugging Face : https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023  . 👉  Fichier en cours d'utilisation : All_Beauty.jsonl.gz

## 🎯 Objectifs du projet
Ce projet a pour objectif de :
- Analyser les commentaires des clients sur Amazon dans la section Beauté afin de dégager des conclusions précises
- Évaluer le ressenti des utilisateurs à travers le texte libre : contentement, critiques, aspects délicats
- Observation des tendances : répartition des notes, progression dans le temps, fréquence des thèmes répétitifs
- Comparer les commentaires authentiques et non authentiques afin de déceler les divergences de perception
- Mettre en pratique une méthode d'analyse simple mais solide en Python à l'aide d'outils disponibles

L'intégralité du processus est conçu pour être réplicable, aisément modifiable pour d'autres produits, et démontrer ta compétence à convertir des informations textuelles brutes en décisions réfléchies.

## 🛠️ Technologies utilisées

| Librairie / Outil         | Usage principal                                                                 |
|---------------------------|----------------------------------------------------------------------------------|
| `pandas`                  | Manipulation de données, nettoyage, traitement tabulaire                        |
| `matplotlib`, `seaborn`   | Visualisations : histogrammes, courbes, boxplots                                |
| `wordcloud`               | Génération de nuages de mots à partir des commentaires clients                  |
| `TextBlob`                | Analyse de sentiment textuel simple et accessible                               |
| `json`, `gzip`            | Chargement et lecture de fichiers `.jsonl.gz`                                   |
| `tqdm`                    | Suivi visuel de la progression lors du traitement des avis                      |
| `Jupyter Notebook`        | Présentation interactive du projet avec exécution pas-à-pas                     |

## 📊  Visualisations
Cette partie compile les principales visualisations provenant de l'étude des commentaires clients sur Amazon (secteur Beauté).  Ces représentations facilitent un résumé rapide des tendances, des opinions clients et des aspects critiques mentionnés dans les retours :
 ## 📈 Distribution des notes : Histogramme des évaluations (de 1 à 5 étoiles), pour visualiser le niveau général de satisfaction.

  ![Distribution des notes](image1.png)

Le graphique révèle que la plupart des clients évaluent hautement les produits cosmétiques sur Amazon, avec une forte concentration autour de 4 à 5 étoiles.  Les commentaires défavorables demeurent peu fréquents, traduisant un grand degré de contentement général.  Avec plus de 700 000 avis, l'ampleur du jeu de données renforce la crédibilité de cette tendance et incite à une étude plus détaillée du contenu des commentaires afin de saisir ce qui séduit véritablement les utilisateurs. 
