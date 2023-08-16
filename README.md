# Python Betterstack-Uptime
![coverage](https://img.shields.io/badge/coverage-85%25-green)

`betterstack-uptime` is a library written in python that can assist in dealing with the Betterstack Uptime API. This is done by converting API endpoints into python objects, and translating the attributes from the API into variables. 

#### Current endpoints implemented
- Monitors
- Monitor SLA
- Monitor Groups
- Heartbeats
- Heartbeat Groups
- Incidents

In future, there will be more endpoints added. These however, will need some extra code in order for them to work properly. If you desperately need another endpoint, feel free to extend the `BaseAPIObject` class, and implement it!

`betterstack-uptime` is free and [open source](https://github.com/iwink/python-betterstack-uptime) software, you are free to use it, share it, modify it and share the modifications with the world. 

## Getting Started

### Requirements

You will need the following software:
- `python>= 3.7`

Older versions of python 3 should work, but are not guaranteed to work. 

### Installing

Run the following command to install the package
```bash
pip install betterstack-uptime
```
### Usage

Just some quick boilerplate code to get you started

##### Get all instances
```python
from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import Monitor

api = UptimeAPI("yourtokenhere")
monitors = Monitor.get_all_instances(api=api)

for monitor in monitors:
    print(monitor.url)
```

## Documentation

Full documentation is available at [https://iwink.github.io/python-betterstack-uptime/](https://iwink.github.io/python-betterstack-uptime/)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to me.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](#).

## Authors

* **Wouter Mellema** - *Initial work* - [wmellema](https://github.com/wmellema)

See also the list of [contributors](https://github.com/iwink/python-betterstack-uptime/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details