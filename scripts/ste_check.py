#!/usr/bin/env python3
"""ste_check: a small heuristic linter for AI tells and STE-style (ASD-STE100-inspired) text.

It checks English and French. In French it also checks typography.

Part of the ste80-humanizer skill. It finds places to look at.
It does not prove compliance with ASD-STE100 and it is not an AI detector.
No dependencies. Python 3.8+.

Usage:
    python ste_check.py FILE [FILE ...]
    python ste_check.py --strict FILE
    cat draft.txt | python ste_check.py -
    python ste_check.py --json FILE
    python ste_check.py --lang fr FILE          (default: auto-detect en or fr)
    python ste_check.py --fix-spaces FILE       (French: put no-break spaces in place)

Exit code: 0 if no findings, 1 if findings, 2 on usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict

# --- Word lists (short, paraphrased working lists; not the ASD dictionary) ---

SWAPS = {
    "utilize": "use", "utilise": "use", "leverage": "use", "employ": "use",
    "perform": "do", "conduct": "do", "accomplish": "do", "facilitate": "help, let",
    "ensure": "make sure", "verify": "make sure", "commence": "start",
    "initiate": "start", "terminate": "stop", "eliminate": "remove",
    "modify": "change", "indicate": "show", "demonstrate": "show",
    "obtain": "get", "acquire": "get", "provide": "give", "assist": "help",
    "attempt": "try", "retain": "keep", "observe": "monitor, see",
    "locate": "find", "determine": "find", "subsequently": "then",
    "however": "but", "therefore": "thus, as a result", "hence": "thus",
    "furthermore": "also", "moreover": "also", "additionally": "also",
    "whereas": "but", "via": "through", "whether": "if",
    "numerous": "many", "adequate": "sufficient", "identical": "same",
    "simultaneously": "at the same time", "prior to": "before",
    "due to": "because of", "in order to": "to", "in the event that": "if",
    "it is important to note": "(delete)", "it's important to note": "(delete)",
    "it should be noted": "(delete)",
    "delve": "examine", "robust": "strong, reliable", "seamless": "(delete)",
    "seamlessly": "(delete)", "comprehensive": "full", "crucial": "important",
    "pivotal": "important", "landscape": "field, area", "realm": "field, area",
    "showcase": "show", "streamline": "simplify", "empower": "let, help",
    "harness": "use", "foster": "help", "underscore": "show",
    "game-changer": "(delete)", "tapestry": "(delete)", "testament": "(delete) or say what it shows",
    "elevate": "improve", "unlock": "let, give", "intricate": "complex", "meticulous": "careful",
    "vibrant": "(delete)", "enhance": "improve", "groundbreaking": "(fact or delete)",
    "cutting-edge": "(fact or delete)", "world-class": "(fact or delete)", "best-in-class": "(fact or delete)",
    "renowned": "(fact or delete)", "stunning": "(delete)", "breathtaking": "(delete)",
    "serves as": "is", "stands as": "is", "boasts": "has",
}

STRICT_ONLY_SWAPS = {
    "need": "necessary (adj)", "may": "can", "might": "can", "could": "can",
    "should": "must", "shall": "must", "would": "will", "since": "because",
    "both": "the two", "further": "more", "additional": "more",
    "acceptable": "permitted", "main": "primary", "portion": "part",
    "required": "necessary", "insert": "put", "rotate": "turn",
    "avoid": "prevent", "follow": "obey", "inspect": "examine",
    "e.g.": "for example", "i.e.": "that is", "etc.": "and other",
}

TELLS = [
    (r"\b(?:it'?s|it is|this is|that'?s|is)\s+not\s+(?:just|only|merely|simply|about)\b", "not-x-but-y", "'not just X, but Y' framing: state the point"),
    (r"\bnot\s+(?:just|only|merely)\b[^.]{0,80}\bbut\b", "not-x-but-y", "'not just X but Y' framing: state the point"),
    (r"\bisn'?t\s+(?:just\s+)?about\b", "not-x-but-y", "'this isn't about X' framing: state the point"),
    (r"^(?:great question|certainly|of course|sure|absolutely)[!,.]", "chatbot", "chatbot opener: delete"),
    (r"\bi hope this helps\b|\blet me know if\b|\bwould you like me to\b|\bfeel free to\b|\bhappy to help\b", "chatbot", "chatbot closer: delete"),
    (r"\blet'?s (?:dive|delve|break (?:this|it) down|explore|unpack)\b|\bhere'?s the thing\b|\bwithout further ado\b", "run-up", "run-up before the point: start with the point"),
    (r"\bat its core\b|\bthe real question is\b|\bfundamentally\b|\bat the end of the day\b", "fake-depth", "fake depth: say the plain claim"),
    (r"\blet that sink in\b|\band that changes everything\b|\bthat'?s the real (?:win|story)\b|\bread that again\b", "closer", "dramatic closer: delete"),
    (r"\bdon'?t get me wrong\b|\bto be clear\b|\bone might be tempted\b", "strawman", "arguing with nobody: remove"),
    (r"\bas of my (?:last|latest) (?:update|training)\b|\bbased on (?:the )?available information\b", "knowledge-hedge", "knowledge-limit hedge: delete"),
    (r"\bin this (?:guide|article|section|post),? (?:we|i)(?:'ll| will)\b", "meta", "writing about the text: give the content"),
    (r"\b(?:could|may|might) (?:potentially|possibly|arguably)\b", "stacked-hedge", "stacked hedge: keep one hedge"),
    (r"\b(?:experts|studies|many people|observers) (?:say|agree|show|believe|suggest)\b", "vague-authority", "vague authority: name the source or delete"),
    (r",\s+(?:highlighting|underscoring|emphasizing|ensuring|reflecting|showcasing|fostering|cultivating|contributing to)\b", "ing-rider", "shallow '-ing' rider: delete or make it a sentence"),
    (r"\b(?:plays|play|played) a (?:pivotal|crucial|key|vital) role\b|\bmarks? a (?:significant|major) milestone\b|\bthe future looks bright\b", "inflation", "inflated significance: say what happened"),
    (r"\b(?:is|are|was|were) associated with\b|\b(?:in connection with|linked to|tied to)\b", "vague-association", "vague connection: name the relation (founded, caused, part of)"),
    (r"\b(?:is|are|was|were|be)(?:\s+\w+ly)?\s+(?:high-quality|well-known|well-documented|long-term|real-time|well-tested|client-facing)\b", "hyphen-pair", "drop the hyphen after the noun ('is well documented')"),
    (r"^(?:that'?s|this is) (?:the real|why it|what) ", "closer", "possible one-line closer: cut it if it repeats the point"),
]

PHRASAL = [
    "set up", "find out", "look into", "look at", "fill in", "fill out",
    "turn on", "turn off", "switch on", "switch off", "go through",
    "point out", "put together", "take out", "come up with", "give up",
    "carry out", "figure out", "check out", "back up", "shut down",
]

ING_NOUN_OK = {
    "during", "following", "opening", "remaining", "according", "something",
    "nothing", "anything", "everything", "thing", "things", "string", "strings",
    "bring", "ring", "spring", "king", "wing", "sing", "single", "logging",
    "caching", "routing", "testing", "debugging", "networking", "staging",
    "setting", "settings", "mapping", "warning", "warnings", "building",
    "meaning", "morning", "evening", "ceiling", "padding", "spacing",
    "rendering", "hosting", "tooling", "training", "pricing", "billing",
    "encoding", "streaming", "scheduling", "parsing", "linting", "formatting",
    "being", "missing", "existing", "incoming", "outgoing", "pending",
}

NOT_PARTICIPLE = {
    "different", "present", "absent", "current", "recent", "frequent", "silent",
    "independent", "efficient", "sufficient", "apparent", "consistent", "important",
    "relevant", "urgent", "evident", "excellent", "competent", "dependent", "transparent",
    "open", "even", "often", "golden", "hidden", "sudden", "wooden", "own", "down",
    "shown", "known", "unknown", "brown", "grown", "drawn", "built", "content",
    "intent", "event", "agent", "client", "point", "front", "want", "difficult",
}

AUX = r"(?:am|is|are|was|were|be|been|being)"
PASSIVE_RE = re.compile(rf"\b{AUX}\s+(?:\w+ly\s+)?(\w+(?:ed|en|wn|lt|nt|pt|ung|ade|one|ept|ought))\b", re.I)
PERFECT_RE = re.compile(r"\b(?:has|have|had)\s+(?:not\s+)?(?:been|\w+ed|\w+en|done|made|gone|seen|run|set|put)\b", re.I)
PROGRESSIVE_RE = re.compile(rf"\b{AUX}\s+(?:not\s+)?(\w+ing)\b", re.I)
MODAL_PASSIVE_RE = re.compile(r"\b(?:can|could|may|might|must|should|shall|will|would)\s+(?:not\s+)?be\s+\w+(?:ed|en)\b", re.I)
CONTRACTION_RE = re.compile(r"\b\w+(?:n't|'re|'ve|'ll|'d|'m)\b|\b(?:it|that|there|what|here)'s\b", re.I)
WORD_RE = re.compile(r"[A-Za-zÀ-ÿœŒ][A-Za-zÀ-ÿœŒ'’\-]*|\d[\w.,:/%-]*")

# --- French (references/french.md, references/french-typography.md) ---

_ER = r"(?:e|es|ent|er|ez|ons|é|ée|és|ées|ant|ait|aient|era|eront)"
_ADJ = r"(?:e|s|es)?"

# (regex on lower-case text with straight apostrophes, label, alternative)
FR_SWAPS = [
    (rf"exploit{_ER}", "exploiter", "utiliser"),
    (r"tir(?:e|es|ent|er|ez|ant) parti d[eu']", "tirer parti de", "utiliser"),
    (rf"révolutionn{_ER}", "révolutionner", "(fait ou supprimer)"),
    (rf"dévoil{_ER}", "dévoiler", "montrer, publier"),
    (rf"impact{_ER}", "impacter", "toucher, changer"),
    (rf"solutionn{_ER}", "solutionner", "résoudre"),
    (rf"initi{_ER}", "initier", "commencer, lancer"),
    (rf"début{_ER}", "débuter", "commencer"),
    (rf"finalis{_ER}", "finaliser", "terminer"),
    (rf"effectu{_ER}", "effectuer", "faire, ou le verbe direct"),
    (r"proc[éè]d(?:e|es|ent|er|ez|ons|é|ant) (?:à|au|aux)", "procéder à", "le verbe direct"),
    (r"mis(?:e|es)? en (?:lumière|exergue|avant)|met(?:s|tent|tre|tant)? en (?:lumière|exergue|avant)", "mettre en lumière", "montrer"),
    (r"témoign(?:e|ent|ant) d[eu']", "témoigner de", "montrer"),
    (r"s'av[èé]r(?:e|ent|er|ait)", "s'avérer", "être"),
    (r"se positionn(?:e|ent) comme|s'impos(?:e|ent) comme|fai(?:t|sant) office d[e']", "se positionner comme", "être"),
    (r"constitu(?:e|ent|ant) (?:un|une|le|la|l'|les|des)", "constituer", "être"),
    (r"dispos(?:e|ent) d[eu']|bénéfici(?:e|ent) d[eu']|arbor(?:e|ent)", "disposer de", "avoir"),
    (r"est en mesure d[e']|sont en mesure d[e']|est susceptible d[e']|sont susceptibles d[e']", "être en mesure de", "pouvoir"),
    (r"a pour (?:but|objectif|vocation) d[e']", "avoir pour but de", "sert à"),
    (r"fai(?:t|re|sant) sens", "faire sens", "avoir du sens"),
    (r"adress(?:e|ent|er|ant) (?:un|le|ce|ces|les|des) (?:problème|enjeu|défi|question|bug|faille|besoin)s?", "adresser un problème", "traiter"),
    (r"au final", "au final", "finalement, ou supprimer"),
    (r"délivr(?:e|es|ent|er|ez|é|ée|és|ées|ant)", "délivrer", "livrer, fournir"),
    (r"support(?:e|ent|er|é|ée|és|ées) (?:désormais |maintenant |aussi |enfin |nativement )?(?:le |la |les |l')?(?:format|protocole|ipv\d|version|norme|standard|navigateur|api)", "supporter (un format)", "prendre en charge"),
    (r"opportunités?", "opportunité", "occasion"),
    (r"digital(?:e|es|aux)?", "digital", "numérique"),
    (r"clés? en main", "clé en main", "(fait ou supprimer)"),
    (r"à la pointe", "à la pointe", "(fait ou supprimer)"),
    (r"en constante évolution", "en constante évolution", "(fait ou supprimer)"),
    (r"leviers?", "levier", "moyen, ou le fait"),
    (r"écosystèmes?", "écosystème", "ensemble d'outils, ou le nom exact"),
    (r"paysage (?:actuel|numérique|technologique|médiatique)", "paysage", "domaine, secteur"),
    (r"décrypt(?:e|ons|er|ez|ant)", "décrypter", "expliquer"),
    (r"méticuleu(?:x|se|ses)|méticuleusement", "méticuleux", "soigneux, ou le fait"),
    (r"se révèl(?:e|ent) être", "se révéler être", "être"),
    (r"jou(?:e|ent) le rôle d[eu']", "jouer le rôle de", "être"),
    (r"de renom|sans précédent|un cadre exceptionnel|une expérience unique|un large éventail|riche patrimoine", "langage de vente", "(fait ou supprimer)"),
    (r"en charge d[eu']", "en charge de", "chargé de"),
    (rf"cruci(?:al{_ADJ}|aux)", "crucial", "important, ou le fait"),
    (rf"primordi(?:al{_ADJ}|aux)", "primordial", "important, ou le fait"),
    (r"incontournables?", "incontournable", "(fait ou supprimer)"),
    (r"véritables?", "véritable", "(supprimer)"),
    (r"holistiques?", "holistique", "complet"),
    (r"robustes?", "robuste", "fiable, solide"),
    (r"révolutionnaires?", "révolutionnaire", "(fait ou supprimer)"),
    (rf"époustouflant{_ADJ}", "époustouflant", "(supprimer)"),
    (r"novat(?:eur|eurs|rice|rices)", "novateur", "(fait ou supprimer)"),
    (r"sans couture", "sans couture", "(supprimer)"),
    (r"de pointe|de classe mondiale|à couper le souffle|haut de gamme", "langage de vente", "(fait ou supprimer)"),
    (r"nich(?:é|ée|és|ées) au cœur", "niché au cœur de", "dire où"),
    (r"pléthore|myriade|panoplie|tapisserie", "pléthore, myriade", "beaucoup de, plusieurs"),
    (r"pierre angulaire|fer de lance", "pierre angulaire", "dire le rôle exact"),
    (r"synergies?", "synergie", "dire ce qui se passe"),
    (r"en outre|de surcroît", "en outre", "aussi, ou supprimer"),
    (r"néanmoins|toutefois|cependant", "néanmoins", "mais"),
    (r"par conséquent", "par conséquent", "donc"),
    (r"afin d[e']", "afin de", "pour"),
    (r"afin qu[e']", "afin que", "pour que"),
    (r"au sein d[eu']", "au sein de", "dans"),
    (r"suite à", "suite à", "après, à cause de"),
    (r"au niveau d[eu']", "au niveau de", "dans, pour, sur"),
    (r"dans le cadre d[eu']", "dans le cadre de", "pour, pendant"),
    (r"par le biais d[eu']", "par le biais de", "par, avec"),
    (r"en termes d[e']", "en termes de", "pour"),
    (r"dans la mesure où", "dans la mesure où", "parce que, si"),
    (r"il convient d[e']", "il convient de", "il faut, ou l'impératif"),
    (r"il est (?:important|essentiel|crucial) de (?:noter|souligner|rappeler)|il (?:est à|faut|convient de) noter qu[e']|notons qu[e']|force est de constater",
     "il est important de noter", "(supprimer)"),
]

FR_STRICT_SWAPS = [
    (r"pourrai(?:t|ent)", "pourrait", "peut"),
    (r"devrai(?:t|ent)|faudrait", "devrait", "doit, il faut"),
    (r"on", "on", "nommer l'acteur"),
    (r"etc\.", "etc.", "donner la liste complète"),
    (r"via", "via", "par, avec"),
]

FR_TELLS = [
    (r"\bn[e']\s?(?:est|sont|était)\s+pas\s+(?:seulement|simplement|juste|uniquement|qu[e'])", "not-x-but-y", "'ce n'est pas seulement X, c'est Y': state the point"),
    (r"\bnon seulement\b[^.]{0,100}\bmais\b", "not-x-but-y", "'non seulement X, mais Y': state the point"),
    (r"\bil ne s'agit pas (?:seulement |simplement |uniquement )?d[e']", "not-x-but-y", "'il ne s'agit pas de X, mais de Y': state the point"),
    (r"\bbien plus qu'un|\bloin d'être (?:un|une) simple\b", "not-x-but-y", "'bien plus qu'un X': state the point"),
    (r"\bne se content(?:e|ent) pas d[e']|,\s+(?:zéro prise de tête|sans friction)\b", "not-x-but-y", "'ne se contente pas de X' or negative tail: state the point"),
    (r"^[\"«\s]*(?:vous avez (?:tout à fait|entièrement|parfaitement) raison|voici (?:un|une) (?:aperçu|résumé|tour d'horizon))\b|\ben tant qu'(?:ia|intelligence artificielle|assistant)\b|\ben tant que modèle de langage\b", "chatbot", "chatbot residue: delete"),
    (r"^[\"«\s]*(?:(?:excellente|très bonne|bonne) question|bien sûr|absolument|certainement|avec plaisir|tout à fait)\s?[!,.]", "chatbot", "chatbot opener: delete"),
    (r"\bj'espère que (?:cela|ça|ceci) (?:vous |t')?(?:aide|aidera|sera utile)|\bn'hésite[zs]? pas à\b|\bsouhaite[zs]-(?:vous|tu) que je\b|\bfaites-moi savoir\b|\bdites-moi si\b", "chatbot", "chatbot closer: delete"),
    (r"\bplongeons\b|\bentrons dans le vif\b|\bvoici ce qu'il faut (?:savoir|retenir)\b|\bsans plus attendre\b|\bdécortiquons\b|\bexplorons\b|\bsoyons honnêtes\b|\bdisons-le\b|\bdans le paysage actuel d[eu']|\bmaintenant que nous avons posé les bases\b|\bla vérité, c'est que\b|^franchement \?|\bil convient de souligner\b", "run-up", "run-up before the point: start with the point"),
    (r"\bau fond,|\bla vraie question (?:est|, c'est)\b|\ben fin de compte\b|\bfondamentalement\b|\bdans un monde où\b|\bà l'ère d[eu']|\bà l'heure où\b|\ble cœur du problème\b|\bce qui compte vraiment\b|\bincarne(?:nt)? l'essence\b", "fake-depth", "fake depth: say the plain claim"),
    (r"\bet (?:ça|cela) change tout\b|\bpoint final\b|\brien de plus,? rien de moins\b|\bà méditer\b|\btout est dit\b|\bc'est toute la différence\b|^(?:en conclusion|en somme|pour résumer),|^(?:le résultat|la raison|la bonne nouvelle|le problème|la solution) \?", "closer", "dramatic closer or self-answered question: delete"),
    (r"\bsoyons clairs?\b|\bentendons-nous bien\b|\bque les choses soient claires\b|\bcontrairement aux idées reçues\b|\bcomprenez-moi bien\b|\bje ne dis pas que\b|\bloin de moi l'idée\b|\bcertains diront\b|\bon pourrait être tenté\b|\b(?:vous pensez peut-être|on pourrait (?:penser|croire)) qu[e']", "strawman", "arguing with nobody: remove"),
    (r"\bà ma connaissance\b|\bd'après mes (?:dernières )?(?:informations|données)\b|\bselon les informations disponibles\b|\bjusqu'à ma dernière mise à jour\b|\bbien que les (?:détails|informations) soient (?:limité|peu documenté)e?s\b|\bnon documentée?s? publiquement\b", "knowledge-hedge", "knowledge-limit hedge: delete"),
    (r"\bdans (?:cet article|ce guide|cette section|ce billet),? (?:nous|je) (?:allons|vais|verrons|verrai)\b|\bcomme (?:mentionné|évoqué|indiqué) (?:précédemment|plus haut|ci-dessus)\b", "meta", "writing about the text: give the content"),
    (r"\b(?:pourrai(?:t|ent)|peu(?:t|vent)|semble(?:nt)?) (?:potentiellement|éventuellement|peut-être|possiblement)\b|\bpourrai(?:t|ent) sembler\b|\bil se pourrait que\b[^.]{0,60}\b(?:peut-être|dans une certaine mesure|potentiellement)\b|\bil semblerait que\b[^.]{0,60}\b(?:peut-être|pourrait|potentiellement)\b", "stacked-hedge", "stacked hedge: keep one hedge"),
    (r"\b(?:les experts|(?:des|les|plusieurs) études|de nombreux (?:experts|observateurs|spécialistes)|les spécialistes) (?:s'accordent|disent|affirment|montrent|estiment|suggèrent|pensent)\b|\bil est (?:largement|généralement) (?:reconnu|admis)\b|\bselon certains observateurs\b", "vague-authority", "vague authority: name the source or delete"),
    (r",\s+(?:soulignant|témoignant|reflétant|illustrant|garantissant|assurant|favorisant|contribuant|renforçant|permettant|offrant|mettant en|symbolisant)\b", "ing-rider", "shallow '-ant' rider: delete or make it a sentence"),
    (r"\bjoue(?:nt)? un rôle (?:clé|crucial|essentiel|central|majeur|déterminant|primordial)\b|\bmarque(?:nt)? (?:un tournant|une étape (?:clé|majeure|importante))\b|\bl'avenir s'annonce\b|\bouvr(?:e|ent) la voie à\b|\blaisse(?:nt)? une empreinte\b|\bs'impos(?:e|ent) comme une référence\b|\bmalgré ces défis\b|\bfait (?:remarquable|notable)\b|\bde (?:façon|manière) impressionnante\b", "inflation", "inflated significance: say what happened"),
    (r"\b(?:est|sont|était|étaient) (?:lié|associé)e?s? (?:à|au|aux)\b|\ben lien avec\b|\ben relation avec\b|\bimpliquée?s? dans\b", "vague-association", "vague connection: name the relation (cause, fait partie de, a fondé)"),
    (r"\b(?:est|sont|était|étaient) en train d[e']", "progressive", "'en train de': use the present tense"),
    (r"\bs'inscri(?:t|vent|re) dans (?:une|la|cette) (?:dynamique|démarche|tendance|logique)\b|\bvien(?:t|nent) (?:renforcer|compléter|enrichir|corriger|s'ajouter|apporter|confirmer)\b|\bse veu(?:t|lent)\b|\bapport(?:e|ent|er) une réponse à\b", "empty-verb", "empty verb or phrase (§29): use the verb that carries the action"),
]

# §27: a connector at the start of a sentence
FR_CONNECTOR_RE = re.compile(
    r"^(?:ainsi|par ailleurs|en effet|de plus|en outre|notamment|dès lors|de surcroît|"
    r"d'autre part|d'une part|enfin|également|aussi|toutefois|cependant|néanmoins|par conséquent),?\s", re.I)

FR_ETRE = r"(?:est|sont|était|étaient|sera|seront|soit|soient|être|été)"
FR_PASSIVE_RE = re.compile(
    rf"(?<![sS]')(?<!\bse )\b{FR_ETRE}\s+(?:\w+ment\s+)?"
    r"(\w+(?:é|ée|és|ées)|faite?s?|mise?s?|prise?s?|écrite?s?|ouverte?s?|conçue?s?|reçue?s?|produite?s?|"
    r"construite?s?|détruite?s?|transmise?s?|requise?s?|fournie?s?|définie?s?|établie?s?|remplie?s?|"
    r"choisie?s?|convertie?s?|traduite?s?|incluse?s?|exclue?s?|résolue?s?|rendue?s?|vendue?s?|perdue?s?|"
    r"obtenue?s?|tenue?s?|maintenue?s?)\b", re.I)
FR_NOT_PASSIVE = re.compile(
    r"^(?:allé|arrivé|entré|rentré|resté|tombé|monté|passé|retourné|né|décédé|situé|censé|âgé|désolé|"
    r"occupé|fatigué|compliqué|adapté|dédié|élevé|privé|isolé|varié|détaillé|intéressé|pressé|"
    r"été|côté|qualité|sécurité|capacité|possibilité|priorité|propriété|société|activité|"
    r"réalité|utilité|simplicité|majorité|quantité|unité|nouveauté|difficulté|liberté|santé|"
    r"clé|moitié|marché|café|résumé|employé|degré)(?:e|s|es)?$", re.I)

_MONTHS = "Janvier|Février|Avril|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre"
_DAYS = "Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche"
_UNITS = r"km|kg|cm|mm|ms|Go|Mo|ko|To|GB|MB|kWh|Hz|px"

# (compiled regex on the prose line, T-rule, message). Case matters here.
FR_TYPO = [
    (re.compile(r"[A-Za-zÀ-ÿ0-9»)%][;!?](?=\s|$|[»)])"), "T1", "no space before ; ! ? (put a no-break space)"),
    (re.compile(r"[A-Za-zÀ-ÿ»)]:(?=\s|$)"), "T1", "no space before the colon (put a no-break space)"),
    (re.compile(r"\w\s[,.](?=\s|$)"), "T1", "space before a comma or a period"),
    (re.compile(r"«(?=\S)|(?<=\S)»"), "T2", "no space inside « » (put no-break spaces)"),
    (re.compile(r"[“”]|\"[^\"]{2,}\""), "T2", "English quotation marks: use « » in French prose"),
    (re.compile(r"(?:^|[.!?]\s+)A (?=partir|cause|condition|noter|l'|la |ce |cet|chaque|propos|présent|terme|défaut|titre|quel)"), "T4", "capital without accent: 'À'"),
    (re.compile(r"\b(?:Etat|Ecole|Etape|Etude|Ecran|Edition|Equipe|Element|Evenement|Egalement|Evidemment|Etant|Etre|Evite[rz])"), "T4", "capital without accent: 'É'"),
    (re.compile(rf"(?<=[a-zà-ÿ,] )(?:{_DAYS}|{_MONTHS})\b"),
     "T4", "day or month with a capital: use lower case"),
    (re.compile(rf"\d(?:[%€]|°C|(?:{_UNITS})\b)"), "T6", "no space between number and unit or symbol (put a no-break space)"),
    (re.compile(rf"\b\d+\.\d+[\s  ]?(?:[%€]|°C|(?:{_UNITS})\b)"), "T5", "decimal point: French uses a comma (do not change code or data)"),
    (re.compile(r"[€$£]\s?\d"), "T6", "currency symbol before the amount: write '150 €'"),
    (re.compile(r"\b\d{1,2}h\d{0,2}\b"), "T7", "time: write '9 h 30'"),
    (re.compile(r"\b\d+(?:ème|ième|eme)s?\b|\b1ère\b"), "T8", "ordinal: write '2e', '1re'"),
    (re.compile(r"\bMr\.?\s|\bMme\.|\bDr\.\s"), "T8", "abbreviation: 'M.', 'Mme', 'Dr'"),
    (re.compile(r"\betc\s?(?:\.{2,}|…)|\.{4,}"), "T8", "'etc.' takes one period. An ellipsis has three"),
    (re.compile(r"\b(?:[Oo]euvre|[Cc]oeur|[Ss]oeur|[Bb]oeuf|[Oo]eil|[Oo]euf|[Vv]oeu|[Nn]oeud|[Mm]anoeuvre)"), "T11", "ligature: write 'œ'"),
]

FR_MARKERS = set("le la les des une est et dans pour que qui avec sur pas vous nous ce cette du au aux sont plus par ne se son ses leur mais ou donc".split())
EN_MARKERS = set("the and is are of to in that with for this it you was be as on not have by from or but they their".split())

NBSP = " "


def detect_lang(text: str) -> str:
    words = re.findall(r"[a-zà-ÿœ]+", text.lower())
    fr = sum(w in FR_MARKERS for w in words)
    en = sum(w in EN_MARKERS for w in words)
    return "fr" if fr > en else "en"


@dataclass
class Finding:
    line: int
    rule: str
    message: str
    excerpt: str


def strip_markdown(text: str) -> list[tuple[int, str]]:
    """Return (line_no, line) for prose lines. Drop code blocks, tables, front matter."""
    out = []
    in_code = False
    in_front = False
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if i == 1 and line.strip() == "---":
            in_front = True
            continue
        if in_front:
            if line.strip() == "---":
                in_front = False
            continue
        if line.lstrip().startswith(("```", "~~~")):
            in_code = not in_code
            continue
        if in_code or line.lstrip().startswith("|") or line.startswith("    "):
            out.append((i, ""))
            continue
        line = re.sub(r"`[^`]*`", "CODE", line)            # inline code = 1 word
        line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)  # links
        line = re.sub(r"https?://\S+", "URL", line)
        if re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", line):
            out.append((i, ""))                               # each list item = own paragraph
            line = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line)
        line = re.sub(r"^\s*>\s?", "", line)                   # quotes
        line = re.sub(r"^#+\s+", "", line)                     # headings
        line = re.sub(r"\*\*|__|\*|_", "", line)
        out.append((i, line))
    return out


def paragraphs(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    paras, buf, start = [], [], None
    for no, line in lines:
        if line.strip():
            if start is None:
                start = no
            buf.append(line.strip())
        elif buf:
            paras.append((start, " ".join(buf)))
            buf, start = [], None
    if buf:
        paras.append((start, " ".join(buf)))
    return paras


def sentences(paragraph: str) -> list[str]:
    protected = re.sub(r"\b(e\.g|i\.e|etc|vs|Dr|Mr|Ms|No|M|MM|cf|p|ex|art|env)\.", lambda m: m.group(0).replace(".", "§"), paragraph)
    parts = re.split(r"(?<=[.!?:…])\s+(?=[A-ZÀ-ÖØ-Þ0-9\"'(«])", protected)
    return [p.replace("§", ".").strip() for p in parts if p.strip()]


def count_words(sentence: str) -> int:
    s = re.sub(r"\([^)]*\)", " PAREN ", sentence)         # parentheses = 1 word
    s = re.sub(r"\"[^\"]*\"|“[^”]*”|«[^»]*»", " QUOTE ", s)  # quoted text = 1 word
    s = re.sub(r"\b(\d[\d.,]*)\s*(%|ms|s|kb|mb|gb|tb|px|kg|g|m|cm|mm|km|h|min)\b", r"\1", s, flags=re.I)
    return len(WORD_RE.findall(s))


def is_imperative(sentence: str, lang: str = "en") -> bool:
    first = (WORD_RE.findall(sentence) or [""])[0].lower()
    if lang == "fr":
        return first.endswith("ez") or first in {"si", "quand", "lorsque", "avant", "après", "pour"}
    return first in {
        "add", "apply", "attach", "click", "close", "configure", "connect", "copy",
        "create", "delete", "disconnect", "do", "download", "edit", "enter", "examine",
        "find", "get", "give", "install", "keep", "let", "make", "measure", "monitor",
        "move", "open", "push", "pull", "put", "read", "remove", "replace", "restart",
        "run", "select", "send", "set", "start", "stop", "turn", "type", "update",
        "upload", "use", "write", "if", "when", "before", "after", "to",
    }


def check_en(no: int, line: str, raw: str, strict: bool, f: list[Finding]) -> None:
    low = line.lower()
    ex = line.strip()[:100]
    if "—" in line or " -- " in line:
        f.append(Finding(no, "dash", "em dash as sentence glue: use a period or colon", ex))
    for m in PASSIVE_RE.finditer(line):
        if m.group(1).lower() in NOT_PARTICIPLE:
            continue
        f.append(Finding(no, "passive", f"possible passive voice: '{m.group(0)}'", ex))
    for m in MODAL_PASSIVE_RE.finditer(line):
        f.append(Finding(no, "modal-passive", f"modal + passive: '{m.group(0)}'", ex))
    for m in PERFECT_RE.finditer(line):
        f.append(Finding(no, "perfect-tense", f"perfect tense: '{m.group(0)}'", ex))
    for m in PROGRESSIVE_RE.finditer(line):
        if m.group(1).lower() not in ING_NOUN_OK:
            f.append(Finding(no, "progressive", f"progressive tense: '{m.group(0)}'", ex))
    for m in re.finditer(r"(?:^|[.,;:]\s+|\b(?:by|while|when|after|before)\s+)(\w+ing)\b", line, re.I):
        w = m.group(1).lower()
        if w not in ING_NOUN_OK and len(w) > 4:
            f.append(Finding(no, "ing-form", f"'-ing' verb form: '{m.group(1)}'", ex))
    for p in PHRASAL:
        if re.search(rf"\b{re.escape(p)}\b", low):
            f.append(Finding(no, "phrasal-verb", f"phrasal verb '{p}'", ex))
    for pat, rule, msg in TELLS:
        if re.search(pat, line, re.I):
            f.append(Finding(no, rule, msg, ex))
    if re.search(r"[“”‘’]", raw):
        f.append(Finding(no, "curly-quotes", "curly quotes: use straight quotes in Markdown and code", ex))
    swaps = dict(SWAPS)
    if strict:
        swaps.update(STRICT_ONLY_SWAPS)
        if CONTRACTION_RE.search(line):
            f.append(Finding(no, "contraction", "contraction (not permitted in strict mode)", ex))
        if re.search(r"\b(?:check|test)(?:s|ed)?\s+(?:the|a|an|that|if|your|all)\b", low):
            f.append(Finding(no, "noun-only", "'check'/'test' used as a verb (STE: noun only)", ex))
    for word, alt in swaps.items():
        if re.search(rf"(?<![\w-]){re.escape(word)}(?![\w-])", low):
            f.append(Finding(no, "word", f"'{word}' -> {alt}", ex))


def check_fr(no: int, line: str, strict: bool, f: list[Finding]) -> None:
    ex = line.strip()[:100]
    # One plain form for the regexes: straight apostrophes, ordinary spaces.
    norm = line.replace("’", "'").replace(NBSP, " ").replace(" ", " ")
    low = norm.lower()
    core = norm.lstrip()
    if core[:1] in "—–":                                   # dialogue dash: correct in French
        core = core[1:]
    if re.search(r"\s[—–]\s|\w—\w| -- ", core):
        f.append(Finding(no, "dash", "dash as sentence glue: use a period, comma, colon or parentheses", ex))
    for m in FR_PASSIVE_RE.finditer(norm):
        if not FR_NOT_PASSIVE.match(m.group(1)):
            f.append(Finding(no, "passive", f"possible passive voice: '{m.group(0)}'", ex))
    for pat, rule, msg in FR_TELLS:
        if re.search(pat, low):
            f.append(Finding(no, rule, msg, ex))
    for rx, rule, msg in FR_TYPO:
        m = rx.search(line.replace("’", "'"))
        if m:
            f.append(Finding(no, f"typo-{rule}", f"{msg}: '{m.group(0).strip()}'", ex))
    swaps = FR_SWAPS + (FR_STRICT_SWAPS if strict else [])
    for pat, label, alt in swaps:
        if re.search(rf"(?<![\w-])(?:{pat})(?![\w-])", low):
            f.append(Finding(no, "word", f"'{label}' -> {alt}", ex))


def check(text: str, strict: bool, lang: str = "auto") -> list[Finding]:
    f: list[Finding] = []
    lines = strip_markdown(text)
    raw_by_no = dict(enumerate(text.splitlines(), 1))
    if lang == "auto":
        lang = detect_lang(" ".join(line for _, line in lines))

    for start, para in paragraphs(lines):
        sents = sentences(para)
        if lang == "fr" and len(sents) >= 3:
            hits = sum(bool(FR_CONNECTOR_RE.match(x.replace("’", "'"))) for x in sents)
            if hits >= 3 or (hits >= 2 and hits * 2 >= len(sents)):
                f.append(Finding(start, "connectors", f"{hits} of {len(sents)} sentences start with a connector (§27): keep only the ones the logic needs", para[:80]))
        if len(sents) > 6:
            f.append(Finding(start, "paragraph-length", f"{len(sents)} sentences in one paragraph (max 6)", para[:80]))
        for s in sents:
            n = count_words(s)
            limit = 20 if is_imperative(s, lang) else 25
            slack = 0 if strict else (5 if lang == "fr" else 3)
            if n > limit + slack:
                kind = "instruction" if limit == 20 else "description"
                f.append(Finding(start, "sentence-length", f"{n} words ({kind} max {limit})", s[:100]))

    for no, line in lines:
        if not line.strip():
            continue
        if ";" in line:
            f.append(Finding(no, "semicolon", "semicolon: write two sentences or a list", line.strip()[:100]))
        if lang == "fr":
            check_fr(no, line, strict, f)
        else:
            check_en(no, line, raw_by_no.get(no, ""), strict, f)
    f.sort(key=lambda x: (x.line, x.rule))
    return f


def summary(text: str) -> dict:
    paras = paragraphs(strip_markdown(text))
    sents = [s for _, p in paras for s in sentences(p)]
    counts = [count_words(s) for s in sents] or [0]
    return {
        "sentences": len(sents),
        "avg_words_per_sentence": round(sum(counts) / max(len(sents), 1), 1),
        "max_words_per_sentence": max(counts),
        "paragraphs": len(paras),
    }


# --- French no-break spaces (T1, T2, T6) ---

_SKIP_RE = re.compile(r"(`[^`]*`|https?://\S+|\]\([^)]*\)|<[^>]+>)")


def _fix_segment(seg: str) -> str:
    seg = re.sub(r"(?<=\S)[  ]([;:!?»])(?!\[)", NBSP + r"\1", seg)            # ordinary space -> no-break
    seg = re.sub(r"([A-Za-zÀ-ÿ0-9»)%])([;!?])(?=\s|$|[»)*_])", r"\1" + NBSP + r"\2", seg)  # missing space
    seg = re.sub(r"([A-Za-zÀ-ÿ»)])(:)(?=\s|$|[*_])", r"\1" + NBSP + r"\2", seg)
    seg = re.sub(r"« ?(?=\S)", "«" + NBSP, seg)
    seg = re.sub(r"(?<=[^\s ])»", NBSP + "»", seg)
    seg = re.sub(rf"(\d) (?=[%€$]|°C|(?:{_UNITS}|h|min|s)\b)", r"\1" + NBSP, seg)
    seg = re.sub(r"(\d)(?=[%€]|°C)", r"\1" + NBSP, seg)                           # 85% -> 85 %
    return seg


def fix_spaces(text: str) -> str:
    """Put no-break spaces where French typography needs them. Leave code, URLs and front matter."""
    out, in_code, in_front = [], False, False
    for i, line in enumerate(text.split("\n")):
        stripped = line.strip()
        if i == 0 and stripped == "---":
            in_front = True
        elif in_front:
            in_front = stripped != "---"
        elif stripped.startswith(("```", "~~~")):
            in_code = not in_code
        elif not in_code and not line.startswith("    ") and not re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line):
            parts = _SKIP_RE.split(line)
            line = "".join(p if k % 2 else _fix_segment(p) for k, p in enumerate(parts))
        out.append(line)
    return "\n".join(out)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Heuristic linter for AI tells and STE-style English and French (not a compliance checker, not an AI detector).")
    ap.add_argument("files", nargs="+", help="files to check, or - for stdin")
    ap.add_argument("--strict", action="store_true", help="strict mode: exact limits, more word rules")
    ap.add_argument("--lang", choices=["auto", "en", "fr"], default="auto", help="language of the text (default: auto-detect)")
    ap.add_argument("--fix-spaces", action="store_true",
                    help="French only: write no-break spaces before ; : ! ? », after « and before units. Changes the file in place (stdin goes to stdout)")
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args(argv)

    total = 0
    report = []
    for path in args.files:
        if path == "-":
            text = sys.stdin.read()
        else:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        lang = args.lang
        if lang == "auto":
            lang = detect_lang(" ".join(line for _, line in strip_markdown(text)))
        if args.fix_spaces:
            if lang != "fr":
                print(f"{path}: not French, no change (use --lang fr to force)", file=sys.stderr)
                if path == "-":
                    sys.stdout.write(text)
                continue
            fixed = fix_spaces(text)
            if path == "-":
                sys.stdout.write(fixed)
            else:
                if fixed != text:
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(fixed)
                print(f"{path}: {fixed.count(NBSP) - text.count(NBSP)} no-break space(s) added")
            continue
        findings = check(text, args.strict, lang)
        total += len(findings)
        stats = summary(text)
        if args.json:
            report.append({"file": path, "lang": lang, "stats": stats, "findings": [asdict(x) for x in findings]})
            continue
        print(f"{path} [{lang}]: {len(findings)} finding(s) | {stats['sentences']} sentences, "
              f"avg {stats['avg_words_per_sentence']} words, max {stats['max_words_per_sentence']}")
        for x in findings:
            print(f"  {x.line:>4}  {x.rule:<16} {x.message}")
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
