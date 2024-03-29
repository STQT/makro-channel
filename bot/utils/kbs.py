from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from aiogram.types import KeyboardButton, SwitchInlineQueryChosenChat

languages = (
    str(_("🇺🇿 O'zbek tili")),
    str(_("🇷🇺 Русский язык"))
)
menu_keyboards_dict = {
    "ru": ("🎁 Об акции", "🌐 Социальные сети", "👤 Личный кабинет", "👥 Пригласить друга"),
    "uz": ("🎁 Aksiya haqida", "🌐 Ijtimoiy tarmoqlar", "👤 Shaxsiy kabinet", "👥 Doʻstni chaqirish")
}


def contact_kb():
    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text=str(_("Отправить телефон")), request_contact=True))
    return markup.adjust(2).as_markup(resize_keyboard=True)


def language_kb():
    markup = ReplyKeyboardBuilder()
    markup.add(
        *(KeyboardButton(text=lang) for lang in languages)
    )
    return markup.adjust(2).as_markup(resize_keyboard=True)


def menu_kb(language_code='ru'):
    markup = ReplyKeyboardBuilder()
    markup.add(
        *(KeyboardButton(text=menu) for menu in menu_keyboards_dict[language_code])
    )
    return markup.adjust(1).as_markup(resize_keyboard=True)


def get_invite_text(user_id, is_markdown=False):
    link = settings.TG_BOT_LINK + "?start=" + str(user_id)
    link = "<a href='" + link + str(_("'>Ссылка</a>")) if is_markdown else link
    text = str(
        _(
            "Ценные призы за подписку! Выигрывайте сертификаты на покупки в Makro\n"
            "ℹ️ {link}"

        )).format(link=link)
    return text


def get_keyboard_fab(user_id):
    builder = InlineKeyboardBuilder()
    text = get_invite_text(user_id)
    builder.button(
        text=str(_("Пригласить друга")),
        switch_inline_query=text
    )
    builder.adjust(1)
    return builder.as_markup()
