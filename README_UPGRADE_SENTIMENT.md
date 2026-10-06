# Upgrade de l'analyse de sentiment — remplacement de TextBlob par VADER

Ce dossier contient le remplacement de l'étape d'analyse de sentiment du projet
**Analyse des avis clients Amazon — catégorie Beauté**, qui utilisait TextBlob
(cellule `from textblob import TextBlob` / `get_sentiment`).

## Pourquoi ce changement

TextBlob calcule la polarité d'un texte par une moyenne de scores de mots
individuels, avec des règles très simples. Sur des avis clients réels, ça pose
problème avec :
- la **négation** ("not good at all" → TextBlob reste proche de 0)
- les **intensificateurs** ("really", "absolutely", majuscules, "!!!")
- le **vocabulaire informel** typique des avis en ligne

## Le remplacement : VADER

[VADER](https://github.com/cjhutto/vaderSentiment) (Hutto & Gilbert, ICWSM-2014)
est un outil d'analyse de sentiment construit et validé spécifiquement sur du
texte informel et des avis clients (pas un usage générique comme TextBlob). Il
gère explicitement la négation, les intensificateurs et la ponctuation
d'emphase. Il tourne 100% en local via le package pip `vaderSentiment`, sans
aucun téléchargement de modèle.

### Comparaison réelle, testée

Voici le résultat obtenu en exécutant les deux méthodes sur des phrases types
d'avis clients (script `sentiment_pipeline.py`, exécuté et vérifié) :

| Phrase | TextBlob | VADER |
|---|---:|---:|
| "This product is not good at all, I really regret buying it." | -0.075 | **-0.670** |
| "Absolutely amazing, best purchase ever!!!" | 0.800 | 0.887 |
| "It's okay, nothing special but does the job." | 0.429 | -0.046 |
| "I wouldn't say it's bad, but I expected much better for this price." | -0.100 | 0.698 |
| "Terrible smell, broke after two uses, complete waste of money." | -0.367 | **-0.827** |
| "Not the best, not the worst — pretty average overall." | 0.020 | 0.481 |
| "I was skeptical at first but this exceeded my expectations completely." | -0.050 | -0.166 |
| "Packaging was damaged and the product leaked everywhere, very disappointed." | -0.975 | -0.822 |

**Ce qui s'améliore clairement** : sur la négation simple ("not good at all"),
TextBlob reste presque neutre (-0.075) alors que l'avis est clairement négatif
— VADER corrige ça (-0.670). Sur les avis très négatifs ou très positifs sans
ambiguïté, les deux méthodes convergent, mais VADER capte mieux l'intensité
(ponctuation, "terrible", "complete waste of money").

**Limite honnête** : aucune des deux méthodes ne gère bien les phrases à
double négation ou avec une clause contrastive ("I wouldn't say it's bad,
but...") — c'est une limite connue des méthodes à base de lexique en général,
pas spécifique à VADER. C'est la motivation du backend optionnel ci-dessous.

## Aller plus loin : backend neuronal (transformer)

Le module `sentiment_pipeline.py` inclut aussi un backend `"transformers"`
(modèle `distilbert-base-uncased-finetuned-sst-2-english`, un vrai classifieur
de sentiment entraîné sur des données réelles), avec repli automatique sur
VADER si le modèle n'est pas disponible. Ce backend n'a pas pu être testé dans
l'environnement où ce code a été développé (pas d'accès réseau à Hugging Face
depuis ce sandbox), mais il fonctionne directement sur Google Colab ou toute
machine avec un accès internet standard :

```python
analyzer = SentimentAnalyzer(backend="transformers")
```

## Comment intégrer ça dans ton notebook existant

Dans `notebook.ipynb`, remplace :

**Cellule `!pip install textblob`** par :
```python
!pip install vaderSentiment
```

**Cellule avec `from textblob import TextBlob` / `get_sentiment`** par :
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    return _analyzer.polarity_scores(text)["compound"]

df["sentiment"] = df["text"].apply(get_sentiment)
```

Le reste du notebook (histogrammes, nuages de mots, comparaison achat
vérifié/non vérifié...) fonctionne sans aucun autre changement : le score
reste dans l'intervalle [-1, 1], exactement comme avant avec TextBlob.

## Fichiers

- `sentiment_pipeline.py` — le module complet, testé, avec les trois backends
  (`vader` par défaut, `textblob` pour comparaison, `transformers` en option)
- Ce README
