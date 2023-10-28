# BENCHMARK 2023 COMPARAISON PAGE RANK EN PIG ET PYSPARK

Membres du groupe : Nathan DESHAYES, Nihel BELHADJ KACEM et Mathis EMERIAU

## Description du projet
Le but de cette expérience est de comparer les performances de l'algorithme pagerank entre une implémentation Pig et une implémentation PySpark.

Ici nous allons calculer le page rank avec plusieurs configurations de cluster --> 3 noeuds, 4 noeuds, 5 noeuds.

Premièrement, nous présentons les configurations utilisées pour réaliser cette expérience [Configuration et execution](#configuration). Ensuite nous comparons les temps d'exécution du pagerank avec des diagrammes à ligne brisée  [Pig VS Pyspark](#PgVSps). Finalement, nous illustrons les meilleurs pagerank calculés [ Les top 5 Résultats des pageranks :](#top5). 


<a id="configuration" style="color: white; ">

## Configuration et execution </a>
- Espace disque machine attribuée (maître/workers) : 500Mo d'espace disque
- La région où les clusters ont été utilisés est europe-central2. 

### Partie Pyspark :

Le fichier "run.sh" permet d'exécuter le pagerank sur un cluster à 4 workers. Pour le faire fonctionner et changer le nombre de workers, il faut changer le paramètre "num-workers" dans la commande de création du cluster (ligne 16) et changer les noms du paramètre "project" et du bucket pour mettre les siens à la place.

Le fichier "pagerank_notype.py" calcule 3 itérations de pagerank pour chaque ligne, sauvegarde les résultats sur le bucket et calcule le temps d'exécution total du pagerank avant de l'afficher en console.

Le fichier "récupèreTop5.py" prend en entrée les résultats de pagerank d'une exécution d'un cluster puis affiche en console les 5 meilleurs valeurs de pagerank.

### Partie Pig :

Le fichier [run_all_pig.py](./pig/run_all_pig.py) permet de lancer les exécutions afin de varier le nombre de noeuds (workers) à chaque fois. Il appelle à chaque exécution [run_pig.sh](./pig/run_pig.sh). Si vous voulez tester de ne lancer qu'une exécution avec 2 noeuds, il y a : [run_2_workers_pig.py](./pig/run_2_workers_pig.py).

Le fichier [run_pig.sh](./pig/run_pig.sh) permet de lancer le cluster qui va exécuter [dataproc.py](./pig/dataproc.py). C'est ici qu'il faut indiquer votre nom de projet, et votre bucket pour l'exécution. Les lignes de commandes qui permettent de copier les fichiers nécessaires à l'exécution sont en commentaires car on suppose que les fichiers ont déjà été copiés dans le bucket. Veillez à les remettre si nécessaire.

Le fichier [dataproc.py](./pig/dataproc.py) est celui qui va exécuter le code pig afin de calculer le page rank. On réalise 3 itérations pour le calcul et il crée un fichier texte afin de sauvegarder le temps d'exécution dans le bucket. On récupérera ensuite cette ligne et on l'insérera à la fin de [time_results.txt](./pig/time_results.txt) pour avoir le temps d'exécution de chacune des exécutions sur le projet. À la fin du calcul du page rank, on récupére les 5 premiers page rank dans le bucket que l'on va récupérer pour les mettre dans le projet dans le fichier [pig_top_page_rank.txt](./pig/pig_top_page_rank.txt).


<a id="PgVSps" style="color: white; ">

## Pig VS Pyspark </a>
Comparaison des temps d'exécution entre pig et pyspark de l'algorithme pagerank, pour chaque configuration de cluster utilisée :


![Texte alternatif](./diagramme.jpeg)

Sur ce graphique nous pouvons constater les points suivants:

- Pour Pig et Pyspark, plus il y a de workers et plus le temps d'exécution du cluster est court
- Pour le même nombre de workers, l'exécution en Pyspark est plus rapide que celle en Pig
- Faire passer le nombre de workers de 3 à 4 diminue fortement le temps d'exécution en Pig et Pyspark, surtout en comparaison du passage de 4 à 5 workers
<a id="top5" style="color: white; ">

## Les top 5 Résultats des pageranks </a>
Suite à l'exécution des clusters, nous avons déterminé que l'entité avec le meilleur pagerank est http://dbpedia.org/resource/Living_people, avec une valeur de pagerank de 36,794.33 (avec pyspark) et 33320.508 (avec Pig) . 

Voici ci-dessous le top 5 des entités ayant, en 3 itérations et avec l'implémentation pyspark, le meilleur pagerank :
| Rank| URL | PageRank |
| :----: | :---: | :---: |
| 🥇 | <http://dbpedia.org/resource/Living_people>  | 36794.33146754654 |
| 🥈 | <http://dbpedia.org/resource/United_States> | 13201.340151981207 |
| 🥉 | <http://dbpedia.org/resource/Race_and_ethnicity_in_the_United_States_Census> | 10371.162005541348 |
| 4 | <http://dbpedia.org/resource/List_of_sovereign_states> | 5195.347361862185 |
| 5 | <http://dbpedia.org/resource/United_Kingdom> | 4923.821309315207 |

Cependant, en utilisant l'implémentation Pig, les valeurs du PageRank sont différentes, ainsi que les entités placées en 4ème et 5ème positions :

 | Rank | URL | PageRank |
| :----: | :---: | :---: |
| 🥇 | <http://dbpedia.org/resource/Living_people> | 33320.508 |
| 🥈 | <http://dbpedia.org/resource/United_States> | 15212.145 |
| 🥉 | <http://dbpedia.org/resource/Race_and_ethnicity_in_the_United_States_Census> | 11309.122 |
| 4  | <http://dbpedia.org/resource/United_Kingdom> | 5373.2163 |
| 5  | <http://dbpedia.org/resource/France> | 5044.9463 |

Cette différence se trouve sûrement au niveau de l'algorithme de pig lorsque les jointures sont réalisées. Cependant, nous n'avons pas réussi à trouver une nouvelle implémentation pour que les résultats entre pig et pyspark soient les mêmes.