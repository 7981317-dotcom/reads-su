"""
Парсер статей с VC.ru

Функционал:
- Извлечение основного контента статьи
- Сохранение в Markdown формате
- Скачивание изображений с сохранением позиций
- Сохранение метаданных (автор, дата, категория, теги)
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
import html2text


class VCParser:
    """Парсер статей с VC.ru"""

    def __init__(self, base_folder="Статьи"):
        self.base_folder = base_folder
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Настройки html2text для конвертации в Markdown
        self.h2t = html2text.HTML2Text()
        self.h2t.body_width = 0  # Не переносить строки
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.ignore_emphasis = False

    def parse_article(self, url):
        """
        Главная функция - парсит статью по URL

        Args:
            url (str): URL статьи на VC.ru

        Returns:
            dict: Информация о результате парсинга
        """
        print(f"[*] Начинаем парсинг: {url}")

        # Валидация URL
        if not self._is_valid_vc_url(url):
            raise ValueError("URL должен быть с сайта vc.ru")

        # Получение HTML страницы
        html = self._fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')

        # Извлечение метаданных
        metadata = self._extract_metadata(soup, url)
        print(f"[+] Заголовок: {metadata['title']}")

        # Создание папки для статьи
        folder_name = self._create_folder_name(metadata['title'], url)
        article_folder = os.path.join(self.base_folder, folder_name)
        images_folder = os.path.join(article_folder, 'images')
        os.makedirs(images_folder, exist_ok=True)

        # Извлечение основного контента
        content_html = self._extract_content(soup)

        # Скачивание изображений и замена на маркеры
        content_html, images_info = self._process_images(content_html, images_folder, url)

        # Конвертация в Markdown
        markdown_content = self._html_to_markdown(content_html, metadata['title'])

        # Сохранение файлов
        self._save_files(article_folder, markdown_content, metadata, images_info)

        result = {
            'success': True,
            'folder': article_folder,
            'title': metadata['title'],
            'images_count': len(images_info)
        }

        print(f"\n[OK] Парсинг завершен!")
        print(f"[DIR] Папка: {article_folder}")
        print(f"[IMG] Изображений: {len(images_info)}")

        return result

    def _is_valid_vc_url(self, url):
        """Проверка что URL принадлежит vc.ru"""
        parsed = urlparse(url)
        return 'vc.ru' in parsed.netloc

    def _fetch_page(self, url):
        """Скачивание HTML страницы"""
        print("[...] Загружаем страницу...")
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text

    def _extract_metadata(self, soup, url):
        """
        Извлечение метаданных статьи

        Args:
            soup: BeautifulSoup объект
            url: URL статьи

        Returns:
            dict: Метаданные статьи
        """
        metadata = {
            'url': url,
            'parsed_at': datetime.now().isoformat()
        }

        # Заголовок
        title_elem = soup.find('h1', class_='content-title')
        if not title_elem:
            title_elem = soup.find('meta', property='og:title')
            metadata['title'] = title_elem.get('content', 'Без названия') if title_elem else 'Без названия'
        else:
            metadata['title'] = title_elem.get_text(strip=True)

        # Автор
        author_elem = soup.find('a', class_='content-header-author__name')
        metadata['author'] = author_elem.get_text(strip=True) if author_elem else 'Неизвестно'

        # Дата публикации
        time_elem = soup.find('time')
        if time_elem and time_elem.get('datetime'):
            metadata['date'] = time_elem.get('datetime')
        else:
            metadata['date'] = datetime.now().isoformat()

        # Категория (из URL)
        url_parts = url.split('/')
        metadata['category'] = url_parts[3] if len(url_parts) > 3 else 'общее'

        # Теги (пробуем найти)
        tags = []
        tag_elems = soup.find_all('a', class_='tag')
        for tag in tag_elems[:5]:  # Максимум 5 тегов
            tags.append(tag.get_text(strip=True))
        metadata['tags'] = tags if tags else ['без тегов']

        return metadata

    def _extract_content(self, soup):
        """
        Извлечение основного контента статьи

        Args:
            soup: BeautifulSoup объект

        Returns:
            BeautifulSoup: Очищенный контент
        """
        print("[...] Извлекаем контент...")

        # Поиск основного контента
        content = soup.find('div', class_='content--full')
        if not content:
            content = soup.find('article')
        if not content:
            raise Exception("Не удалось найти основной контент статьи")

        # Удаляем ненужные блоки
        for selector in [
            'script', 'style', 'iframe',
            '.comments', '.recommend', '.sidebar',
            '.advertisement', '.promo', '.related'
        ]:
            for elem in content.select(selector):
                elem.decompose()

        return content

    def _process_images(self, content, images_folder, base_url):
        """
        Скачивание изображений и замена на относительные ссылки

        Args:
            content: BeautifulSoup контент
            images_folder: Путь к папке для изображений
            base_url: Базовый URL для относительных ссылок

        Returns:
            tuple: (обновленный контент, список информации об изображениях)
        """
        print("[...] Обрабатываем изображения...")

        images_info = []
        img_tags = content.find_all('img')

        for idx, img in enumerate(img_tags, 1):
            try:
                # Получаем URL изображения
                img_url = img.get('src') or img.get('data-src')
                if not img_url:
                    continue

                # Преобразуем в абсолютный URL
                img_url = urljoin(base_url, img_url)

                # Определяем расширение
                ext = self._get_image_extension(img_url)
                filename = f"image_{idx}{ext}"
                filepath = os.path.join(images_folder, filename)

                # Скачиваем изображение
                self._download_image(img_url, filepath)

                # Заменяем src на относительный путь
                img['src'] = f"images/{filename}"

                # Сохраняем информацию
                images_info.append({
                    'original_url': img_url,
                    'filename': filename,
                    'alt': img.get('alt', ''),
                    'position': idx
                })

                print(f"  [+] Скачано: {filename}")

            except Exception as e:
                print(f"  [!] Ошибка при скачивании изображения {idx}: {e}")
                continue

        return content, images_info

    def _get_image_extension(self, url):
        """Определение расширения изображения из URL"""
        parsed = urlparse(url)
        path = parsed.path.lower()

        if '.jpg' in path or '.jpeg' in path:
            return '.jpg'
        elif '.png' in path:
            return '.png'
        elif '.gif' in path:
            return '.gif'
        elif '.webp' in path:
            return '.webp'
        else:
            return '.jpg'  # По умолчанию

    def _download_image(self, url, filepath):
        """Скачивание изображения"""
        response = self.session.get(url, timeout=15, stream=True)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def _html_to_markdown(self, content, title):
        """
        Конвертация HTML в Markdown

        Args:
            content: BeautifulSoup контент
            title: Заголовок статьи

        Returns:
            str: Текст в формате Markdown
        """
        print("[...] Конвертируем в Markdown...")

        # Конвертируем HTML в Markdown
        html_str = str(content)
        markdown = self.h2t.handle(html_str)

        # Добавляем заголовок статьи в начало
        markdown = f"# {title}\n\n{markdown}"

        # Базовая очистка
        markdown = self._clean_markdown(markdown)

        return markdown

    def _clean_markdown(self, text):
        """Базовая очистка Markdown текста"""
        # Удаляем множественные пустые строки
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Удаляем лишние пробелы в конце строк
        text = re.sub(r' +\n', '\n', text)

        return text.strip()

    def _create_folder_name(self, title, url):
        """Создание имени папки из заголовка или URL"""
        # Пробуем извлечь slug из URL
        url_parts = url.rstrip('/').split('/')
        if len(url_parts) > 0:
            slug = url_parts[-1]
            # Удаляем ID из slug (например: 2294129-ayaz-shabutdinov...)
            slug = re.sub(r'^\d+-', '', slug)
            if slug and len(slug) > 5:
                return slug[:100]  # Ограничиваем длину

        # Если не получилось - создаем из заголовка
        folder_name = re.sub(r'[^\w\s-]', '', title.lower())
        folder_name = re.sub(r'[-\s]+', '-', folder_name)
        return folder_name[:100]

    def _save_files(self, folder, markdown_content, metadata, images_info):
        """
        Сохранение файлов статьи

        Args:
            folder: Путь к папке статьи
            markdown_content: Текст в Markdown
            metadata: Метаданные
            images_info: Информация об изображениях
        """
        print("[...] Сохраняем файлы...")

        # Сохраняем article.md
        article_path = os.path.join(folder, 'article.md')
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"  [+] Сохранен: article.md")

        # Добавляем информацию об изображениях в метаданные
        metadata['images_count'] = len(images_info)
        metadata['images'] = images_info

        # Сохраняем metadata.json
        metadata_path = os.path.join(folder, 'metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"  [+] Сохранен: metadata.json")


def main():
    """Основная функция для тестирования"""
    # URL статьи для парсинга
    url = "https://vc.ru/marketing/2298779-prichiny-poteri-klientov-reklamnymi-agentstvami"

    # Создаем парсер
    parser = VCParser()

    try:
        # Парсим статью
        result = parser.parse_article(url)
        print("\n" + "="*50)
        print("[OK] УСПЕХ!")
        print(f"Папка: {result['folder']}")
        print(f"Заголовок: {result['title']}")
        print(f"Изображений: {result['images_count']}")
        print("="*50)

    except Exception as e:
        print(f"\n[ERROR] ОШИБКА: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
