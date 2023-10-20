import os

args = [2,4,6]

for nb_worker in args:
    call_with_args = "bash ./pig/run_test.sh '%s'" % (str(nb_worker))
    os.system(call_with_args)


print('bravo')