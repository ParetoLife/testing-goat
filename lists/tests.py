from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class NewListTest(TestCase):
    def test_can_save_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        added_item = Item.objects.first()
        self.assertEqual(added_item.text, "A new list item")

    def test_redirect_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})

        self.assertRedirects(response, "/lists/unique-identifier/")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/unique-identifier/")
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_list_items(self):
        Item.objects.create(text="first text")
        Item.objects.create(text="second text")

        response = self.client.get("/lists/unique-identifier/")

        self.assertContains(response, "first text")
        self.assertContains(response, "second text")


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        Item.objects.create(text="My first item")
        Item.objects.create(text="The 2nd one")

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, "My first item")
        self.assertEqual(saved_items[1].text, "The 2nd one")
