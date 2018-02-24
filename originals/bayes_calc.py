from numpy.random import beta as beta_dist
from threshold import bayesian_expected_error
from matplotlib import pyplot as plt
from matplotlib import ticker as mtick
from matplotlib.ticker import FuncFormatter
from calc_ab import pr_b_gt_a
import numpy as np

N_samp = 1000000 # number of samples to draw
c = 1 #used to vary sample size by a scalar multiplier

## INSERT YOUR OWN DATA HERE
clicks_A = (1773)*c
views_A = (211447)*c
clicks_B = (1804)*c # 
views_B = (207466)*c
alpha = 1#30 #prior
beta = 1#70 #prior
A_samples = beta_dist(clicks_A+alpha, views_A-clicks_A+beta, N_samp)
B_samples = beta_dist(clicks_B+alpha, views_B-clicks_B+beta, N_samp)

print [round(np.percentile((B_samples-A_samples)/B_samples, 2.5), 4), round(np.percentile((B_samples-A_samples)/B_samples, 97.5), 4)]
    #C_95_Int = [round(np.percentile((B_samples-A_samples), 2.5), 4), round(np.percentile((B_samples-A_samples), 97.5), 4)]
print [round(np.percentile((B_samples-A_samples)/B_samples, 10), 4), round(np.percentile((B_samples-A_samples)/B_samples, 90), 4)]

# percent lift needed
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

temp = []
temp2 = []
for i in range(1000000):
	#if A_samples[i] > B_samples[i]: temp.append(A_samples[i]-B_samples[i])
	temp.append(max(A_samples[i]-B_samples[i], 0.0))
	temp2.append(max(B_samples[i]-A_samples[i], 0.0))

print "Cost of mistakenly choosing B: " + str(np.mean(temp))
print "Cost of mistakenly choosing A: " + str(np.mean(temp2))

print [-(np.mean(A_samples) - (np.mean(A_samples) - .02*np.mean(A_samples))), np.mean(A_samples) - (np.mean(A_samples) - .02*np.mean(A_samples))]
C_90_Int = [round(np.percentile((B_samples-A_samples)/A_samples, 5), 4), round(np.percentile((B_samples-A_samples)/A_samples, 90), 4)]
print "TEST"
print C_90_Int

print "  "
print bayesian_expected_error([views_A, views_B], [clicks_A, clicks_B])
print pr_b_gt_a(clicks_A, views_A-clicks_A, clicks_B, views_B-clicks_B) < .03
#print np.mean(B_samples > A_samples)
#print np.mean( 100.*(A_samples - B_samples)/B_samples > 3 )
plt.figure(1)

plt.subplot(211)
formatter = FuncFormatter(lambda x, y: str(x) + '%')
plt.gca().xaxis.set_major_formatter(formatter)
plt.title('Beta Posterior of Variation (Green) and Control (Blue)')

plt.hist(A_samples*100, bins=75)
#plt.subplot(312)
plt.hist(B_samples*100, bins=75)
#plt.subplot(313)
plt.subplot(212)
plt.title('Beta Posterior of $\Delta$ % Increase')
plt.hist((B_samples-A_samples)/B_samples * 100, bins = 100, histtype='stepfilled', alpha=0.85, label='Beta posterior of $\Delta$', color='#A60628', normed=True)
plt.annotate('Probability %s \nis greater \nthan %s: %.2f' % ("Variation", "Control", np.mean(B_samples > A_samples)), (0,30))
#plt.vlines(0, 0, 50, linestyle='--', color='black')
#plt.autoscale()
# fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
formatter = FuncFormatter(lambda x, y: str(x) + '%')
plt.gca().xaxis.set_major_formatter(formatter)

#plt.axis([0, .10, -20, 20])
# #
plt.tight_layout()
plt.show()
