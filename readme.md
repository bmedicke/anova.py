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
You will need to intercept the https traffic between your phone and the Anova API server.  <br>
We'll be using [mitmproxy](https://mitmproxy.org/) to run a [man-in-the-middle attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

#### on the intercepting server
```sh
# install mitmproxy
pip3 install mitmproxy

# now run it:
mitmproxy

# or if you prefer a browser UI:
mitmweb
```

#### on your phone

- set up an http proxy with your server's IP address and 8080 as the port (mitmproxy default)
- go to http://mitm.it and install the certificate
- run the Anova Wi-Fi app

#### back on your server

- filter for `api.anovaculinary.com` and look for any POST or GET request
- your `cooker_id` is the string between `https://api.anovaculinary.com/cookers/` and `?request_key`
- your `secret` is the string after `&secret=`

Don't forget to remove or disable the http proxy when you are done. You might also want to remove the certificate too.<br>
Please don't hammer the server. The iOS app polls about once every 5 seconds, try to stick to that. The cooker does not even seem to update that often, so there is no point in polling any faster.
