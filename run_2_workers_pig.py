import os

arg_test = 2
script = "run_pig.sh"
call_with_args = "bash ./pig/'%s' '%s'" % (script, str(arg_test))
os.system(call_with_args)

print('bravo')