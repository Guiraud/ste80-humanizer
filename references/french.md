# Le français : passe 1 et passe 2

Lisez ce fichier avant de modifier un texte français. Il donne les tics d'IA en français (§1 à §29), les règles de structure adaptées au français (S1 à S15) et les mots simples. La typographie (T1 à T12) est dans `french-typography.md`.

Les numéros sont ceux de SKILL.md. Signalez vos corrections avec ces numéros, par exemple « §1, §12, S6, T1 ».

ASD-STE100 est une norme pour l'anglais. Ce fichier applique ses règles de structure au français. Il ne suit pas un dictionnaire contrôlé français. Écrivez « en style STE », jamais « conforme STE ».

## Trois principes

- Travaillez en français. Ne traduisez pas le texte.
- Gardez le registre de l'auteur. Gardez son choix entre « tu » et « vous », et son choix sur l'écriture inclusive. Un seul choix par texte.
- Les règles de fidélité de SKILL.md s'appliquent sans changement : gardez chaque fait, chaque nombre et chaque degré de certitude.

## Passe 1 : les tics d'IA en français

Les numéros §1 à §26 suivent le catalogue de blader/humanizer. La section G (§27 à §29) ajoute trois tics propres au français. Elle reprend la section G de ferr079/humanizer-fr.

*Faible seul* signifie : agissez seulement si d'autres tics sont proches. Plusieurs tics ensemble font un indice. Un seul tic faible ne prouve rien.

### A. Mettre en scène au lieu de dire (agir dès la première occurrence)

| § | Tic | À repérer | Correction |
|---|---|---|---|
| 1 | Pas X mais Y | ce n'est pas seulement X, c'est Y. Non seulement X, mais aussi Y. Il ne s'agit pas de X, mais de Y. Ne se contente pas de X, il Y. Bien plus qu'un X. Loin d'être un simple X. Le même contraste sur deux phrases : « Cela ne veut pas dire X. Cela veut dire Y. » Une queue négative : « …, zéro prise de tête », « …, sans friction » | Dites le fait. Gardez le contraste seulement si le lecteur croit X, ou si les deux moitiés portent une information. |
| 2 | Chutes et fragments | « Et ça change tout. » « Tout est dit. » « C'est toute la différence. » « À méditer. » Une question suivie de sa réponse : « Le résultat ? Un gain de temps. » « En conclusion », « En somme », « Pour résumer » suivis d'une redite. Une rafale : « Pas de cloud. Pas d'abonnement. Pas de compromis. » | Supprimez la chute qui répète. Gardez-la si elle ajoute un fait. Fusionnez les fragments en une affirmation. |
| 3 | Fausse profondeur | au fond, en réalité, la vraie question est, ce qui compte vraiment, le cœur du problème, X est le langage de Y, X n'est pas un outil mais un miroir, incarne l'essence même de | Écrivez l'affirmation précise. |
| 4 | Entrée en scène | il est important de noter que, il convient de souligner que, à l'ère de, dans un monde où, dans le paysage actuel de, plongeons dans, entrons dans le vif du sujet, sans plus attendre, voici ce qu'il faut retenir, maintenant que nous avons posé les bases, « Franchement ? », « La vérité, c'est que » | Supprimez l'amorce. Commencez par le fait. « Franchement » au milieu d'une phrase familière est normal. |
| 5 | Débat sans adversaire | soyons clairs, entendons-nous bien, comprenez-moi bien, je ne dis pas que, loin de moi l'idée de, certains diront que, on pourrait être tenté de, contrairement aux idées reçues | Supprimez la défense. Gardez une objection que le texte attribue à quelqu'un, ou une option que le lecteur envisage vraiment. |

**Avant :**
> Ce n'est pas seulement un outil de build plus rapide, c'est une nouvelle façon de penser votre pipeline.

**Après :**
> L'outil de build met chaque étape en cache. Après une petite modification, la reconstruction prend quelques secondes.

**Avant :**
> Nous avons déplacé l'API vers la périphérie. Le résultat ? Une latence de 40 ms. Et ça change tout.

**Après :**
> Nous avons déplacé l'API vers la périphérie. La latence est maintenant de 40 ms.

**Avant (fausse alternative) :**
> Les jetons changent toutes les 24 heures. On pourrait être tenté de redémarrer le service par une tâche cron, mais cela couperait les sessions. La rotation se fait à chaud.

**Après :**
> Les jetons changent toutes les 24 heures. La rotation se fait à chaud, sans couper les sessions.

### B. Le rythme mécanique

| § | Tic | À repérer | Correction |
|---|---|---|---|
| 6 | Triades forcées | « rapide, fiable et évolutif ». Trois exemples parallèles puis une leçon. Trois faits courts puis une morale | Gardez trois éléments seulement si le sens en a trois. |
| 7 | Débuts répétés *(faible seul)* | Il lit... Il vérifie... Il lance... | Fusionnez les phrases ou commencez par l'action. Une répétition voulue pour le rythme reste. Pour les connecteurs en tête de phrase, voir §27. |
| 8 | Tirets partout | l'incise entre tirets (— ou –), ` -- ` | Aucun tiret d'incise dans le texte final, sauf si l'échantillon de l'auteur en emploie. Utilisez un point, une virgule, un deux-points ou des parenthèses. Le tiret de dialogue et le tiret d'intervalle restent (T9). |
| 9 | Précautions empilées *(faible seul)* | pourrait potentiellement, peut éventuellement, il se pourrait que, dans une certaine mesure, de manière générale, il semblerait que | Gardez une seule précaution si la source la donne. « Peut-être » et « souvent » seuls sont des habitudes humaines. |
| 10 | Paires à trait d'union | Ce tic est anglais. | Ne l'appliquez pas. Le numéro reste pour garder la correspondance. Les règles du trait d'union sont en T9. |
| 11 | Phrases sans sujet *(faible seul)* | « Aucun compte requis. Données synchronisées. » | Nommez l'acteur (S6). Le passif et « on » sont plus courants en français qu'en anglais. En passe 1, seul leur usage systématique est un tic. |

**Avant :**
> Le nouveau tableau de bord est rapide, intuitif et puissant.

**Après :**
> Le nouveau tableau de bord se charge en moins d'une seconde. Il affiche toutes les alertes sur une page.

### C. L'enflure et l'autorité empruntée

Le fait est souvent juste. Gardez le fait et supprimez l'habillage.

| § | Tic | À repérer | Correction |
|---|---|---|---|
| 12 | Mots usés par l'IA | crucial, primordial, incontournable, véritable (comme intensif), robuste (au figuré), fluide, transparent (au figuré), clé en main, à la pointe, en constante évolution, novateur, holistique, pléthore, myriade, panoplie, levier, synergie, écosystème (au figuré), paysage (au sens abstrait), pierre angulaire, décrypter, méticuleux, exploiter, tirer parti de | Utilisez le mot simple (liste plus bas). Gardez le sens technique : un système robuste aux pannes, un écosystème biologique. |
| 13 | Importance gonflée | marque un tournant, joue un rôle clé, témoigne de, s'impose comme une référence, ouvre la voie à, laisse une empreinte durable, un héritage durable, « Malgré ces défis, … continue de prospérer », l'avenir s'annonce prometteur, « fait remarquable », « de façon impressionnante ». Une section « Défis et perspectives » toute faite | Gardez le fait. Terminez sur le dernier fait concret. Si la source donne de vrais projets, citez-les. |
| 14 | Lien vague | lié à, associé à, en lien avec, en relation avec, impliqué dans | Nommez la relation que la source donne. Si elle ne la donne pas, gardez la tournure vague. N'inventez pas un rôle. |
| 15 | Participes présents en fin de phrase | « , soulignant », « , témoignant de », « , illustrant », « , reflétant », « , symbolisant », « , permettant ainsi de », « , garantissant », « , mettant en valeur » | Supprimez la fin de phrase, sauf si la source appuie son affirmation. |
| 16 | Langage de vente | révolutionnaire, époustouflant, de pointe, de classe mondiale, de renom, sans précédent, à couper le souffle, niché au cœur de, riche patrimoine, une expérience unique, un cadre exceptionnel, un large éventail, un engagement fort en faveur de | Dites ce que la chose est et ce qu'elle fait. |
| 17 | Autorité empruntée | les experts s'accordent, il est largement reconnu, beaucoup pensent, selon certains observateurs, plusieurs études montrent (sans les citer). Une liste de médias prestigieux. Un nombre d'abonnés | Nommez qui a dit quoi, ou supprimez. N'inventez jamais une source. L'absence de source seule n'est pas un tic. |
| 18 | Éviter « être » et « avoir » | constitue, représente, s'avère, se révèle être, se positionne comme, s'impose comme, joue le rôle de, fait office de, dispose de, bénéficie de, arbore, propose (pour « a ») | Écrivez « est », « sont », « a ». |

**Avant :**
> La version 2.0 marque un tournant, témoignant d'une évolution plus large vers des outils pensés pour les développeurs.

**Après :**
> La version 2.0 ajoute une interface en ligne de commande. Elle ne prend plus en charge Node 16.

**Avant (lien vague) :**
> Il est associé à l'orchestre Rajhans, qu'il a fondé et qu'il dirige.

**Après :**
> Il a fondé l'orchestre Rajhans et le dirige.

Les termes du métier ne sont pas des tics. Gardez « commit », « build », « pull request » si l'équipe les utilise.

### D. La mise en forme mécanique

| § | Tic | À repérer | Correction |
|---|---|---|---|
| 19 | Gras décoratif | des mots en gras sans raison, une étiquette en gras et un deux-points sur chaque élément de liste | Supprimez le gras. Passez la liste en prose si les étiquettes n'apportent rien. Gardez le gras pour les avertissements et les libellés d'interface. |
| 20 | Titres décoratifs | Des Majuscules À Chaque Mot, des émojis, des flèches (→), un filet horizontal entre chaque section, un titre de niveau 1 qui répète le titre du document | Une majuscule au premier mot et aux noms propres (T4). Nommez le contenu de la section. Donnez le titre une seule fois. |
| 21 | Guillemets droits ou anglais *(faible seul)* | `"..."` ou `“...”` pour une citation dans la prose | Utilisez « » (T2). Beaucoup de claviers produisent des guillemets droits. Laissez le code tel quel. |

### E. Les restes du dialogue et du brouillon (supprimer)

| § | Tic | À repérer | Correction |
|---|---|---|---|
| 22 | Restes de chatbot | Excellente question !, Bien sûr !, Vous avez tout à fait raison, Voici un…, J'espère que cela vous aide, N'hésitez pas à, Souhaitez-vous que je, En tant que modèle de langage, En tant qu'IA | Supprimez l'emballage. Gardez le contenu. |
| 23 | Limites de connaissance | à ma connaissance, d'après mes dernières informations, selon les informations disponibles, bien que les détails soient limités, non documenté publiquement. Une supposition après l'aveu : « elle a probablement grandi », « ce qui suggère » | Dites ce que la source ne montre pas, ou supprimez. Ne comblez pas le vide. |
| 24 | Titre répété | « ## Sécurité » puis « La sécurité est importante. » | Supprimez cette ligne. |
| 25 | Texte sur le document | Dans cet article, nous allons voir. Le tableau ci-dessous compare. Comme mentionné précédemment. A été ajouté pour remplacer. Généré à partir de | Parlez du sujet, pas du document. Gardez une source que le lecteur peut suivre. |

Dans une lettre, « Je reste à votre disposition » et « Veuillez agréer » sont des formules normales. Ne les supprimez pas.

### F. Écrire pour le mauvais lecteur

| § | Tic | À repérer | Correction |
|---|---|---|---|
| 26 | Réexpliquer ce que le lecteur sait | une réponse qui répète le problème et le diagnostic avant la décision | Commencez par la décision. Gardez le seul fait qui manque au lecteur. |

### G. Propre au français

| § | Tic | À repérer | Correction |
|---|---|---|---|
| 27 | Connecteurs en surnombre *(faible seul)* | un connecteur en tête de presque chaque phrase : ainsi, par ailleurs, en effet, de plus, en outre, notamment, dès lors, de surcroît, force est de constater que | Supprimez les connecteurs que la logique ne demande pas. Un connecteur utile reste. C'est la série qui fait le tic. |
| 28 | Anglicismes calqués | adresser un problème, supporter (un format), délivrer (un service), initier (un projet), impacter, au final, faire sens, être en charge de, une opportunité (une occasion), digital (numérique), « définitivement » pour « vraiment », « éventuellement » pour « finalement » | Utilisez le tour français : traiter, prendre en charge, livrer, lancer, toucher, finalement, avoir du sens, être chargé de, une occasion, numérique. Gardez le calque s'il est devenu l'usage du lecteur. |
| 29 | Verbes et formules vides | mettre en lumière, s'inscrire dans une démarche, venir + infinitif (« vient renforcer »), permettre de (en série), se veut, apporter une réponse à, procéder à | Gardez le verbe qui porte l'action (S8). |

**Avant :**
> Ainsi, le serveur démarre. Par ailleurs, il journalise les erreurs. De plus, il envoie une alerte.

**Après :**
> Le serveur démarre, journalise les erreurs et envoie une alerte.

**Avant :**
> Cette version adresse le bug et supporte désormais IPv6.

**Après :**
> Cette version corrige le bug et prend désormais en charge IPv6.

**Avant :**
> Cette mise à jour s'inscrit dans une démarche de sécurité et vient corriger deux failles.

**Après :**
> Cette mise à jour corrige deux failles.

### Quand ne pas agir

- Une citation, un titre d'œuvre, un nom propre, ou une phrase qui parle de la tournure au lieu de l'employer.
- Une répétition voulue pour le rythme : « Je suis venu, j'ai vu, j'ai vaincu. »
- Un texte écrit avant le 30 novembre 2022.
- Les détails qui portent la voix de l'auteur : un détail précis et inattendu, des sentiments mêlés, de l'argot d'une époque, une vraie digression ou une autocorrection.

## Passe 2 : la structure STE80 en français

Les quinze règles de SKILL.md s'appliquent. Ce tableau donne ce qui change en français.

| S | Règle | En français, à 80 % | Strict |
|---|---|---|---|
| 1 | Une idée par phrase. Une action par étape. | Deux faits liés partagent une phrase avec « et » ou « parce que ». | Une seule affirmation. |
| 2 | Instructions : 20 mots. Descriptions : 25 mots. Un mot élidé et le mot suivant comptent pour un (« l'outil »). | Le français demande souvent plus de mots que l'anglais. Acceptez jusqu'à 25 et 30 mots. | Limites fixes : 20 et 25. |
| 3 | La condition d'abord, puis la commande. | « Si le voyant est rouge, coupez l'alimentation. » | Identique |
| 4 | Gardez les articles, « que » et le « ne » de la négation. | Les fragments sont admis dans les tableaux, les titres et les libellés. | Jamais. |
| 5 | Une suite d'étapes ou d'options devient une liste verticale. Numérotez les étapes. | Ne découpez pas un raisonnement en puces. | Identique |
| 6 | Voix active. Nommez l'acteur. | Passif admis si l'acteur est inconnu. Évitez « on » quand vous connaissez l'acteur. Évitez le passif pronominal (« le fichier se charge par le serveur »). | Identique |
| 7 | Temps simples : présent, passé composé, imparfait, futur simple, impératif. | Le passé composé est le passé normal. Pas de passé simple hors récit. Pas de futur antérieur ni de conditionnel passé. | Identique |
| 8 | Mettez l'action dans le verbe. | « vérifier », pas « procéder à la vérification de ». Pas de chaînes de participes présents ni de gérondifs. | Identique |
| 9 | Modaux francs : « peut », « doit », le futur. | « devrait » et « pourrait » pour un vrai doute ou un conseil. | Seulement peut, doit, futur. |
| 10 | Mots simples, un seul sens par mot. | Gardez un mot quand le remplacement sonne faux. Gardez les termes du métier. | Mots simples seulement. |
| 11 | Un terme par chose. | L'école enseigne à varier les mots. Dans un texte technique, ne le faites pas. | Identique |
| 12 | Pas de chaîne de noms. | Trois compléments avec « de » au plus. Coupez la chaîne avec un verbe. | Identique |
| 13 | Un sujet par paragraphe, six phrases au plus. | Identique | Identique |
| 14 | Séparez les étapes et les descriptions. L'avertissement précède l'étape. | Identique | Identique |
| 15 | Pas de point-virgule. Tirets : §8. | La typographie suit T1 à T12. | Pas d'abréviation « etc. ». |

### Les instructions

Écrivez les étapes à l'impératif avec « vous » : « Ouvrez le fichier. » Si le texte source utilise l'infinitif (« Ouvrir le fichier ») ou « tu », gardez ce choix. Un seul mode par procédure.

### Exemples

**S6, voix active. Avant :**
> Le jeton est validé par la passerelle avant que la requête ne soit transmise.

**Après :**
> La passerelle valide le jeton. Ensuite, elle transmet la requête.

**S8, le verbe porte l'action. Avant :**
> Il convient de procéder à la mise à jour de la base avant d'effectuer le redémarrage du service.

**Après :**
> Mettez la base à jour. Ensuite, redémarrez le service.

**S12, chaîne de noms. Avant :**
> la procédure de mise à jour de la configuration du serveur de base de données de production

**Après :**
> la procédure qui met à jour la configuration du serveur de production. Ce serveur héberge la base de données.

**S1 et S9, une idée par phrase et un modal franc. Avant :**
> Le fichier de configuration, qui est chargé au démarrage et dont les valeurs pourraient éventuellement être remplacées par des variables d'environnement, contrôle la taille du cache.

**Après :**
> Le fichier de configuration contrôle la taille du cache. L'application lit ce fichier au démarrage. Des variables d'environnement peuvent remplacer ses valeurs.

« Pourraient éventuellement » devient « peuvent », pas « remplacent ». La certitude garde sa force.

## Les mots simples

Utilisez le remplacement s'il sonne juste. Sinon, gardez le mot.

| Au lieu de | Écrivez |
|---|---|
| exploiter, tirer parti de, avoir recours à | utiliser |
| effectuer, réaliser, procéder à | faire, ou le verbe direct |
| débuter, initier | commencer, lancer |
| finaliser | terminer |
| nécessiter | demander, avoir besoin de |
| permettre de (répété) | le verbe direct : « l'outil trie », pas « l'outil permet de trier » |
| mettre en lumière, mettre en exergue, souligner | montrer, dire |
| impacter | toucher, changer |
| solutionner | résoudre |
| s'avérer, constituer, représenter | être |
| disposer de, bénéficier de | avoir |
| être en mesure de, être susceptible de | pouvoir |
| avoir pour but de | servir à |
| afin de, dans le but de, en vue de | pour |
| suite à | après, à cause de |
| au sein de | dans |
| au niveau de | dans, pour, sur |
| dans le cadre de | pour, pendant |
| par le biais de, via | par, avec |
| en termes de | pour |
| dans la mesure où | parce que, si |
| néanmoins, toutefois, cependant | mais |
| par conséquent | donc |
| en outre, de surcroît | aussi, ou rien |
| il convient de | il faut, ou l'impératif |
| il est important de noter que | supprimez |
| à l'heure actuelle | aujourd'hui, maintenant |
| la quasi-totalité de | presque tous |
| un certain nombre de | plusieurs, ou le nombre |
| crucial, primordial | important, ou le fait |
| robuste | fiable, solide |
| adresser (un problème) | traiter, résoudre |
| supporter (un format) | prendre en charge |
| délivrer (un service) | livrer, fournir |
| une opportunité | une occasion |
| digital | numérique |
| vient renforcer, vient corriger | renforce, corrige |
| se veut simple | est simple, ou supprimez |
| s'inscrire dans une démarche de | supprimez, ou le verbe direct |

## Exemple complet

**Texte source :**
> Excellente question ! Les sondes de vivacité de Kubernetes constituent un mécanisme puissant permettant au kubelet de déterminer si un conteneur est sain — et ce n'est pas seulement un contrôle de santé, c'est votre première ligne de défense. Lorsqu'une sonde échoue, le conteneur est automatiquement redémarré par le kubelet, garantissant ainsi la disponibilité de votre application. Néanmoins, il est important de noter que des sondes mal configurées pourraient potentiellement provoquer des redémarrages en cascade, c'est pourquoi des paramètres comme `initialDelaySeconds` et `failureThreshold` doivent être ajustés avec soin.
>
> Réglez-les bien, et votre cluster se répare tout seul.

**Résultat :**
> Une sonde de vivacité indique au kubelet si un conteneur est sain. Si la sonde échoue, le kubelet redémarre le conteneur. L'application reste ainsi disponible.
>
> Une sonde mal configurée peut aussi provoquer des redémarrages en cascade. Pour l'éviter, ajustez `initialDelaySeconds` et `failureThreshold` avec soin.

Corrections : §22 l'ouverture, §18 « constituent », §16 « mécanisme puissant », §8 le tiret, §1 « pas seulement », §15 « garantissant ainsi », §4 « il est important de noter », S10 « néanmoins », §9 « pourraient potentiellement », §2 la chute. Puis S6 la voix active, S1 une idée par phrase, S14 l'instruction séparée, T1 les espaces.

Chaque fait reste : le kubelet, le redémarrage, la disponibilité, les redémarrages en cascade et les deux paramètres. « Pourraient potentiellement » devient « peut », pas « provoque ».
