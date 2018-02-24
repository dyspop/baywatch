from numpy.random import beta as beta_dist
from numpy import mean, sqrt, percentile, var
from flask import jsonify
from scipy.stats import norm, invgamma
import math
import numpy as np

def calculate_statistics(pool, events, samples_to_draw):
  #useful for identifying which variables are possible to be pulled out for scaling or different distributions, despite appearing like arbitrary abstractions
  c = 1 #used to vary sample size by a scalar multiplier
  alpha = 1 #30 #prior
  beta = 1 #70 #prior
  views = pool*c
  clicks = events*c

  return beta_dist(clicks+alpha, views-clicks+beta, samples_to_draw)

def cost_of_mistaken_choice(A_conv_samples, B_conv_samples, samples_to_draw):
  costs = {}
  temp = []
  temp2 = []

  for i in range(samples_to_draw):
    temp.append(max(A_conv_samples[i]-B_conv_samples[i], 0.0))
    temp2.append(max(B_conv_samples[i]-A_conv_samples[i], 0.0))

  costs["test"] = np.mean(temp)
  costs["base"] = np.mean(temp2)

  return costs

def draw_mus(N, xbar, SSD, m0, k0, s_sq0, v0, n_samples):
  #no idea how this part works, see ../originals/ for notes
  kN = float(k0 + N)
  mN = (k0/kN)*m0 + (N/kN)*xbar
  vN = v0 + N
  vN_times_s_sqN = v0*s_sq0 + SSD + (N*k0*(m0-xbar)**2)/kN
  alpha = vN/2
  beta = vN_times_s_sqN/2
  sig_sq_samples = beta*invgamma.rvs(alpha, size=n_samples)
  var_norm = sqrt(sig_sq_samples/kN)
  mu_samples = norm.rvs(mN, scale=var_norm, size=n_samples)

  return mu_samples

def ab_test(base_pool, test_pool, base_events, test_events, samples_to_draw):

  results = {}
  confidence_intervals = {}
  probabilities_of_lifts = {} 
  winners = {}
  precision_in_lift_delta_percentage = {}
  choose_winner_at_precision_in_lift_delta_percentage = {}

  #this a/b relationship is evident in a few places, and could be made a more general function to extend to more variations.
  #these are not a separate function so that we use the same sample beta distributions for further operations
  #conversion samples
  A_conv_samples = calculate_statistics(base_pool, base_events, samples_to_draw)
  B_conv_samples = calculate_statistics(test_pool, test_events, samples_to_draw)
  
  #mus
  # A_order_samples = draw_mus(base_events, mean(A_conv_samples), var(A_conv_samples), 0, 1, 1, 1, samples_to_draw)
  # B_order_samples = draw_mus(test_events, mean(B_conv_samples), var(B_conv_samples), 0, 1, 1, 1, samples_to_draw)

  A_order_samples = draw_mus(base_events, mean(A_conv_samples), var(A_conv_samples), 0, 1, 1, 1, samples_to_draw)
  B_order_samples = draw_mus(test_events, mean(B_conv_samples), var(B_conv_samples), 0, 1, 1, 1, samples_to_draw)

  A_rps_samples = A_conv_samples*A_order_samples
  B_rps_samples = B_conv_samples*B_order_samples

  #is A/base winner
  A_winner_state = (mean(A_rps_samples) >= mean(B_rps_samples))

  # set current winner and loser
  # cast to strings because while eval returns a bool it won't serialize with jsonify in a list of key pairs
  winners["base"] = str(A_winner_state)
  winners["test"] = str(not (A_winner_state))

  for i in range (100):
    #confidence intervals
    confidence = 100-i
    confidence_intervals[confidence] = [round(np.percentile((B_conv_samples-A_conv_samples)/B_conv_samples, confidence/2), 4), round(np.percentile((B_conv_samples-A_conv_samples)/B_conv_samples, i), 4)]
    #lifts percentages
    lift = (i*0.01)+1
    p = np.mean(B_conv_samples >= A_conv_samples*lift)
    if p > 0.001:
        lift = (lift-1)
        probabilities_of_lifts[p] = lift
    if p == 0:
      break

  # #attempt at elegant precision representation, something's off w/the returned number though. more precise trends from 100 toward 50, less precise from 50 toward 100
  # AB_diff_samples = ((B_rps_samples - A_rps_samples) / A_rps_samples)*100
  # for i in range (100):
  #   if (percentile(AB_diff_samples, 100-i)-percentile(AB_diff_samples, i) <= 8) == True:
  #     results["precision_in_lift_delta_percentage"] = precision_in_lift_delta_percentage = 100-i
  #     break

  # note that means and variance as computed by numpy appear very different than expected values in the hardcoded source scripts
  # AB_diff_samples = ((B_rps_samples - A_rps_samples) / A_rps_samples)*100
  # return "c_mean = " + str(mean(A_conv_samples)) + " c_var = " + str(var(A_conv_samples))  + " v_mean = " + str(mean(B_conv_samples)) + " v_var = " + str(var(B_conv_samples))

  # working check for minimum precision in lift delta percentage based very literally on /originals/rpv_stop_crit.py 
  # i don't like this because it assumes 95 precision and sloppily uses the eval overlap in <= 8 and >= 15 to estimate winner choice
  AB_diff_samples = ((B_rps_samples - A_rps_samples) / A_rps_samples)*100
  # results["choose_winner"] = str(((percentile(AB_diff_samples, 95)-percentile(AB_diff_samples, 5)) <= 8))
  for i in range(100):
    choose_winner_at_precision_in_lift_delta_percentage[str(i)] = str(((percentile(AB_diff_samples, 100-i)-percentile(AB_diff_samples, i)) <= 8))


  results["choose_winner_at_precision_in_lift_delta_percentage"] = choose_winner_at_precision_in_lift_delta_percentage
  results["confidence_intervals"] = confidence_intervals
  results["cost_of_mistakenly_choosing"] = cost_of_mistaken_choice(A_conv_samples, B_conv_samples, samples_to_draw)
  results["probabilities_of_lifts"] = probabilities_of_lifts
  results["winners"] = winners
  
  return jsonify(results)