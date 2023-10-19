import os

arg1 = 2

call_with_args = "bash ./pig/run_test.sh 2"
#call_with_args = "bash ./pig/run_test.sh '%s'" % (str(arg1))

res = os.system(call_with_args)

print('hbjdzjhesdjdsehsdhvhjdfdfdfjdjdjdfjdjfjdfdfjkddjf', res)