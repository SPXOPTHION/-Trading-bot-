#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# استخدم التوكن والـ Chat ID الموجود
TELEGRAM_TOKEN = "8699821370:AAEQUSbLTgf7MmWqo5vV5LHPOz30wfqOfqw"
CHAT_ID = "7854020427"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start - يظهر القائمة الرئيسية"""
    welcome_message = """
👋 مرحباً بك في بوت توصيات الأسهم!

🎯 اختر ما تريد:
"""
    
    # إنشاء الأزرار بشكل صحيح
    keyboard = [
        [InlineKeyboardButton("📈 توصيات CALL", callback_data='call')],
        [InlineKeyboardButton("📉 توصيات PUT", callback_data='put')],
        [InlineKeyboardButton("🔄 مسح الآن", callback_data='scan')],
        [InlineKeyboardButton("ℹ️ معلومات", callback_data='info')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الأزرار"""
    query = update.callback_query
    
    # يجب الرد على الـ callback فوراً
    await query.answer()
    
    if query.data == 'call':
        await query.edit_message_text("📈 جاري البحث عن توصيات CALL...")
        # يمكنك إضافة الكود الخاص بك هنا
        await asyncio.sleep(1)
        await query.edit_message_text("✅ نتائج CALL:\n\nAPPL: شراء قوي")
        
    elif query.data == 'put':
        await query.edit_message_text("📉 جاري البحث عن توصيات PUT...")
        await asyncio.sleep(1)
        await query.edit_message_text("✅ نتائج PUT:\n\nTSLA: بيع")
        
    elif query.data == 'scan':
        await query.edit_message_text("🔄 جاري المسح الشامل...")
        await asyncio.sleep(2)
        await query.edit_message_text("✅ المسح اكتمل!\n\n📊 عدد الإشارات: 5")
        
    elif query.data == 'info':
        await query.edit_message_text("""
ℹ️ معلومات البوت:

📌 النسخة: 1.0
⏰ آخر تحديث: فبراير 2026
🎯 الأسهم المتابعة: 65

⚠️ إخلاء مسؤولية:
التوصيات لأغراض تعليمية فقط
"""
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /help"""
    help_text = """
🆘 أوامر البوت:

/start - عرض القائمة الرئيسية
/help - عرض المساعدة
/scan - مسح فوري

كل أزرار القائمة متفاعلة ✅
    """
    await update.message.reply_text(help_text)

def main():
    """تشغيل البوت"""
    # إنشاء التطبيق
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # تشغيل البوت
    print("✅ البوت يعمل الآن...")
    print("🚀 الرجاء إرسال /start في Telegram")
    
    app.run_polling()

if __name__ == "__main__":
    main()