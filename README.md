# Python Betterstack-Uptime
![coverage](https://img.shields.io/badge/coverage-85%25-green)

API Library for the Uptime module by Betterstack

## Getting Started

### Installing

Run the following command to install the package
```bash
pip install betterstack-uptime
```
### Usage

Just a quick boilerplate piece of code to get you started

#### Get all instances
```python
from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import Montitor

api = UptimeAPI("yourtokenhere")
monitors = Monitor.get_all_instances(api=api)

for monitor in monitors:
    print(monitor.url)
```
#### Get downtime for monitor
```python
from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import Montitor

start_date = "2023-07-14"
end_date = "2023-08-14"

api = UptimeAPI("yourtokenhere")
monitor = Monitor(api=api, id=1234)
monitor._sla.timeframe = (start_date, end_date)

print(monitor._sla.availablilty)
print(monitor._sla.total_downtime)
print(monitor._sla.number_of_incidents)
```

#### Delete incident when header matches
```python
from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import Incident

api = UptimeAPI("yourtokenhere")
incidents = Incident.get_all_instances(api=api)

for incident in incidents:
    if "SSL" in incident.cause and "expire soon" in incident.cause:
        print("Almost expired SSL cert, %s %s" % (incident.started_at, incident.resolved_at), ", deleting")
        incident.delete()
    if hasattr(incident, "response_options") and incident.response_options and "someheader: someoption" in incident.response_options:
        print("Deleting %s" % incident.name)
        incident.delete()
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to me.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](#).

## Authors

* **Wouter Mellema** - *Initial work* - [wmellema](https://github.com/wmellema)

See also the list of [contributors](https://github.com/iwink/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

