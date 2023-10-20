import os


arg_test = 2
call_with_args = "bash ./pig/run_test.sh '%s'" % (str(arg_test))
os.system(call_with_args)

print('bravo')