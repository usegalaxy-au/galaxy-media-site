"""Load test a remote web server.

`requirements.txt` should be pip installed into a virtual env.

Run with:

$ locust --host=https://usegalaxy-au.neoformit.com --locustfile locustfile.py

You may need to change your machine's "open file limits".
On Linux you can do this on a per-session basis with:

$ ulimit -S -n 20000

"""

from locust import FastHttpUser, task, between


class WebsiteUser(FastHttpUser):
    """Define a site user.

    The homepage will be hit 40X more often than other pages.
    """

    wait_time = between(10, 30)

    @task(40)
    def homepage(self):
        """Request the homepage.

        This involves a db query to get events and news items followed by an
        HTML render.
        """
        self.client.get('/')

    @task(1)
    def events_index(self):
        """Visit the events page.

        This requires a slightly larger db query than the homepage.
        """
        self.client.get('/events')

    @task(1)
    def news_index(self):
        """Visit the news page."""
        self.client.get('/news')

    @task(1)
    def event_article(self):
        """Visit an event article page."""
        self.client.get('/events/1/')
