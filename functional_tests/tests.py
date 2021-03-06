from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time
import os

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.options = webdriver.FirefoxOptions()
        self.options.headless = True
        self.browser = webdriver.Firefox(options=self.options)
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = f"http://{staging_server}"

    def tearDown(self):
        self.browser.quit()

    def wait_for_item_in_list_table(self, item_to_check):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(item_to_check, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    def test_can_start_list_and_retrieve_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys("Buy peacock feathers")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_item_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_item_in_list_table("1: Buy peacock feathers")
        self.wait_for_item_in_list_table("2: Use peacock feathers to make a fly")

    def test_multiple_users_have_unique_lists(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_new_item")
        edith_text = "Buy peacock feathers"
        inputbox.send_keys(edith_text)
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list_table(f"1: {edith_text}")

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # A new user, Francis, checks out the site as well
        # # We restart the browser to ensure no info is kept from Edith's session
        self.browser.quit()
        self.browser = webdriver.Firefox(options=self.options)

        # Francis visits the home page, and should not see Edith's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text

        self.assertNotIn(edith_text, page_text)

        # Francis starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list

    def test_layout_and_styling(self):
        # Edith goes to the home page, using a standard browser window size
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She sees that the input box is nicely centered
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10,
        )

        # After starting a new list, she sees that the inputbox is still nicely
        # centered.
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list_table("1: testing")

        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10,
        )
