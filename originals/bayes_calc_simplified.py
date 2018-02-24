from numpy.random import beta as beta_dist
from numpy import percentile

import numpy as np

N_samp = 10000000 # number of samples to draw
c = 1 #used to vary sample size by a scalar multiplier

## INSERT YOUR OWN DATA HERE
clicks_A = (44)*c
views_A = (9610)*c
clicks_B = (426)*c
views_B = (83617)*c
alpha = 1#30 #prior
beta = 1#70 #prior
A_samples = beta_dist(clicks_A+alpha, views_A-clicks_A+beta, N_samp)
B_samples = beta_dist(clicks_B+alpha, views_B-clicks_B+beta, N_samp)

#confidence intervals: eg 2.5 = 95, 10 = 80
print [round(np.percentile((B_samples-A_samples)/B_samples, 2.5), 4), round(np.percentile((B_samples-A_samples)/B_samples, 97.5), 4)]
print [round(np.percentile((B_samples-A_samples)/B_samples, 10), 4), round(np.percentile((B_samples-A_samples)/B_samples, 90), 4)]

# percent lift needed
# base lift 1, 
'''
prev_p = 100
for i in range(10000):
  lift_perc = i * 0.01
  p = np.mean(B_samples >= A_samples*lift_perc) * 100
  if prev_p != p:
    print str(prev_p) + "% probability of a " + str(lift_perc) + "% lift"
    print str(p) + "% probability of a " + str(lift_perc) + "% lift"
  prev_p = p
  if p == 0.0:
    break
'''

lift_perc = 1.01
print np.mean(B_samples >= A_samples*1.01)
print np.mean(B_samples >= A_samples*1.03)
print np.mean(B_samples >= A_samples*1.05)
print np.mean(B_samples >= A_samples*1.08)
#print np.mean(B_samples >= A_samples*1.05)
#print np.mean(B_samples >= A_samples*1.10)
#print np.mean(B_samples >= A_samples*.99)
#print np.mean(A_samples > B_samples)
print np.mean(B_samples > A_samples)

AB_diff_samps = ((B_samples - A_samples) / A_samples)*100

print ""
print np.mean(B_samples > A_samples)

temp = []
temp2 = []
for i in range(1000000):
	temp.append(max(A_samples[i]-B_samples[i], 0.0))
	temp2.append(max(B_samples[i]-A_samples[i], 0.0))
B_cost = np.mean(temp)
A_cost = np.mean(temp2)

print "Cost of mistakenly choosing B: " + str(B_cost)
print "Cost of mistakenly choosing A: " + str(A_cost)

#actual_diff = str(B_cost - A_cost)
#print "the difference is " + actual_diff

print [-(np.mean(A_samples) - (np.mean(A_samples) - .02*np.mean(A_samples))), np.mean(A_samples) - (np.mean(A_samples) - .02*np.mean(A_samples))]
C_90_Int = [round(np.percentile((B_samples-A_samples)/A_samples, 5), 4), round(np.percentile((B_samples-A_samples)/A_samples, 90), 4)]
print "TEST"
print C_90_Int