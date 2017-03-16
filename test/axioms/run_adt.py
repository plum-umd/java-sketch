import subprocess, sys

NUM_TESTS=subprocess.check_output(['find', 'input_adt', '-name', 'm[0-9].sk']).count('\n')
NUM_TRIALS=int(sys.argv[1])

with open('results_adt.csv', 'w') as f: pass
for i in range(NUM_TESTS):
    times = []
    for j in range(NUM_TRIALS):
        print 'test {}, trial {}'.format(i,j)
        nm = 'input_adt/m{}.sk'.format(i)
        t = subprocess.check_output(['sketch', '--fe-inc', 'input_adt/', nm],
                                    stderr=subprocess.STDOUT)
        start = t.rfind('Total time = ') + len('Total time = ')
        times.append(float(t[start:t.find('\n', start)]))
    # times.append(sum(times)/len(times))
    with open('results_adt.csv', 'a') as f:
        [f.write('{:.2f}\t'.format(n)) for n in times]
        f.write('\n')


