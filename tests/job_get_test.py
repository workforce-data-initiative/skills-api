from app import app
import json
import unittest
from tests.api_test_case import ApiTestCase

from tests.factories import GeographyFactory, \
    JobImportanceFactory, \
    JobMasterFactory, \
    QuarterFactory


class JobGetTestCase(ApiTestCase):

    def test_with_uuid(self):
        job = JobMasterFactory()
        app.db.session.add(job)
        response = self.app.get('v1/jobs/{}'.format(job.uuid))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data())
        self.assertEqual(response_data['title'], job.title)

    def test_with_soc_code(self):
        job = JobMasterFactory()
        app.db.session.add(job)
        response = self.app.get('v1/jobs/{}'.format(job.onet_soc_code))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data())
        self.assertEqual(response_data['title'], job.title)

    def test_missing_geo(self):
        job = JobMasterFactory()
        app.db.session.add(job)
        response = self.app.get('v1/jobs/{}?fips=40500'.format(job.uuid))
        self.assertEqual(response.status_code, 404)

    def test_geo_mismatch(self):
        job = JobMasterFactory()
        right_geography = GeographyFactory()
        wrong_geography = GeographyFactory()
        quarter = QuarterFactory()
        app.db.session.begin(subtransactions=True)
        app.db.session.add(job)
        app.db.session.add(right_geography)
        app.db.session.add(wrong_geography)
        app.db.session.add(quarter)
        app.db.session.commit()
        importance = JobImportanceFactory(
            geography_id=right_geography.geography_id,
            quarter_id=quarter.quarter_id,
            job_uuid=job.uuid
        )
        app.db.session.add(importance)
        response = self.app.get(
            'v1/jobs/{}?fips={}'.format(
                job.uuid,
                wrong_geography.geography_name
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_geo_match(self):
        job = JobMasterFactory()
        right_geography = GeographyFactory()
        wrong_geography = GeographyFactory()
        quarter = QuarterFactory()
        app.db.session.begin(subtransactions=True)
        app.db.session.add(job)
        app.db.session.add(right_geography)
        app.db.session.add(wrong_geography)
        app.db.session.add(quarter)
        app.db.session.commit()

        importance = JobImportanceFactory(
            geography_id=right_geography.geography_id,
            quarter_id=quarter.quarter_id,
            job_uuid=job.uuid
        )
        app.db.session.add(importance)
        response = self.app.get(
            'v1/jobs/{}?fips={}'.format(
                job.uuid,
                right_geography.geography_name
            )
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data())
        self.assertEqual(response_data['title'], job.title)

if __name__ == '__main__':
    unittest.main()
