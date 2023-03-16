import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import argparse
from tqdm import tqdm
import pandas as pd
import sys

from utils import fit_scipy_distributions


parser = argparse.ArgumentParser(description='Simulate permutations and yield critical significance values')
parser.add_argument("--total", type=int, help='Size of the total set')
parser.add_argument("--subset", type=int, help='Size for each random subset')
parser.add_argument("--hits", type=int, help='Size for the random subset of hits of which we are interested to see how many are included within each random subset')
parser.add_argument("--permutations", type=int, default=1000, help='Number of permutations')
parser.add_argument("--tail", type=int, default=1, help='1 or 2, if 1 the num. of SD for critical value is 1.645 (one-tailed), if 2 this value is 1.96 (two-tailed), default one-tailed')
parser.add_argument("--bins", type=int, default=20, help='Number of bins to use in the historgram')

args = parser.parse_args()

n_total_set = args.total
n_subset = args.subset
n_hits = args.hits
n_permutations = args.permutations

results_permutations = []
for perm in range(n_permutations):
	# print(f'perm: {perm}')
	# create list of hits, within the total set limits
	hits = random.sample(range(n_total_set), n_hits)
	# print(f'hits: {hits}')
	# draw subset randomly from total set
	subset = random.sample(range(n_total_set), n_subset)
	# print(f'subset: {subset}')
	# check how many hits are in the subset
	hits_present = 0
	for hit in hits:
		if hit in subset:
			# print(f'hit found in subset: {hit}')
			hits_present += 1
	results_permutations.append(hits_present)

mean_hits = np.mean(results_permutations)
sd_hits = np.std(results_permutations, ddof=1)
if args.tail == 1:
	print("\nOne-tailed test\n")
	num_sd = 1.645
elif args.tail == 2:
	print("\nTwo-tailed test\n")
	num_sd = 1.96
else:
	sys.exit("Error: --tail value different from 1 or 2")
margin_of_error = sd_hits * num_sd

critical_val_right = mean_hits + margin_of_error
critical_val_left = mean_hits - margin_of_error
# normality test
stat, p = st.shapiro(results_permutations)
alpha = 0.05

print(results_permutations)
print(f'mean: {mean_hits}')
print(f'SD: {sd_hits}')
print(f'margin of error: {margin_of_error}')
print(f'critical value (right): {critical_val_right}')
print(f'critical value (left): {critical_val_left}')
# normality test
print('Statistics=%.3f, p=%.3f' % (stat, p))
if p > alpha:
	print('Sample looks Gaussian (fail to reject H0)')
else:
	print('Sample does not look Gaussian (reject H0)')
	# print list of most likely distributions
	print("\nList of most likely distributions: \n")
	print(fit_scipy_distributions(results_permutations, bins=100))

# histogram
plt.hist(results_permutations, bins=args.bins)
# plt.show()
plt.savefig("permutations.png")

# print distribution values to file
with open("permutations.txt", "w") as out:
	for perm in results_permutations:
		out.write(str(perm) + "\n")
