from mirrval.job_validator import Validator
from mirrval.job_validator import write_unfound_jobs
from mirrmock.mock_data_storage import MockDataStorage
from mirrcore.regulations_api import RegulationsAPI

def test_download(self):
    api = RegulationsAPI('FAKE_KEY')
    storage = MockDataStorage()
    # Test the download function
    validator = Validator(api, storage)
    endpoint = 'dockets'
    validator.download(endpoint)
    # Assert that all jobs have been validated
    self.assertEqual(validator.counter['Total_validated'], storage.get_collection_size(endpoint))

def test_write_unfound_jobs(self):
    # Test the write_unfound_jobs function
    unfound_jobs = {}
    res = {'id': 1, 'type': 'docket', 'links': {'self': 'http://example.com/docket/1'}}
    write_unfound_jobs(res, unfound_jobs)
    # Assert that missing_docket contains the URL
    self.assertIn('http://example.com/docket/1', unfound_jobs['missing_docket'])