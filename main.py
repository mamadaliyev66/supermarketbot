import pyrebase
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5976543252:AAEQJVjJA0qVnXNUecMs_nIzd1RcuXbBySM'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

Config = {
    "apiKey": "AIzaSyB_DUljDu1O0ZaAqhL4SgRjwNP_BAtgoyc",
    "authDomain": "tgbot-98a9c.firebaseapp.com",
    "databaseURL": "https://tgbot-98a9c-default-rtdb.firebaseio.com",
    "projectId": "tgbot-98a9c",
    "storageBucket": "tgbot-98a9c.appspot.com",
    "messagingSenderId": "949866262678",
    "appId": "1:949866262678:web:209fa2ce57d978f06692b7",
    "measurementId": "G-8Y1H4S9L22"
}

firebase = pyrebase.initialize_app(Config)

db = firebase.database()

auth = firebase.auth()
storage = firebase.storage()

user = auth.sign_in_with_email_and_password('nethunterm@gmail.com', 's55tgk37')
keyboard = ''
btns_array = []


@dp.message_handler(commands=['start'])
async def startFun(message: types.Message):
    global keyboard
    global btns_array
    btns_array = []
    marketname = db.child('marketname').child('name').get().val()
    btns = db.child('start').get().val()
    btns = list(btns)
    for i in range(1, len(btns) + 1):
        btn = db.child('start').child('btn' + str(i)).get().val()
        btns_array.append([btn])
    keyboard = types.ReplyKeyboardMarkup(btns_array, resize_keyboard=True, one_time_keyboard=True)
    await message.reply(
        f"{marketname}ning Rasmiy Botiga Xush Kelibsiz !",
        reply_markup=keyboard
    )


admin_butttons = [
    ['➕Yangi Mahsulot Qoshish➕'],
    ["⚙️Mahsulotlar Ro'yxati⚙️"],
    ["◀️Admin Paneldan Chiqish🚪"]
]


@dp.message_handler(commands=['Admin123'])
async def AdminPanel(message: types.Message):
    adminKeyboard = types.ReplyKeyboardMarkup(admin_butttons, resize_keyboard=True, one_time_keyboard=True)
    await message.reply(
        'Well Come To Admin Panel ',
        reply_markup=adminKeyboard
    )


product_btn = []
p_name_ctg = []
admin_new_p_catg = []
newinf = ''
newpb = ''
newcost = ''
newname = ''
admin_new_p_catg2 = []
category_admin_pressed_btn = ''


@dp.message_handler()
async def listener(message: types.Message):
    global keyboard
    global admin_new_p_catg2
    global product_btn
    global p_name_ctg
    global btns_array
    global admin_new_p_catg
    text = message.text
    global newinf
    global newpb
    global newcost
    global newname
    global category_admin_pressed_btn
    try:
        for i in range(0, len(btns_array)):
            all_btns = btns_array[i][0]
            if text == all_btns:
                p_name_ctg = []
                products = db.child(text).get().val().keys()
                products = list(products)
                admin_new_p_catg = []
                for i in range(0, len(products)):
                    product_btn.append([products[i]])
                    p_name_ctg.append(products[i])
                    admin_new_p_catg.append(products[i] + '➕')
                product_btn.append(['Main Menu'])
                keyboard_product = types.ReplyKeyboardMarkup(product_btn, resize_keyboard=True, one_time_keyboard=True)
                await message.reply(
                    f"O'zingizga Kerakli Mahsulotni Tanlang 👇👇 :",
                    reply_markup=keyboard_product
                )
    except:
        print("This is Not")
    if text == 'Main Menu':
        await message.reply(
            "Main Menu",
            reply_markup=keyboard

        )
    if text in p_name_ctg:
        thisDB = db.child(btns_array[0][0]).child(text).child('All').get().val()
        thisDB = list(thisDB)
        keyboard_product = types.ReplyKeyboardMarkup(product_btn, resize_keyboard=True, one_time_keyboard=True,
                                                     input_field_placeholder='Wait . . .')
        for k in range(0, len(thisDB)):
            getDB = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).get().val()
            product_types = list(getDB)
            name = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).child(
                product_types[2]).get().val()
            info = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).child(
                product_types[1]).get().val()
            cost = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).child(
                product_types[0]).get().val()
            pb = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).child(
                product_types[3]).get().val()
            if pb == 'dollar':
                pb = '$'
            try:
                url = storage.child(f'{text}/p{str(k + 1)}.jpg').get_url(user['idToken'])
                await message.answer_photo(
                    url
                )
            except:
                print("No Image Found")
            await message.answer(
                f"Nomi: {name}"
                f"\n\n"
                f"Malumot: {info}"
                f"\n\n"
                f"Narxi: {str(cost) + str(pb)}"
            )
        await message.answer("Bizda Bor Mahsulotlar Shular edi. 👆",
                             reply_markup=keyboard_product
                             )
    keyboard_product_admin = ''
    if text == '➕Yangi Mahsulot Qoshish➕':
        products = db.child('Mahsulotlar').get().val().keys()
        products = list(products)
        admin_new_p_catg = []
        admin_new_p_catg2 = []
        for i in range(0, len(products)):
            admin_new_p_catg.append([products[i] + '➕'])
            admin_new_p_catg2.append(products[i] + '➕')
        admin_new_p_catg.append(['Back To Admin Panel'])
        keyboard_product_admin = types.ReplyKeyboardMarkup(admin_new_p_catg, resize_keyboard=True,
                                                           one_time_keyboard=True)
        await message.answer(
            "Turini Tanlang: ",
            reply_markup=keyboard_product_admin
        )
    if text in admin_new_p_catg2:
        text_length = len(text)
        category_admin_pressed_btn = text[0:text_length - 1]
    if text == 'Back To Admin Panel':
        adminKeyboard = types.ReplyKeyboardMarkup(admin_butttons, resize_keyboard=True, one_time_keyboard=True)
        await message.answer(
            "You Returned Admin Panel",
            reply_markup=adminKeyboard
        )
    add_btn = [["Qo'shish✅"]]
    adminKeyboard = types.ReplyKeyboardMarkup(add_btn, resize_keyboard=True, one_time_keyboard=True)
    for g in range(0, len(admin_new_p_catg) - 1):
        if text == admin_new_p_catg[g][0]:
            await message.answer(
                "Menga Qo'shmoqchi Bo'lgan Mahsulotingizni Nomini Jo'nating . \n "
                'Mahsulot Nomini Kiritish: nomi mahsulot nomi\n',
            )
    data = {}
    if text[0:4].lower() == "nomi":
        newname = text[5:]
        await message.reply(
            f'Yang Mahsulot Nomi Qabul Qilindi ✅'
        )
        await message.answer(
            f"Menga Yangi Mahsulotni Narxini ' narxi ' so'zidan so'ng  Jo'nating: \n\n"
            "Iltimos valutasini yozmang. ❌❌\n"
            "❗️Valutasini So'raganimda Jo'natasiz ❗️\n\n"
            "Misol Uchun : \n\n"
            "narxi 700"
        )
    if text[0:5].lower() == 'narxi':
        newcost = text[6:]
        await message.reply(
            f"Yangi Mahsulot Narxi  Qabul Qilindi ✅"
        )
        await message.answer(
            f"Menga Yangi Mahsulotni Narxini Pul Birligini ' pb ' so'zidan so'ng Jo'nating: \n\n"
            "Iltimos faqat valutasini Jo'nating. ❌❌\n"
            "Misol Uchun : \n\n"
            "pb dollar\npb som\npb euro"
        )
    if text[0:2].lower() == "pb":
        newpb = text[3:]
        if newpb == 'dollar' or newpb == ' dollar' or newpb == 'dollar ' or newpb == ' dollar ':
            newpb = '$'
        await message.reply(
            f"Maxsulotning Narxi va Valutasi Qabul Qilindi ✅"
        )
        await message.answer(
            f"Maxsulot Haqida Malumotni ' info ' so'zidan so'ng jo'nating :\n\n"
            f"❌ Malumotni info so'zidan song yozishingiz kerak yoqsa malumot qabul qilinmaydi ! ! ❌\n\n"
            f"Misol uchun: \n"
            f"info Bu mahsulot haqida malumot"
        )

    if text[0:4].lower() == 'info':
        newinf = text[5:]
        await message.reply(
            f"Mahsulot Haqida Malumot Qabul Qilindi ✅\n\n"
        )
        await message.answer(
            f"O'ylashimcha Barcha Malumotlar Qabul Qilindi ✅✅\n\n"
            f"Qo'shish✅ Tugmasini Bosish orqali Saqlashingiz Mumkun ! ",
            reply_markup=adminKeyboard
        )

    if text == "Qo'shish✅":
        if newname != "":
            if newcost != '':
                if newpb != '':
                    if newinf != '':
                        data.update({"name": newname, "cost": newcost, "pb": newpb, "info": newinf})
                        keyboard_product_admin = types.ReplyKeyboardMarkup(admin_new_p_catg, resize_keyboard=True,
                                                                           one_time_keyboard=True)
                        await message.answer(
                            f"Nomi : {newname} \n"
                            "\n\n"
                            f"Malumotlar: {newinf}\n\n"
                            f"narxi: {str(newcost) + str(newpb)}\n\n"
                            f"🟢Mahsulot Bazaga Muvafaqqiyatli qo'shildi✅✅",

                            reply_markup=keyboard_product_admin
                        )
                        p_get = db.child("Mahsulotlar").child(category_admin_pressed_btn).child(
                            "All").get().val().keys()
                        p = "p" + str(len(list(p_get)) + 1)
                        db.child('Mahsulotlar').child(category_admin_pressed_btn).child("All").child(p).set(data)
                    else:
                        await message.reply("Maxsulot haqida Malumot Mavjud Emas ❌")
                else:
                    await message.reply("Maxsulot Narxining Pul Birligi(valutasi) mavjud emas !")
            else:
                await message.reply("Maxsulot Narxi Mavjud Emas")
        else:
            await message.reply("Maxsulot Nomi Mavjud Emas.", reply_markup=keyboard_product_admin)

    if text == "⚙️Mahsulotlar Ro'yxati⚙️":
        reply_text = ''
        products_all_root = list(db.child("Mahsulotlar").get().val().keys())
        adminKeyboard = types.ReplyKeyboardMarkup(admin_butttons, resize_keyboard=True, one_time_keyboard=True)
        for i in range(0, len(products_all_root)):
            products_all_root_inside = list(
                db.child("Mahsulotlar").child(products_all_root[i]).child("All").get().val().keys())
            await message.answer(
                f"{products_all_root[i]}lar Ro'yxati\n"
                f"Jami: {len(products_all_root_inside)}ta"
            )
            for j in range(0, len(products_all_root_inside)):
                products_all_root_inside_i = list(
                    db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                        products_all_root_inside[j]).get().val())
                pname = db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                    products_all_root_inside[j]).child('name').get().val()
                pinfo = db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                    products_all_root_inside[j]).child('info').get().val()
                pcost = db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                    products_all_root_inside[j]).child('cost').get().val()
                ppb = db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                    products_all_root_inside[j]).child('pb').get().val()
                await message.answer(
                    f'Nomi: {pname}\n'
                    f"Malumot: {pinfo}\n"
                    f"Narxi: {pcost}{ppb}",
                )
        await message.answer("Barcha Mahsulotlar Shular Edi 👆 ",
                             reply_markup=adminKeyboard
                             )
    if text == "◀️Admin Paneldan Chiqish🚪":
        keyboard = types.ReplyKeyboardMarkup(btns_array, resize_keyboard=True, one_time_keyboard=True)
        await message.answer(
            "Main Menu",
            reply_markup=keyboard
        )

    if text.lower() == "biz haqimizda":
        keyboard = types.ReplyKeyboardMarkup(btns_array, resize_keyboard=True, one_time_keyboard=True)
        await message.answer_photo(
            'https://firebasestorage.googleapis.com/v0/b/tgbot-98a9c.appspot.com/o/market%2Fmarket.jpg?alt=media&token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1NWU0ZDkxOGE0ODY0YWQxMzUxMDViYmRjMDEwYWY5Njc5YzM0MTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGdib3QtOThhOWMiLCJhdWQiOiJ0Z2JvdC05OGE5YyIsImF1dGhfdGltZSI6MTY3MzU5MDg5MSwidXNlcl9pZCI6IjM3TTNRa29Mb2daakFIczRGS0lPeHlTUlB6STMiLCJzdWIiOiIzN00zUWtvTG9nWmpBSHM0RktJT3h5U1JQekkzIiwiaWF0IjoxNjczNTkwODkxLCJleHAiOjE2NzM1OTQ0OTEsImVtYWlsIjoibmV0aHVudGVybUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibmV0aHVudGVybUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.Xw_NQfsLGr7Hmr6XJWOvj3KcB5qd9CSTzJeEcVp0t-ScsgapdztZaw9RJzKBrvoFcNoyny1Bdi-9tnCH_8q5ugP28Ec3dqZYLHGDFdwicZKUuVuWr5rLfXczKLXVD3Gk1yONwddfCe3T9IP4BV06K9B2-b8hkr5B83-5oGK8vv2pzT6iLCfmwoY1y9WhRsm9Z1L370KZBOBDITkIoNYShqz70zrRy1MTlcxPgZzQK1BRt7BxgPXZBPr4XzK4ym49Ez1KtGu98M-D5grGRAaxq8flJYMotoe5u6Ot_NIz-dcz_iInri2dmEMeRcf2-Ies6Lw54g1hEI66vxzmr6sX6g'
        )
        await message.answer(
        "Farg'ona vodiysi,Rishton tumani uchun muddatli to'lov asosida 3000dan ortiq mahsulotlar.\n\n"
        "✅Yetkazish va o'rnatish bepul\n\n"
        "▫️▫️▫️▫️▫️\n\n"
        "☎️ +99873 452 33 22"
        , reply_markup=keyboard
        )

    import pyrebase
    from aiogram import Bot, Dispatcher, executor, types

    API_TOKEN = '2109667277:AAF7H179Zj9baAIMwH2PZDstwFXx3Ky0oSk'

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)

    Config = {
        "apiKey": "AIzaSyB_DUljDu1O0ZaAqhL4SgRjwNP_BAtgoyc",
        "authDomain": "tgbot-98a9c.firebaseapp.com",
        "databaseURL": "https://tgbot-98a9c-default-rtdb.firebaseio.com",
        "projectId": "tgbot-98a9c",
        "storageBucket": "tgbot-98a9c.appspot.com",
        "messagingSenderId": "949866262678",
        "appId": "1:949866262678:web:209fa2ce57d978f06692b7",
        "measurementId": "G-8Y1H4S9L22"
    }

    firebase = pyrebase.initialize_app(Config)

    db = firebase.database()

    auth = firebase.auth()
    storage = firebase.storage()

    user = auth.sign_in_with_email_and_password('nethunterm@gmail.com', 's55tgk37')
    keyboard = ''
    btns_array = []

    @dp.message_handler(commands=['start'])
    async def startFun(message: types.Message):
        global keyboard
        global btns_array
        btns_array = []
        marketname = db.child('marketname').child('name').get().val()
        btns = db.child('start').get().val()
        btns = list(btns)
        for i in range(1, len(btns) + 1):
            btn = db.child('start').child('btn' + str(i)).get().val()
            btns_array.append([btn])
        keyboard = types.ReplyKeyboardMarkup(btns_array, resize_keyboard=True, one_time_keyboard=True)
        await message.reply(
            f"{marketname}ning Rasmiy Botiga Xush Kelibsiz !",
            reply_markup=keyboard
        )

    admin_butttons = [
        ['➕Yangi Mahsulot Qoshish➕'],
        ["⚙️Mahsulotlar Ro'yxati⚙️"],
        ["◀️Admin Paneldan Chiqish🚪"]
    ]

    @dp.message_handler(commands=['Admin123'])
    async def AdminPanel(message: types.Message):
        adminKeyboard = types.ReplyKeyboardMarkup(admin_butttons, resize_keyboard=True, one_time_keyboard=True)
        await message.reply(
            'Well Come To Admin Panel ',
            reply_markup=adminKeyboard
        )

    product_btn = []
    p_name_ctg = []
    admin_new_p_catg = []
    newinf = ''
    newpb = ''
    newcost = ''
    newname = ''
    admin_new_p_catg2 = []
    category_admin_pressed_btn = ''

    @dp.message_handler()
    async def listener(message: types.Message):
        global keyboard
        global admin_new_p_catg2
        global product_btn
        global p_name_ctg
        global btns_array
        global admin_new_p_catg
        text = message.text
        global newinf
        global newpb
        global newcost
        global newname
        global category_admin_pressed_btn
        try:
            for i in range(0, len(btns_array)):
                all_btns = btns_array[i][0]
                if text == all_btns:
                    p_name_ctg = []
                    products = db.child(text).get().val().keys()
                    products = list(products)
                    admin_new_p_catg = []
                    for i in range(0, len(products)):
                        product_btn.append([products[i]])
                        p_name_ctg.append(products[i])
                        admin_new_p_catg.append(products[i] + '➕')
                    product_btn.append(['Main Menu'])
                    keyboard_product = types.ReplyKeyboardMarkup(product_btn, resize_keyboard=True,
                                                                 one_time_keyboard=True)
                    await message.reply(
                        f"O'zingizga Kerakli Mahsulotni Tanlang 👇👇 :",
                        reply_markup=keyboard_product
                    )
        except:
            print("This is Not")
        if text == 'Main Menu':
            await message.reply(
                "Main Menu",
                reply_markup=keyboard

            )
        if text in p_name_ctg:
            thisDB = db.child(btns_array[0][0]).child(text).child('All').get().val()
            thisDB = list(thisDB)
            keyboard_product = types.ReplyKeyboardMarkup(product_btn, resize_keyboard=True, one_time_keyboard=True,
                                                         input_field_placeholder='Wait . . .')
            for k in range(0, len(thisDB)):
                getDB = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).get().val()
                product_types = list(getDB)
                name = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).child(
                    product_types[2]).get().val()
                info = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).child(
                    product_types[1]).get().val()
                cost = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).child(
                    product_types[0]).get().val()
                pb = db.child(btns_array[0][0]).child(text).child('All').child(thisDB[k]).child(
                    product_types[3]).get().val()
                if pb == 'dollar':
                    pb = '$'
                try:
                    url = storage.child(f'{text}/p{str(k + 1)}.jpg').get_url(user['idToken'])
                    await message.answer_photo(
                        url
                    )
                except:
                    print("No Image Found")
                await message.answer(
                    f"Nomi: {name}"
                    f"\n\n"
                    f"Malumot: {info}"
                    f"\n\n"
                    f"Narxi: {str(cost) + str(pb)}"
                )
            await message.answer("Bizda Bor Mahsulotlar Shular edi. 👆",
                                 reply_markup=keyboard_product
                                 )
        keyboard_product_admin = ''
        if text == '➕Yangi Mahsulot Qoshish➕':
            products = db.child('Mahsulotlar').get().val().keys()
            products = list(products)
            admin_new_p_catg = []
            admin_new_p_catg2 = []
            for i in range(0, len(products)):
                admin_new_p_catg.append([products[i] + '➕'])
                admin_new_p_catg2.append(products[i] + '➕')
            admin_new_p_catg.append(['Back To Admin Panel'])
            keyboard_product_admin = types.ReplyKeyboardMarkup(admin_new_p_catg, resize_keyboard=True,
                                                               one_time_keyboard=True)
            await message.answer(
                "Turini Tanlang: ",
                reply_markup=keyboard_product_admin
            )
        if text in admin_new_p_catg2:
            text_length = len(text)
            category_admin_pressed_btn = text[0:text_length - 1]
        if text == 'Back To Admin Panel':
            adminKeyboard = types.ReplyKeyboardMarkup(admin_butttons, resize_keyboard=True, one_time_keyboard=True)
            await message.answer(
                "You Returned Admin Panel",
                reply_markup=adminKeyboard
            )
        add_btn = [["Qo'shish✅"]]
        adminKeyboard = types.ReplyKeyboardMarkup(add_btn, resize_keyboard=True, one_time_keyboard=True)
        for g in range(0, len(admin_new_p_catg) - 1):
            if text == admin_new_p_catg[g][0]:
                await message.answer(
                    "Menga Qo'shmoqchi Bo'lgan Mahsulotingizni Nomini Jo'nating . \n "
                    'Mahsulot Nomini Kiritish: nomi mahsulot nomi\n',
                )
        data = {}
        if text[0:4].lower() == "nomi":
            newname = text[5:]
            await message.reply(
                f'Yang Mahsulot Nomi Qabul Qilindi ✅'
            )
            await message.answer(
                f"Menga Yangi Mahsulotni Narxini ' narxi ' so'zidan so'ng  Jo'nating: \n\n"
                "Iltimos valutasini yozmang. ❌❌\n"
                "❗️Valutasini So'raganimda Jo'natasiz ❗️\n\n"
                "Misol Uchun : \n\n"
                "narxi 700"
            )
        if text[0:5].lower() == 'narxi':
            newcost = text[6:]
            await message.reply(
                f"Yangi Mahsulot Narxi  Qabul Qilindi ✅"
            )
            await message.answer(
                f"Menga Yangi Mahsulotni Narxini Pul Birligini ' pb ' so'zidan so'ng Jo'nating: \n\n"
                "Iltimos faqat valutasini Jo'nating. ❌❌\n"
                "Misol Uchun : \n\n"
                "pb dollar\npb som\npb euro"
            )
        if text[0:2].lower() == "pb":
            newpb = text[3:]
            if newpb == 'dollar' or newpb == ' dollar' or newpb == 'dollar ' or newpb == ' dollar ':
                newpb = '$'
            await message.reply(
                f"Maxsulotning Narxi va Valutasi Qabul Qilindi ✅"
            )
            await message.answer(
                f"Maxsulot Haqida Malumotni ' info ' so'zidan so'ng jo'nating :\n\n"
                f"❌ Malumotni info so'zidan song yozishingiz kerak yoqsa malumot qabul qilinmaydi ! ! ❌\n\n"
                f"Misol uchun: \n"
                f"info Bu mahsulot haqida malumot"
            )

        if text[0:4].lower() == 'info':
            newinf = text[5:]
            await message.reply(
                f"Mahsulot Haqida Malumot Qabul Qilindi ✅\n\n"
            )
            await message.answer(
                f"O'ylashimcha Barcha Malumotlar Qabul Qilindi ✅✅\n\n"
                f"Qo'shish✅ Tugmasini Bosish orqali Saqlashingiz Mumkun ! ",
                reply_markup=adminKeyboard
            )

        if text == "Qo'shish✅":
            if newname != "":
                if newcost != '':
                    if newpb != '':
                        if newinf != '':
                            data.update({"name": newname, "cost": newcost, "pb": newpb, "info": newinf})
                            keyboard_product_admin = types.ReplyKeyboardMarkup(admin_new_p_catg, resize_keyboard=True,
                                                                               one_time_keyboard=True)
                            await message.answer(
                                f"Nomi : {newname} \n"
                                "\n\n"
                                f"Malumotlar: {newinf}\n\n"
                                f"narxi: {str(newcost) + str(newpb)}\n\n"
                                f"🟢Mahsulot Bazaga Muvafaqqiyatli qo'shildi✅✅",

                                reply_markup=keyboard_product_admin
                            )
                            p_get = db.child("Mahsulotlar").child(category_admin_pressed_btn).child(
                                "All").get().val().keys()
                            p = "p" + str(len(list(p_get)) + 1)
                            db.child('Mahsulotlar').child(category_admin_pressed_btn).child("All").child(p).set(data)
                        else:
                            await message.reply("Maxsulot haqida Malumot Mavjud Emas ❌")
                    else:
                        await message.reply("Maxsulot Narxining Pul Birligi(valutasi) mavjud emas !")
                else:
                    await message.reply("Maxsulot Narxi Mavjud Emas")
            else:
                await message.reply("Maxsulot Nomi Mavjud Emas.", reply_markup=keyboard_product_admin)

        if text == "⚙️Mahsulotlar Ro'yxati⚙️":
            reply_text = ''
            products_all_root = list(db.child("Mahsulotlar").get().val().keys())
            adminKeyboard = types.ReplyKeyboardMarkup(admin_butttons, resize_keyboard=True, one_time_keyboard=True)
            for i in range(0, len(products_all_root)):
                products_all_root_inside = list(
                    db.child("Mahsulotlar").child(products_all_root[i]).child("All").get().val().keys())
                await message.answer(
                    f"{products_all_root[i]}lar Ro'yxati\n"
                    f"Jami: {len(products_all_root_inside)}ta"
                )
                for j in range(0, len(products_all_root_inside)):
                    products_all_root_inside_i = list(
                        db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                            products_all_root_inside[j]).get().val())
                    pname = db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                        products_all_root_inside[j]).child('name').get().val()
                    pinfo = db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                        products_all_root_inside[j]).child('info').get().val()
                    pcost = db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                        products_all_root_inside[j]).child('cost').get().val()
                    ppb = db.child("Mahsulotlar").child(products_all_root[i]).child("All").child(
                        products_all_root_inside[j]).child('pb').get().val()
                    await message.answer(
                        f'Nomi: {pname}\n'
                        f"Malumot: {pinfo}\n"
                        f"Narxi: {pcost}{ppb}",
                    )
            await message.answer("Barcha Mahsulotlar Shular Edi 👆 ",
                                 reply_markup=adminKeyboard
                                 )
        if text == "◀️Admin Paneldan Chiqish🚪":
            keyboard = types.ReplyKeyboardMarkup(btns_array, resize_keyboard=True, one_time_keyboard=True)
            await message.answer(
                "Main Menu",
                reply_markup=keyboard
            )

        if text.lower() == "biz haqimizda":
            keyboard = types.ReplyKeyboardMarkup(btns_array, resize_keyboard=True, one_time_keyboard=True)
            await message.answer_photo(
                'https://firebasestorage.googleapis.com/v0/b/tgbot-98a9c.appspot.com/o/market%2Fmarket.jpg?alt=media&token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1NWU0ZDkxOGE0ODY0YWQxMzUxMDViYmRjMDEwYWY5Njc5YzM0MTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGdib3QtOThhOWMiLCJhdWQiOiJ0Z2JvdC05OGE5YyIsImF1dGhfdGltZSI6MTY3MzU5MDg5MSwidXNlcl9pZCI6IjM3TTNRa29Mb2daakFIczRGS0lPeHlTUlB6STMiLCJzdWIiOiIzN00zUWtvTG9nWmpBSHM0RktJT3h5U1JQekkzIiwiaWF0IjoxNjczNTkwODkxLCJleHAiOjE2NzM1OTQ0OTEsImVtYWlsIjoibmV0aHVudGVybUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibmV0aHVudGVybUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.Xw_NQfsLGr7Hmr6XJWOvj3KcB5qd9CSTzJeEcVp0t-ScsgapdztZaw9RJzKBrvoFcNoyny1Bdi-9tnCH_8q5ugP28Ec3dqZYLHGDFdwicZKUuVuWr5rLfXczKLXVD3Gk1yONwddfCe3T9IP4BV06K9B2-b8hkr5B83-5oGK8vv2pzT6iLCfmwoY1y9WhRsm9Z1L370KZBOBDITkIoNYShqz70zrRy1MTlcxPgZzQK1BRt7BxgPXZBPr4XzK4ym49Ez1KtGu98M-D5grGRAaxq8flJYMotoe5u6Ot_NIz-dcz_iInri2dmEMeRcf2-Ies6Lw54g1hEI66vxzmr6sX6g'
            )
            await message.answer(
                "Farg'ona vodiysi,Rishton tumani uchun muddatli to'lov asosida 3000dan ortiq mahsulotlar.\n\n"
                "✅Yetkazish va o'rnatish bepul\n\n"
                "▫️▫️▫️▫️▫️\n\n"
                "☎️ +99873 452 33 22"
                , reply_markup=keyboard
            )

        if text.lower() == "bog'lanish":
            keyboard = types.ReplyKeyboardMarkup(btns_array, resize_keyboard=True, one_time_keyboard=True)
            await message.answer_photo(
                'https://firebasestorage.googleapis.com/v0/b/tgbot-98a9c.appspot.com/o/market%2Fmarket.jpg?alt=media&token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1NWU0ZDkxOGE0ODY0YWQxMzUxMDViYmRjMDEwYWY5Njc5YzM0MTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGdib3QtOThhOWMiLCJhdWQiOiJ0Z2JvdC05OGE5YyIsImF1dGhfdGltZSI6MTY3MzU5MDg5MSwidXNlcl9pZCI6IjM3TTNRa29Mb2daakFIczRGS0lPeHlTUlB6STMiLCJzdWIiOiIzN00zUWtvTG9nWmpBSHM0RktJT3h5U1JQekkzIiwiaWF0IjoxNjczNTkwODkxLCJleHAiOjE2NzM1OTQ0OTEsImVtYWlsIjoibmV0aHVudGVybUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibmV0aHVudGVybUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.Xw_NQfsLGr7Hmr6XJWOvj3KcB5qd9CSTzJeEcVp0t-ScsgapdztZaw9RJzKBrvoFcNoyny1Bdi-9tnCH_8q5ugP28Ec3dqZYLHGDFdwicZKUuVuWr5rLfXczKLXVD3Gk1yONwddfCe3T9IP4BV06K9B2-b8hkr5B83-5oGK8vv2pzT6iLCfmwoY1y9WhRsm9Z1L370KZBOBDITkIoNYShqz70zrRy1MTlcxPgZzQK1BRt7BxgPXZBPr4XzK4ym49Ez1KtGu98M-D5grGRAaxq8flJYMotoe5u6Ot_NIz-dcz_iInri2dmEMeRcf2-Ies6Lw54g1hEI66vxzmr6sX6g'
            )
            await message.answer(

                "Farg'ona vodiysi,Rishton tumani uchun muddatli to'lov asosida 3000dan ortiq mahsulotlar\n\n"
                "✅Yetkazish va o'rnatish bepul\n\n"
                "🌐 Biz Bilan Bog'aning\n\n"
                "📱Telefon Raqam: +998 90 777 55 20\n\n"
                "📮 @lider_trade",
                reply_markup=keyboard
            )

    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=False)



    if text.lower() == "bog'lanish":
        keyboard = types.ReplyKeyboardMarkup(btns_array, resize_keyboard=True, one_time_keyboard=True)
        await message.answer_photo(
'https://firebasestorage.googleapis.com/v0/b/tgbot-98a9c.appspot.com/o/market%2Fmarket.jpg?alt=media&token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1NWU0ZDkxOGE0ODY0YWQxMzUxMDViYmRjMDEwYWY5Njc5YzM0MTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGdib3QtOThhOWMiLCJhdWQiOiJ0Z2JvdC05OGE5YyIsImF1dGhfdGltZSI6MTY3MzU5MDg5MSwidXNlcl9pZCI6IjM3TTNRa29Mb2daakFIczRGS0lPeHlTUlB6STMiLCJzdWIiOiIzN00zUWtvTG9nWmpBSHM0RktJT3h5U1JQekkzIiwiaWF0IjoxNjczNTkwODkxLCJleHAiOjE2NzM1OTQ0OTEsImVtYWlsIjoibmV0aHVudGVybUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibmV0aHVudGVybUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.Xw_NQfsLGr7Hmr6XJWOvj3KcB5qd9CSTzJeEcVp0t-ScsgapdztZaw9RJzKBrvoFcNoyny1Bdi-9tnCH_8q5ugP28Ec3dqZYLHGDFdwicZKUuVuWr5rLfXczKLXVD3Gk1yONwddfCe3T9IP4BV06K9B2-b8hkr5B83-5oGK8vv2pzT6iLCfmwoY1y9WhRsm9Z1L370KZBOBDITkIoNYShqz70zrRy1MTlcxPgZzQK1BRt7BxgPXZBPr4XzK4ym49Ez1KtGu98M-D5grGRAaxq8flJYMotoe5u6Ot_NIz-dcz_iInri2dmEMeRcf2-Ies6Lw54g1hEI66vxzmr6sX6g'
            )
        await message.answer(

            "Farg'ona vodiysi,Rishton tumani uchun muddatli to'lov asosida 3000dan ortiq mahsulotlar\n\n"
            "✅Yetkazish va o'rnatish bepul\n\n"
            "🌐 Biz Bilan Bog'aning\n\n"
            "📱Telefon Raqam: +998 90 777 55 20\n\n"
            "📮 @lider_trade",
            reply_markup=keyboard
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
