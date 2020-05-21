
# Tools requirements

  * Homebrew (macOS package installer) `Homebrew 2.2.17-55-gdc0346a`
  * PyEnv `1.2.18`
  * Python `3.8.2`
  * jQ (JSON Query) `jq-1.6`
  * git `2.26.0`
  * VSCode `1.45.1 5763d909d5f12fe19f215cbfdd29a91c0fa9208a x64`

## Installation

#### PyEnv

Python Version Manager

```bash
brew install pyenv
```

#### Python 3.8.2

```bash
pyenv install 3.8.2
```

### `genson`

Generates and processes JSON Schemas.

> **NOTE**: Because we're using `pyenv` do not use the `--user` flag when 
> installing modules through pip. Also it is not necessary to use `pip3`, simply
> `pip` will suffice.

```bash
pip install genson
pyenv rehash
```
