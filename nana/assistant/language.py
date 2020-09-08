from nana.modules.database.lang_db import switch_to_locale, prev_locale
from nana.tr_engine.strings import tld, LANGUAGES
from nana.tr_engine.list_locale import list_locales
import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nana import setbot, AdminSettings


@setbot.on_message(filters.user(AdminSettings) & filters.command(["setlang"]) & filters.private)
async def locale(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        text = tld(message.chat.id, "language_code_not_valid")
        text += "\n**Currently available languages:**"
        for lang in LANGUAGES:
            locale = list_locales[lang]
            text += "\n**{}** - `{}`".format(locale, lang)
        await message.reply(text, parse_mode='markdown')
        return
    locale = args[1].lower()
    if locale == 'en-us':
        locale = 'en-US'
    if locale in ['en-uk', 'en-gb']:
        locale = 'en-GB'

    if locale in list_locales:
        if locale in LANGUAGES:
            switch_to_locale(message.chat.id, locale)
            await message.reply(tld(message.chat.id, 'language_switch_success_pm').format(list_locales[locale]))
        else:
            text = tld(message.chat.id, "language_not_supported").format(
                list_locales[locale])
            text += "\n**Currently available languages:**"
            for lang in LANGUAGES:
                locale = list_locales[lang]
                text += "\n**{}** - `{}`".format(locale, lang)
            await message.reply(text, parse_mode='markdown')
    else:
        LANGUAGE = prev_locale(message.chat.id)
        if LANGUAGE:
            locale = LANGUAGE.locale_name
            native_lang = list_locales[locale]
            await message.reply(tld(
                message.chat.id, "language_current_locale").format(native_lang),
                               parse_mode='markdown')
        else:
            await message.reply(tld(message.chat.id, "language_current_locale").format("English (US)"), parse_mode='markdown')
