# Test Memory Usage of Custom Actions

### Setup

`pip install -r requirements.txt`

### Usage

Run the test command - with the existing custom action this should take about 3 seconds to complete.

`python test_action_mem.py` 

Results will be saved as txt and json. To visualise the results, run

`mprof plot memory_usage_custom_action_plot.txt`