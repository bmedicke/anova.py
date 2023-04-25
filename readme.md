### what is it?

Python 3.6 module to interface with the Anova private API.


### motivation

> API access is something we’re considering for the future, and we’re researching the ways people would want to interact with it. 

That was [more than a year](https://www.reddit.com/r/sousvide/comments/3p1kas/hello_from_anova_ask_us_anything_about_the_wifi_pc/cw6qoh7/?st=ixa812m5&sh=86182a3b&context=10) ago. This is a little nudge ;)

### how to use it

```python
import anova

cooker_id = 'anova xxx-xxxxxxxxxxx'
secret = 'xxxxxxxxxx'

cooker = anova.AnovaCooker(cooker_id, secret)

# get status of the device. all methods return json:
print(cooker.get_status())
```

```json
{
  "status": {
      "cooker_id": "anova xxx-xxxxxxxxxxx",
      "current_temp": 27.3,
      "is_running": false,
      "speaker_mode": true,
      "target_temp": 30,
      "temp_unit": "c"
  }
}
```

Examples:

```python
# set temperature and start it:
cooker.target_temperature = 60
cooker.running = True

# check if running:
print(cooker.running)
#  True

# get current temperature and unit:
print(cooker.current_temperature)
#  59.8
print(cooker.temperature_unit)
# 'c'

# to use the timer we have to create a job.
# 45 degrees (currently set unit), 900 seconds:
cooker.create_job(45, 900)

# 80 degrees Fahrenheit, 600 seconds:
cooker.create_job(80, 600, 'f')
```

TODO: add documentation

### installation for development

```sh
# clone it and cd to the project folder.
pip3 install -e .
```

### getting your cooker_id and secret

You could use `anova.util.get_secret_cookerid` with ip address as argument.

```python
from anova.util import get_secret_cookerid

cooker_id, secret = get_secret_cookerid("192.168.1.234")
print(f"Cooker id: {cooker_id}")
print(f"Secret: {secret}")
```
