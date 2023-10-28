# BENCHMARK 2023 COMPARAISON PAGE RANK EN PIG ET PYSPARK

Membres de groupes : Nathan DESHAYES, Nihel BELHADJ KACEM et Mathis EMERIAU

## Description du projet
Le but de cette expérience c'est de comparer les performances de l'algorithme pagerank, entre une implémentation Pig et une implémentation PySpark.

comparaison des performances sur pagerank, entre une implantation Pig et une implantation PySpark (Comme dans la video NDSI 2012). Je veux plusieurs configurations de cluster --> 3 noeuds, 4 noeuds, 5 noeuds.

Les données sont dans le bucket google cloud : gs:///public_lddm_data/

Les code sources sont dispos à: https://github.com/momo54/large_scale_data_management



## Configuration et execution
- Espace disque machine attribuée (maître/workers) : 500Mo d'espace disque
- La région où les clusters ont été utilisés est europe-central2. 

### Partie Pyspark :

Le fichier "run.sh" permet d'exécuter le pagerank sur un cluster à 4 workers. Pour le faire fonctionner et changer le nombre de workers, il faut changer le paramètre "num-workers" dans la commande de création du cluster (ligne 16) et changer les noms du paramètre "project" et du bucket pour mettre les siens à la place.

Le fichier "pagerank_notype.py" calcule 3 itérations de pagerank pour chaque ligne, sauvegarde les résultats sur le bucket et calcule le temps d'exécution total du pagerank avant de l'afficher en console.

Le fichier "récupèreTop5.py" prend en entrée les résultats de pagerank d'une exécution d'un cluster puis affiche en console les 5 meilleurs valeurs de pagerank.

### Partie Pig :
Le fichier [run_pig.sh](./pig/run_pig.sh) permet d'exécuter le pagerank sur un cluster à 4 workers. Pour le faire fonctionner et changer le nombre de workers, il faut changer le paramètre "num-workers" dans la commande de création du cluster (ligne 16) et changer les noms du paramètre "project" et du bucket pour mettre les siens à la place.

Le fichier "[dataproc.py](./pig/run_pig.sh)" calcule 3 itérations de pagerank pour chaque ligne, sauvegarde les résultats sur le bucket et calcule le temps d'exécution total du pagerank avant de l'afficher en console.

Le fichier "[pig_top_page_rank.txt](./pig/pig_top_page_rank.txt)" prend en entrée les résultats de pagerank d'une exécution d'un cluster puis affiche en console les 15 meilleurs valeurs de pagerank.


## Temps d'exécution

### Partie Pyspark : 
- 3 workers : 31,91 minutes
- 4 workers : 23,35 minutes
- 5 workers : 22,53 minutes

### Partie Pig :
- 3 workers : 41,733 minutes
- 4 workers : 35,3833 minutes
- 5 workers : 33,05 minutes

## Résultats 5 des pageranks:
Nous avons obtenu que l'entité avec le meilleur pagerank c'est l'uri http://dbpedia.org/resource/Living_people, avec un pagerank de 36,794.33. On présente ci-après le top 5 des uris ayant le meilleur pagerank, issue de 3 itérations de l'algorithme pagerank.
| Rank| URL | PageRank |
| :----: | :---: | :---: |
| 🥇 | <http://dbpedia.org/resource/Living_people>  | 36794.33146754654 |
| 🥈 | <http://dbpedia.org/resource/United_States> | 13201.340151981207 |
| 🥉 | <http://dbpedia.org/resource/Race_and_ethnicity_in_the_United_States_Census> | 10371.162005541348 |
| 4 | <http://dbpedia.org/resource/List_of_sovereign_states> | 5195.347361862185 |
| 5 | <http://dbpedia.org/resource/United_Kingdom> | 4923.821309315207 |



## Pig VS Pyspark
Ci-après suit un diagramme à ligne brisée illustrant la comparaison des temps d'exécution entre les implémentations pagerank, pour chaque configuration de cluster utilisée:


![Texte alternatif](./diagramme.jpeg)

Sur ce graphique nous pouvons constater les points suivants:

- Pig est l'implémentation la moins performante avec peu des noeuds, ce qui pourrait s'expliquer par les écritures des résultats intermediaries sur le disque avec des ressources limitées.
- PySpark avec du partitionnement est l'implémentation qui performe le mieux en moyen, néanmoins cette implémentation atteint un seuil à 4 noeuds.
- Pig bénéficie le plus de l'augmentation du nombre de noeuds, ce qui devient plus évident dans le range de 4 à 5 noeuds. Nous pouvons apprécier que les implémentations sur PySpark atteignent un seuil dans leurs temps d'exécution dans cette range de 4 à 5 noeuds, tandis que le temps d'exécution continue à diminuer pour Pig.
- L'implémentation sur Pig rattrape l'implémentation sur PySpark Basic pour la configuration à 5 noeuds.
- Avec des ressources limitées (2 noeuds), Pyspark ne semble pas bénéficier d'une amélioration en raison du partionnement.
Les meilleurs pagerank computés dans le cadre de ces exécutions sont présentés dans la section suivante.

## Conclusion:
