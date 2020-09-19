from nana.modules.database.lang_db import switch_to_locale, prev_locale
from nana.tr_engine.strings import tld, LANGUAGES
from nana.tr_engine.list_locale import list_locales
import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nana import setbot, Owner


async def language_button_callback(_, __, query):
    if re.match(r"set_lang_", query.data):
        return True


language_button_create = filters.create(language_button_callback)


@setbot.on_callback_query(language_button_create)
async def locale_button(client, query):
    lang_match = re.findall(r"en-US|hi", query.data)
    if lang_match:
        if lang_match[0]:
            switch_to_locale(Owner, lang_match[0])
            await query.answer(text=tld('language_switch_success_pm').format(list_locales[lang_match[0]]))
        else:
            await query.answer(text="Error!", show_alert=True)
    try:
        LANGUAGE = prev_locale(Owner)
        locale = LANGUAGE.locale_name
        curr_lang = list_locales[locale]
    except Exception:
        curr_lang = "English (US)"

    text = tld("language_select_language")
    text += tld("language_current_locale").format(curr_lang)
    buttons = [[InlineKeyboardButton("English (US) 🇺🇸", callback_data="set_lang_en-US"), InlineKeyboardButton("Hindi 🇮🇳", callback_data="set_lang_hi")]]
    await client.edit_message_text(chat_id=Owner, message_id=query.message.message_id, text=text, parse_mode='markdown',
        reply_markup=InlineKeyboardMarkup(buttons))
    await client.answer_callback_query(query.id)

