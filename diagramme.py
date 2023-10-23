import matplotlib.pyplot as plt

with open ('results.txt', 'r') as fichier 
     temps_execution=[]
     nombre_workers=[]
     for ligne in fichier:
         mots = ligne.split()
         nb_workers = int(mots[mots.index("workers") - 1])
         temps = int(mots[mots.index("seconds") - 1])
         nombre_workers.append(nb_workers)
         temps_execution.append(temps)

#plt.grid(True)
# with open ('results_pyspark.txt', 'r') as fichier 
#      temps_dex2=[]
#      workers_nbr2=[]
#      for ligne in fichier:
#         mots = ligne.split()
#         nb_workers = int(mots[mots.index("workers") - 1])
#         temps = int(mots[mots.index("seconds") - 1])
#         nombre_workers.append(nb_workers)
#         temps_execution.append(temps)

plt.plot(nombre_workers, temps_execution, marker='o')
#plt.plot(nombre_workers2, temps_execution2, marker='x')
plt.xlabel('Nombre de Workers')

plt.ylabel('Temps d\'exécution (secondes)')
plt.title('Diagramme Temps d\'exécution en fonction du Nombre de Workers')

plt.show()