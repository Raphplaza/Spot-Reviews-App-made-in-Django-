from time import time
from django.test import TestCase

# Create your tests here.
import  datetime
from django.test import TestCase
from django.utils import timezone

from .models import SurfSpot

from django.urls import reverse

class SurfSpotModelTests(TestCase):
    def test_was_published_recently_with_future_added_surfspot(self):
        
        #was_published_recently() returns False for surfspots whose pub_date
        # is in the future.

        time = timezone.now() + datetime.timedelta(days=30)
        future_posted_surfspot = SurfSpot(pub_date=time)
        self.assertIs(future_posted_surfspot.was_published_recently(),False)
    
    
    def test_was_published_recently_with_old_posted_surfspot(self):

    #was_published_recently() returns False for surfspots whose pub_date
    #is older than 1 day.

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_posted_surfspot = SurfSpot(pub_date=time)
        self.assertIs(old_posted_surfspot.was_published_recently(), False)

    
    def test_was_published_recently_with_recently_posted_surfspot(self):
    
    #was_published_recently() returns True for surfspots whose pub_date
    #is within the last day.
    
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recently_posted_surfspot = SurfSpot(pub_date=time)
        self.assertIs(recently_posted_surfspot.was_published_recently(), True)




def create_surfspot(surfspotname, days):

    #Create a surfspot with the given `name` and published the
    #given number of `days` offset to now (negative for surfspots published
    #in the past, positive for surfspots that have yet to be published).
    
    time = timezone.now() + datetime.timedelta(days=days)
    return SurfSpot.objects.create(surfspotname, pub_date=time)


class SurfSpotIndexViewTests(TestCase):
    def test_no_spots_added(self):
    
        #If no surfspot exist, an appropriate message is displayed.
    
        response = self.client.get(reverse('spots:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No surfspots available")
        self.assertQuerysetEqual(response.context['surfspot_list'], [])

    def test_past_added_surfspot(self):
      
        #Surfspots with a pub_date in the past are displayed on the
        #index page.
       
        surfspot = create_surfspot(name="Past added_surfspot.", days=-30)
        response = self.client.get(reverse('spots:index'))
        self.assertQuerysetEqual(
            response.context['surfspot_list'],
            [surfspot],
        )

    def test_future_added_surfspot(self):
        
        #Surfspots with a pub_date in the future aren't displayed on
        #the index page.
        
        create_surfspot(name="Future spot.", days=30)
        response = self.client.get(reverse('spots:index'))
        self.assertContains(response, "No surfspots available")
        self.assertQuerysetEqual(response.context['surfspot_list'], [])

    def test_future_and_past_surfspot(self):
        
        #Even if both past and future surfspots exist, only past surfspots
        #are displayed.
        
        surfspot = create_surfspot(name="Past spot.", days=-30)
        create_surfspot(name="Future spot.", days=30)
        response = self.client.get(reverse('spots:index'))
        self.assertQuerysetEqual(
            response.context['surfspot_list'],
            [surfspot],
        )