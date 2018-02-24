#!baywatch/bin/python
from flask import Flask, jsonify, request, abort, make_response
from models import ab_test, calculate_statistics
import config

app = Flask(__name__)

@app.route('/')
@app.route('/baywatch/')
def index():
  # views comin'

  return """
  API route is /baywatch/api/v0.1/ab_test/<br>
  Please read the <a href=\"https://github.com/dyspop/baywatch/\">documentation</a>
  """

@app.route('/baywatch/api/v0.1/ab_test/')
def run_test():
  #required args
  base_pool =       int(request.args.get('base_pool'))
  test_pool =       int(request.args.get('test_pool'))
  base_events =     int(request.args.get('base_events'))
  test_events =     int(request.args.get('test_events'))
  #optional args
  if request.args.get('samples_to_draw'):
    samples_to_draw = int(request.args.get('samples_to_draw'))
  else:
    samples_to_draw = int(config.SAMPLES_TO_DRAW)
  format = request.args.get('format')

  #error responses
  if (
    base_pool or 
    test_pool or 
    base_events or 
    test_events or 
    samples_to_draw
  ) is None or not (
    base_pool and 
    test_pool and 
    base_events and 
    base_events and 
    test_events
  ):
    abort(404, "Missing test parameter(s).")
  if (
    base_pool or 
    test_pool or 
    samples_to_draw
  ) <= 0 or test_events > test_pool or base_events > base_pool:
    abort(404, "Invalid test parameter(s).")
  else:
    return ab_test(base_pool, test_pool, base_events, test_events, samples_to_draw)

if __name__ == '__main__':
    app.run(debug=config.DEBUG)
