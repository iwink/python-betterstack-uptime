# Python Betterstack-Uptime

![coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)

`betterstack-uptime` is a library written in python that can assist in dealing with the Betterstack Uptime API. This is done by converting API endpoints into python objects, and translating the attributes from the API into variables.

## Current endpoints implemented

### Monitoring

- Monitors
- Monitor SLA
- Monitor Groups
- Heartbeats
- Heartbeat Groups
- Incidents

### Status Pages

- Status Pages
- Status Page Sections
- Status Page Resources
- Status Page Groups

### On-call & Escalations

- On-Call Calendars
- On-Call Events
- Escalation Policies (v3 API)

If you need another endpoint, feel free to extend the `BaseAPIObject` class and implement it!

`betterstack-uptime` is free and [open source](https://github.com/iwink/python-betterstack-uptime) software, you are free to use it, share it, modify it and share the modifications with the world.

## Getting Started

### Requirements

You will need the following software:

- `python >= 3.10`

Python 3.10+ is required for type hint syntax support.

### Installing

Run the following command to install the package

```bash
pip install betterstack-uptime
```

### Usage

Just some quick boilerplate code to get you started

#### Get all instances

```python
from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import Monitor

api = UptimeAPI("yourtokenhere")
monitors = Monitor.get_all_instances(api=api)

for monitor in monitors:
    print(monitor.url)
```

#### Working with Status Pages

```python
from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import StatusPage

api = UptimeAPI("yourtokenhere")

# Get all status pages
for status_page in StatusPage.get_all_instances(api):
    print(f"{status_page.company_name}: {status_page.aggregate_state}")
    
    # Lazy-loaded sections and resources
    for section in status_page.sections:
        print(f"  Section: {section.name}")
    
    for resource in status_page.resources:
        print(f"  Resource: {resource.public_name} - {resource.status}")
```

#### Working with On-Call Calendars

```python
from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import OnCallCalendar

api = UptimeAPI("yourtokenhere")

# Get all on-call calendars
for calendar in OnCallCalendar.get_all_instances(api):
    print(f"{calendar.team_name}: {calendar.name}")
    
    # Get current on-call users
    for user in calendar.on_call_users:
        print(f"  On-call: {user.get('meta', {}).get('email')}")
    
    # Create a rotation
    calendar.create_rotation(
        users=["alice@example.com", "bob@example.com"],
        rotation_length=1,
        rotation_period="week",
        start_rotations_at="2025-01-01T00:00:00Z",
        end_rotations_at="2025-12-31T23:59:59Z",
    )
```

#### Working with Escalation Policies

```python
from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import EscalationPolicy, PolicyStep

api = UptimeAPI("yourtokenhere")

# Get all escalation policies (uses v3 API)
for policy in EscalationPolicy.get_all_instances(api):
    print(f"{policy.name}: {len(policy.steps)} steps")

# Create a new policy with helper class
steps = [
    PolicyStep(
        step_type="escalation",
        wait_before=0,
        urgency_id=123456,
        step_members=[{"type": "current_on_call"}],
    ).to_dict(),
    PolicyStep(
        step_type="escalation",
        wait_before=600,  # 10 minutes
        urgency_id=123456,
        step_members=[{"type": "entire_team"}],
    ).to_dict(),
]
```

## Documentation

Full documentation is available at [https://iwink.github.io/python-betterstack-uptime/](https://iwink.github.io/python-betterstack-uptime/)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to me.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/iwink/python-betterstack-uptime/tags).

## Authors

- **Wouter Mellema** - *Initial work* - [wmellema](https://github.com/wmellema)

See also the list of [contributors](https://github.com/iwink/python-betterstack-uptime/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
