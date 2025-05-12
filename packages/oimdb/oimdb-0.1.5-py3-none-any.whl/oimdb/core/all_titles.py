import subprocess
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def ensure_playwright_browser_installed():
    try:
        subprocess.run(["playwright", "install", "chromium"], check=True, stdout=subprocess.DEVNULL)
    except Exception as e:
        raise RuntimeError("Не удалось установить браузер для Playwright. Установи вручную: `playwright install chromium`") from e


def get_alternate_titles(imdb_id: str) -> list[tuple[str, str]]:
    """
    Получает альтернативные названия фильма по IMDb ID (например: "tt1375666")
    Возвращает список кортежей (код страны или "original", название).
    """
    url = f"https://www.imdb.com/title/{imdb_id}/releaseinfo/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        page.goto(url)

        try:
            page.locator("button.ipc-see-more__button:has(span:text('All'))").nth(1).wait_for(timeout=5000)
        except PlaywrightTimeoutError:
            raise Exception("Кнопка 'All' для альтернативных названий не найдена")

        before_count = page.locator("li.ipc-metadata-list__item").count()

        page.locator("button.ipc-see-more__button:has(span:text('All'))").nth(1).click()
        page.wait_for_function(
            f"() => document.querySelectorAll('li.ipc-metadata-list__item').length > {before_count}",
            timeout=5000
        )

        page.locator("li.ipc-metadata-list__item").first.wait_for(timeout=0)

        items = page.locator("li.ipc-metadata-list__item")
        results = []

        for i in range(items.count()):
            item = items.nth(i)
            try:
                label = item.locator("span.ipc-metadata-list-item__label").inner_text(timeout=100)
                title = item.locator("span.ipc-metadata-list-item__list-content-item").inner_text(timeout=100)

                label = "original" if "(original title)" in label.lower() else label.strip().lower()
                results.append((label, title.strip()))
            except PlaywrightTimeoutError:
                continue

        browser.close()
        return results

print(get_alternate_titles("tt2024544"))