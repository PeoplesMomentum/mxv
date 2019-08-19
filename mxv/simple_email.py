from django.core.mail import EmailMultiAlternatives

# sends a simple email
def send_simple_email(to, subject, body):
    message = EmailMultiAlternatives(to = [to, ], from_email = 'My Momentum <mymomentum@peoplesmomentum.com>', subject = subject, body = body)
    message.attach_alternative(content = body, mimetype = "text/html")
    message.send()