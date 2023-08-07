__author__ = "Ruu3f"
__version__ = "1.0.0"

from re import search
from string import digits
from random import choices
from requests import Session
from json import dumps, loads


class Bard:
    """
    A class that interacts with the Google Bard to generate answers to user prompts.

    Args:
        cookie (str): The value of the __Secure-1PSID cookie for authentication.
        proxies (str, optional): Proxy configuration for HTTP requests. Default is None.

    Attributes:
        proxies (str): Proxy configuration for HTTP requests.
        cookie (str): The value of the __Secure-1PSID cookie for authentication.
        session (Session): The HTTP session used for making requests to the Bard API.
        snlm0e (str): The value of the SNlM0e parameter extracted from the Secure_1PSID cookie.

    Methods:
        generate_answer(prompt): Generates an answer for the given user prompt.
        _create_session(): Creates an HTTP session with necessary headers and cookies.
        _get_snlm0e(): Extracts the SNlM0e value from the Secure_1PSID cookie.

    """

    def __init__(self, cookie: str, proxies: str = None):
        """
        Initialize the Bard instance.

        Args:
            cookie (str): The value of the __Secure-1PSID cookie for authentication.
            proxies (str, optional): Proxy configuration for HTTP requests. Default is None.
        """
        self.proxies = proxies
        self.cookie = cookie
        self.session = self._create_session()
        self.snlm0e = self._get_snlm0e()

    def generate_answer(self, prompt):
        """
        Generate an answer for the given user prompt.

        Args:
            prompt (str): The user's prompt for which an answer is to be generated.

        Returns:
            dict: A dictionary containing the generated answer and related information.
        """
        request_id = int("".join(choices(digits, k=4)))
        params = {
            "bl": "boq_assistant-bard-web-server_20230713.13_p0",
            "_reqid": str(request_id),
            "rt": "c",
        }
        prompt_struct = [[prompt], None, [None, "", ""]]
        data = {
            "f.req": dumps(["", dumps(prompt_struct)]),
            "at": self.snlm0e,
        }
        resp = self.session.post(
            "https://bard.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
            params=params,
            data=data,
            timeout=30,
        )
        parsed_answer = loads(loads(resp.content.splitlines()[3])[0][2])
        images = (
            {img[0][0][0] for img in parsed_answer[4][0][4]}
            if parsed_answer[4][0][4]
            else set()
        )
        links = [
            item
            for current in parsed_answer[4]
            if isinstance(current, list)
            for item in current
            if isinstance(item, str)
            and item.startswith("http")
            and "favicon" not in item
        ]

        lang_code, code = None, None
        try:
            lang_code = parsed_answer[4][0][1][0].split("```")[1].split("\n")[0].strip()
            code = parsed_answer[4][0][1][0].split("```")[1][len(lang_code):]
        except (IndexError, TypeError, KeyError, ValueError):
            pass

        answer = {
            "content": parsed_answer[4][0][1][0],
            "conversation_id": parsed_answer[1][0],
            "response_id": parsed_answer[1][1],
            "factuality_queries": parsed_answer[3],
            "text_query": parsed_answer[2][0] if parsed_answer[2] else "",
            "choices": [{"id": x[0], "content": x[1]} for x in parsed_answer[4]],
            "links": links,
            "images": images,
            "language_code": lang_code,
            "code": code,
        }
        return answer

    def _create_session(self):
        """
        Create an HTTP session with necessary headers and cookies.

        Returns:
            Session: An instance of the requests.Session class.
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
        session.proxies = self.proxies
        return session

    def _get_snlm0e(self):
        """
        Extract the SNlM0e value from the Secure_1PSID cookie.

        Returns:
            str: The extracted SNlM0e value.

        Raises:
            Exception: If the cookie value is incorrect or if SNlM0e value is not found.
        """
        if not self.cookie or self.cookie[-1] != ".":
            raise Exception("Incorrect __Secure-1PSID cookie value.")
        resp = self.session.get(
            "https://bard.google.com/", timeout=30, proxies=self.proxies
        )
        if resp.status_code != 200:
            raise Exception("Unable to fetch the response.")
        snlm0e = search(r"SNlM0e\":\"(.*?)\"", resp.text).group(1)
        if not snlm0e:
            raise Exception("SNlM0e value not found in the given Secure_1PSID cookie.")
        return snlm0e
