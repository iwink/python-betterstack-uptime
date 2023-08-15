import unittest
import sys
import json
from urllib.parse import urljoin
if sys.version_info >= (3, 3):  # pragma: no cover
    from unittest import mock
else:  # pragma: no cover
    import mock  # noqa: F401

from betterstack.uptime.objects import Monitor
from betterstack.uptime import UptimeAPI

site1 = json.loads("""
{
    "data": {
        "id": "1",
        "type": "monitor",
        "attributes": {
            "url": "https://example.com",
            "pronounceable_name": "MyWeirdExampleSite",
            "auth_username": "",
            "auth_password": "",
            "monitor_type": "status",
            "monitor_group_id": null,
            "last_checked_at": "2023-05-08T00:00:00.000Z",
            "status": "up",
            "policy_id": null,
            "required_keyword": null,
            "verify_ssl": true,
            "check_frequency": 30,
            "call": false,
            "sms": false,
            "email": true,
            "push": true,
            "team_wait": null,
            "http_method": "get",
            "request_timeout": 30,
            "recovery_period": 180,
            "request_headers": [],
            "request_body": "",
            "follow_redirects": true,
            "remember_cookies": true,
            "created_at": "2023-02-01T00:00:00.000Z",
            "updated_at": "2023-04-10T00:00:00.000Z",
            "ssl_expiration": 14,
            "domain_expiration": null,
            "regions": ["us","eu","as","au"],
            "expected_status_codes": [],
            "port": null,
            "confirmation_period": 0,
            "paused_at": null,
            "paused" :false,
            "maintenance_from": null,
            "maintenance_to": null,
            "maintenance_timezone": "Amsterdam"
        },
        "relationships": {
            "policy": {
                "data": null
            }
        }
    }
}""")
site2 = json.loads("""
{
    "data": {
        "id": "2",
        "type": "monitor",
        "attributes": {
            "url": "https://secondexample.com",
            "pronounceable_name": "MySecondExampleSite",
            "auth_username": "",
            "auth_password": "",
            "monitor_type": "status",
            "monitor_group_id": null,
            "last_checked_at": "2023-05-08T00:00:00.000Z",
            "status": "up",
            "policy_id": null,
            "required_keyword": null,
            "verify_ssl": true,
            "check_frequency": 30,
            "call": false,
            "sms": false,
            "email": true,
            "push": true,
            "team_wait": null,
            "http_method": "get",
            "request_timeout": 30,
            "recovery_period": 180,
            "request_headers": [],
            "request_body": "",
            "follow_redirects": true,
            "remember_cookies": true,
            "created_at": "2023-02-01T00:00:00.000Z",
            "updated_at": "2023-04-10T00:00:00.000Z",
            "ssl_expiration": 14,
            "domain_expiration": null,
            "regions": ["us","eu","as","au"],
            "expected_status_codes": [],
            "port": null,
            "confirmation_period": 0,
            "paused_at": null,
            "paused" :false,
            "maintenance_from": null,
            "maintenance_to": null,
            "maintenance_timezone": "Amsterdam"
        },
        "relationships": {
            "policy": {
                "data": null
            }
        }
    }
}""")
site3 = json.loads("""
{
    "data": {
        "id": "3",
        "type": "monitor",
        "attributes": {
            "url": "https://thirdexample.com",
            "pronounceable_name": "MyThirdExampleSite",
            "auth_username": "",
            "auth_password": "",
            "monitor_type": "status",
            "monitor_group_id": null,
            "last_checked_at": "2023-05-08T00:00:00.000Z",
            "status": "up",
            "policy_id": null,
            "required_keyword": null,
            "verify_ssl": true,
            "check_frequency": 30,
            "call": false,
            "sms": false,
            "email": true,
            "push": true,
            "team_wait": null,
            "http_method": "get",
            "request_timeout": 30,
            "recovery_period": 180,
            "request_headers": [],
            "request_body": "",
            "follow_redirects": true,
            "remember_cookies": true,
            "created_at": "2023-02-01T00:00:00.000Z",
            "updated_at": "2023-04-10T00:00:00.000Z",
            "ssl_expiration": 14,
            "domain_expiration": null,
            "regions": ["us","eu","as","au"],
            "expected_status_codes": [],
            "port": null,
            "confirmation_period": 0,
            "paused_at": null,
            "paused" :false,
            "maintenance_from": null,
            "maintenance_to": null,
            "maintenance_timezone": "Amsterdam"
        },
        "relationships": {
            "policy": {
                "data": null
            }
        }
    }
}""")


class BaseMockResponse():
    def __init__(self, json_data, status_code, ok):
        self.json_data = json_data
        self.status_code = status_code
        self.ok = ok

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception

    def json(self):
        return self.json_data


class MonitorTests(unittest.TestCase):

    def setUp(self):
        self.api = UptimeAPI("HelloTest")

    def mock_monitor_post(*args, **kwargs):
        return BaseMockResponse(site3, 200, True)

    def mock_monitor_patch(*args, **kwargs):
        adjusted_json = site1
        for k, v in kwargs['json'].items():
            adjusted_json['data']['attributes'][k] = v
        adjusted_json['data']['attributes']['updated_at'] = "1970-01-01T00:00:00.000Z"
        return BaseMockResponse(adjusted_json, 200, True)

    def mock_monitor_get(*args, **kwargs):
        if kwargs['url'] == urljoin("https://uptime.betterstack.com/api/v2/", 'monitors/1'):
            return BaseMockResponse(site1, 200, True)
        if kwargs['url'] == urljoin("https://uptime.betterstack.com/api/v2/", 'monitors/2'):
            return BaseMockResponse(site2, 200, True)
        if kwargs['url'] == urljoin("https://uptime.betterstack.com/api/v2/", 'monitors/3'):
            return BaseMockResponse(site3, 200, True)
        if kwargs['url'] == urljoin("https://uptime.betterstack.com/api/v2/", 'monitors'):
            sites = [site1['data'], site2['data']]
            if 'params' in kwargs.keys():
                for k, v in kwargs['params'].items():
                    sites = list(filter(lambda x: x['attributes'][k] == v, sites))
            lst = {
                "data": sites,
                "pagination": {
                    "first": None,
                    "last": None,
                    "prev": None,
                    "next": None
                }
            }
            return BaseMockResponse(lst, 200, True)
        return BaseMockResponse({}, 404, False)

    @mock.patch('betterstack.uptime.requests.get', side_effect=mock_monitor_get)
    def test_get_existing(self, mock_get):
        monitor = Monitor(api=self.api, id=1)
        self.assertEqual(monitor.url, "https://example.com")
        self.assertEqual(monitor.pronounceable_name, "MyWeirdExampleSite")

    @mock.patch('betterstack.uptime.requests.get', side_effect=mock_monitor_get)
    def test_get_all_instances(self, mock_get, *args):
        print(args)
        monitors = Monitor.get_all_instances(self.api)
        self.assertEqual(len(list(monitors)), 2)

    @mock.patch('betterstack.uptime.requests.get', side_effect=mock_monitor_get)
    @mock.patch('betterstack.uptime.requests.patch', side_effect=mock_monitor_patch)
    def test_modify_single_value(self, mock_get, mock_patch):
        monitor = Monitor(api=self.api, id=1)
        monitor.set_variable("paused", True)

        self.assertEqual(monitor._updated_vars, ["paused"])
        self.assertEqual(monitor.paused, True)
        monitor.save()
        self.assertEqual(monitor.paused, True)
        self.assertEqual(monitor._updated_vars, [])
        self.assertEqual(monitor.updated_at, "1970-01-01T00:00:00.000Z")

    @mock.patch('betterstack.uptime.requests.get', side_effect=mock_monitor_get)
    def test_monitor_filter(self, mock_get):
        filtered_monitors = list(Monitor.filter(self.api, url="https://example.com"))
        self.assertEqual(len(filtered_monitors), 1)
        self.assertEqual(filtered_monitors[0].pronounceable_name, "MyWeirdExampleSite")
        filtered_monitors_fail = list(Monitor.filter(self.api, url="https://someexample.com"))
        self.assertEqual(len(filtered_monitors_fail), 0)

    @mock.patch('betterstack.uptime.requests.get', side_effect=mock_monitor_get)
    @mock.patch('betterstack.uptime.requests.post', side_effect=mock_monitor_post)
    def test_get_or_create_monitor(self, mock_get, mock_post):
        created, monitor = Monitor.get_or_create(self.api, url="https://example.com")
        self.assertFalse(created)
        self.assertEqual(monitor.pronounceable_name, "MyWeirdExampleSite")

        created, monitor = Monitor.get_or_create(self.api, url="https://thirdexample.com")
        self.assertTrue(created)
        self.assertEqual(monitor.pronounceable_name, "MyThirdExampleSite")
