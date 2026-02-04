import asyncio
import logging
import uuid
from aiogram import Bot, Dispatcher, types
from platega import AsyncPlategaClient
from platega.models import PaymentMethod, PaymentDetails, CreateTransactionRequest
import config

# Логгирование
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# Клиент Platega
platega_client = AsyncPlategaClient(
    merchant_id=config.PLATEGA_MERCHANT_ID,
    secret_key=config.PLATEGA_SECRET_KEY
)

@dp.inline_query()
async def inline_payment_handler(query: types.InlineQuery):
    text = query.query.strip()
    
    # Если ввод пустой или не число — не реагируем
    if not text or not text.isdigit():
        return

    amount = int(text)

    try:
        # Формирование запроса к Platega
        request_data = CreateTransactionRequest(
            paymentMethod=PaymentMethod.SBP_QR,
            paymentDetails=PaymentDetails(
                amount=float(amount),
                currency="RUB"
            ),
            description=f"Оплата (Inline) от {query.from_user.id}",
            return_url="https://t.me/your_bot_username",
            failedUrl="https://t.me/your_bot_username",
            payload=f"order_inline_{query.from_user.id}_{uuid.uuid4().hex[:8]}"
        )

        # Создание ссылки
        response = await platega_client.create_invoice(request_data)
        payment_url = response.redirect

        # Формирование результата для меню
        result = types.InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"Оплатить {amount} RUB через СБП",
            description="Нажми, чтобы отправить ссылку на оплату",
            input_message_content=types.InputTextMessageContent(
                message_text=f"💸 Ссылка на оплату {amount} RUB (СБП):\n{payment_url}",
                disable_web_page_preview=True
            )
        )

        # Отправка ответа пользователю (меню выбора)
        await query.answer([result], cache_time=1, is_personal=True)

    except Exception as e:
        logging.error(f"Error creating inline invoice: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
