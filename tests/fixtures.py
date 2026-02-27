"""Shared test fixtures and constants for API mocking."""

# Base URLs for testing
BASE_URL = "https://uptime.betterstack.com/api/v2/"
V3_BASE_URL = "https://uptime.betterstack.com/api/v3/"
TEST_BASE_URL = "http://some.weird/api/v2/"


# Monitor fixture data
MONITOR_1 = {
    "data": {
        "id": "1",
        "type": "monitor",
        "attributes": {
            "url": "https://example.com",
            "pronounceable_name": "MyWeirdExampleSite",
            "auth_username": "",
            "auth_password": "",
            "monitor_type": "status",
            "monitor_group_id": None,
            "last_checked_at": "2023-05-08T00:00:00.000Z",
            "status": "up",
            "policy_id": None,
            "required_keyword": None,
            "verify_ssl": True,
            "check_frequency": 30,
            "call": False,
            "sms": False,
            "email": True,
            "push": True,
            "team_wait": None,
            "http_method": "get",
            "request_timeout": 30,
            "recovery_period": 180,
            "request_headers": [],
            "request_body": "",
            "follow_redirects": True,
            "remember_cookies": True,
            "created_at": "2023-02-01T00:00:00.000Z",
            "updated_at": "2023-04-10T00:00:00.000Z",
            "ssl_expiration": 14,
            "domain_expiration": None,
            "regions": ["us", "eu", "as", "au"],
            "expected_status_codes": [],
            "port": None,
            "confirmation_period": 0,
            "paused_at": None,
            "paused": False,
            "maintenance_from": None,
            "maintenance_to": None,
            "maintenance_timezone": "Amsterdam",
        },
        "relationships": {"policy": {"data": None}},
    }
}

MONITOR_2 = {
    "data": {
        "id": "2",
        "type": "monitor",
        "attributes": {
            "url": "https://secondexample.com",
            "pronounceable_name": "MySecondExampleSite",
            "auth_username": "",
            "auth_password": "",
            "monitor_type": "status",
            "monitor_group_id": None,
            "last_checked_at": "2023-05-08T00:00:00.000Z",
            "status": "up",
            "policy_id": None,
            "required_keyword": None,
            "verify_ssl": True,
            "check_frequency": 30,
            "call": False,
            "sms": False,
            "email": True,
            "push": True,
            "team_wait": None,
            "http_method": "get",
            "request_timeout": 30,
            "recovery_period": 180,
            "request_headers": [],
            "request_body": "",
            "follow_redirects": True,
            "remember_cookies": True,
            "created_at": "2023-02-01T00:00:00.000Z",
            "updated_at": "2023-04-10T00:00:00.000Z",
            "ssl_expiration": 14,
            "domain_expiration": None,
            "regions": ["us", "eu", "as", "au"],
            "expected_status_codes": [],
            "port": None,
            "confirmation_period": 0,
            "paused_at": None,
            "paused": False,
            "maintenance_from": None,
            "maintenance_to": None,
            "maintenance_timezone": "Amsterdam",
        },
        "relationships": {"policy": {"data": None}},
    }
}

MONITOR_3 = {
    "data": {
        "id": "3",
        "type": "monitor",
        "attributes": {
            "url": "https://thirdexample.com",
            "pronounceable_name": "MyThirdExampleSite",
            "auth_username": "",
            "auth_password": "",
            "monitor_type": "status",
            "monitor_group_id": None,
            "last_checked_at": "2023-05-08T00:00:00.000Z",
            "status": "up",
            "policy_id": None,
            "required_keyword": None,
            "verify_ssl": True,
            "check_frequency": 30,
            "call": False,
            "sms": False,
            "email": True,
            "push": True,
            "team_wait": None,
            "http_method": "get",
            "request_timeout": 30,
            "recovery_period": 180,
            "request_headers": [],
            "request_body": "",
            "follow_redirects": True,
            "remember_cookies": True,
            "created_at": "2023-02-01T00:00:00.000Z",
            "updated_at": "2023-04-10T00:00:00.000Z",
            "ssl_expiration": 14,
            "domain_expiration": None,
            "regions": ["us", "eu", "as", "au"],
            "expected_status_codes": [],
            "port": None,
            "confirmation_period": 0,
            "paused_at": None,
            "paused": False,
            "maintenance_from": None,
            "maintenance_to": None,
            "maintenance_timezone": "Amsterdam",
        },
        "relationships": {"policy": {"data": None}},
    }
}


def make_paginated_response(data: list, next_url: str | None = None) -> dict:
    """Helper to create a paginated API response."""
    return {
        "data": data,
        "pagination": {
            "first": None,
            "last": None,
            "prev": None,
            "next": next_url,
        },
    }
