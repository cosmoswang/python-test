from inbox import Inbox

inbox = Inbox()

@inbox.collate
def handle(to, sender, subject, body):
    print(to, sender, subject, body)

# Bind directly.
inbox.serve(address='0.0.0.0', port=4467)