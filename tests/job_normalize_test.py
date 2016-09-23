from app import app
import httpretty
import json
import re
import unittest


class JobNormalizeTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def mock_endpoint_with_response(self, source_filename):
        httpretty.HTTPretty.allow_net_connect = False
        url_regex = 'http://{}/.*'.format(app.app.config['ELASTICSEARCH_HOST'])
        with open(source_filename) as f:
            output = f.read()
        httpretty.register_uri(
            httpretty.GET,
            re.compile(url_regex),
            body=output,
            content_type='application/json'
        )

    @httpretty.activate
    def test_with_hits(self):
        self.mock_endpoint_with_response('tests/es_normalize_output.json')
        response = self.app.get('v1/jobs/normalize?job_title=cupcake+ninja')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data())
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['title'], 'Sales Managers')

    @httpretty.activate
    def test_with_defined_limit(self):
        self.mock_endpoint_with_response('tests/es_normalize_output.json')
        response = self.app.get('v1/jobs/normalize?job_title=cupcake+ninja&limit=2')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data())
        self.assertEqual(len(response_data), 2)
        self.assertEqual(
            response_data[1]['title'],
            'First-Line Supervisors/Managers of Non-Retail Sales Workers'
        )

    @httpretty.activate
    def test_no_hits(self):
        self.mock_endpoint_with_response('tests/es_nohit_output.json')
        response = self.app.get('v1/jobs/normalize?job_title=baker')
        self.assertEqual(response.status_code, 404)

    def test_no_title(self):
        response = self.app.get('v1/jobs/normalize')
        self.assertEqual(response.status_code, 400)

    def test_bad_limit(self):
        response = self.app.get('v1/jobs/normalize?job_title=test&limit=999999')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
