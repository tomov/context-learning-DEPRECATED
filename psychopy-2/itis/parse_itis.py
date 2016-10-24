# assumes outputs generated by gen.sh using optseq2 
# (in folder par, etc)
#

import os
import sys
import csv
import random

# expand the ITI / stim sequence with choice, off times, etc
#
def denormalize(jitter, stimTime, stim):
    choice = []
    off = []
    cueId = []
    contextId = []
    t = 0
    for i in range(len(stimTime)):
        choice.append(t)
        t += stimTime[i]
        off.append(t)
        t += jitter[i]

        stim_i = stim[i].lower()
        if 'x1' in stim_i:
            cueId.append(0)
        elif 'x2' in stim_i:
            cueId.append(1)
        else:
            assert 'x3' in stim_i
            cueId.append(2)

        if 'c1' in stim_i:
            contextId.append(0)
        elif 'c2' in stim_i:
            contextId.append(1)
        else:
            assert 'c3' in stim_i
            contextId.append(2)

    return choice, off, cueId, contextId

# parse an ITI / stim sequence from a given csv file
#
def parse(fname):
    duration = []
    start = []
    stim = []
    with open(fname) as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            row = filter(None, row)
            start.append(float(row[0]))
            duration.append(float(row[2]))
            stim.append(row[4])
    jitter = duration[1::2]
    stimTime = duration[0::2]
    start = start[0::2]
    stim = stim[0::2]
    assert len(stimTime) == len(stim)

    choice, off, cueId, contextId = denormalize(jitter, stimTime, stim)
    assert choice == start, " wtf " + str(choice) + " vs " + str(start)

    #print choice
    #print off
    #print jitter
    #print stimTime
    #print stim
    return choice, off, jitter, stimTime, stim, cueId, contextId


# generate a test ITI / stim sequence for 1 run
#
def gen_test():
    stim = ['x1c1', 'x1c3', 'x3c1', 'x3c3']
    random.shuffle(stim)

    jitter = [2, 4, 6] # randomly shuffle ITI's of 2, 4, and 6 seconds, one of each
    random.shuffle(jitter)
    jitter.append(0) # no ITI after last test trial

    stimTime = [6] * 4 # each test trial is 6 seconds


    choice, off, cueId, contextId = denormalize(jitter, stimTime, stim)

    print choice
    print off
    print jitter
    print stimTime
    print stim
    return choice, off, jitter, stimTime, stim, cueId, contextId

if __name__ == "__main__":
    pars = os.listdir("par")

    train = []
    test = []

    for fname in pars:
        if fname.endswith('.par'):
            print fname
            x = parse(os.path.join("par", fname))
            if fname.startswith('itis_test'):
                test.append(x)
            else:
                train.append(x)

    assert len(train) % 9 == 0, "Should have multiple of 9 (# runs per subject) files; found " + str(len(train)) + " instead"
    n_subjects = len(train) / 9

    # these days we generate the test ITI / stim sequences manually
    #
    if len(test) == 0:
        for _ in range(len(train)):
            x = gen_test()
            test.append(x)

    next_train_idx = 0
    next_test_idx = 0
    # this is the file we potentially give to katie to analyze our stuff
    # note that this format is wrong -- her script requires a different format
    # but that's okay b/c we don't really need her analysis right now
    #
    with open('for_katie.csv', 'w') as f:
        cols = ['Subject', 'Run', 'Trial', 'Choice', 'Off', 'Jitter', 'StimTime', 'cueId', 'contextId']
        f.write(','.join(cols) + '\n')
        for subj in range(n_subjects):
            for run in range(9):
                # write it out the itis for each subject for each run in a separate file
                # this is crucial for psychopy to work in fMRI mode -- it reads the itis from here
                # format = trial # (0-based), jitter (in s), cueId (0-based), contextId (0-based)
                # this is parsed in the psychopy file, in new_run routine, in shuffleRestaurantsAndFoods code block
                #
                itis_file = os.path.join('csv', 'con%03d_run%d_itis.csv' % (subj, run))
                with open(itis_file, 'w') as itif:
                    itif.write(','.join(['trialN', 'itiTime', 'cueId', 'contextId']) + '\n')

                    # write training trials
                    #
                    choice, off, jitter, stimTime, stim, cueId, contextId = train[next_train_idx]
                    assert sum(jitter) == 144 - 4 * 20, "Sum of train jitters is wrong: " + str(sum(jitter))
                    for i in range(20):
                        row = [subj + 1, run + 1, i + 1, choice[i], off[i], jitter[i], stimTime[i], stim[i], cueId[i], contextId[i]]
                        f.write(','.join(str(x) for x in row) + '\n')
                        itif.write(','.join(str(x) for x in [i, jitter[i], cueId[i], contextId[i]]) + '\n')

                    next_train_idx += 1
                   
                    # write test trials
                    #   
                    t = off[-1] + jitter[-1] # starting point for test trials
                    choice, off, jitter, stimTime, stim, cueId, contextId = test[next_test_idx]
                    for i in range(4):
                        row = [subj + 1, run + 1, i + 20 + 1, choice[i] + t, off[i] + t, jitter[i], stimTime[i], stim[i], cueId[i], contextId[i]]
                        f.write(','.join(str(x) for x in row) + '\n')
                        itif.write(','.join(str(x) for x in [i + 20, jitter[i], cueId[i], contextId[i]]) + '\n')
                    assert sum(jitter) == 36 - 6 * 4, "Sum of test jitters is wrong: " + str(sum(jitter))
                    next_test_idx += 1
