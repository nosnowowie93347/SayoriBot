# SayoriBot: An updated version of my original bot, Terrabot.

<p align="center">
  <a href="https://discord.gg/mTBrXyWxAF"><img src="https://img.shields.io/discord/739934735387721768?logo=discord"></a>
<p align="center">
  More info about the template i used for this repository
  <a href="https://github.com/kkrypt0nn/Python-Discord-Bot-Template/releases"><img src="https://img.shields.io/github/v/release/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="https://github.com/kkrypt0nn/Python-Discord-Bot-Template/commits/main"><img src="https://img.shields.io/github/last-commit/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="https://github.com/kkrypt0nn/Python-Discord-Bot-Template"><img src="https://img.shields.io/github/languages/code-size/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="https://conventionalcommits.org/en/v1.0.0/"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## How to set up

To set up the bot it was made as simple as possible.

### `config.json` file

There is [`config.json`](config.json) file where you can put the
needed things to edit.

Here is an explanation of what everything is:

| Variable                  | What it is                                     |
| ------------------------- | ---------------------------------------------- |
| YOUR_BOT_PREFIX_HERE      | The prefix you want to use for normal commands |
| YOUR_BOT_INVITE_LINK_HERE | The link to invite the bot                     |

### `.env` file

To set up the token you will have to either make use of the [`.env.example`](.env.example) file, either copy or rename it to `.env` and replace `YOUR_BOT_TOKEN_HERE` with your bot's token.

Alternatively you can simply create an environment variable named `TOKEN`.

## How to start

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows), or your Command Prompt (
Windows)
.

Before running the bot you will need to install all the requirements with this command:

```
python -m pip install -r requirements.txt
```

After that you can start it with

```
python bot.py
```

> **Note** You may need to replace `python` with `py`, `python3`, `python3.11`, etc. depending on what Python versions you have installed on the machine.

## Built With

- [Python 3.11.5](https://www.python.org/)
