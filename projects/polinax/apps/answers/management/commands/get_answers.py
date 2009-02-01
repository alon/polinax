from urllib import urlopen
from datetime import datetime
import re
import feedparser
from django.core.management.base import NoArgsCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from groups.models import AssociatedContent
from profiles.models import Profile
from answers.models import Answer
from parties.models import Feed
search_re = re.compile(Site.objects.get(id=settings.SITE_ID).domain + reverse("view_question", args=[0])[:-2] + '(\d+)')

LONG_AGO = datetime(1970,1,1)
class Command(NoArgsCommand):
    help = 'Read all the feeds and get some fresh answers.'
    

    def _get_entry_date(self, entry):
        if hasattr(entry, 'published_parsed'):
            return datetime(*entry.published_parsed[:6])
        else:
            return datetime(*entry.updated_parsed[:6])

    def parse_feeds(self, feeds):      
        result = []
        next_last = LONG_AGO
        for feed in feeds:
            f = feedparser.parse(feed.url)
            for i in f.entries:
                entry_date = self._get_entry_date(i)
                if entry_date > feed.last_read:
                    if entry_date > next_last:
                        next_last = entry_date
                    try:
                        c = i.content[0].value
                    except AttributeError:
                        c = urlopen(i.link).read()
                    m = search_re.search(c)
                    if m:
                        result.append({"adder":feed.user,
                            "url":i.link,
                            "q_id": int(m.groups()[0]),
                            "summary": i.title,
                        })
            # update the last date read
            if next_last != LONG_AGO:
                feed.last_read = next_last
                feed.save()
        return result

    def handle_noargs(self, **options):
        
        feeds = Feed.objects.filter(public=True)
        answers = self.parse_feeds(feeds)
        print answers
        for a in answers:
            Answer.objects.create(**a) 
        
