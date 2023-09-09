[![PyPI](https://img.shields.io/pypi/v/simplebardapi)](https://pypi.org/project/simplebardapi)
[![Downloads](https://static.pepy.tech/badge/simplebardapi)](https://pypi.org/project/simplebardapi)
[![Status](https://img.shields.io/pypi/status/simplebardapi)](https://pypi.org/project/simplebardapi)

# simplebardapi
A simpler and faster version of BardAPI.

## Get started:

```
python -m pip install -U simplebardapi
```

Join my [Discord server](https://dsc.gg/devhub-rsgh) for live chat, support, or if you have any issues with this package.

## Support this repository:
- ⭐ **Star the project:** Star this repository. It means a lot to me! 💕
- 🎉 **Join my Discord Server:** Chat with me and others. [Join here](https://dsc.gg/devhub-rsgh):

[![DiscordWidget](https://discordapp.com/api/guilds/1137347499414278204/widget.png?style=banner2)](https://dsc.gg/devhub-rsgh)

## Example:

```python
from simplebardapi import Bard

Secure_1PSID = "yourCookieValue"
bard = Bard(Secure_1PSID)
while True:
    prompt = input("👦: ")
    try:
        resp = bard.generate_answer(prompt)
        print(f"🤖: {resp}")
    except Exception as e:
        print(f"🤖: {e}")
```
