# La typographie française (T1 à T12)

Appliquez ces règles à tout texte français, après la passe 1 et la passe 2. Elles suivent le *Lexique des règles typographiques en usage à l'Imprimerie nationale* et les recommandations de l'Académie française.

Une typographie anglaise dans un texte français est aussi un indice d'IA : pas d'espace avant « ? », des guillemets droits, un point décimal, une majuscule à chaque mot du titre.

## Ce que vous ne touchez pas

- Le code, les commandes, les chemins, les URL, les données et le YAML.
- Les citations exactes et les noms de produits.
- La valeur d'un nombre. Vous changez sa forme, jamais sa valeur. Si `1,000` est ambigu (mille ou un), ne changez rien et signalez-le.
- Le balisage Markdown. Le signe `-` d'une liste reste un `-`.

## Quand ces règles cèdent

SKILL.md et ce fichier se contredisent sur trois points. Voici la règle qui gagne.

| Sujet | Usage typographique | Règle de ce skill |
|---|---|---|
| Incise | Le tiret demi-cadratin encadre une incise. | §8 gagne. Pas de tiret d'incise. Utilisez des virgules ou des parenthèses. |
| Point-virgule | Il termine les éléments d'une liste. | S15 gagne. Pas de point-virgule. Voir T10. |
| Guillemets | Les guillemets droits sont anglais. | T2 gagne dans la prose française. §21 reste vrai pour le code. |

## Les règles

### T1. Les espaces et la ponctuation

| Signe | Avant | Après |
|---|---|---|
| virgule, point, points de suspension | rien | une espace |
| deux-points, point-virgule, point d'exclamation, point d'interrogation | une espace insécable | une espace |
| apostrophe | rien | rien |
| parenthèse ouvrante, crochet ouvrant | une espace | rien |
| parenthèse fermante, crochet fermant | rien | une espace, sauf devant une virgule ou un point |

**Avant :** `Vraiment? Attention! Voici: un cas.`

**Après :** Vraiment ? Attention ! Voici : un cas.

L'espace insécable est le caractère U+00A0. Elle empêche le signe de passer seul à la ligne suivante. Si la cible ne la conserve pas (terminal, message de commit, formulaire en texte brut), une espace ordinaire est admise. Ne supprimez jamais l'espace.

En mode fichier, lancez `python scripts/ste_check.py --fix-spaces FICHIER` après la réécriture. La commande pose les espaces insécables de T1, T2 et T6. Elle ne touche pas au code ni aux URL.

### T2. Les guillemets

- Citation dans la prose : les guillemets français « », avec une espace insécable à l'intérieur de chaque guillemet.
- Citation dans une citation : les guillemets anglais doubles, sans espace intérieure.
- Ne cumulez pas l'italique et les guillemets.
- Un identifiant, une valeur ou un libellé d'interface reste dans son format de code.

**Avant :** `Il a dit "bonjour".`

**Après :** Il a dit « bonjour ».

### T3. L'apostrophe

- Texte publié (article, lettre, billet) : l'apostrophe typographique (’, U+2019).
- Fichier technique en Markdown, code, commande : l'apostrophe droite (').
- Suivez l'usage du fichier. Ne mélangez pas les deux dans un même texte.

### T4. Les majuscules

- Les majuscules portent leurs accents et leur cédille : À, É, È, Ç, Œ. Les sigles n'en portent pas (ENA).
- Les jours, les mois, les langues et les adjectifs de nationalité prennent une minuscule : lundi, janvier, le français, une entreprise allemande.
- Le nom d'un peuple prend une majuscule : les Français.
- Après un deux-points : une minuscule, sauf si une citation ou une phrase complète commence.
- Titre de section : une majuscule au premier mot et aux noms propres. Pas de majuscule à chaque mot.
- Titre d'œuvre qui commence par un article défini : majuscule à l'article, au premier nom et aux adjectifs placés avant ce nom (*Le Rouge et le Noir*, *La Petite Marchande de prose*). Sinon, majuscule au premier mot seulement (*Un amour de Swann*).

**Avant :** `A partir de Lundi, les Meilleures Pratiques De Sécurité changent.`

**Après :** À partir de lundi, les meilleures pratiques de sécurité changent.

### T5. Les nombres

- Le signe décimal est la virgule : 25,50.
- Une espace insécable sépare les groupes de trois chiffres : 1 000, 5 000 000.
- Dans un texte courant, écrivez en lettres de zéro à seize, et en chiffres au-delà. Un nombre suivi d'un symbole reste en chiffres : 5 km, 12 %.
- Un nombre en lettres prend son unité en lettres : deux cents kilomètres.
- Les nombres composés prennent des traits d'union : vingt-trois, quatre-vingt-dix.
- Dans un texte technique, gardez la forme de la source (chiffres ou lettres). Les numéros de version, les ports et les identifiants ne changent jamais.

### T6. Les unités et les symboles

- Une espace insécable précède le symbole : 200 km, 25 kg, 85 %, 25 °C, 48 €.
- Pas de point abréviatif et pas de pluriel : 200 km.
- Respectez la casse du symbole : m, kg, A, Mo.
- Le symbole monétaire suit le montant : 150,00 €.
- Les signes mathématiques prennent une espace insécable de chaque côté : 2 + 2 = 4.

**Avant :** `Le taux atteint 99.5% pour $20 par mois.`

**Après :** Le taux atteint 99,5 % pour 20 $ par mois.

### T7. Les dates et les heures

- Date : jour, mois en lettres sans majuscule, année. Exemple : le samedi 9 septembre 2023.
- Date numérique dans un tableau : 17-09-1980.
- Heure : le symbole h entre deux espaces insécables, sur 24 heures. Exemples : 9 h 30, 14 h 05.
- Minutes inférieures à dix : avec un zéro. Écrivez 8 h 05.
- Un horodatage technique (ISO 8601, journal d'exécution) ne change pas.

### T8. Les abréviations, les ordinaux et les sigles

- Point abréviatif si la dernière lettre du mot manque : M., etc., cf.
- Pas de point si la dernière lettre reste : Mme, Dr.
- « Monsieur » s'abrège « M. », pas `Mr`.
- « etc. » prend un seul point. Il ne précède jamais des points de suspension.
- Numéro : `n<sup>o</sup>` ou nº (U+00BA). Le signe degré ne convient pas.
- Ordinaux : 1er, 1re, 2e, 3e. Pas `2ème`. Siècles en chiffres romains : le XVIe siècle.
- Sigles : en capitales, sans points, sans pluriel, en romain (SNCF, AFNOR).
- Les points de suspension sont trois, jamais quatre.

### T9. Les tirets et le trait d'union

| Signe | Usage | Espaces |
|---|---|---|
| trait d'union (-) | mots composés (c'est-à-dire), inversion (dit-il, est-ce) | aucune |
| tiret demi-cadratin (–) | intervalle entre deux nombres ou deux dates : 1998–2000 | aucune |
| tiret cadratin (—) | début d'une réplique de dialogue | une espace insécable après |
| signe moins (−) | calcul | une espace insécable de chaque côté |

L'incise entre tirets est correcte en typographie. Ce skill la retire quand même (§8), sauf si l'échantillon de l'auteur en contient.

Dans un dialogue, chaque réplique commence sur une nouvelle ligne. L'incise courte reste entre virgules : « Je vous assure, dit-il, que c'est vrai. »

### T10. Les listes

- En Markdown, gardez le balisage de liste (`-` ou `1.`).
- Choisissez une forme et gardez-la dans toute la liste.
- Forme 1 : chaque élément est une phrase. Il commence par une majuscule et finit par un point.
- Forme 2 : les éléments sont courts. Ils commencent par une minuscule et n'ont pas de ponctuation finale.
- N'utilisez pas la forme classique avec un point-virgule à la fin de chaque élément (S15).

### T11. Les ligatures

- La ligature œ est obligatoire : œuvre, cœur, sœur, bœuf, œil, nœud, manœuvre.
- La ligature æ s'emploie dans ex æquo et curriculum vitæ.
- Les ligatures fi et fl sont décoratives. Laissez la police les gérer.

### T12. L'italique

- Titres d'œuvres : livres, films, tableaux.
- Mots étrangers qui ne sont pas entrés dans le français. Un terme du métier courant (commit, build) reste en romain.
- Pas d'italique pour le nom d'une institution étrangère (Yale University).
- « cf. » et « N.B. » restent en romain.

## La mise en page

Ces règles s'appliquent seulement si vous produisez un document mis en page (Word, PDF, HTML). Elles ne concernent pas le texte brut ni le Markdown.

- Césure : coupez entre deux syllabes. Ne coupez pas un nom propre, ni autour d'une apostrophe, ni pour isoler une seule lettre.
- Ne laissez pas un signe de ponctuation en début de ligne.
- Évitez la ligne veuve (dernière ligne d'un paragraphe seule en haut de page) et la ligne orpheline (première ligne seule en bas de page).
- Faites l'alinéa avec un retrait de première ligne, pas avec une tabulation.
- Placez un titre plus près du texte qui le suit que du texte qui le précède.
- Utilisez les petites capitales pour les siècles en chiffres romains.

## Liste de contrôle

1. Une espace insécable précède chaque « : », « ! » et « ? » (T1).
2. Les citations sont entre « » (T2).
3. Les majuscules ont leurs accents. Les jours et les mois sont en minuscules (T4).
4. Les nombres ont une virgule décimale et une espace avant l'unité (T5, T6).
5. Les heures suivent le modèle 9 h 30 (T7).
6. Le texte ne contient ni tiret d'incise ni point-virgule (§8, S15).
7. Le code, les URL et les valeurs n'ont pas changé.
