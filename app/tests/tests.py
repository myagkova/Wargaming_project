from django.test import Client, TestCase


class Tests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_page_show_correct_context(self):
        with open('app/tests/text1.txt') as text1:
            response = self.client.post('/upload/', {'upload': text1})
            self.assertEqual(response.status_code, 200)

            words_list = response.context.get('words')
            print(words_list)
            data = {
                'Beautiful': [1, 0.0], 'is': [1, 0.0], 'better': [1, 0.0],
                'than': [1, 0.0], 'ugly': [1, 0.0]
            }
            self.assertEqual(words_list, data)

        with open('app/tests/text2.txt') as text2:
            response = self.client.post('/upload/', {'upload': text2})
            self.assertEqual(response.status_code, 200)
            words_list2 = response.context.get('words')
            print(words_list2)
            data2 = {
                'Explicit': [1, 0.3], 'implicit': [1, 0.3],
                'is': [1, 0.0], 'better': [1, 0.0], 'than': [1, 0.0]
            }
            self.assertEqual(words_list2, data2)
