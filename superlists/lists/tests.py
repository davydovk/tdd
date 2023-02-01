from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        """ Тест: используется домашний шаблон """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        """ Тест: можно сохранить POST-запрос """
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """ Тест: переадресует после post-запроса """
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/uniq_list/')

    def test_only_saves_items_when_necessary(self):
        """ Тест: сохраняет элементы, только когда нужно """
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    """ Тест модели элемента списка """

    def test_saving_and_retrieving_items(self):
        """ Тест сохранения и получения элементов списка """
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):
    """ Тест представления списка """

    def test_uses_list_template(self):
        """ Тест: использует шаблон списка """
        response = self.client.get('/lists/uniq_list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        """ Тест: отображаются все элементы списка """
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/uniq_list/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
