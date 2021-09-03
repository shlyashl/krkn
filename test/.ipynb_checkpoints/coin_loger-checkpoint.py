import random
import numpy as np


def bernoulli_list(tries, one_prob, rezolution):
    return [1 if random.randint(0, rezolution - 1) < rezolution * one_prob else 0 for i in np.arange(tries)]


def bernoulli_is_same_result_list(tries, one_prob, rezolution):
    # bernoulli_list [ for i in np.arange(tries)]

    is_same_list = []
    bernoulli_vals = []

    prev_bernoulli_val = 1 if random.randint(0, rezolution - 1) < rezolution * one_prob else 0
    for i in np.arange(tries):
        bernoulli_val = 1 if random.randint(0, rezolution - 1) < rezolution * one_prob else 0
        is_same_val = 1 if prev_bernoulli_val + bernoulli_val == 1 else 0
        if bernoulli_val == 1:
            is_same_list.append(is_same_val)


    return is_same_list


tries = 100000
one_prob = .5
rezolution = 100


for i in range(10):
    r = sum(bernoulli_is_same_result_list(tries, one_prob, tries))/tries
    print(r, '\n\n')


# for i in range(10):
#     r = sum(bernoulli_list(tries, one_prob, tries))/tries
#     print(r)