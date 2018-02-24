# Baywatch v0.1

Baywatch is a bayesian A/B testing API  
Current version returns statistical analyses on the input data

## Installation

Tested on Python 2.7.10 and 3.6.3 doesn't use `print()` `;)`.

to run locally:

### in a virtual environment (recommended)

1. install pip https://pip.pypa.io/en/stable/installing/
2. install virtualenv https://pypi.python.org/pypi/virtualenv
3. create and activate a virtualenv 
  * `$ virtualenv env && source env/bin/activate` 
4. install required packages
    $ pip install requirements.txt
5. clone the repo
6. make it an executable with `$ chmod a+x app.py` 
7. then `$ ./app.py` will run the app
8. when done deactivate the virtualenv with `deactivate` 

### create a configuration file

Add a config.py to the app root folder. The main thing for development is to enable debug mode to see in-browser debugging and tracebacks. an example looks like:

`DEBUG = True`  
`SAMPLES_TO_DRAW = 1000000`
`SECRET_KEY = ''`  
`DATABASE_URI = ''`

more configuration examples can be found at http://flask.pocoo.org/docs/0.10/config/

---
runs locally at http://127.0.0.1:5000/

app interface will be at http://127.0.0.1:5000/baywatch/

API is at /baywatch/api/v0.1/ab_test/

## Usage

Submit query arguments and the application will return confidence intervals for 0-100% confidence, as well as return the probabilities of lift percentages in the test against the control, where appropriate and not redundant.

Example query:

    hostpath/baywatch/api/v0.1/ab_test/?base_pool=411524&base_events=3425&test_pool=41343&test_events=1231&samples_to_draw=10000

API accepts five arguments:

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
