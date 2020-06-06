from django.test import TestCase

from lists.models import Item, List


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

        created_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{created_list.id}/")


class NewItemTest(TestCase):
    def test_can_add_item_to_existing_list(self):
        List.objects.create()  # Prepopulate the DB with a different list
        new_list = List.objects.create()

        self.client.post(
            f"/lists/{new_list.id}/add_item", data={"item_text": "A new list item"},
        )

        item = Item.objects.get(list=new_list)
        self.assertEqual(item.text, "A new list item")

    def test_redirect_to_list_view(self):
        List.objects.create()  # Prepopulate the DB with a different list
        new_list = List.objects.create()

        response = self.client.post(
            f"/lists/{new_list.id}/add_item", data={"item_text": "A new list item"},
        )

        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        _list = List.objects.create()
        response = self.client.get(f"/lists/{_list.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_display_only_items_of_specific_list(self):
        _list = List.objects.create()
        Item.objects.create(text="first text", list=_list)
        Item.objects.create(text="second text", list=_list)

        other_list = List.objects.create()
        Item.objects.create(text="other text", list=other_list)
        Item.objects.create(text="other text2", list=other_list)

        response = self.client.get(f"/lists/{_list.id}/")
        self.assertContains(response, "first text")
        self.assertContains(response, "second text")
        self.assertNotContains(response, "other text")
        self.assertNotContains(response, "other text2")


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        _list = List()
        _list.save()

        Item.objects.create(text="My first item", list=_list)
        Item.objects.create(text="The 2nd one", list=_list)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, _list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, "My first item")
        self.assertEqual(saved_items[0].list, _list)
        self.assertEqual(saved_items[1].text, "The 2nd one")
        self.assertEqual(saved_items[1].list, _list)
