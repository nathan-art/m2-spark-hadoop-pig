import os

results_file_name = "results.txt"
os.system("rm '%s'" % (results_file_name))

args = [2,4,6]
script = "run_pig.sh"
for nb_worker in args:
    call_with_args = "bash ./pig/'%s' '%s'" % (script, str(nb_worker))
    os.system(call_with_args)


print('bravo')