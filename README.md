# Baywatch v0.1

Baywatch is a bayesian A/B testing API  
Current version returns statistical analyses on the input data

## Installation

Tested on Python 2.7.10 and 3.6.3 doesn't use `print()` `;)`.

to run locally:

### in a virtual environment (recommended)

1. install pip https://pip.pypa.io/en/stable/installing/
2. install virtualenv https://pypi.python.org/pypi/virtualenv
3. copy this, paste it into your terminal and hit enter/return:

```
git clone git@github.com:dyspop/baywatch.git && cd baywatch && \
virtualenv env && source env/bin/activate && pip3 install -r \
requirements.txt && chmod a+x app.py && echo \
'DEBUG=True\nSAMPLES_TO_DRAW=1000000' >config.py && open \
'http://127.0.0.1:5000/baywatch/api/v0.1/ab_test/?base_pool=411524&base_events=3425&test_pool=41343&test_events=1231&samples_to_draw=1000' \
&& python app.py
```

You may have to refresh your browser while the app starts, depending on your computer/browser speeds.

---
runs locally at http://127.0.0.1:5000/

app interface will be at http://127.0.0.1:5000/baywatch/

API is at /baywatch/api/v0.1/ab_test/

## Usage

Submit query arguments and the application will return confidence intervals for 0-100% confidence, as well as return the probabilities of lift percentages in the test against the control, where appropriate and not redundant.

The return is a json object with these results as features:

### Choose winner at nth precision in lift delta percentage

`choose_winner_at_precision_in_lift_delta_percentage` This will always be a set of key-value pairs with keys being n (as `0`-`100`) and the result being a boolean. This means the winner can be choseen at the nth level of precision from the lift delta. This easily makes it available to see at what level of precision the winner was chosen rather than taking precision as an argument and returning the boolean state of the result without regard to how close the result was to the precision.

Example results (truncated and reformated for clarity):
```
{
  "choose_winner_at_precision_in_lift_delta_percentage": {
    "0": "False", 
    "1": "False", 
    "2": "False", 
    [ ... omitted for readability ... ] 
    "47": "False", 
    "48": "False", 
    "49": "False",
    "50": "True", 
    "51": "True", 
    "52": "True",
    [ ... omitted for readability ... ]
    "97": "True", 
    "98": "True", 
    "99": "True"
  }, 
``` 

In the example above it is at as low as a 50% precision where a winner is chosen. This is a strong result. The closer the the choice to 100 precision (which this API does not return) the weaker the test result is. (note: this may be reworked to a simpler result in future version to just one value, in which case it would be represented as `"choose_winner_at_precision_in_lift_delta_percentage": 50,`

---

### Confidence Intervals

`confidence_intervals` This will always be a set of key-value pairs with the keys being n (as `0`-`100`) and the result being an array of the results of the test at that nth confidence interval for the test "base vs test" as `[{base}, {test}]`.

Example results (truncated and reformated for clarity):
```
"confidence_intervals": { 
    "1": [ 0.4819, 0.9913 ], 
    "2": [ 0.5383, 0.9868 ], 
    "3": [ 0.5754, 0.9832 ],
    [ ... omitted for readability ... ]
    "47": [ 0.8188, 0.8996 ], 
    "48": [ 0.8204, 0.8976 ], 
    "49": [ 0.8229, 0.8954 ], 
    "50": [ 0.8247, 0.8936 ], 
    "51": [ 0.8265, 0.8911 ], 
    "52": [ 0.8284, 0.889 ],
    [ ... omitted for readability ... ]
    "97": [ 0.8901, 0.6402 ], 
    "98": [ 0.8911, 0.6041 ], 
    "99": [ 0.8925, 0.5383 ], 
    "100": [ 0.8936, 0.0031 ]
  }, 
```

In the example above it is at a confidence interval of 1 the base result is low and the test is high (just due to randomized sample generation of this particular test run), but as the interval approaches 100 the results flip. This can be useful as an eyeballing the test-generated randomization characteristics if you need to call into question the results of the test. The variance should be a constant of the inputs so rerunning the test and comparing results here is less useful than simply bumping up the samples to draw parameter.

---

### Cost of Mistakenly Choosing

`cost_of_mistakenly_choosing` a measure of the probability that choosing the variation will not produce the lift expected (currently `1%` lift is only supported).

```
  "cost_of_mistakenly_choosing": {
    "base": 0.269577203662007, 
    "test": 0.0
  },
```

This is very useful in helping to determine when a test result may be overlooked for some other concern, for example if they are very close to eachother.

---

### Probabilities of Lifts

`probabilities_of_lifts` a set of (currently one) key-value pairs where key is the lift percentage and the value is its corresponding probability. This tells you how probable it is that the key lift amount (currently `1%` only supported) will successfully occur if you choose the winner.

```
  "probabilities_of_lifts": {
    "0.994": 0.99, 
    "0.9942": 0.97, 
    "0.9943": 0.96, 
    "0.9947": 0.9500000000000002, 
    "0.9948": 0.94, 
    "0.995": 0.9300000000000002, 
    "0.9951": 0.9199999999999999, 
    "0.9953": 0.9100000000000001, 
    "0.9954": 0.8999999999999999, 
    "0.9955": 0.8700000000000001, 
    "0.9956": 0.8599999999999999, 
    "0.9958": 0.8500000000000001, 
    "0.9961": 0.8399999999999999, 
    "0.9964": 0.8300000000000001, 
    "0.9969": 0.8200000000000001, 
    "0.9971": 0.81, 
    "0.9972": 0.8, 
    "0.9974": 0.79, 
    "0.9975": 0.77, 
    "0.9976": 0.76, 
    "0.9977": 0.73, 
    "0.9978": 0.72, 
    "0.9979": 0.69, 
    "0.9981": 0.6800000000000002, 
    "0.9982": 0.6600000000000001, 
    "0.9983": 0.6400000000000001, 
    "0.9986": 0.6299999999999999, 
    "0.9987": 0.6200000000000001, 
    "0.9988": 0.55, 
    "0.999": 0.45999999999999996, 
    "0.9992": 0.43999999999999995, 
    "0.9994": 0.41000000000000014, 
    "0.9996": 0.31000000000000005, 
    "0.9997": 0.29000000000000004, 
    "0.9998": 0.28, 
    "0.9999": 0.050000000000000044, 
    "1.0": 0.0
  }, 
```

This reveals at which the test becomes improbable to be true. For example in our test above you could say it is 99% probable that there is a 0.994% lift, and it is 0% probable that there is a 1% lift between the loser and the winner. This is a very nice, narrowly accurate result.

---

### Winners

`winners` a simple boolean per each test variation. 

```
  "winners": { "base": "False", "test": "True" }
}
```

This is the overall test result! In this case the test won. Looking at the rest of the data makes it obvious, and this is in this case simply a confirmation. Use this result when determination is otherwise difficult.

---

Example query for the above example results:

    http://127.0.0.1:5000/baywatch/api/v0.1/ab_test/?base_pool=50&base_events=1&test_pool=50&test_events=15&samples_to_draw=10000
    
---


The API accepts five arguments:

| argument  | required  | accepted ranges | notes  |
|---|---|---|---|
| `base_pool`  | yes  | gte `1`  | This is the base pool you're testing against. e.g. how many views did the control page of the landing page test get? |
| `base_events`  | yes  | gte `0`  | This is the base event occurrence you're testing against. e.g. how many clicks or conversions did the control page of the landing page get?  |
| `test_pool`  | yes  | gte `1`  | The same as base_pool but for the variation you're testing against the control  |
| `test_events`  | yes  | gte `0`  | The same as base_events but for the variation you're testing against the control  |
| `samples_to_draw`  | yes  | gte `1`  | It is currently recommended to send 1000000 for a fairly quick but accurate calculation. (This probably shouldn't be required but instead default to a number or calculated sample count to estimate accuracy against server load, or speed vs accuracy, or both.)  |
| `format`  | no  | `json`  | this is intended to specify the output format, for example json, csv, xml, txt etc  |

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits

Initial python scripts adapted by Dan Black from Michael McCarthy's. 
Miguel Grinberg's Flask megatutorial and API tutorial.
