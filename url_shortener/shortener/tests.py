from django.test import TestCase
from django.urls import reverse

from .models import Link

import json

class GotoTests(TestCase):
    def test_goto_non_existing_url(self):
        """
        Если пришли на короткий URL, который не существует, ожидается 404
        """
        # Arrange
        non_existing_short_url = 'nouri'

        # Act
        response = self.client.get(reverse('shortener:goto', args=[non_existing_short_url]))

        # Assert
        self.assertContains(response, 'Short URL doesn\'t exist.', status_code=404)

    def test_goto_non_valid_character(self):
        """
        Если короткий URL содержит недопустимый символ, ожидается 404
        """
        # Arrange
        non_valid_short_url = 'l0'

        # Act
        response = self.client.get(reverse('shortener:goto', args=[non_valid_short_url]))

        # Assert
        self.assertContains(response, 'Short URL doesn\'t exist.', status_code=404)

    def test_goto_overflow_url(self):
        """
        Если короткий URL при конвертации из base58 превосходит SQLITE_MAX_INT (2**63+1), ожидается 404
        """
        # Arrange
        overflow_short_url = 'aaaaaaaaaaaaaaaaaaaaaaaaaaa'

        # Act
        response = self.client.get(reverse('shortener:goto', args=[overflow_short_url]))

        # Assert
        self.assertContains(response, 'Short URL doesn\'t exist.', status_code=404)

class StatsTests(TestCase):
    def test_stats_existing_url(self):
        """
        Если запрашиваем статистику для существующего короткого URL, ожидается 200
        """
        # Arrange
        valid_url = 'http://example.com/'

        # Act
        response_create = self.client.post(reverse('shortener:create'), {'url': valid_url})
        response_create_json = json.loads(str(response_create.content, encoding='utf8'))
        response_stats = self.client.get(response_create_json['short_url'] + '+')

        # Assert
        self.assertEquals(response_stats.status_code, 200)

    def test_stats_non_existing_url(self):
        """
        Если запрашиваем статистику для несуществующего короткого URL, ожидается 404
        """
        # Arrange
        non_existing_short_url = 'nouri'

        # Act
        response_stats = self.client.get(reverse('shortener:goto', args=[non_existing_short_url]) + '+')

        # Assert
        self.assertEquals(response_stats.status_code, 404)

class CreateTests(TestCase):
    def test_create_empty_url(self):
        """
        Создаём короткий URL из ничего, ожидается JSON-ответ с ошибкой
        """
        # Arrange
        empty_url = ''

        # Act
        response_create = self.client.post(reverse('shortener:create'), {'url': empty_url})

        # Assert
        self.assertEqual(response_create.status_code, 400)
        self.assertJSONEqual(
            str(response_create.content, encoding='utf8'),
            { "error": "No URL given." }
        )

    def test_create_non_valid_url(self):
        """
        Создаём короткий URL из некорректного, ожидается JSON-ответ с ошибкой
        """
        # Arrange
        non_valid_url = 'examplecom'

        # Act
        response_create = self.client.post(reverse('shortener:create'), {'url': non_valid_url})

        # Assert
        self.assertEqual(response_create.status_code, 400)
        self.assertJSONEqual(
            str(response_create.content, encoding='utf8'),
            { "error": "URL is not valid." }
        )

    def test_create_valid_url(self):
        """
        Создаём короткий URL из корректного, ожидается JSON-ответ с коротким URL и редирект на длинный
        """
        # Arrange
        valid_url = 'http://example.com/'

        # Act
        response_create = self.client.post(reverse('shortener:create'), {'url': valid_url})
        response_create_json = json.loads(str(response_create.content, encoding='utf8'))
        response_goto = self.client.get(response_create_json['short_url'])

        # Assert
        self.assertEqual(response_create.status_code, 200)
        self.assertIn('short_url', response_create_json.keys())
        self.assertRedirects(response_goto, expected_url=valid_url)

    def test_create_valid_existing_url(self):
        """
        Создаём короткий URL из корректного, который уже сокращали,
        ожидается JSON-ответ с коротким URL,
        короткие URL при первом и втором вызове create совпадают
        """
        # Arrange
        valid_url = 'http://example.com/'

        # Act
        response_create_first = self.client.post(reverse('shortener:create'), {'url': valid_url})
        response_create_first_json = json.loads(str(response_create_first.content, encoding='utf8'))
        response_create_second = self.client.post(reverse('shortener:create'), {'url': valid_url})
        response_create_second_json = json.loads(str(response_create_second.content, encoding='utf8'))

        # Assert
        self.assertEqual(response_create_first.status_code, 200)
        self.assertEqual(response_create_second.status_code, 200)
        self.assertEqual(response_create_first_json['short_url'], response_create_second_json['short_url'])

