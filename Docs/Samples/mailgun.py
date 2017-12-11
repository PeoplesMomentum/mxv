import requests
def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox7cd9e45750fd440d9be90c7bd2154c0b.mailgun.org/messages",
        auth=("api", "key-0e33de0328720772d172c20c7eb2e1d6"),
        data={"from": "Excited User <mailgun@sandbox7cd9e45750fd440d9be90c7bd2154c0b.mailgun.org>",
              "to": ["mark.reardon@peoplesmomentum.com", "mark.reardon@peoplesmomentum.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})