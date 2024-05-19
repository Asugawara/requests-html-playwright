import pytest


def test_tutorial_and_usage_session():
    from requests_html_playwright import HTMLSession

    session = HTMLSession()
    r = session.get("https://python.org/")
    assert r.html.url == "https://www.python.org/"


def test_tutorial_and_usage_asession():
    from requests_html_playwright import AsyncHTMLSession

    asession = AsyncHTMLSession()

    async def get_pythonorg():
        r = await asession.get("https://python.org/")
        return r

    async def get_reddit():
        r = await asession.get("https://reddit.com/")
        return r

    async def get_google():
        r = await asession.get("https://google.com/")
        return r

    results = asession.run(get_pythonorg, get_reddit, get_google)
    urls = sorted([result.html.url.split("?")[0] for result in results])
    assert urls == [
        "https://www.google.com/",
        "https://www.python.org/",
        "https://www.reddit.com/",
    ]

    r = asession.run(get_pythonorg)[0]
    assert r.html.links
    assert r.html.absolute_links

    about = r.html.find("#about", first=True)
    assert about.text
    assert about.attrs
    assert about.html
    assert about.find("a")
    assert about.absolute_links
    assert r.html.search("Python is a {} language")[0]


def test_tutorial_and_usage_selector():
    from requests_html_playwright import HTMLSession

    session = HTMLSession()
    r = session.get("https://python.org/")
    sel = "#about > ul > li.tier-2.element-1 > a"
    assert r.html.find(sel, first=True).text

    assert r.html.xpath('//*[@id="about"]/ul/li[1]/a')


def test_javascript_support():
    from requests_html_playwright import HTMLSession

    session = HTMLSession()
    r = session.get("https://pythonclock.org")
    before_render = r.html.search("Python 2.7 will retire in...{}Enable Guido Mode")[0]
    assert before_render

    r.html.render()
    after_render = r.html.search("Python 2.7 will retire in...{}Enable Guido Mode")[0]
    assert after_render

    assert before_render != after_render

    periods = [element.text for element in r.html.find(".countdown-period")]
    amounts = [element.text for element in r.html.find(".countdown-amount")]
    countdown_data = dict(zip(periods, amounts))
    assert countdown_data


def test_without_requests():
    from requests_html_playwright import HTML

    doc = """<a href='https://httpbin.org'>"""
    html = HTML(html=doc)
    assert html.links == "https://httpbin.org"
