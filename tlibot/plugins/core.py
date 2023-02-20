import asyncio

import requests
from pyrogram import Client
from pyrogram.types import CallbackQuery, Message

from client.api import TLIBotApiClient
from tlibot.auth.users import Resource, user_resource_map, users_list
from tlibot.bot_config import TLI, command
from tlibot.filters import course_selected, dersyukle, not_started, step_factory
from tlibot.utils import CONTACT_PEOPLE, button_maker


@TLI.on_message(command("iptal") & ~not_started)
async def cancel_process(_: Client, message: Message) -> None:
    users_list.remove_user(message.from_user.id)
    await message.reply_text(
        text="`İşlem iptal edildi. Başka bir işlem için /start komutunu kullanabilirsin.`",
        quote=True,
    )


@TLI.on_message(not_started & command("start"))
async def say_hello(_: Client, message: Message) -> None:
    from_user = message.from_user
    created, user = users_list.get_or_create(
        from_user.id, from_user.username, from_user.first_name
    )

    msg = await message.reply_text(
        text=f"`Merhaba {message.from_user.mention().capitalize()}. Turkey Learning Initiative Telegram botuna hoşgeldin.`",
        quote=True,
    )
    await asyncio.sleep(1)
    msg = await msg.edit_text(
        text=f"`{msg.text} Bu botu kullanarak websitemizde yayınlanmak üzere ders kaynakları paylaşabilirsin.`"
    )
    await asyncio.sleep(1)
    await msg.edit_text(
        text=f"`{msg.text} Başlamak için aşağıdaki Ders Yükle butonunu kullanabilirsin. İşleme başladıktan sonra istediğin zaman iptal etmek için /iptal komutunu kullanabilirsin.`",
        reply_markup=button_maker(
            {
                "dersyukle": "Ders Yükle",
            },
            1,
        ),
    )


@TLI.on_callback_query(dersyukle)
async def get_lecture_title(client: Client, callback_query: CallbackQuery):
    user = users_list.get_user(callback_query.from_user.id)
    if user:
        user.set_step(1)
        resource = user_resource_map[user.id] = Resource()
        resource.set_uploader(f"@{user.username} (Telegram-Bot)")
    else:
        await callback_query.answer(
            "İşlem iptal edildi. Başka bir işlem için /start komutunu kullanabilirsin.",
            show_alert=True,
        )
        return
    await client.send_message(
        callback_query.from_user.id, f"Lütfen ders/kaynak adını giriniz:"
    )


@TLI.on_message(step_factory(1))
async def get_lecture_description(_: Client, message: Message):
    user = users_list.get_user(message.from_user.id)
    if user:
        user.set_step(2)
        user_resource_map[user.id].set_title(message.text)
    await message.reply_text("Lütfen ders/kaynak açıklamasını giriniz:", quote=True)


@TLI.on_message(step_factory(2))
async def get_lecture_author(_: Client, message: Message):
    user = users_list.get_user(message.from_user.id)
    if user:
        user.set_step(3)
        user_resource_map[user.id].set_description(message.text)
    await message.reply_text(
        f"Lütfen ders/kaynak yazarını/sahibini giriniz:", quote=True
    )


@TLI.on_message(step_factory(3))
async def get_lecture_tags(_: Client, message: Message):
    user = users_list.get_user(message.from_user.id)
    if user:
        user.set_step(4)
        user_resource_map[user.id].set_author(message.text)
    await message.reply_text(
        "Lütfen bu kaynakla ilgili en az 2 anahtar kelimeyi aralarında virgül olacak şekilde giriniz (Örn: matematik,diferansiyel):",
        quote=True,
    )


@TLI.on_message(step_factory(4))
async def get_lecture_course(_: Client, message: Message):
    user = users_list.get_user(message.from_user.id)
    if user:
        user.set_step(5)
        user_resource_map[user.id].set_tags(message.text)

    msg = await message.reply_text(
        text=f"`Lütfen aşağıdaki butonlardan bu kaynağın hangi ders için olduğunu seçiniz.`",
        quote=True,
    )
    await asyncio.sleep(1)
    await msg.edit_text(
        text=f"`{msg.text}`",
        reply_markup=button_maker(
            TLIBotApiClient.get_courses(),
            4,
        ),
    )


@TLI.on_callback_query(course_selected)
async def send_file_upload_message(client: Client, callback_query: CallbackQuery):
    user = users_list.get_user(callback_query.from_user.id)
    if not user:
        await callback_query.answer(
            "İşlem iptal edildi. Başka bir işlem için /start komutunu kullanabilirsin.",
            show_alert=True,
        )
        return

    user.set_step(6)
    resource = user_resource_map[user.id]
    resource.set_course(callback_query.data)
    message = (
        "Kaynak bilgileri aşağıdaki gibi oluşturulacak. "
        "Lütfen bilgiler yanlışsa /iptal komutunu kullanarak işlemi iptal ediniz. "
        "Bilgileri onaylıyorsanız kaynağı PDF olarak yükleyip gönderebilirsiniz:\n"
        f"Yazar: {resource.author}\n"
        f"Ders: {TLIBotApiClient.get_courses()[resource.course]}\n"
        f"Açıklama: {resource.description}\n"
        f"Başlık: {resource.title}\n"
        f"Etiketler: {', '.join(resource.tags)}\n"
    )
    await client.send_message(callback_query.from_user.id, message)


@TLI.on_message(step_factory(6))
async def handle_file_upload(client: Client, message: Message):
    user = users_list.get_user(message.from_user.id)
    if not user:
        await message.reply_text(
            "İşlem iptal edildi. Başka bir işlem için /start komutunu kullanabilirsin.",
            quote=True,
        )
        return
    document = message.document
    if document is None or document.mime_type != "application/pdf":
        await message.reply_text(
            "Kaynak yüklemek için lütfen bir PDF dosyası gönderiniz.", quote=True
        )
        return
    user.set_step(7)
    resource = user_resource_map[user.id]
    uploaded_file = await client.download_media(message, in_memory=True)
    resource.set_file(uploaded_file)
    successful_upload = resource.upload_to_tli()
    if successful_upload:
        msg = await message.reply_text(
            "Kaynağınız Turkish Learning Initiative web sitesine gönderildi. "
            "Onaylandığında yayınlanacaktır.",
            quote=True,
        )
    else:
        msg = await message.reply_text(
            "Kaynağınız Turkish Learning Initiative web sitesine gönderilemedi. "
            "Lütfen daha sonra tekrar deneyiniz.",
            quote=True,
        )
    users_list.remove_user(user.id)
    await asyncio.sleep(1)
    await msg.edit_text(
        text=f"{msg.text}\nYeni kaynak yüklemek için /start komutunu kullanabilirsiniz.",
    )
