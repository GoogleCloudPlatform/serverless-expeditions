from locust import HttpUser, between, task

class Voter(HttpUser):
    weight = 1
    wait_time = between(0.1, 1)

    @task
    def tabs(self):
        self.client.post('/', {'team': 'TABS'})

    @task
    def spaces(self):
        self.client.post('/', {'team': 'SPACES'})


class Loader(HttpUser):
    weight = 5
    wait_time = between(0.1, 1)

    @task
    def home(self):
        self.client.get('/')