import matplotlib.pyplot as plt


with open ('./pig/time_results.txt', 'r') as fichier :
     temps_execution=[]
     nombre_workers=[]
     for ligne in fichier:
          mots = ligne.split()
          nb_workers = int(mots[mots.index("workers)") - 1])
          temps= float(mots[mots.index("seconds.") - 1])
          nombre_workers.append(nb_workers)
          temps_execution.append(temps)


temps_execution2=[1914.6, 1401, 1320]

plt.plot(nombre_workers, temps_execution, marker='o',label='pig')
plt.plot(nombre_workers, temps_execution2, marker='x',label='spark')
plt.xlabel('Nombre de Workers')
plt.ylabel('Temps d\'exécution (seconde)')
plt.title('Diagramme Temps d\'exécution en fonction du Nombre de Workers')
plt.legend(loc='upper right')
plt.savefig("diagramme.jpeg") 