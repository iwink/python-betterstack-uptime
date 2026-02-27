Working with Status Pages
=========================

Get All Status Pages
--------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import StatusPage

    api = UptimeAPI("your-token")

    for status_page in StatusPage.get_all_instances(api):
        print(f"{status_page.company_name}")
        print(f"  Subdomain: {status_page.subdomain}")
        print(f"  State: {status_page.aggregate_state}")

Get Sections and Resources
--------------------------

Sections and resources are lazy-loaded when accessed.

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import StatusPage

    api = UptimeAPI("your-token")

    for status_page in StatusPage.get_all_instances(api):
        print(f"Status Page: {status_page.company_name}")

        # Sections are fetched on first access
        for section in status_page.sections:
            print(f"  Section: {section.name} (position: {section.position})")

        # Resources are fetched on first access
        for resource in status_page.resources:
            print(f"  Resource: {resource.public_name}")
            print(f"    Type: {resource.resource_type}")
            print(f"    Status: {resource.status}")
            print(f"    Availability: {resource.availability}")

Create a Status Page
--------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import StatusPage

    api = UptimeAPI("your-token")

    status_page = StatusPage.new(
        api,
        company_name="My Company",
        subdomain="my-company",
        timezone="UTC",
        history=90,
    )

    print(f"Created status page: {status_page.subdomain}")

Working with Status Page Groups
-------------------------------

.. code-block:: python

    from betterstack.uptime import UptimeAPI
    from betterstack.uptime.objects import StatusPageGroup

    api = UptimeAPI("your-token")

    # Get all groups
    for group in StatusPageGroup.get_all_instances(api):
        print(f"Group: {group.name}")

    # Create a new group
    group = StatusPageGroup.new(api, name="Production Status Pages")
