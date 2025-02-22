

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwLxww5g9coLp42LZxVQ3qvMYv-e7bCb_ve4erdMP16B9nMYYYRQhDB3mpAJSWCmTY/exec"

async def nhap_kho(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("⚠️ Sai định dạng! Nhập: /nhapkho Tên nguyên liệu - SL nhập - Tổng SL")
        return

    message_text = " ".join(context.args).strip()
    username = update.message.from_user.full_name  # Lấy tên người gửi

    parts = [p.strip() for p in message_text.split("-")]
    if len(parts) != 3:
        await update.message.reply_text("⚠️ Sai định dạng! Nhập: /nhapkho Tên nguyên liệu - SL nhập - Tổng SL")
        return

    try:
        ten_nguyen_lieu, so_luong_nhap, tong_so_luong = parts
        so_luong_nhap = int(so_luong_nhap)  # Đảm bảo là số

        data = {
            "action": "nhapkho",
            "ten_nguyen_lieu": ten_nguyen_lieu,
            "so_luong_nhap": so_luong_nhap,
            "tong_so_luong": tong_so_luong,
            "nguoi_nhap": username
        }

        response = requests.post(WEB_APP_URL, json=data)
        json_data = response.json()
        if json_data.get("status") == "success":
            await update.message.reply_text(f"✅ Đã nhập kho: {ten_nguyen_lieu} - Nhập {so_luong_nhap} - Tổng {tong_so_luong}")
        else:
            await update.message.reply_text(f"⚠️ Lỗi từ server: {json_data.get('message', 'Không rõ nguyên nhân')}")
    except ValueError:
        await update.message.reply_text("⚠️ Lỗi: Số lượng nhập phải là số nguyên.")
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi xử lý nhập kho: {str(e)}")

async def xuat_kho(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("⚠️ Sai định dạng! Nhập: /xuatkho Tên nguyên liệu - SL xuất - SL còn lại")
        return

    message_text = " ".join(context.args).strip()
    username = update.message.from_user.full_name

    parts = [p.strip() for p in message_text.split("-")]
    if len(parts) != 3:
        await update.message.reply_text("⚠️ Sai định dạng! Nhập: /xuatkho Tên nguyên liệu - SL xuất - SL còn lại")
        return

    try:
        ten_nguyen_lieu, so_luong_xuat, so_luong_con_lai = parts
        so_luong_xuat = int(so_luong_xuat)  # Đảm bảo là số
        so_luong_con_lai = int(so_luong_con_lai)
        data = {
            "action": "xuatkho",
            "ten_nguyen_lieu": ten_nguyen_lieu,
            "so_luong_xuat": so_luong_xuat,
            "so_luong_con_lai": so_luong_con_lai,
            "nguoi_xuat": username
        }

        response = requests.post(WEB_APP_URL, json=data)
        json_data = response.json()
        if json_data.get("status") == "success":
            await update.message.reply_text(f"✅ Đã xuất kho: {ten_nguyen_lieu} - Xuất {so_luong_xuat} - Còn {so_luong_con_lai}")
        else:
            await update.message.reply_text(f"⚠️ Lỗi từ server: {json_data.get('message', 'Không rõ nguyên nhân')}")
    except ValueError:
        await update.message.reply_text("⚠️ Lỗi: Số lượng xuất phải là số nguyên.")
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi xử lý xuất kho: {str(e)}")


def main():
    TOKEN = "7572766270:AAGlFhr0CRXkPvEiHYTNejapWwnamrWRpAs"
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("nhapkho", nhap_kho))  # Không cần dấu ngoặc tròn
    application.add_handler(CommandHandler("xuatkho", xuat_kho))  # Không cần dấu ngoặc tròn

    application.run_polling()



if __name__ == "__main__":
    main()
