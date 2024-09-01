import random

from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        # self.client.get("/top")
        self.client.post("/set_step", params={"user_id": random.randint(1, 10_000_00),
                                              "step": random.randint(1, 10_000), })
