# Random NickName generator

Random NickName generator is a simple library for generating unique nicknames based on random adjectives and nouns. It can be useful for creating nicknames for games, social networks or other online platforms.

## Установка

```python
from nick_gen import generate_nickname

# 1 nickname
print("Сгенерированный никнейм:", generate_nickname())

# if you want some nicknames
unique_nicknames = {generate_nickname() for _ in range(5)}
print("Несколько сгенерированных никнеймов:", unique_nicknames)