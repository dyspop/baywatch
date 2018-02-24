from numpy.random import beta as beta_dist
from numpy import mean, sqrt, percentile, histogram
from scipy.stats import norm, invgamma

def draw_mus(N, xbar, SSD, m0, k0, s_sq0, v0, n_samples=10000):
    # SSD = variance
    # combining the prior with the datva - page 79 of Gelman et al.
    # to make sense of this note that
    # inv-chi-sq(v,s^2) = inv-gamma(v/2,(v*s^2)/2)
    kN = float(k0 + N)
    mN = (k0/kN)*m0 + (N/kN)*xbar
    vN = v0 + N
    vN_times_s_sqN = v0*s_sq0 + SSD + (N*k0*(m0-xbar)**2)/kN

    # 1) draw the variances from an inverse gamma
    # (params: alpha, beta)
    alpha = vN/2
    beta = vN_times_s_sqN/2
    # thanks to wikipedia, we know that:
    # if X ~ inv-gamma(a,1) then b*X ~ inv-gamma(a,b)
    sig_sq_samples = beta*invgamma.rvs(alpha, size=n_samples)

    # 2) draw means from a normal conditioned on the drawn sigmas
    # (params: mean_norm, var_norm)
    mean_norm = mN
    var_norm = sqrt(sig_sq_samples/kN)
    mu_samples = norm.rvs(mean_norm, scale=var_norm, size=n_samples)

    # 3) return the mu_samples and sig_sq_samples
    return mu_samples

c = 1
c_conversions = 1770*c
c_visits = 211385*c
v_conversions = 1799*c
v_visits = 207434*c
#lift_perc = .03
c_mean = 80.03
c_var = 503950.69
v_mean = 78.64
v_var = 493547.51

N_samp = 75000
clicks_A = c_conversions
views_A = c_visits
clicks_B = v_conversions
views_B = v_visits
alpha = 1
beta = 1
A_conv_samps = beta_dist(clicks_A+alpha, views_A-clicks_A+beta, N_samp)
B_conv_samps = beta_dist(clicks_B+alpha, views_B-clicks_B+beta, N_samp)

A_order_samps = draw_mus(c_conversions, c_mean, c_var, 0, 1, 1, 1, N_samp)
B_order_samps = draw_mus(v_conversions, v_mean, v_var, 0, 1, 1, 1, N_samp)

A_rps_samps = A_conv_samps*A_order_samps
B_rps_samps = B_conv_samps*B_order_samps

# set current winner
if (mean(A_rps_samps) >= mean(B_rps_samps)):
     Current_Winner_rps_samps = A_rps_samps
     Current_Loser_rps_samps = B_rps_samps
     current_winner_str = "CHOOSE CONTROL"
else:
     Current_Winner_rps_samps = B_rps_samps
     Current_Loser_rps_samps = A_rps_samps
     current_winner_str = "CHOOSE VARIATION"

# check for minimum precision in lift delta percentage
AB_diff_samps = ((B_rps_samps - A_rps_samps) / A_rps_samps)*100
if ((percentile(AB_diff_samps, 95)-percentile(AB_diff_samps, 5)) <= 8):
    print "STOP - " + current_winner_str
    #quit()
elif ((percentile(AB_diff_samps, 95)-percentile(AB_diff_samps, 5)) >= 15):
    print "CONTINUE - MIN PREC NOT MET"
    #quit()


if (mean(Current_Winner_rps_samps > Current_Loser_rps_samps*(1.03)) >= .9):
     print "STOP - " + current_winner_str + " 3%"
elif (mean(Current_Winner_rps_samps > Current_Loser_rps_samps*(1.01)) >= .9):
     print "STOP - " + current_winner_str + " 1%"
else:
     print "CONTINUE - SIG NOT REACHED"

#print conf
print mean(A_rps_samps)
print mean(B_rps_samps)
print mean(B_rps_samps > A_rps_samps)
print mean(AB_diff_samps)
#print histogram(AB_diff_samps)
#print [(percentile(B_rps_samps, .5)*1.03-percentile(B_rps_samps, .5)*.97)*.8]
print [percentile(AB_diff_samps, 95)-percentile(AB_diff_samps, 5)]
#print [percentile(AB_diff_samps, 5), percentile(AB_diff_samps, 50), percentile(AB_diff_samps, 95)]

print 
#return conf
