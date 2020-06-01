from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_POST_request(self):
        self.client.post("/", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        added_item = Item.objects.first()
        self.assertEqual(added_item.text, "A new list item")

    def test_redirect_on_POST(self):
        response = self.client.post("/", data={"item_text": "A new list item"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_only_save_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_display_all_list_items(self):
        Item.objects.create(text="first text")
        Item.objects.create(text="second text")

        response = self.client.get("/")

        self.assertIn("first text", response.content.decode())
        self.assertIn("second text", response.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        Item.objects.create(text="My first item")
        Item.objects.create(text="The 2nd one")

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, "My first item")
        self.assertEqual(saved_items[1].text, "The 2nd one")
