import os

results_file_name = "results.txt"
os.system("rm '%s'" % (results_file_name))

pr_results_file_name = "pig_small_page_rank.txt"
os.system("rm '%s'" % (pr_results_file_name))

args = [2,4] # add 6 later
script = "run_pig.sh"
for nb_worker in args:
    print('### EXECUTION WITH ', nb_worker, 'WORKERS ###')
    call_with_args = "bash ./pig/'%s' '%s'" % (script, str(nb_worker))
    os.system(call_with_args)


print('bravo')