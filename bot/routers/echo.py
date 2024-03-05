from aiogram import Router, types
from django.utils.translation import gettext_lazy as _, activate
from app.users.models import TelegramUser as User
from bot.utils.kbs import menu_keyboards_dict, get_keyboard_fab

router = Router()


@router.message()
async def echo_handler(message: types.Message, user: User) -> None:
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
                    "💚 Ценные призы за подписку! Выигрывайте сертификаты на покупки в Makro"
                    "ℹ️ Подписывайте на наш официальный телеграмм канал @makrosupermarket_uz, "
                    "регистрируйтесь в боте и участвуйте в розыгрыше сертификатов."
                    " ✨ Разыгрываем 5 сертификатов по 500 000 сум."
                    "📅 Период проведения конкурса: ..."
                )))
        elif message.text in ("👤 Личный кабинет", "👤 Shaxsiy kabinet"):
            count = await user.referrals.acount()
            referred_by_user = None
            if user.referred_by_id:
                referred_by_obj = await User.objects.select_related(
                    'referred_by'
                ).aget(
                    referred_by_id=user.referred_by_id
                )
                referred_by_user = referred_by_obj.referred_by.fullname
            await message.answer(str(
                _(
                    "ФИО: {fullname}\n"
                    "Телефон: {phone}\n"
                    "Приглашено: {refferal} людей\n"
                    "{referred_by}"
                    "Приведите 5 друзей и удвойте свои шансы на победу!"
                ).format(
                    fullname=user.fullname,
                    phone=user.phone,
                    refferal=count,
                    referred_by=str(
                        _("Вас пригласил: {referred_by}\n").format(
                            referred_by=referred_by_user)
                    ) if referred_by_user else ""
                )),
                reply_markup=get_keyboard_fab(message.from_user.id)
            )
    else:
        await message.answer(str(_("Неверная команда")))
