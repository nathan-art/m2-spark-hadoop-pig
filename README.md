# BENCHMARK 2023 COMPARAISON PAGE RANK EN PIG ET PYSPARK

Membres de groupes : Nathan DESHAYES, Nihel BELHADJ KACEM et Mathis EMERIAU

## Description du projet

comparaison des performances sur pagerank, entre une implantation Pig et une implantation PySpark (Comme dans la video NDSI 2012). Je veux plusieurs configurations de cluster --> 3 noeuds, 4 noeuds, 5 noeuds.

Les données sont dans le bucket google cloud : gs:///public_lddm_data/

Les code sources sont dispos à: https://github.com/momo54/large_scale_data_management

### Configuration du cluster sur Google Cloud

Espace disque machine attribuée (maître/workers) : 500Mo d'espace disque


## Partie Pyspark

### Configuration et execution

La région où les clusters ont été utilisés est europe-central2. La zone utilisée est europe-central2-c. 

Les données sur lesquelles le pagerank est appliqué sont partitionnées en 15 morceaux.

Le fichier "run.sh" permet d'exécuter le pagerank sur un cluster à 4 workers. Pour le faire fonctionner et changer le nombre de workers, il faut changer le paramètre "num-workers" dans la commande de création du cluster (ligne 16) et changer les noms du paramètre "project" et du bucket pour mettre les siens à la place.

Le fichier "pagerank_notype.py" calcule 3 itérations de pagerank pour chaque ligne, sauvegarde les résultats sur le bucket et calcule le temps d'exécution total du pagerank avant de l'afficher en console.

Le fichier "récupèreTop5.py" prend en entrée les résultats de pagerank d'une exécution d'un cluster puis affiche en console les 5 meilleurs valeurs de pagerank.

### Temps d'exécution

- 3 workers : 31,91 minutes
- 4 workers : 23,35 minutes
- 5 workers : 22,53 minutes


### Résultats

Top 5 des pageranks :

1. http://dbpedia.org/resource/Living_people> : 36794.33146754654
2. http://dbpedia.org/resource/United_States> : 13201.340151981207
3. http://dbpedia.org/resource/Race_and_ethnicity_in_the_United_States_Census> : 10371.162005541348
4. http://dbpedia.org/resource/List_of_sovereign_states> : 5195.347361862185
5. http://dbpedia.org/resource/United_Kingdom> : 4923.821309315207
