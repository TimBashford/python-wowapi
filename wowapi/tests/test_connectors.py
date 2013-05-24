from wowapi.connectors import APIConnector
from wowapi.exceptions import APIError

import json
from mock import patch
import requests
import unittest


class APIConnectorTest(unittest.TestCase):

    def setUp(self):
        self.host = "eu.battle.net"

    def test_get_query_parameters(self):
        instance = APIConnector(self.host, locale="en_GB", custom="test")
        instance.allowed_filters = ["locale", ]
        url_parameters = instance.get_query_parameters()
        self.assertEqual(1, len(url_parameters))
        self.assertNotIn("custom", url_parameters)

    def test_get_url(self):
        instance = APIConnector(self.host, "guild", "player")
        url = instance.get_url()
        self.assertEqual("http://api/wow/guild/player", url)

    def test_https(self):
        instance = APIConnector(self.host, "guild", "player", secure=True)
        self.assertEqual("https://", instance.protocol)

    def test_timeout(self):
        instance = APIConnector(self.host)
        with patch.object(requests, 'get') as mock_method:
            with self.assertRaises(APIError):
                mock_method.side_effect = requests.Timeout
                instance.get_resource()

    def test_connection_error(self):
        instance = APIConnector(self.host)
        with patch.object(requests, 'get') as mock_method:
            with self.assertRaises(APIError):
                mock_method.side_effect = requests.ConnectionError
                instance.get_resource()

    def test_http_error(self):
        instance = APIConnector(self.host)
        with patch.object(requests, 'get') as mock_method:
            with self.assertRaises(APIError):
                mock_method.side_effect = requests.HTTPError
                instance.get_resource()

    def test_status_not_ok(self):
        instance = APIConnector(self.host)
        with patch.object(requests.models.Response, 'ok') as mock_method:
            with self.assertRaises(APIError):
                mock_method.side_effect = requests.RequestException
                instance.get_resource()

    def test_json_decode_error(self):
        instance = APIConnector(self.host)
        with patch.object(requests.models.Response, 'json') as mock_method:
            with self.assertRaises(APIError):
                mock_method.side_effect = ValueError
                instance.get_resource()
