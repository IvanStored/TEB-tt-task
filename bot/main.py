import logging

import aiogram.utils.markdown as md
from aiogram import types

from aiogram.dispatcher import FSMContext

from aiogram.types import ParseMode, Message
from aiogram.utils import executor
from werkzeug.security import generate_password_hash

from bot.settings import bot, dp, form
from bot.utils import validate_password, validate_age
from flask_app import app


from flask_app.utils import user_service


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    """
    Start bot and FSM
    :param message:
    :param state:
    :return:
    """
    logging.basicConfig(
        level=logging.INFO,
        filename=f"user_{message.from_user.id}.log",
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logging.info(f"Start chat with user {message.from_user.id}")

    with app.app_context():
        user = user_service.get_user_by_id(user_id=message.from_user.id)

    if user is None:
        async with state.proxy() as data:
            data["user_info"] = await bot.get_chat(message.from_user.id)

        await form.password.set()
        await message.answer(text="Hello, answer please at follow questions:")
        await message.reply(
            text="""
            Create a password(it would be save in hash)
                    - At least 8 characters long
                    - Contains at least one uppercase letter
                    - Contains at least one lowercase letter
                    - Contains at least one digit
                    - Contains at least one special character (!@#$%^&*)
                """,
            reply_markup=None,
        )
    else:
        await state.finish()
        await message.answer(
            text="You already have account: /profile", reply_markup=None
        )


@dp.message_handler(
    lambda message: not validate_password(message.text), state=form.password
)
async def invalid_password(message: types.Message) -> Message:
    return await message.reply(text="Bad password")


@dp.message_handler(state=form.password)
async def process_password(message: types.Message, state: FSMContext) -> None:
    """
    Process password from user, save in temp data
    :param message:
    :param state:
    :return: None
    """
    async with state.proxy() as data:
        data["password"] = message.text
        logging.info("Get password")
    await message.delete()
    await form.next()

    await message.answer(text="How old are you?")


@dp.message_handler(
    lambda message: not validate_age(message.text),
    state=form.age,
)
async def process_age_invalid(message: types.Message) -> Message:
    return await message.reply(
        text="Age gotta be a positive number.\nHow old are you? (digits only)"
    )


@dp.message_handler(
    lambda message: message.text.isdigit(),
    state=form.age,
)
async def process_age(message: types.Message, state: FSMContext) -> None:
    """
    Process age from user, save in temp data
    :param message:
    :param state:
    :return: None
    """
    async with state.proxy() as data:
        data["age"] = int(message.text)
        logging.info(f"Get age: {message.text}")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    markup.add("Male", "Female")

    markup.add("Other")

    await message.reply(text="What is your gender?", reply_markup=markup)
    await form.next()


@dp.message_handler(
    lambda message: message.text not in ["Male", "Female", "Other"], state=form.gender
)
async def process_gender_invalid(message: types.Message) -> Message:
    return await message.reply(
        text="Bad gender name. Choose your gender from the keyboard."
    )


@dp.message_handler(state=form.gender)
async def process_gender(message: types.Message, state: FSMContext) -> None:
    """
    Process gender from user, save in temp data
    :param message:
    :param state:
    :return: None
    """
    async with state.proxy() as data:
        data["gender"] = message.text
        logging.info(f"Get gender: {message.text}")

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button_phone = types.KeyboardButton(text="Send phone", request_contact=True)

    keyboard.add(button_phone)

    await bot.send_message(
        chat_id=message.chat.id, text="Phone number", reply_markup=keyboard
    )
    await form.next()


@dp.message_handler(state=form.phone)
async def process_phone_invalid(message: types.Message) -> Message:
    if not message.contact:
        return await message.reply(text="Incorrect phone number. Please press button")


@dp.message_handler(state=form.phone, content_types=["contact"])
async def get_phone(message: types.Message, state: FSMContext) -> None:
    """
        Process phone number from user, save in temp data
    :param message:
    :param state:
    :return:
    """
    if message.contact.phone_number is not None:
        user_photos = await message.from_user.get_profile_photos()

        try:
            photo_url = await user_photos.photos[0][0].get_url()
            logging.info(f"Get last photo: {photo_url}")

        except Exception as e:
            logging.warning("No photo")
            photo_url = ""

        async with state.proxy() as data:
            data["phone"] = message.contact.phone_number
            logging.info(f"Get phone: {message.contact.phone_number}")

        markup = types.ReplyKeyboardRemove()
        password = generate_password_hash(data["password"], method="sha256")

        with app.app_context():
            result = user_service.create_user(
                user_id=data["user_info"].id,
                user_name=data["user_info"].username,
                first_name=data["user_info"].first_name,
                last_name=data["user_info"].last_name,
                bio=data["user_info"].bio,
                photo_url=photo_url,
                password=password,
                gender=data["gender"],
                age=data["age"],
                phone=data["phone"],
                is_premium=True if message.from_user.is_premium else False,
            )
        if result:
            await message.answer(text=result, reply_markup=markup)
        else:
            await message.answer(
                "Now you can back to https://teb-tt-task.onrender.com and login!",
                reply_markup=markup,
            )
    logging.info("Finish\n=================")
    await state.finish()


@dp.message_handler(commands="profile")
async def profile(message: types.Message) -> None:
    """
        Command, for checking your profile
    :param message:
    :return: None
    """
    with app.app_context():
        user = user_service.get_user_by_id(user_id=message.from_user.id)

    if user is not None:
        await message.answer(
            text=md.text(
                md.text("Hi! Nice to meet you,", md.bold(user.first_name)),
                md.text(
                    f"{'Please, login with phone number' if user.user_name == '' else f'Username: {user.user_name}'}"
                ),
                md.text("Age:", md.code(user.age)),
                md.text("Gender:", user.gender),
                md.text("Phone:", user.phone),
                sep="\n",
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await message.answer(
            text="Oops, u don`t have account yet, /start <- start registration",
            reply_markup=None,
        )


@dp.message_handler(commands=["update"])
async def update_info(message: types.Message) -> None:
    """
        Automatic update username, full name, bio
    :param message:
    :return: None
    """
    user_info = await bot.get_chat(chat_id=message.from_user.id)
    with app.app_context():
        result = user_service.update_information(user_info=user_info)
    if result:
        await message.reply(text=result)
    else:
        await message.reply(text="Information was updated")


@dp.message_handler(commands=["delete"])
async def delete_account(message: types.Message) -> None:
    """
    Command for delete your account from site using callback queries
    :param message:
    :return: None
    """
    kb = types.InlineKeyboardMarkup(row_width=2)
    button = types.InlineKeyboardButton(text="Yes", callback_data="confirm")
    button2 = types.InlineKeyboardButton(text="No", callback_data="decline")

    kb.add(button, button2)

    await message.reply(text="Are you sure?", reply_markup=kb)


@dp.callback_query_handler()
async def confirm_or_decline(callback: types.CallbackQuery):
    if callback.data == "decline":
        return await callback.answer(text="Nice!")
    elif callback.data == "confirm":
        with app.app_context():
            result = user_service.delete_account(user_id=callback.from_user.id)
        if result:
            return await callback.answer(text=result)
        return await callback.answer(text="Account was deleted")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
