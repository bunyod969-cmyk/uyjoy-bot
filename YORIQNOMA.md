# UyBozor Bot — Ishga tushirish yo’riqnomasi

## 1-QADAM: Bot token olish (2 daqiqa)

1. Telegramda **@BotFather** ga yozing
1. `/newbot` yuboring
1. Bot nomini kiriting: `UyBozor`
1. Username kiriting: `uybozor_bot` (yoki boshqa)
1. **Token** olinadi — saqlang!

-----

## 2-QADAM: Sizning Telegram ID ni aniqlash

1. Telegramda **@userinfobot** ga yozing
1. `/start` yuboring
1. **Id** raqamini saqlang (ADMIN_ID uchun kerak)

-----

## 3-QADAM: GitHub ga yuklash

1. **github.com** da akkaunt oching
1. Yangi repository yarating: `uybozor-bot`
1. Ushbu fayllarni yuklang:
- `bot.py`
- `requirements.txt`
- `Procfile`

-----

## 4-QADAM: Railway ga deploy qilish

1. **railway.app** ga kiring
1. **“New Project”** tugmasini bosing
1. **“Deploy from GitHub repo”** tanlang
1. `uybozor-bot` reponi tanlang
1. **Variables** bo’limiga o’ting va qo’shing:
   
   ```
   BOT_TOKEN = (BotFather dan olgan tokeningiz)
   ADMIN_ID  = (Telegram ID raqamingiz)
   ```
1. **Deploy** tugmasini bosing

-----

## 5-QADAM: Ishlatish

Bot tayyor! Telegramda botingizni toping va `/start` yuboring.

**Admin sifatida:**

- Har yangi e’lon sizga keladi
- ✅ Tasdiqlash yoki ❌ Rad etish tugmalarini bosing

-----

## Bot imkoniyatlari

|Tugma               |Vazifa              |
|--------------------|--------------------|
|📢 E’lon berish      |Yangi e’lon qo’shish|
|🔍 E’lonlarni ko’rish|Barcha e’lonlar     |
|🔎 Qidirish          |Shahar/nom bo’yicha |
|ℹ️ Yordam            |Qo’llanma           |

-----

Muammo bo’lsa — Claude ga yozing! 😊