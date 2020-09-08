import yaml
from codecs import encode, decode

from nana import logging as LOGGER
from nana.modules.database.lang_db import prev_locale

LANGUAGES = ['en-US', 'en-GB', 'id', 'ru', 'es', 'hi']

strings = {}

for i in LANGUAGES:
    strings[i] = yaml.full_load(open("locales/" + i + ".yml", "r"))


def tld(chat_id, t, show_none=True):
    LANGUAGE = prev_locale(chat_id)

    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('en-US') and t in strings['en-US']:
            result = decode(
                encode(strings['en-US'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape')
            return result
        elif LOCALE in ('en-GB') and t in strings['en-GB']:
            result = decode(
                encode(strings['en-GB'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape')
            return result
        elif LOCALE in ('id') and t in strings['id']:
            result = decode(
                encode(strings['id'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape')
            return result
        elif LOCALE in ('ru') and t in strings['ru']:
            result = decode(
                encode(strings['ru'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape')
            return result
        elif LOCALE in ('es') and t in strings['es']:
            result = decode(
                encode(strings['es'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape')
            return result
        elif LOCALE in ('hi') and t in strings['hi']:
            result = decode(
                encode(strings['hi'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape')
            return result

    if t in strings['en-US']:
        result = decode(
            encode(strings['en-US'][t], 'latin-1', 'backslashreplace'),
            'unicode-escape')
        return result

    err = f"No string found for {t}.\nReport it in @nanabotsupport."
    LOGGER.warning(err)
    return err


def tld_list(chat_id, t):
    LANGUAGE = prev_locale(chat_id)

    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('en-US') and t in strings['en-US']:
            return strings['en-US'][t]
        elif LOCALE in ('en-GB') and t in strings['en-GB']:
            return strings['en-GB'][t]
        elif LOCALE in ('id') and t in strings['id']:
            return strings['id'][t]
        elif LOCALE in ('ru') and t in strings['ru']:
            return strings['ru'][t]
        elif LOCALE in ('es') and t in strings['es']:
            return strings['es'][t]
        elif LOCALE in ('hi') and t in strings['hi']:
            return strings['hi'][t]

    if t in strings['en-US']:
        return strings['en-US'][t]

    LOGGER.warning(f"#NOSTR No string found for {t}.")
    return f"No string found for {t}.\nReport it in @nanabotsupport."