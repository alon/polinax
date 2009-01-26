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

class Command(NoArgsCommand):
    help = 'Read all the feeds and get some fresh answers.'
    
    def parse_feeds(self, feeds):      
        result = []
        for feed in feeds:
            f = feedparser.parse(feed.url)
            if f.updated == feed.last_read:
                break;
            for i in f.entries:
                if datetime(*i.published_parsed[:6]) > feed.last_read:
                    print i
                    c = i.content[0].value
                    m = search_re.search(c)
                    if m:
                        a = {"adder":feed.user,
                            "text":c,
                            "url":i.link,
                            "q_id": int(m.groups()[0]),
                            "summary": i.title,
                                 }
                        result.append(a)
            # update the last date read
            feed.last_read = datetime(*f.updated[:6])
            feed.save()
        return result

    def handle_noargs(self, **options):
        
        feeds = Feed.objects.filter(public=True)
        answers = self.parse_feeds(feeds)
        print answers
        for a in answers:
            Answer.objects.create(**a) 
        
