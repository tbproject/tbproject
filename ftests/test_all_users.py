# -*- coding: utf-8 -*-
from datetime import date

from selenium import webdriver as wd
from django.core.urlresolvers import reverse
from django.utils.translation import activate
from django.utils import formats
# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class HomeNewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = wd.Firefox()
        self.browser.implicitly_wait(3)
        activate('en')
    def tearDown(self):
        self.browser.quit()

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def test_home_title(self):
        url = self.get_full_url("home")
        self.browser.get(url)
        self.assertIn("TaskBuster", self.browser.title)

    def test_h1_css(self):
        url = self.get_full_url("home")
        self.browser.implicitly_wait(3)
        self.browser.get(url)
        self.browser.implicitly_wait(3)
        h1 = self.browser.find_element_by_tag_name("h1")
        color = h1.value_of_css_property("color")
        self.assertEqual(color, "rgba(200, 50, 255, 0.5)")

    def test_home_files(self):
        url_robots = self.live_server_url + "/robots.txt"
        url_humans = self.live_server_url + "/humans.txt"
        self.browser.get(url_robots)
        self.assertNotIn("Not Found", self.browser.title)
        self.browser.get(url_humans)
        self.assertNotIn("Not Found", self.browser.title)

    def test_internationalization(self):
        for lang, h1text in [
            ('en', "Welcome to TaskBuster"),
            ("ru", "Ya - TaskBuster. Priyatno poznakomitsa!"),
        ]:
            activate(lang)
            self.browser.get(self.get_full_url("home"))
            h1 = self.browser.find_element_by_tag_name("h1")
            self.assertEqual(h1.text, h1text)

    def test_localization(self):
        today = date.today()
        for lang in ['en', 'ru']:
            activate(lang)
            self.browser.get(self.get_full_url("home"))
            local_date = self.browser.find_element_by_id("local-date")
            non_local_date = self.browser.find_element_by_id("non-local-date")
            self.assertEqual(formats.date_format(today, use_l10n=True), local_date.text)
            self.assertEqual(today.strftime("%Y-%m-%d"), non_local_date.text)

    def test_timezone(self):
        self.browser.get(self.get_full_url("home"))
        tz = self.browser.find_element_by_id("time-tz").text
        utc = self.browser.find_element_by_id("time-utc").text
        ny = self.browser.find_element_by_id("time-ny").text
        self.assertNotEqual(tz, utc)
        self.assertNotIn(ny, [tz, utc])




# import unittest
#
#
# class NewVisitorTest(unittest.TestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(3)
#
#     def tearDown(self):
#         self.browser.quit()
#
#     def test_it_worked(self):
#         self.browser.get('http://localhost:8000')
#         self.assertIn('Welcome to Django', self.browser.title)
#
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
