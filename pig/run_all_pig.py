import os


args = [3,4,5]
script = "run_pig.sh"
for nb_worker in args:
    print('### EXECUTION WITH ', nb_worker, 'WORKERS ###')
    call_with_args = "bash ./'%s' '%s'" % (script, str(nb_worker))
    os.system(call_with_args)


# Save only the pages and their page rank (so delete neighbors which are useless here)
with open('pig_top_page_rank.txt', 'r') as fichier:
    # Read the lines from the file
    lignes = fichier.readlines()

with open('pig_top_page_rank.txt', 'w') as fichier:
    # Iterate through the lines
    for ligne in lignes:
        # Split the line into words using spaces as delimiters
        mots = ligne.split()

        # Keep only the first two words
        mots = mots[:2]

        # Join the first two words back into a line
        nouvelle_ligne = ' '.join(mots) + '\n'
        fichier.write(nouvelle_ligne)


print('bravo')