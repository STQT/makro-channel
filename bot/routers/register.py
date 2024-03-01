import phonenumbers
from aiogram import Router, types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.conf import settings
from django.utils.translation import gettext_lazy as _, activate
from aiogram.types import KeyboardButton, ReplyKeyboardRemove

from bot.filters.states import Registration
from app.users.models import TelegramUser as User
from bot.helpers import format_phone_number
from bot.utils.kbs import contact_kb, language_kb, languages, menu_kb

router = Router()


@router.message(Command("start"))
async def on_start(message: types.Message, state: FSMContext, user: User):
    if not user.language or not user.phone or not user.fullname:
        hello_text = ("Вас приветствует бот сети супермаркетов Makro! Этот бот поможет "
                      "Вам в регистрации промокодов для участия в розыгрыше. "
                      "Для дальнейшей регистрации выберите пожалуйста язык.\n"
                      "Makro supermarketlar tarmog'ining boti sizni qutlaydi! "
                      "Ushbu bot sizga o'yinda ishtirok etish uchun "
                      "promokodlarni ro'yxatdan o'tkazishda yordam beradi. "
                      "Ro'yxatdan o'tish uchun tilni tanlang.")

        await message.answer(hello_text, reply_markup=language_kb())
        await state.set_state(Registration.language)
    else:
        await message.answer(str(_("Выберите раздел")), reply_markup=menu_kb(user.language))


@router.message(Registration.language)
async def registration_language(message: types.Message, state: FSMContext, user: User):
    if message.text and message.text in languages:
        lang = 'uz' if message.text == languages[0] else 'ru'
        user.language = lang
        activate(lang)
        await user.asave()
        await state.set_state(Registration.fio)
        await message.answer(str(_("Пожалуйста, введите свое имя и фамилию.\n"
                                   "❗️Обращаем Ваше внимание – имя и фамилия должны соответствовать "
                                   "удостоверению вашей личности.")),
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(str(_("Неверная команда")))


@router.message(Registration.fio)
async def registration_phone(message: types.Message, state: FSMContext, user: User):
    user.fullname = message.text
    await user.asave()
    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text=str(_("Отправить телефон")), request_contact=True))
    await message.answer(str(_("Введите Ваш контактный номер телефона регистрации промо-кода. "
                               "В случае выигрыша приза, мы будем связываться с Вами по указанному номеру телефона.")),
                         reply_markup=contact_kb())
    await state.set_state(Registration.phone)


@router.message(Registration.phone)
async def registration_finish(message: types.Message, state: FSMContext, user: User):
    error_text = str(_("Неправильно указан номер телефона. \n"
                       "Пожалуйста, введите номер телефона в формате +998 хх ххх хх хх"))
    if message.contact:
        user.phone = message.contact.phone_number
        await user.asave()
    elif message.text:
        formatted_phone = format_phone_number(message.text)
        if not formatted_phone.startswith("+998"):
            await message.answer(_("В акции можно учавствовать с узбекистанским номером"))
            return
        if len(formatted_phone) == 13:
            parsed_number = phonenumbers.parse(formatted_phone)
            is_valid = phonenumbers.is_valid_number(parsed_number)
            if is_valid:
                user.phone = formatted_phone
                await user.asave()
            else:
                await message.answer(error_text, reply_markup=contact_kb())
                return
        else:
            await message.answer(error_text, reply_markup=contact_kb())
            return
    else:
        await message.answer(error_text, reply_markup=contact_kb())
        return
    chat_member = await message.bot.get_chat_member(settings.TG_CHANNEL_ID, message.from_user.id)
    if chat_member.status == ChatMemberStatus.LEFT:
        await message.answer(
            str(_(
                "Вы успешно зарегистрировались на платформе! Чтобы учавствовать в розыгрыше подпишитесь на канал!")),
            reply_markup=menu_kb(user.language))
        await message.answer(settings.TG_CHANNEL_LINK)
    else:
        user.is_joined = True
        await user.asave()
        await message.answer(
            str(_(
                "Поздравляем! Вы учавствуете в розыгрыше"
            )),
            reply_markup=menu_kb(user.language)
        )
    await state.clear()
