from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.get("/")  # Update this URL to match your Flask app's route

