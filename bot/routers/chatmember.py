import logging

from aiogram import Router, types
from aiogram.enums import ChatMemberStatus
from django.conf import settings

from app.users.models import TelegramUser
from django.utils.translation import gettext_lazy as _, activate

from bot.utils.kbs import menu_kb

router = Router()


@router.chat_member()
async def chat_member_handler(chat_member: types.ChatMemberUpdated):
    channel_id = settings.TG_CHANNEL_ID
    channel_link = settings.TG_CHANNEL_LINK
    chat_id = str(chat_member.chat.id)
    try:
        user = await TelegramUser.objects.aget(id=chat_member.from_user.id)
        if (
            chat_id == channel_id and
            chat_member.new_chat_member.status in
            (
                ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR
            )
        ):
            # If join user
            user.is_joined = True
            activate(user.language)
            await user.asave()
            await chat_member.bot.send_message(
                chat_member.from_user.id,
                str(_(
                    "Поздравляем! Вы учавствуете в розыгрыше сертификатов на покупки в Makro"
                )),
                reply_markup=menu_kb(user.language)
            )

        elif chat_id == channel_id:
            # If left or promote user
            user.is_joined = False
            activate(user.language)
            await user.asave()
            await chat_member.bot.send_message(
                chat_member.from_user.id,
                "Вы вышли с канала! Просим повторно подписаться, чтобы учавствовать в розыгрыше!\n"
                f"{channel_link}"
            )
    except TelegramUser.DoesNotExist:
        logging.warning(f"This user joining without bot: {chat_member.from_user.full_name}")


@router.my_chat_member()
async def my_chat_member_handler(chat_member: types.ChatMemberUpdated):
    if chat_member.new_chat_member.status != ChatMemberStatus.MEMBER:
        # If stop user
        user = await TelegramUser.objects.aget(id=chat_member.from_user.id)
        user.is_joined = False
        user.is_active = False
        await user.asave()
