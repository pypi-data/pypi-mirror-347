import requests , bs4
from colorama import Fore

class Paste:
    def __init__(self):
        self.url = "https://pastebin.com/api/api_post.php"
        self.getter = "https://pastebin.com/"

    def upload(
            self  ,
            code: str, title: str,
            api_dev_key: str = "CUAJ74b3fJlHmg0Cl3EBVWUWN-sim8p-" ,
            syntax="text", expire_date="1D",
            private = 1
    ):
        data = {
            "api_dev_key": api_dev_key,
            "api_option": "paste",
            "api_paste_code": code,
            "api_paste_name": title,
            "api_paste_format": syntax,
            "api_paste_expire_date": expire_date,
            "api_paste_private": private
        }

        response = requests.post(self.url, data=data)

        if response.status_code == 200:
            print(f"{Fore.GREEN}SUCCESS{Fore.WHITE}: This is your link , "+ response.text)
        else:
            print("Error:", response.text)

    def get(self, id: str):

        self.getter = self.getter.rstrip("/")

        html_response = requests.get(f"{self.getter}/{id}")
        soup = bs4.BeautifulSoup(html_response.text, "html.parser")

        h1_tag = soup.find("h1")
        info_span = soup.find("span", class_="unlisted")

        if h1_tag and info_span and "title" in info_span.attrs:
            title = h1_tag.text.strip()
            info = info_span["title"]

            raw_response = requests.get(f"{self.getter}/raw/{id}")
            if raw_response.status_code == 200:
                print(
                    f"""{Fore.WHITE}[ {Fore.RED}* {Fore.WHITE}] {Fore.GREEN}SUCCESS{Fore.WHITE}:\n- Info : {info} \n- Title : {title} . \n- Code : \n{raw_response.text}""")
            else:
                print(f"{Fore.RED}ERROR{Fore.WHITE}: Unable to fetch raw content.")
        else:
            print(f"{Fore.RED}ERROR{Fore.WHITE}: Could not find title or info. Possibly a bot check or invalid page.")


