"""
Analyse de sentiment des avis clients — module de remplacement pour TextBlob
=============================================================================

Ce module remplace l'étape d'analyse de sentiment du projet "Analyse des avis
clients Amazon — catégorie Beauté" (qui utilisait TextBlob) par une méthode
plus adaptée au domaine des avis clients, avec une option d'upgrade vers un
vrai modèle de langage pré-entraîné (transformer).

Pourquoi remplacer TextBlob
----------------------------
TextBlob calcule la polarité d'un texte par une simple moyenne de scores
associés aux mots (dictionnaire de polarité + quelques règles basiques sur les
adjectifs). Il gère mal :
  - la négation sur des tournures complexes ("not good at all")
  - les intensificateurs ("really", "absolutely", majuscules, points
    d'exclamation répétés) — très fréquents dans les avis clients
  - le vocabulaire informel typique des avis en ligne

Les deux backends proposés ici
--------------------------------
  - BACKEND PAR DÉFAUT : "vader" (VADER — Valence Aware Dictionary and sEntiment
    Reasoner, Hutto & Gilbert, ICWSM-2014). Lexique + règles spécifiquement
    conçus et validés pour les avis clients et le texte informel (réseaux
    sociaux, reviews) : gère la négation, les intensificateurs, la ponctuation
    et les majuscules d'emphase. 100% local, aucun téléchargement de modèle
    (le lexique est inclus dans le package pip `vaderSentiment`).

  - BACKEND OPTIONNEL : "transformers" — un modèle de langage pré-entraîné
    (`distilbert-base-uncased-finetuned-sst-2-english`), classifieur de
    sentiment binaire entraîné sur de vraies données, bien plus puissant que
    toute méthode à base de lexique. Nécessite un accès à Hugging Face pour
    télécharger les poids (voir note ci-dessous).

Note sur l'environnement de développement
-------------------------------------------
Comme pour le projet RAG (Code du travail), ce code a été développé et testé
dans un environnement cloud dont la politique réseau bloque le téléchargement
de poids de modèles depuis Hugging Face. Le backend "transformers" est donc
implémenté et prêt à l'emploi, mais n'a pas pu être testé dans cet
environnement précis — sur Google Colab ou toute machine avec un accès
internet standard, il fonctionne directement (voir `_try_load_transformers`).
Le backend par défaut ("vader") a lui été testé de bout en bout.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SentimentBackend = Literal["vader", "transformers", "textblob"]


@dataclass
class SentimentResult:
    score: float  # dans [-1, 1], -1 = très négatif, +1 = très positif
    label: str    # "positif" | "neutre" | "négatif"
    backend: str


def _label_from_score(score: float) -> str:
    if score >= 0.05:
        return "positif"
    if score <= -0.05:
        return "négatif"
    return "neutre"


class SentimentAnalyzer:
    """Interface unique pour l'analyse de sentiment, avec plusieurs backends
    interchangeables. Usage recommandé :

        analyzer = SentimentAnalyzer(backend="vader")
        df["sentiment"] = df["text"].apply(analyzer.score)
    """

    def __init__(self, backend: SentimentBackend = "vader"):
        self.requested_backend = backend
        self.backend: SentimentBackend = backend
        self._vader = None
        self._hf_pipeline = None
        self._textblob_cls = None

        if backend == "vader":
            self._load_vader()
        elif backend == "transformers":
            self._try_load_transformers()
        elif backend == "textblob":
            self._load_textblob()
        else:
            raise ValueError(f"Backend inconnu : {backend}")

    def _load_vader(self) -> None:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

        self._vader = SentimentIntensityAnalyzer()
        self.backend = "vader"

    def _load_textblob(self) -> None:
        from textblob import TextBlob

        self._textblob_cls = TextBlob
        self.backend = "textblob"

    def _try_load_transformers(self) -> None:
        try:
            from transformers import pipeline  # type: ignore

            self._hf_pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
            )
            self.backend = "transformers"
            print(
                "[SentimentAnalyzer] Backend neuronal 'transformers' "
                "(distilbert-sst2) chargé avec succès."
            )
        except Exception as exc:  # noqa: BLE001
            print(
                "[SentimentAnalyzer] Backend 'transformers' indisponible "
                f"({exc.__class__.__name__}: {exc}). Repli sur VADER (100% local)."
            )
            self._load_vader()

    def score(self, text: str) -> float:
        """Retourne un score de sentiment dans [-1, 1], compatible avec le
        format utilisé dans le notebook d'origine (df["sentiment"])."""
        if not isinstance(text, str) or not text.strip():
            return 0.0

        if self.backend == "vader":
            return self._vader.polarity_scores(text)["compound"]

        if self.backend == "textblob":
            return self._textblob_cls(text).sentiment.polarity

        if self.backend == "transformers" and self._hf_pipeline is not None:
            out = self._hf_pipeline(text[:512])[0]  # tronqué à 512 tokens max
            sign = 1.0 if out["label"] == "POSITIVE" else -1.0
            return sign * out["score"]

        raise RuntimeError("Aucun backend de sentiment n'est chargé.")

    def analyze(self, text: str) -> SentimentResult:
        s = self.score(text)
        return SentimentResult(score=s, label=_label_from_score(s), backend=self.backend)


if __name__ == "__main__":
    # Jeu de phrases de test représentatif des difficultés classiques pour
    # un modèle de sentiment à base de simple dictionnaire : négation,
    # intensificateurs, ponctuation d'emphase, ironie légère.
    exemples = [
        "This product is not good at all, I really regret buying it.",
        "Absolutely amazing, best purchase ever!!!",
        "It's okay, nothing special but does the job.",
        "I wouldn't say it's bad, but I expected much better for this price.",
        "Terrible smell, broke after two uses, complete waste of money.",
        "Not the best, not the worst — pretty average overall.",
        "I was skeptical at first but this exceeded my expectations completely.",
        "Packaging was damaged and the product leaked everywhere, very disappointed.",
    ]

    vader = SentimentAnalyzer(backend="vader")
    blob = SentimentAnalyzer(backend="textblob")

    print(f"{'Phrase':<70} {'TextBlob':>10} {'VADER':>10}")
    print("-" * 94)
    for texte in exemples:
        s_blob = blob.score(texte)
        s_vader = vader.score(texte)
        print(f"{texte[:68]:<70} {s_blob:>10.3f} {s_vader:>10.3f}")
