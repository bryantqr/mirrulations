import json


class JobQueue:

    def __init__(self, database):
        self.database = database

    def add_job(self, url):
        job_id = self.get_job_id()
        job = {'job_id': job_id,
               'url': url}
        self.database.lpush('jobs_waiting_queue', json.dumps(job))

    def get_num_jobs(self):
        return self.database.llen('jobs_waiting_queue')

    def get_job(self):
        return json.loads(self.database.lpop('jobs_waiting_queue'))

    def get_job_id(self):
        job_id = self.database.incr('last_job_id')
        return job_id

    def get_last_timestamp_string(self):
        if self.database.exists('last_timestamp'):
            return self.database.get('last_timestamp').decode()
        return '1972-01-01 00:00:00'

    def set_last_timestamp(self, date_string):
        self.database.set('last_timestamp', date_string.replace('T', ' ')
                          .replace('Z', ''))
