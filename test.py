from betteruptime.api import BetterUptimeAPI
from betteruptime.api.monitors import Monitor

# Add token here
token=""

api = BetterUptimeAPI(token)
loginiwink = Monitor(api, "993416")
loginiwink.set_variable("paused", False).save()
