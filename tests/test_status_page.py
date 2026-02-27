"""Tests for StatusPage, StatusPageSection, StatusPageResource, and StatusPageGroup."""

import unittest

import responses

from betterstack.uptime import UptimeAPI
from betterstack.uptime.objects import (
    StatusPage,
    StatusPageGroup,
    StatusPageResource,
    StatusPageSection,
)

from .fixtures import BASE_URL, make_paginated_response


class TestStatusPage(unittest.TestCase):
    """Tests for the StatusPage class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")
        self.status_page_data = {
            "id": "123456789",
            "type": "status_page",
            "attributes": {
                "company_name": "Best Company",
                "company_url": "https://best-company.com",
                "contact_url": None,
                "logo_url": None,
                "timezone": "Tokyo",
                "subdomain": "best-company-tokyo",
                "custom_domain": None,
                "custom_css": None,
                "custom_javascript": "",
                "google_analytics_id": None,
                "min_incident_length": 400,
                "announcement": None,
                "announcement_embed_visible": False,
                "announcement_embed_css": "",
                "announcement_embed_link": "",
                "automatic_reports": False,
                "status_page_group_id": None,
                "subscribable": False,
                "hide_from_search_engines": False,
                "password_enabled": False,
                "ip_allowlist": [],
                "history": 90,
                "aggregate_state": "operational",
                "design": "v1",
                "navigation_links": [],
                "theme": "light",
                "layout": "vertical",
                "created_at": "2020-08-10T07:34:38.848Z",
                "updated_at": "2020-12-08T14:12:31.680Z",
            },
        }

    def test_create_status_page_from_response(self):
        """Test creating a StatusPage from API response."""
        status_page = StatusPage._from_api_response(self.api, self.status_page_data)

        self.assertEqual(status_page.id, "123456789")
        self.assertEqual(status_page.type, "status_page")
        self.assertEqual(status_page.company_name, "Best Company")
        self.assertEqual(status_page.subdomain, "best-company-tokyo")
        self.assertEqual(status_page.timezone, "Tokyo")
        self.assertEqual(status_page.aggregate_state, "operational")
        self.assertEqual(status_page.history, 90)
        self.assertFalse(status_page.password_enabled)

    def test_generate_url(self):
        """Test URL generation for StatusPage."""
        status_page = StatusPage._from_api_response(self.api, self.status_page_data)
        self.assertEqual(status_page.generate_url(), "status-pages/123456789")

    def test_generate_global_url(self):
        """Test global URL generation for StatusPage."""
        self.assertEqual(StatusPage.generate_global_url(), "status-pages")

    @responses.activate
    def test_fetch_sections(self):
        """Test fetching sections for a status page."""
        section_data = {
            "id": "456",
            "type": "status_page_section",
            "attributes": {
                "name": "EU Datacenter",
                "position": 0,
                "created_at": "2020-08-10T07:34:38.848Z",
                "updated_at": "2020-12-08T14:12:31.680Z",
            },
        }
        responses.add(
            responses.GET,
            f"{BASE_URL}status-pages/123456789/sections",
            json=make_paginated_response([section_data]),
            status=200,
        )

        status_page = StatusPage._from_api_response(self.api, self.status_page_data)
        sections = status_page.fetch_sections()

        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].name, "EU Datacenter")
        self.assertEqual(sections[0].position, 0)

    @responses.activate
    def test_sections_property_lazy_loading(self):
        """Test lazy loading of sections via property."""
        section_data = {
            "id": "456",
            "type": "status_page_section",
            "attributes": {
                "name": "US Datacenter",
                "position": 1,
            },
        }
        responses.add(
            responses.GET,
            f"{BASE_URL}status-pages/123456789/sections",
            json=make_paginated_response([section_data]),
            status=200,
        )

        status_page = StatusPage._from_api_response(self.api, self.status_page_data)

        # First access triggers fetch
        sections = status_page.sections
        self.assertEqual(len(sections), 1)

        # Second access uses cache (no additional request)
        sections_again = status_page.sections
        self.assertEqual(len(responses.calls), 1)  # Only one API call made

    @responses.activate
    def test_fetch_resources(self):
        """Test fetching resources for a status page."""
        resource_data = {
            "id": "789",
            "type": "status_page_resource",
            "attributes": {
                "status_page_section_id": 456,
                "resource_id": 112233,
                "resource_type": "Monitor",
                "history": True,
                "widget_type": "history",
                "public_name": "API Server",
                "explanation": "",
                "position": 0,
                "availability": 0.99963,
                "status": "operational",
            },
        }
        responses.add(
            responses.GET,
            f"{BASE_URL}status-pages/123456789/resources",
            json=make_paginated_response([resource_data]),
            status=200,
        )

        status_page = StatusPage._from_api_response(self.api, self.status_page_data)
        resources = status_page.fetch_resources()

        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0].public_name, "API Server")
        self.assertEqual(resources[0].resource_type, "Monitor")
        self.assertEqual(resources[0].availability, 0.99963)

    @responses.activate
    def test_resources_property_lazy_loading(self):
        """Test lazy loading of resources via property."""
        resource_data = {
            "id": "789",
            "type": "status_page_resource",
            "attributes": {
                "public_name": "Database",
                "resource_type": "Monitor",
                "status": "operational",
            },
        }
        responses.add(
            responses.GET,
            f"{BASE_URL}status-pages/123456789/resources",
            json=make_paginated_response([resource_data]),
            status=200,
        )

        status_page = StatusPage._from_api_response(self.api, self.status_page_data)

        # First access triggers fetch
        resources = status_page.resources
        self.assertEqual(len(resources), 1)

        # Second access uses cache
        resources_again = status_page.resources
        self.assertEqual(len(responses.calls), 1)


class TestStatusPageSection(unittest.TestCase):
    """Tests for the StatusPageSection class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")
        self.section_data = {
            "id": "456",
            "type": "status_page_section",
            "attributes": {
                "name": "EU Datacenter",
                "position": 0,
                "created_at": "2020-08-10T07:34:38.848Z",
                "updated_at": "2020-12-08T14:12:31.680Z",
            },
        }

    def test_create_section_from_response(self):
        """Test creating a StatusPageSection from API response."""
        section = StatusPageSection._from_api_response(self.api, self.section_data)

        self.assertEqual(section.id, "456")
        self.assertEqual(section.name, "EU Datacenter")
        self.assertEqual(section.position, 0)

    def test_generate_url_with_status_page_id(self):
        """Test URL generation for StatusPageSection with status_page_id."""
        section = StatusPageSection._from_api_response(self.api, self.section_data)
        section._status_page_id = "123"
        self.assertEqual(section.generate_url(), "status-pages/123/sections/456")

    def test_generate_url_without_status_page_id_raises(self):
        """Test that generate_url raises without status_page_id."""
        section = StatusPageSection._from_api_response(self.api, self.section_data)
        with self.assertRaises(ValueError) as context:
            section.generate_url()
        self.assertIn("status_page_id is required", str(context.exception))

    def test_generate_global_url_raises(self):
        """Test that generate_global_url raises for sections."""
        with self.assertRaises(ValueError) as context:
            StatusPageSection.generate_global_url()
        self.assertIn("requires a status_page_id", str(context.exception))


class TestStatusPageResource(unittest.TestCase):
    """Tests for the StatusPageResource class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")
        self.resource_data = {
            "id": "789",
            "type": "status_page_resource",
            "attributes": {
                "status_page_section_id": 456,
                "resource_id": 112233,
                "resource_type": "Monitor",
                "history": True,
                "widget_type": "history",
                "public_name": "API Server",
                "explanation": "Our main API endpoint",
                "position": 0,
                "availability": 0.99963,
                "status": "operational",
                "status_history": [
                    {
                        "day": "2022-01-01",
                        "status": "operational",
                        "downtime_duration": 0,
                        "maintenance_duration": 0,
                    }
                ],
            },
        }

    def test_create_resource_from_response(self):
        """Test creating a StatusPageResource from API response."""
        resource = StatusPageResource._from_api_response(self.api, self.resource_data)

        self.assertEqual(resource.id, "789")
        self.assertEqual(resource.public_name, "API Server")
        self.assertEqual(resource.resource_type, "Monitor")
        self.assertEqual(resource.resource_id, 112233)
        self.assertEqual(resource.availability, 0.99963)
        self.assertEqual(resource.status, "operational")
        self.assertTrue(resource.history)
        self.assertEqual(resource.widget_type, "history")

    def test_generate_url_with_status_page_id(self):
        """Test URL generation for StatusPageResource with status_page_id."""
        resource = StatusPageResource._from_api_response(self.api, self.resource_data)
        resource._status_page_id = "123"
        self.assertEqual(resource.generate_url(), "status-pages/123/resources/789")

    def test_generate_url_without_status_page_id_raises(self):
        """Test that generate_url raises without status_page_id."""
        resource = StatusPageResource._from_api_response(self.api, self.resource_data)
        with self.assertRaises(ValueError) as context:
            resource.generate_url()
        self.assertIn("status_page_id is required", str(context.exception))

    def test_generate_global_url_raises(self):
        """Test that generate_global_url raises for resources."""
        with self.assertRaises(ValueError) as context:
            StatusPageResource.generate_global_url()
        self.assertIn("requires a status_page_id", str(context.exception))

    def test_status_history_attribute(self):
        """Test that status_history is correctly parsed."""
        resource = StatusPageResource._from_api_response(self.api, self.resource_data)

        self.assertIsNotNone(resource.status_history)
        self.assertEqual(len(resource.status_history), 1)
        self.assertEqual(resource.status_history[0]["day"], "2022-01-01")
        self.assertEqual(resource.status_history[0]["status"], "operational")


class TestStatusPageGroup(unittest.TestCase):
    """Tests for the StatusPageGroup class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = UptimeAPI("test-token")
        self.group_data = {
            "id": "1372854",
            "type": "status_page_group",
            "attributes": {
                "name": "Testing group",
                "created_at": "2024-11-07T11:33:24.408Z",
                "updated_at": "2024-11-07T11:33:24.408Z",
                "sort_index": None,
            },
        }

    def test_create_group_from_response(self):
        """Test creating a StatusPageGroup from API response."""
        group = StatusPageGroup._from_api_response(self.api, self.group_data)

        self.assertEqual(group.id, "1372854")
        self.assertEqual(group.name, "Testing group")
        self.assertIsNone(group.sort_index)

    def test_generate_url(self):
        """Test URL generation for StatusPageGroup."""
        group = StatusPageGroup._from_api_response(self.api, self.group_data)
        self.assertEqual(group.generate_url(), "status-page-groups/1372854")

    def test_generate_global_url(self):
        """Test global URL generation for StatusPageGroup."""
        self.assertEqual(StatusPageGroup.generate_global_url(), "status-page-groups")

    @responses.activate
    def test_get_all_status_page_groups(self):
        """Test fetching all status page groups."""
        responses.add(
            responses.GET,
            f"{BASE_URL}status-page-groups",
            json=make_paginated_response([self.group_data]),
            status=200,
        )

        groups = list(StatusPageGroup.get_all_instances(self.api))

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].name, "Testing group")
