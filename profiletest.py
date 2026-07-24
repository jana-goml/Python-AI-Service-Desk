import cProfile
import requests
 
def run():
    for _ in range(100):
        response = requests.post(
            "http://127.0.0.1:8000/tickets/",
            json={"title": "Assessment","priority": "High","assignee_email": "janavarsh@example.com"}
        )
        assert response.status_code in (200,201)
cProfile.run("run()")