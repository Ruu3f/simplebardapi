__author__ = "Ruu3f"
__version__ = "1.0.1"


from string import digits
from random import choices
from re import search, error
from json import dumps, loads
from requests import Session, exceptions


class Bard:
    """
    Bard class for interacting with the Google Bard API.

    Args:
        cookie (str): The value of the '__Secure-1PSID' cookie.
        proxies (str, optional): The proxies to use for requests, if any.

    Attr:
        cookie (str): The value of the '__Secure-1PSID' cookie.
        proxies (str, optional): The proxies to use for requests, if any.
        session (requests.Session): A session object for making HTTP requests.
        snlm0e (str): The 'SNlM0e' value obtained from the website.
    """

    def __init__(self, cookie: str, proxies: str = None):
        self.proxies = proxies
        self.cookie = cookie
        self.session = self._create_session()
        self.snlm0e = self._get_snlm0e()

    def generate_answer(self, prompt):
        """
        Generate an answer to a given prompt.

        Args:
            prompt (str): The input prompt for generating an answer.

        Returns:
            dict: A dictionary containing the generated answer, conversation ID, response ID,
            available choices, and images (if any).
        """
        resp = self.session.post(
            "https://bard.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
            params={
                "bl": "boq_assistant-bard-web-server_20230713.13_p0",
                "_reqid": int("".join(choices(digits, k=4))),
                "rt": "c",
            },
            data={
                "f.req": dumps(["", dumps([[prompt], None, [None, "", ""]])]),
                "at": self.snlm0e,
            },
            timeout=15,
            proxies=self.proxies,
        )
        parsed_answer = loads(loads(resp.content.splitlines()[3])[0][2])
        return {
            "content": parsed_answer[4][0][1][0],
            "conversation_id": parsed_answer[1][0],
            "response_id": parsed_answer[1][1],
            "choices": [{"id": x[0], "content": x[1]} for x in parsed_answer[4]],
            "images": (
                {img[0][0][0] for img in parsed_answer[4][0][4]}
                if parsed_answer[4][0][4]
                else set()
            ),
        }

    def _create_session(self):
        """
        Create and configure an HTTP session for making requests.

        Returns:
            requests.Session: A configured session object.
        """
        session = Session()
        session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
        session.cookies.set("__Secure-1PSID", self.cookie)
        session.cookies.set("__Secure-1PSIDCC", "")
        session.cookies.set("__Secure-1PSIDTS", "")
        session.proxies = self.proxies
        return session

    def _get_snlm0e(self):
        """
        Fetch and extract the 'SNlM0e' value from the website.

        Returns:
            str: The extracted 'SNlM0e' value.

        Raises:
            Exception: If the response code isn't 200 or 'SNlM0e' value is not found.
        """
        resp = self.session.get(
            "https://bard.google.com/", timeout=30, proxies=self.proxies
        )
        if resp.status_code != 200:
            raise exceptions.RequestException("Unable to fetch the response.")
        snlm0e = search(r"SNlM0e\":\"(.*?)\"", resp.text).group(1)
        if not snlm0e:
            raise error(
                "SNlM0e value not found in the given Secure_1PSID cookie value."
            )
        return snlm0e
