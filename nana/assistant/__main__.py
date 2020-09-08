import os
from platform import python_version

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from nana.tr_engine.strings import tld
from nana import (app,
                  setbot,
                  AdminSettings,
                  DB_AVAILABLE,
                  USERBOT_VERSION,
                  ASSISTANT_VERSION,
                  BotUsername,
                  Owner,
                  OwnerName,
                  NANA_IMG)

if DB_AVAILABLE:
    from nana.modules.database.chats_db import get_all_chats


@setbot.on_message(filters.private & ~filters.user(AdminSettings))
async def un_auth(_client, message):
    if message.chat.id is not AdminSettings:
        msg = f"""
Hi {message.chat.first_name},
You must be looking forward on how I work.
In that case I can give you helpful links to self host me on your own.
Here are some links for you
        """
        buttons = [
            [
                InlineKeyboardButton(
                    "Documentation", url="https://aman-a.gitbook.io/nana-remix/"
                )
            ],
            [
                InlineKeyboardButton(
                    "Repository", url="https://github.com/pokurt/Nana-Remix"
                ),
                InlineKeyboardButton("Support", url="https://t.me/nanabotsupport"),
            ],
        ]
        await message.reply(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        return


@setbot.on_message(filters.user(AdminSettings) & filters.command(["start"]))
async def start(_client, message):
    if message.chat.type != 'private':
        await message.reply('henlo ^0^')
    else:
        if len(message.text.split()) >= 2:
            helparg = message.text.split()[1]
            if helparg == "help_inline":
                await message.reply(tld(message.chat.id, "inline_help_text").format(BotUsername))
                return
        try:
            me = await app.get_me()
        except ConnectionError:
            me = None
        if not me:
            userbot_stat = 'Stopped'
        else:
            userbot_stat = 'Running'
        if DB_AVAILABLE:
            db_stat = len(get_all_chats())
        else:
            db_stat = 'None'
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Help", callback_data="help_back")]])
        await setbot.send_photo(message.chat.id,
                                NANA_IMG,
                                caption=tld(message.chat.id, "start_message").format(
                                                                                OwnerName,
                                                                                python_version(),
                                                                                userbot_stat,
                                                                                USERBOT_VERSION,
                                                                                ASSISTANT_VERSION,
                                                                                DB_AVAILABLE,
                                                                                db_stat),
            reply_markup=buttons)


@setbot.on_message(filters.user(AdminSettings) & filters.command(["getme"]))
async def get_myself(client, message):
    try:
        me = await app.get_me()
    except ConnectionError:
        await message.reply("Bot is currently turned off!")
        return
    getphoto = await client.get_profile_photos(me.id)
    if len(getphoto) == 0:
        getpp = None
    else:
        getpp = getphoto[0].file_id
    text = "**ℹ️ Your profile:**\n"
    text += "First name: {}\n".format(me.first_name)
    if me.last_name:
        text += "Last name: {}\n".format(me.last_name)
    text += "User ID: `{}`\n".format(me.id)
    if me.username:
        text += "Username: @{}\n".format(me.username)
    text += "Phone number: `{}`\n".format(me.phone_number)
    text += "`Nana Version    : v{}`\n".format(USERBOT_VERSION)
    text += "`Manager Version : v{}`".format(ASSISTANT_VERSION)
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Hide phone number", callback_data="hide_number")]])
    if me.photo:
        await client.send_photo(message.chat.id, photo=getpp, caption=text, reply_markup=button)
    else:
        await message.reply(text, reply_markup=button)


# For callback query button
def dynamic_data_filter(data):
    async def func(flt, _, query):
        return flt.data == query.data

    # "data" kwarg is accessed with "flt.data" above
    return filters.create(func, data=data)


@setbot.on_callback_query(dynamic_data_filter("hide_number"))
async def get_myself_btn(client, query):
    try:
        me = await app.get_me()
    except ConnectionError:
        await client.answer_callback_query(query.id, "Bot is currently turned off!", show_alert=True)
        return

    if query.message.caption:
        text = query.message.caption.markdown
    else:
        text = query.message.text.markdown

    num = ["*" * len(me.phone_number)]

    if "***" not in text.split("Phone number: `")[1].split("`")[0]:
        text = text.replace("Phone number: `{}`\n".format(me.phone_number), "Phone number: `{}`\n".format("".join(num)))
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Show phone number", callback_data="hide_number")]])
    else:
        text = text.replace("Phone number: `{}`\n".format("".join(num)), "Phone number: `{}`\n".format(me.phone_number))
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Hide phone number", callback_data="hide_number")]])

    if query.message.caption:
        await query.message.edit_caption(caption=text, reply_markup=button)
    else:
        await query.message.edit(text, reply_markup=button)


@setbot.on_callback_query(dynamic_data_filter("report_errors"))
async def report_some_errors(client, query):
    await app.join_chat("@nanabotsupport")
    text = "Hi @pokurt, i got an error for you.\nPlease take a look and fix it if possible.\n\nThank you ❤️"
    err = query.message.text
    open("nana/cache/errors.txt", "w").write(err)
    await query.message.edit_reply_markup(reply_markup=None)
    await app.send_document("nanabotsupport", "nana/cache/errors.txt", caption=text)
    os.remove("nana/cache/errors.txt")
    await client.answer_callback_query(query.id, "Report was sent!")


namevars = ""
valuevars = ""


@setbot.on_callback_query(dynamic_data_filter("add_vars"))
async def add_vars(_client, query):
    global namevars
    await query.message.edit_text("Send Name Variable :")
    setbot.on_message()


async def name_vars(_client, message):
    global namevars
    namevars = message.text