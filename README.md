# Inky Twitter

This app displays tweets on an e-ink display attached to a Raspberry Pi.

## Pre-requisites

### Hardware

- Raspberry Pi (running Raspbian Buster)
- Pimoroni Inky wHAT e-ink display

### Software

- Python 3
- [Inky Python library](https://github.com/pimoroni/inky)
- [Pillow Python library](https://pillow.readthedocs.io/en/stable/index.html)
- [Twitter Python library](https://python-twitter.readthedocs.io/en/latest/)

### Other stuff

- Access to the [Twitter Developer API](https://developer.twitter.com)

## Set up

1. Make a copy of `keys-template.py` and rename it to `keys.py`
2. Inside `keys.py` change the values to match your Twitter API keys
3. Inside `accounts.py` change the accounts and display names to match two accounts you'd like to display (you could probably squeeze more or fewer accounts on to the screen if you change the font sizes)
4. Navigate to the directory and run `inky-twitter.py`

Your display should update to look something like this:

![](https://github.com/johnpeart/inky-twitter/blob/master/screenshot.jpg)

## Credits

Inspired by Adam Bowie's [Twitter feeds display](https://www.adambowie.com/blog/2019/09/news-twitter-feeds-and-inky-what-e-ink-display/).

Fonts are open sourced and from [iA Writer](https://github.com/iaolo/iA-Fonts)