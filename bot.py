import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "8965942057:AAGfmy2SaldA0ebWJT2FoF-IK-jWo7B8A5Y")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "7942622482"))
DB_FILE = "elon_db.json"

CHOOSING_TYPE, ENTER_TITLE, ENTER_PRICE, ENTER_AREA, ENTER_LOCATION, ENTER_PHONE, ENTER_DESC, ENTER_PHOTO, SEARCH_QUERY = range(9)

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"elonlar": [], "counter": 0}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def main_keyboard():
    return ReplyKeyboardMarkup([
        ["📢 E'lon berish"],
        ["🔍 E'lonlarni ko'rish", "🔎 Qidirish"],
        ["ℹ️ Yordam"]
    ], resize_keyboard=True)

def type_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Xonadon", callback_data="type_xonadon"),
         InlineKeyboardButton("🏡 Uy", callback_data="type_uy")],
        [InlineKeyboardButton("🌿 Yer", callback_data="type_yer"),
         InlineKeyboardButton("🏢 Tijorat", callback_data="type_tijorat")],
        [InlineKeyboardButton("❌ Bekor", callback_data="cancel")]
    ])

def admin_keyboard(elon_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{elon_id}"),
         InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{elon_id}")]
    ])

def format_elon(elon):
    return (
        f"🏷 Tur: {elon['tur']}\n"
        f"📌 Sarlavha: {elon['sarlavha']}\n"
        f"💰 Narx: {elon['narx']}\n"
        f"📐 Maydon: {elon['maydon']}\n"
        f"📍 Manzil: {elon['manzil']}\n"
        f"📞 Telefon: {elon['telefon']}\n"
        f"📝 Tavsif: {elon['tavsif']}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    text = (
        f"Assalomu alaykum, {name}!\n\n"
        "🏠 UyBozor Botga xush kelibsiz!\n\n"
        "Ko'chmas mulk elonlari bering va koring.\n\n"
        "Quyidagi tugmalardan tanlang 👇"
    )
    await update.message.reply_text(text, reply_markup=main_keyboard())

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ Yordam\n\n"
        "📢 E'lon berish - yangi elon\n"
        "🔍 E'lonlarni ko'rish - barcha elonlar\n"
        "🔎 Qidirish - shahar yoki nom boyicha\n\n"
        "Muammo bolsa adminga yozing."
    )
    await update.message.reply_text(text)

async def elon_berish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("📢 Elon turini tanlang:", reply_markup=type_keyboard())
    return CHOOSING_TYPE

async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "cancel":
        await query.edit_message_text("Bekor qilindi.")
        return ConversationHandler.END
    type_map = {
        "type_xonadon": "🏠 Xonadon",
        "type_uy": "🏡 Uy",
        "type_yer": "🌿 Yer",
        "type_tijorat": "🏢 Tijorat"
    }
    context.user_data["tur"] = type_map[query.data]
    await query.edit_message_text(f"{context.user_data['tur']} tanlandi.\n\nSarlavhani kiriting:\nMisol: 3 xonali kvartira Chilonzor")
    return ENTER_TITLE

async def enter_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sarlavha"] = update.message.text
    await update.message.reply_text("💰 Narxni kiriting:\nMisol: 85000$ yoki 950 000 000 som")
    return ENTER_PRICE

async def enter_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["narx"] = update.message.text
    await update.message.reply_text("📐 Maydonni kiriting:\nMisol: 78 kv.m yoki 8 sotix")
    return ENTER_AREA

async def enter_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["maydon"] = update.message.text
    await update.message.reply_text("📍 Manzilni kiriting:\nMisol: Toshkent, Chilonzor tumani")
    return ENTER_LOCATION

async def enter_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["manzil"] = update.message.text
    await update.message.reply_text("📞 Telefon raqamni kiriting:\nMisol: +998901234567")
    return ENTER_PHONE

async def enter_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["telefon"] = update.message.text
    await update.message.reply_text("📝 Qoshimcha malumot kiriting.\nYoq bolsa - yoq deb yozing.")
    return ENTER_DESC

async def enter_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tavsif"] = update.message.text
    await update.message.reply_text("📸 Rasm yuboring (ixtiyoriy)\nRasm yoq bolsa /skip yozing")
    return ENTER_PHOTO

async def enter_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["rasm"] = update.message.photo[-1].file_id
    else:
        context.user_data["rasm"] = None
    await save_elon(update, context)
    return ConversationHandler.END

async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["rasm"] = None
    await save_elon(update, context)
    return ConversationHandler.END

async def save_elon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    db["counter"] += 1
    elon_id = db["counter"]
    elon = {
        "id": elon_id,
        "user_id": update.effective_user.id,
        "username": update.effective_user.username or "Noma'lum",
        "tur": context.user_data["tur"],
        "sarlavha": context.user_data["sarlavha"],
        "narx": context.user_data["narx"],
        "maydon": context.user_data["maydon"],
        "manzil": context.user_data["manzil"],
        "telefon": context.user_data["telefon"],
        "tavsif": context.user_data["tavsif"],
        "rasm": context.user_data.get("rasm"),
        "tasdiqlangan": False
    }
    db["elonlar"].append(elon)
    save_db(db)
    await update.message.reply_text(
        f"Elon #{elon_id} qabul qilindi!\nAdmin tasdiqlagandan song ko'rinadi.",
        reply_markup=main_keyboard()
    )
    elon_text = format_elon(elon)
    try:
        if elon.get("rasm"):
            await context.bot.send_photo(ADMIN_ID, elon["rasm"],
                caption=f"Yangi elon #{elon_id}\n\n{elon_text}",
                reply_markup=admin_keyboard(elon_id))
        else:
            await context.bot.send_message(ADMIN_ID,
                f"Yangi elon #{elon_id}\n\n{elon_text}",
                reply_markup=admin_keyboard(elon_id))
    except Exception as e:
        logger.error(f"Admin xabar xato: {e}")

async def elonlarni_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    tasdiqlangan = [e for e in db["elonlar"] if e["tasdiqlangan"]]
    if not tasdiqlangan:
        await update.message.reply_text("Hozircha elon yoq.", reply_markup=main_keyboard())
        return
    await update.message.reply_text(f"Jami {len(tasdiqlangan)} ta elon:")
    for elon in tasdiqlangan[-10:]:
        text = f"Elon #{elon['id']}\n\n{format_elon(elon)}"
        try:
            if elon.get("rasm"):
                await update.message.reply_photo(elon["rasm"], caption=text)
            else:
                await update.message.reply_text(text)
        except Exception:
            await update.message.reply_text(text)

async def qidirish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Qidiruv sozini kiriting:\nMisol: Chilonzor, yer, 3 xonali")
    return SEARCH_QUERY

async def qidirish_natija(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kalit = update.message.text.lower()
    db = load_db()
    natijalar = [
        e for e in db["elonlar"]
        if e["tasdiqlangan"] and (
            kalit in e["sarlavha"].lower() or
            kalit in e["manzil"].lower() or
            kalit in e["tur"].lower()
        )
    ]
    if not natijalar:
        await update.message.reply_text("Elon topilmadi.", reply_markup=main_keyboard())
        return ConversationHandler.END
    await update.message.reply_text(f"{len(natijalar)} ta elon topildi:")
    for elon in natijalar[:5]:
        text = f"Elon #{elon['id']}\n\n{format_elon(elon)}"
        try:
            if elon.get("rasm"):
                await update.message.reply_photo(elon["rasm"], caption=text)
            else:
                await update.message.reply_text(text)
        except Exception:
            await update.message.reply_text(text)
    return ConversationHandler.END

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if update.effective_user.id != ADMIN_ID:
        await query.answer("Siz admin emassiz!", show_alert=True)
        return
    data = query.data
    db = load_db()
    if data.startswith("approve_"):
        elon_id = int(data.split("_")[1])
        for elon in db["elonlar"]:
            if elon["id"] == elon_id:
                elon["tasdiqlangan"] = True
                save_db(db)
                try:
                    await query.edit_message_reply_markup(reply_markup=None)
                except Exception:
                    pass
                await context.bot.send_message(query.message.chat_id, f"Elon #{elon_id} tasdiqlandi!")
                try:
                    await context.bot.send_message(elon["user_id"], f"Elon #{elon_id} tasdiqlandi!")
                except Exception:
                    pass
                break
    elif data.startswith("reject_"):
        elon_id = int(data.split("_")[1])
        db["elonlar"] = [e for e in db["elonlar"] if e["id"] != elon_id]
        save_db(db)
        try:
            await query.edit_message_reply_markup(reply_markup=None)
        except Exception:
            pass
        await context.bot.send_message(query.message.chat_id, f"Elon #{elon_id} rad etildi.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Bekor qilindi.", reply_markup=main_keyboard())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    elon_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📢 E'lon berish$"), elon_berish_start)],
        states={
            CHOOSING_TYPE: [CallbackQueryHandler(choose_type)],
            ENTER_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_title)],
            ENTER_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_price)],
            ENTER_AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_area)],
            ENTER_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_location)],
            ENTER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_phone)],
            ENTER_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_desc)],
            ENTER_PHOTO: [
                MessageHandler(filters.PHOTO, enter_photo),
                CommandHandler("skip", skip_photo),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    qidirish_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^🔎 Qidirish$"), qidirish_start)],
        states={
            SEARCH_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, qidirish_natija)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(elon_handler)
    app.add_handler(qidirish_handler)
    app.add_handler(MessageHandler(filters.Regex("^🔍 E'lonlarni ko'rish$"), elonlarni_korish))
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ Yordam$"), help_cmd))
    app.add_handler(CallbackQueryHandler(admin_callback, pattern="^(approve|reject)_"))
    logger.info("Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
ENDOFFILE
python3 -c "import ast; ast.parse(open('/home/claude/elonbot/bot_new.py').read()); print('OK')"
