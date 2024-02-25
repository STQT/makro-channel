from aiogram import Router, types
from django.utils.translation import gettext_lazy as _, activate
from app.users.models import TelegramUser as User
from bot.utils.kbs import menu_keyboards_dict

router = Router()


@router.message()
async def echo_handler(message: types.Message, user: User) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker etc.)
    """
    menu_text_list = [menu for emoji_list in menu_keyboards_dict.values() for menu in emoji_list]
    activate(user.language)

    if message.text in menu_text_list:
        if message.text in ("🌐 Социальные сети", "🌐 Ijtimoiy tarmoqlar"):
            socials = str(
                _("Наши социальные сети \n"
                  "<a href='https://www.facebook.com/makromarket.uz'>Facebook</a> | "
                  "<a href='https://www.instagram.com/makro_supermarket'>Instagram</a> | "
                  "<a href='https://t.me/makrosupermarket_uz'>Telegram</a>")
            )
            await message.answer(socials, disable_web_page_preview=True)

        elif message.text in ("🎁 Об акции", "🎁 Aksiya haqida"):
            await message.answer(str(
                _(
                    "Текст акции"
                ))
            )

    else:
        await message.answer(_("Неверная команда"))
