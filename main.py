import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import firebase_admin
from firebase_admin import credentials, db

# Firebase সেটআপ
cred = credentials.Certificate("serviceAccountKey.json") 
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://srx-fc926-default-rtdb.firebaseio.com'
})

TOKEN = "8878802711:AAGyYQonV6ftDgL0ZwriPNoPFFr8lLPvvOs"
ADMIN_ID = 8757063670

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# মেইন মেনু (ইউজারদের জন্য)
def main_menu():
    keyboard = [
        [InlineKeyboardButton("Create Task", callback_data='create'), InlineKeyboardButton("My Task", callback_data='mytask')],
        [InlineKeyboardButton("Account", callback_data='account'), InlineKeyboardButton("Deposit", callback_data='deposit')],
        [InlineKeyboardButton("WITHDRAW", callback_data='withdraw')],
        [InlineKeyboardButton("Leaderboard", callback_data='leaderboard'), InlineKeyboardButton("Invite", callback_data='invite')],
        [InlineKeyboardButton("Watch Tutorial", callback_data='tutorial')]
    ]
    return InlineKeyboardMarkup(keyboard)

# এডমিন মেনু (শুধুমাত্র আপনার জন্য)
def admin_menu():
    keyboard = [
        [InlineKeyboardButton("Confirm Deposit", callback_data='adm_dep_conf'), InlineKeyboardButton("Confirm Withdraw", callback_data='adm_wit_conf')],
        [InlineKeyboardButton("Manage Users", callback_data='adm_users'), InlineKeyboardButton("Add Task", callback_data='adm_add_task')]
    ]
    return InlineKeyboardMarkup(keyboard)

# স্টার্ট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Earnify! Choose an option:", reply_markup=main_menu())

# এডমিন কমান্ড
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("Admin Control Panel:", reply_markup=admin_menu())
    else:
        await update.message.reply_text("You are not authorized to use this.")

# বাটন হ্যান্ডলার
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # সাধারণ বাটন হ্যান্ডলিং
    if query.data == 'account':
        await query.edit_message_text(text="Account Details: Balance = $0.00", reply_markup=main_menu())
    
    # এডমিন বাটন হ্যান্ডলিং
    elif query.data == 'adm_dep_conf':
        await query.edit_message_text(text="Admin: Confirming Deposits...", reply_markup=admin_menu())
    elif query.data == 'adm_wit_conf':
        await query.edit_message_text(text="Admin: Confirming Withdrawals...", reply_markup=admin_menu())
    # এখানে অন্যান্য লজিক যোগ করুন

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin)) # এডমিন কমান্ড রেজিস্টার করা হলো
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()
