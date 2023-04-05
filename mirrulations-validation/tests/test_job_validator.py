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

