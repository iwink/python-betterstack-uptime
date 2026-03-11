Working with On-Call Scheduling
================================

Get On-Call Calendars
---------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import OnCallCalendar

    api = UptimeAPI("your-token")

    for calendar in OnCallCalendar.get_all_instances(api):
        print(f"Calendar: {calendar.name or 'Default'}")
        print(f"  Team: {calendar.team_name}")
        print(f"  Default: {calendar.default_calendar}")

Get Current On-Call Users
-------------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import OnCallCalendar

    api = UptimeAPI("your-token")

    for calendar in OnCallCalendar.get_all_instances(api):
        print(f"Calendar: {calendar.team_name}")

        # on_call_users is parsed from API relationships
        for user in calendar.on_call_users:
            email = user.get("meta", {}).get("email", "Unknown")
            print(f"  On-call: {email}")

Get On-Call Events
------------------

Events are lazy-loaded when accessed.

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import OnCallCalendar

    api = UptimeAPI("your-token")

    for calendar in OnCallCalendar.get_all_instances(api):
        print(f"Calendar: {calendar.team_name}")

        # Events are fetched on first access
        for event in calendar.events:
            print(f"  {event.starts_at} - {event.ends_at}")
            print(f"    Users: {', '.join(event.users or [])}")
            print(f"    Override: {event.override}")

Create a Rotation
-----------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import OnCallCalendar

    api = UptimeAPI("your-token")

    # Get the default calendar for a team
    for calendar in OnCallCalendar.get_all_instances(api):
        if calendar.team_name == "Production" and calendar.default_calendar:
            # Create a weekly rotation
            result = calendar.create_rotation(
                users=[
                    "alice@example.com",
                    "bob@example.com",
                    "charlie@example.com",
                ],
                rotation_length=1,
                rotation_period="week",
                start_rotations_at="2025-01-01T00:00:00Z",
                end_rotations_at="2025-12-31T23:59:59Z",
            )
            print(f"Created rotation: {result}")
            break

Working with Escalation Policies
--------------------------------

Escalation policies use the v3 API endpoint.

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import EscalationPolicy, PolicyStep

    api = UptimeAPI("your-token")

    # Get all policies
    for policy in EscalationPolicy.get_all_instances(api):
        print(f"Policy: {policy.name}")
        print(f"  Team: {policy.team_name}")
        print(f"  Repeat count: {policy.repeat_count}")
        print(f"  Steps: {len(policy.steps or [])}")

        for i, step in enumerate(policy.steps or []):
            print(f"    Step {i + 1}: {step['type']}")
            print(f"      Wait before: {step.get('wait_before', 0)}s")

Building Policy Steps
---------------------

Use the ``PolicyStep`` helper class to construct escalation steps.

.. code-block:: python

    from betterstack.uptime.objects import PolicyStep

    # Escalation step - notify current on-call immediately
    step1 = PolicyStep(
        step_type="escalation",
        wait_before=0,
        urgency_id=123456,
        step_members=[{"type": "current_on_call"}],
    )

    # Escalation step - notify entire team after 10 minutes
    step2 = PolicyStep(
        step_type="escalation",
        wait_before=600,
        urgency_id=123456,
        step_members=[{"type": "entire_team"}],
    )

    # Time branching step - route to different policy on weekends
    weekend_step = PolicyStep(
        step_type="time_branching",
        wait_before=0,
        timezone="UTC",
        days=["sat", "sun"],
        time_from="00:00",
        time_to="23:59",
        policy_id=789,
    )

    # Convert to dict for API
    steps = [step1.to_dict(), step2.to_dict()]
