import argparse
from botasaurus.browser import browser, Driver
import time

def get_args():
    parser = argparse.ArgumentParser(description="Browse a URL using botasaurus")
    parser.add_argument("url", help="URL to visit")
    parser.add_argument("--cookie", help="Return only this cookie", default=None)
    parser.add_argument("--on-redirect", help="Terminate when redirected to this URL", default=None)
    args = parser.parse_intermixed_args()
    return args

def get_cookie(bot, cookie_name):
    cookies = bot.get_cookies()
    for c in cookies:
        if c.get("name") == cookie_name:
            return c
    return None

def get_session(bot:Driver, cookie_name):
    if cookie_name:
        print(get_cookie(bot, cookie_name))
    else:
        print("; ".join(f"{item['name']}={item['value']}" for item in bot.get_cookies()))

@browser(headless=False)
def scrape_heading_task(bot: Driver, args):
    bot.get(args.url)
    if args.on_redirect:
        # Polling every 0.5s
        while True:
            current_url = bot.current_url
            if current_url == args.on_redirect:
                break
            time.sleep(0.5)
    else:
        # Inject floating button to submit manually
        bot.run_js('''
                if (!document.getElementById("botasaurus-submit-btn")) {
                    let btn = document.createElement("button");
                    btn.innerText = "Submit";
                    btn.id = "botasaurus-submit-btn";
                    btn.style.position = "fixed";
                    btn.style.bottom = "20px";
                    btn.style.right = "20px";
                    btn.style.padding = "10px 20px";
                    btn.style.backgroundColor = "#008CBA";
                    btn.style.color = "white";
                    btn.style.border = "none";
                    btn.style.borderRadius = "5px";
                    btn.style.zIndex = "9999";
                    document.body.appendChild(btn);
                    btn.onclick = function() {
                        document.title = "BOTASUBMIT_CLICKED";
                    }
                }
        ''')
        # Wait for user to click button (poll title)
        while True:
            if bot.title == "BOTASUBMIT_CLICKED":
                break
            time.sleep(0.5)
    get_session(bot, args.cookie)
def main():
    args = get_args()
    scrape_heading_task(args)
