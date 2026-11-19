
import os
import json

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

# =====================
# CAU HINH
# =====================

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 7726937606

ADMIN_FILE = "admins.json"

admins = set()
enabled = True


# =====================
# LUU ADMIN
# =====================

def load_admins():
    global admins

    try:
        with open(ADMIN_FILE, "r") as f:
            data = json.load(f)
            admins = set(int(x) for x in data)
    except (FileNotFoundError, json.JSONDecodeError):
        admins = set()


def save_admins():
    with open(ADMIN_FILE, "w") as f:
        json.dump(sorted(admins), f)


# =====================
# KIEM TRA QUYEN
# =====================

def is_owner(update):
    return (
        update.effective_user
        and update.effective_user.id == OWNER_ID
    )


def is_admin(update):
    return (
        update.effective_user
        and (
            update.effective_user.id == OWNER_ID
            or update.effective_user.id in admins
        )
    )


# =====================
# START
# =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "BOT DANG HOAT DONG\n"
        "Dung /help de xem lenh."
    )


# =====================
# HELP
# =====================

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Bat dau\n"
        "/help - Xem lenh\n"
        "/ping - Kiem tra bot\n"
        "/on - Bat bot\n"
        "/off - Tat bot\n"
        "/themadmin ID - Them admin\n"
        "/xoaadmin ID - Xoa admin\n"
        "/admins - Danh sach admin"
    )


# =====================
# PING
# =====================

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("BOT ONLINE!")


# =====================
# THEM ADMIN
# =====================

async def themadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    if not context.args:
        await update.message.reply_text("Dung: /themadmin ID")
        return

    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID khong hop le")
        return

    if user_id == OWNER_ID:
        await update.message.reply_text("Owner da co quyen cao nhat")
        return

    admins.add(user_id)
    save_admins()

    await update.message.reply_text(
        f"Da them admin ID: {user_id}"
    )


# =====================
# XOA ADMIN
# =====================

async def xoaadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    if not context.args:
        await update.message.reply_text("Dung: /xoaadmin ID")
        return

    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID khong hop le")
        return

    if user_id not in admins:
        await update.message.reply_text("ID nay khong phai admin")
        return

    admins.remove(user_id)
    save_admins()

    await update.message.reply_text(
        f"Da xoa admin ID: {user_id}"
    )


# =====================
# DANH SACH ADMIN
# =====================

async def admins_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    text = "OWNER:\n"
    text += str(OWNER_ID)
    text += "\n\nDANH SACH ADMIN:\n"

    if admins:
        text += "\n".join(str(x) for x in sorted(admins))
    else:
        text += "Chua co admin"

    await update.message.reply_text(text)


# =====================
# ON
# =====================

async def on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global enabled

    if not is_admin(update):
        return

    enabled = True
    await update.message.reply_text("BOT DA BAT")


# =====================
# OFF
# =====================

async def off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global enabled

    if not is_admin(update):
        return

    enabled = False
    await update.message.reply_text("BOT DA TAT")


# =====================
# MAIN
# =====================

def main():
    if not TOKEN:
        raise RuntimeError("THIEU BOT_TOKEN")

    load_admins()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))

    app.add_handler(CommandHandler("themadmin", themadmin))
    app.add_handler(CommandHandler("xoaadmin", xoaadmin))
    app.add_handler(CommandHandler("admins", admins_cmd))

    app.add_handler(CommandHandler("on", on))
    app.add_handler(CommandHandler("off", off))

    print("BOT DANG CHAY...")

    app.run_polling()


if __name__ == "__main__":
    main()
