from config import photos,elite_photos,ero_photos,arc_photos,trap_photos,casino_pics
from threading import Thread
import random
import schedule
import telebot
from telebot import types
import time
import logging
import math
from datetime import datetime
from flask import Flask, request, send_from_directory, send_file, jsonify
import os
from PIL import Image,ImageDraw,ImageFont, ImageStat
import emoji
import textwrap
from petpetgif.saveGif import save_transparent_gif
from pkg_resources import resource_stream
from sqlalchemy import create_engine
import json
import requests

token = '5388861642:AAGb08Jk5d_ukvzENmIY8JXn94UySQPsJ9A'
bot = telebot.TeleBot(token, threaded=False)

#cursor = create_engine("mysql+mysqldb://Bibasosinka:foxy1987@Bibasosinka.mysql.pythonanywhere-services.com/Bibasosinka$default",pool_recycle=280)
cursor = create_engine("sqlite:///nekoslavia.db",pool_recycle=280)
#conn = connect(host="Bibasosinka.mysql.pythonanywhere-services.com",user="Bibasosinka",password="foxy1987", database="Bibasosinka$default")
#cursor = engine.connect()
#cursor = conn.cursor()

frames = 10
resolution = (512, 512)
delay = 20

APP_URL = f'https://nekoslaviabot.mihamishu123.repl.co/{token}'
app = Flask(__name__)
bot.remove_webhook()
bot.set_webhook(url=APP_URL)

random.seed()

enemies = [['Gayster',3,243,24],['Gayster blaster (незаряж.)',2,232,92],['Gayster blaster (заряж.)',2,232,92],['Петрович',3,175,15],['Gay bomb',1,240,183],['ЛГБТ Слизень',3,186,163],['Враждебная слизь',1,240,207]]

cans = [0]
can = True
dcan = True

patch_version = 106
patch_title = 'Заебись'
patch_text = 'Бот заработал, но это не точно'
patch_image = 'AgACAgIAAx0CZQN7rQACznBjQgABiPsE5FE7am8mfAOKiXsSOEsAAju9MRuS1hFKlyErHhjWQfcBAAMCAANzAAMqBA'

skill_list = ['<b>Нет навыка ❌</b>\n','<b>Крепкое здоровье 🫀 (пассив)</b>\nКвадраты восстанавливают здоровье вместо блоков\n','<b>Повышенная сила 🟡 (пассив)</b>\nБольше жёлтых кругов на поле, при их складывании появляется звезда\n','<b>Повышенная скорость 💙 (пассив)</b>\nБольше синих сердец на поле, при их складывании появляется звезда\n','<b>Последний шанс 💔 (пассив)</b>\nВ два раза больше урона при 1 хп\n','<b>Энергичность ⚡️ (пассив)</b>\nВ два раза больше урона при максимальном хп\n','<b>Девять жизней 🐱 (пассив)</b>\nСпасает от смерти один раз\n','<b>Атака со спины 💫 (пассив)</b>\n4 хода на первый ход\n','<b>Звезда ⭐️ (актив)</b>\nПревращает выбранную фигуру в звезду\n','<b>Разрушение 💥 (актив)</b>\nРазрушает выбранную фигуру, заменяя её пустотой\n','<b>Перемешать 🔄 (актив)</b>\nПеремешывает поле, при этом количество фигур каждого цвета не изменяется\n','<b>Превентивный удар 🗡 (актив)</b>\nЗабирает один ход, но наносит урон врагу\n','<b>Защитная стойка 🛡 (актив)</b>\nЗабирает один ход, но даёт один блок\n','<b>Звёздный час 🌟 (актив)</b>\nДве случайные фигуры заменяет звёздами\n','<b>Ход конём 🧩 (актив)</b>\nЕсли выбранных фигур на поле не меньше одиннадцати, заменяет их на пустоту и делает действие в зависимости от типа фигуры (1 блок, 1 урон или 1 ход)\n']
passive_skill_list = ['<b>Нет навыка ❌</b>\n',
'<b>Крепкое здоровье 🫀 (пассив)</b>\nКвадраты восстанавливают здоровье вместо блоков\n',
'<b>Повышенная сила 🟡 (пассив)</b>\nБольше жёлтых кругов на поле, при их складывании появляется звезда\n',
'<b>Повышенная скорость 💙 (пассив)</b>\nБольше синих сердец на поле, при их складывании появляется звезда\n',
'<b>Последний шанс 💔 (пассив)</b>\nНа одну единицу урона больше если 2 хп или меньше\n',
'<b>Энергичность ⚡️ (пассив)</b>\nНа одну единицу урона больше при максимальном хп\n',
'<b>Девять жизней 🐱 (пассив)</b>\nСпасает от смерти один раз\n',
'<b>Атака со спины 💫 (пассив)</b>\n4 хода на первый ход\n',
'<b>Удача ☘️ (пассив)</b>\n5% шанс увернуться от любой атаки, срабатывает не более двух раз за бой\n',
'<b>Справедливость ⚖️ (пассив)</b>\nДополнительный ход если твоё хп меньше суммарного хп врагов, не работает на первый ход\n',
'<b>Неоправданный риск ♠️ (пассив)</b>\nНа одну единицу урона больше если атаковать во время последнего хода не имея при этом блоков\n'
]
active_skill_list = ['<b>Нет навыка ❌</b>\n',
'<b>Звезда ⭐️ (актив)</b>\nПревращает выбранную фигуру в звезду\n',
'<b>Разрушение 💥 (актив)</b>\nРазрушает выбранную фигуру, заменяя её пустотой\n',
'<b>Перемешать 🔄 (актив)</b>\nПеремешывает поле, при этом количество фигур каждого цвета не изменяется\n',
'<b>Превентивный удар 🗡 (актив)</b>\nЗабирает один ход, но наносит урон врагу\n',
'<b>Защитная стойка 🛡 (актив)</b>\nЗабирает один ход, но даёт один блок\n',
'<b>Звёздный час 🌟 (актив)</b>\nДве случайные фигуры заменяет звёздами\n',
'<b>Ход конём 🧩 (актив)</b>\nЕсли выбранных фигур на поле не меньше одиннадцати, заменяет их на пустоту и делает действие в зависимости от типа фигуры (1 блок, 1 урон или 1 ход)\n',
'<b>Аннигиляция 🔥 (актив)</b>\nУничтожает ряд фигур на поле\n',
'<b>Звёздная ярость ✨ (актив)</b>\nУничтожает выбранную звезду, но даёт 1 ход\n',
'<b>Умножение 💕 (актив)</b>\nДобавляет 2 фигуры выбранного цвета на поле, работает со звёздами\n'
]

skill_names = ['Нет навыка ❌',
'Звезда ⭐️',
'Разрушение 💥',
'Перемешать 🔄',
'Превентивный удар 🗡',
'Защитная стойка 🛡',
'Звёздный час 🌟',
'Ход конём 🧩',
'Аннигиляция 🔥',
'Звёздная ярость ✨',
'Умножение 💕'
]
nekosas = {'540255407': '16 4',
'738931917': '17 2',
'523497602': '4 7',
'729883976': '19 2',
'448214297': '29 4',
'503671007': '3 10',
'460507186': '19 1',
'783003689': '27 1'}
def date_string(cur):
    dy = int(cur.day)
    if dy < 10:
        dy = '0'+str(dy)
    else:
        dy = str(dy)
    mn = int(cur.month)
    if mn < 10:
        mn = '0'+str(mn)
    else:
        mn = str(mn)
    yr = str(cur.year)
    date = dy+'.'+mn+'.'+yr
    return date
def pack(mas):
    data = {"data": mas}
    data = json.dumps(data,ensure_ascii=False)
    return data
def unpack(data):
    mas = json.loads(data)
    mas = mas["data"]
    return mas
def dominant_color(filename):
        #Resizing parameters
        width, height = 150,150
        image = Image.open(filename)
        image = image.resize((width, height),resample = 0)
        #Get colors from image object
        pixels = image.getcolors(width * height)
        #Sort them by count number(first element of tuple)
        sorted_pixels = sorted(pixels, key=lambda t: t[0])
        #Get the most frequent color
        dominant_color = sorted_pixels[-1][1]
        return dominant_color
def make(source, dest, clr):
    images = []
    base = Image.open(source).convert('RGBA').resize(resolution)

    for i in range(frames):
        squeeze = i if i < frames/2 else frames - i
        width = 0.8 + squeeze * 0.02
        height = 0.8 - squeeze * 0.05
        offsetX = (1 - width) * 0.5 + 0.1
        offsetY = (1 - height) - 0.08

        canvas = Image.new('RGBA', size=resolution, color=clr)
        canvas.paste(base.resize((round(width * resolution[0]), round(height * resolution[1]))), (round(offsetX * resolution[0]), round(offsetY * resolution[1])))
        pet = Image.open(resource_stream(__name__, f"bot/pet{i}.gif")).convert('RGBA').resize(resolution)
        canvas.paste(pet, mask=pet)
        images.append(canvas)

    save_transparent_gif(images, durations=20, save_file=dest)
def gazeta():
    global patch_image
    lines = textwrap.wrap(patch_text, width=35)
    ptxt = ''
    for line in lines:
        ptxt = ptxt + line + '\n'
    im0 = Image.open('bot/gazetka.png')
    font = ImageFont.truetype('bot/times-new-roman.ttf', size=50)
    draw = ImageDraw.Draw(im0)
    draw.text((70, 130), ptxt, font=font, fill=(82, 64, 64))
    w = font.getlength(patch_title)
    draw.text(((924-w)/2,50), patch_title, font=font, fill=(82, 64, 64))
    im0.save('bot/result.png')
    f = open("bot/result.png","rb")
    m = bot.send_photo(-1001694727085, photo=f)
    patch_image = m.photo[len(m.photo) - 1].file_id
gazeta()
papers_images = []
prof = ['Монтажник','Электрик','Токарь','Сварщик','Охранник']
bad_prof = random.choice(prof)
def papers():
    global papers_images,prof,bad_prof
    for k in range(1,11):
        propusk = random.choice([True,False])
        reason = 0
        if not propusk:
            reason = random.randint(1,5)
        im0 = Image.open('bot/zavod/papers.png')
        im1 = Image.open('bot/zavod/table'+str(k)+'.png')
        im0.paste(im1.convert('RGB'), (0,0))
        if reason == 1:
            k2 = random.randint(1,10)
            while k == k2:
                k2 = random.randint(1,10)
            im2 = Image.open('bot/zavod/pas'+str(k2)+'.png')
            im0.paste(im2.convert('RGB'), (445,35))
        else:
            im2 = Image.open('bot/zavod/pas'+str(k)+'.png')
            im0.paste(im2.convert('RGB'), (445,35))
        names = ['Мику', 'Бака', 'Наруто', 'Макима', 'Шмара']
        families = ['Некочановна','Славонековна','Кринжеделовна','Сосалка','Дегенератовна']
        draw = ImageDraw.Draw(im0)
        font = ImageFont.truetype('bot/segoeprint_bold.ttf', size=24)
        text = random.choice(names) + ' ' + random.choice(families)
        draw.text((650, 100), text, font=font,fill="#f0f0f0", stroke_width=2, stroke_fill='#141414')
        font = ImageFont.truetype('bot/segoeprint_bold.ttf', size=20)
        if reason == 2:
            p = bad_prof
            text = 'Профессия: ' + p
            draw.text((650, 137), text, font=font, fill="#141414", stroke_width=0, stroke_fill='#141414')
        else:
            p = random.choice(prof)
            while p == bad_prof:
                p = random.choice(prof)
            text = 'Профессия: ' + p
            draw.text((650, 137), text, font=font, fill="#141414", stroke_width=0, stroke_fill='#141414')
        if reason == 3:
            days = random.randint(10,363)
            date = date_string(datetime.fromtimestamp(time.time() + days*3600*24))
            text = 'Выдано: ' + date
            draw.text((650, 165), text, font=font, fill="#141414", stroke_width=0, stroke_fill='#141414')
        else:
            days = random.randint(20,363)
            date = date_string(datetime.fromtimestamp(time.time() - days*3600*24))
            text = 'Выдано: ' + date
            draw.text((650, 165), text, font=font, fill="#141414", stroke_width=0, stroke_fill='#141414')
        if reason == 4:
            days = random.randint(1,15)
            date = date_string(datetime.fromtimestamp(time.time() - days*3600*24))
            text = 'До: ' + date
            draw.text((650, 193), text, font=font, fill="#141414", stroke_width=0, stroke_fill='#141414')
        else:
            days = random.randint(10,363)
            date = date_string(datetime.fromtimestamp(time.time() + days*3600*24))
            text = 'До: ' + date
            draw.text((650, 193), text, font=font, fill="#141414", stroke_width=0, stroke_fill='#141414')
        if reason == 5:
            pechat = random.choice([True,False])
            if pechat:
                im3 = Image.open('bot/zavod/skamik.png')
                im0.paste(im3.convert('RGB'), (840,110),im3)
        else:
            im3 = Image.open('bot/zavod/slavik.png')
            im0.paste(im3.convert('RGB'), (840,110),im3)
        im0.save('bot/zavod/result.png')
        f = open("bot/zavod/result.png","rb")
        m = bot.send_photo(-1001694727085, photo=f)
        img = m.photo[len(m.photo) - 1].file_id
        papers_images.append(str(img) + ' ' + str(propusk))
        time.sleep(2)
papers()


def equ(a):
    if -1 in a:
        return False
    for i in range(5):
        b = a.copy()
        for j in range(len(b)):
            if b[j] == 5:
                b[j] = i
        if b.count(b[0]) == len(b):
            return True
    return False
def fielder(field,sk1,sk2,do_stars):
    atack = 0
    blocks = 0
    turns = 0
    stars = 0
    skills = [sk1,sk2]
    b = [0,1,2,3,4]
    if 2 in skills:
        b.append(2)
    if 3 in skills:
        b.append(4)
    while True:
        found = False
        for j in range(6):
            i = 0
            a = [field[j*6+i],field[j*6+i+1],field[j*6+i+2],field[j*6+i+3],field[j*6+i+4],field[j*6+i+5]]
            if equ(a):

                if 2 in a and 2 in skills:
                    stars += 1
                if 4 in a and 3 in skills:
                    stars += 1

                if 0 in a or 1 in a:
                    blocks = blocks + 3
                elif 2 in a or 3 in a:
                    atack = atack + 3
                elif 4 in a:
                    turns = turns + 3
                field[j*6+i] = -1
                field[j*6+i+1] = -1
                field[j*6+i+2] = -1
                field[j*6+i+3] = -1
                field[j*6+i+4] = -1
                field[j*6+i+5] = -1
                found = True
        for i in range(6):
            j = 0
            a = [field[j*6+i],field[(j+1)*6+i],field[(j+2)*6+i],field[(j+3)*6+i],field[(j+4)*6+i],field[(j+5)*6+i]]
            if equ(a):

                if 2 in a and 2 in skills:
                    stars += 1
                if 4 in a and 3 in skills:
                    stars += 1

                if 0 in a or 1 in a:
                    blocks = blocks + 3
                elif 2 in a or 3 in a:
                    atack = atack + 3
                elif 4 in a:
                    turns = turns + 3
                field[j*6+i] = -1
                field[(j+1)*6+i] = -1
                field[(j+2)*6+i] = -1
                field[(j+3)*6+i] = -1
                field[(j+4)*6+i] = -1
                field[(j+5)*6+i] = -1
                found = True
        for j in range(6):
            for i in range(2):
                a = [field[j*6+i],field[j*6+i+1],field[j*6+i+2],field[j*6+i+3],field[j*6+i+4]]
                if equ(a):

                    if 2 in a and 2 in skills:
                        stars += 1
                    if 4 in a and 3 in skills:
                        stars += 1

                    if 0 in a or 1 in a:
                        blocks = blocks + 2
                    elif 2 in a or 3 in a:
                        atack = atack + 2
                    elif 4 in a:
                        turns = turns + 2
                    field[j*6+i] = -1
                    field[j*6+i+1] = -1
                    field[j*6+i+2] = -1
                    field[j*6+i+3] = -1
                    field[j*6+i+4] = -1
                    found = True
        for j in range(2):
            for i in range(6):
                a = [field[j*6+i],field[(j+1)*6+i],field[(j+2)*6+i],field[(j+3)*6+i],field[(j+4)*6+i]]
                if equ(a):

                    if 2 in a and 2 in skills:
                        stars += 1
                    if 4 in a and 3 in skills:
                        stars += 1

                    if 0 in a or 1 in a:
                        blocks = blocks + 2
                    elif 2 in a or 3 in a:
                        atack = atack + 2
                    elif 4 in a:
                        turns = turns + 2
                    field[j*6+i] = -1
                    field[(j+1)*6+i] = -1
                    field[(j+2)*6+i] = -1
                    field[(j+3)*6+i] = -1
                    field[(j+4)*6+i] = -1
                    found = True
        for j in range(6):
            for i in range(3):
                a = [field[j*6+i],field[j*6+i+1],field[j*6+i+2],field[j*6+i+3]]
                if equ(a):

                    if 2 in a and 2 in skills:
                        stars += 1
                    if 4 in a and 3 in skills:
                        stars += 1

                    if 0 in a or 1 in a:
                        blocks = blocks + 1
                    elif 2 in a or 3 in a:
                        atack = atack + 1
                    elif 4 in a:
                        turns = turns + 1
                    field[j*6+i] = -1
                    field[j*6+i+1] = -1
                    field[j*6+i+2] = -1
                    field[j*6+i+3] = -1
                    found = True
        for j in range(3):
            for i in range(6):
                a = [field[j*6+i],field[(j+1)*6+i],field[(j+2)*6+i],field[(j+3)*6+i]]
                if equ(a):

                    if 2 in a and 2 in skills:
                        stars += 1
                    if 4 in a and 3 in skills:
                        stars += 1

                    if 0 in a or 1 in a:
                        blocks = blocks + 1
                    elif 2 in a or 3 in a:
                        atack = atack + 1
                    elif 4 in a:
                        turns = turns + 1
                    field[j*6+i] = -1
                    field[(j+1)*6+i] = -1
                    field[(j+2)*6+i] = -1
                    field[(j+3)*6+i] = -1
                    found = True
        if -1 in field and found == False:
            found = True
        if found == False:
            break
        while True:
            for i in range(36):
                if field[i] == -1:
                    if i < 6:
                        if stars > 0 and do_stars:
                            stars -= 1
                            field[i] = 5
                        else:
                            field[i] = random.choice(b)
                    else:
                        field[i] = field[i-6]
                        field[i-6] = -1
            if -1 not in field:
                break

    result = [atack,blocks,turns]
    return result
def combinator(cards):
    numbers = []
    colors = []
    for card in cards:
        b = round((card%1)*10)
        a = round(card)
        numbers.append(a)
        colors.append(b)
    max_low = sorted(numbers)
    max_low.reverse()
    #Старшая карта
    comb = 0 + max(numbers)/100
    #Пара
    for n in max_low:
        if numbers.count(n) >= 2:
            comb = 1 + n/100
            break
    #Две пары
    p1 = 0
    p2 = 0
    for n in max_low:
        if numbers.count(n) >= 2 and n != p1 and n != p2:
            if p1 == 0:
                p1 = n
            else:
                p2 = n
        if p1 != 0 and p2 != 0:
            comb = 2 + max(p1,p2)/100 + min(p1,p2)/10000
            break
    #Сет
    for n in max_low:
        if numbers.count(n) >= 3:
            comb = 3 + n/100
            break
    #Стрит
    max_l = sorted(list(set(max_low)))
    max_l.reverse()
    for i in range(len(cards)):
        try:
            if max_l[i] == max_l[i+1]+1 and max_l[i+1] == max_l[i+2]+1 and max_l[i+2] == max_l[i+3]+1 and max_l[i+3] == max_l[i+4]+1:
                comb = 4 + max_l[i]/100
                break
        except:
            pass
    #Флеш
    for color in colors:
                if colors.count(color) >= 5:
                    crd = cards.copy()
                    for x in crd:
                        if round((x%1)*10) != color:
                            crd.remove(x)
                    comb = 5 + (round(max(crd)))/100
                    break
    #Фулл хаус
    two = 0
    three = 0
    for n in max_low:
        if numbers.count(n) >= 3:
            three = n
        elif numbers.count(n) >= 2:
            two = n
        if two != 0  and three != 0:
            comb = 6 + three/100 + two/10000
            break

    #Каре
    for n in max_low:
                if numbers.count(n) >= 4:
                    comb = 7 + n/100
                    break
    #Стрит флеш
    for j in range(4):
        max_l = []
        for x in cards:
            if round((x%1)*10) == j + 1:
                max_l.append(round(x))
        max_l = sorted(max_l)
        max_l.reverse()
        for i in range(len(max_l)):
            try:
                if max_l[i] == max_l[i+1]+1 and max_l[i+1] == max_l[i+2]+1 and max_l[i+2] == max_l[i+3]+1 and max_l[i+3] == max_l[i+4]+1:
                    if max_l[i] == 14:
                        comb = 9 + max_l[i]/100
                    else:
                        comb = 8 + max_l[i]/100
                    break

            except:
                pass

    return comb
def check_poker(idk):
    data = cursor.execute('SELECT * FROM poker')
    data = data.fetchall()
    if data is None:
        return False
    for d in data:
        players = unpack(d[7])
        if idk in players:
            return True
    return False
@bot.message_handler(commands=["start"])
def msg_start(message):
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
        data = data.fetchone()
        if data is None:
            p = random.choice(photos)
            kormit = int(time.time()-4*3600)
            gulat = int(time.time())
            cursor.execute("INSERT INTO neko (id,name,rep,gulat,kormit,photo,bolnitsa,zavod,base,car,event,coins,buff,licension) VALUES ("+str(message.from_user.id)+",'Некодевочка',0,"+str(gulat)+","+str(kormit)+",'"+p+"',0,0,0,0,0,0,0,"+str(time.time() + 345600)+")")

            bot.send_message(message.chat.id,'Добро пожаловать в Некославию! Каждому гражданину, согласно конституции, полагается некодевочка, держи свою\n\n/cmd - список комманд\n\n/help - полезные ссылки')
            time.sleep(2)
            text = 'Надо бы пояснить тебе наши порядки. <b>Некославия</b> - великая держава, а великая держава должна заботиться о благополучии своих гражданах, не так ли? Для этого запущена специальная социальная программа - каждому полагается по некодевочке, без очередей и налогов. К счастью, благодаря новейшим разработкам у нас их достаточно. По закону каждый некослав обязан заботиться о своей некодевочке, а её смерть уголовно наказуема'
            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsJRi4vTvzOG-zrdVRRS3iQhKUm-K_QAC37oxG6IdGEsIcBwLxnaZgwEAAwIAA3MAAykE',caption = text,parse_mode='HTML')
            time.sleep(2)
            text = 'А вот и твоя некодевочка. Вероятно, она проголодалась пока ждала тебя. Напиши /neko чтобы убедиться в этом, а когда покормишь - не забудь дать ей имя'
            bot.send_photo(message.chat.id, photo = p,caption = text,parse_mode='HTML')
            photo_design = 'AgACAgIAAx0CZQN7rQAC1H9jUKXUvp7PcTBU56QeArc8auJhJgAC5MQxGxUkiUrpDEdocq5guwEAAwIAA3MAAyoE'
            m = bot.send_photo(-1001694727085,photo=photo_design,caption = 'Идёт обработка...')
            file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = 'bot/files/' + file_info.file_path
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            im0 = Image.open(src)
            w,h = im0.size
            if w > h:
                nh = 630
                nw = int((630/h)*w)
            else:
                nw = 600
                nh = int((600/w)*h)
            if nw < 600:
                nw = 600
            if nh < 630:
                nh = 630
            im0 = im0.resize((nw, nh),  Image.ANTIALIAS)
            im1 = Image.open('bot/white1.png')
            im1.paste(im0.convert('RGB'), (40,34))
            im0 = im1
            im1 = Image.open('bot/02.png')
            im0.paste(im1.convert('RGB'), (0,0), im1)
            im0 = im0.convert('RGBA')
            pixdata = im0.load()
            for y in range(im0.size[1]):
                for x in range(im0.size[0]):
                    if pixdata[x,y][0]==255 and pixdata[x,y][1]==0 and pixdata[x,y][2]==0:
                        pixdata[x, y] = (255, 255, 255,0)

            chel = message.from_user.first_name
            if len(chel) > 18:
                chel = (chel[:18] + '..')
            m = bot.send_photo(-1001694727085,photo=p,caption = 'Идёт обработка...')
            file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = 'bot/files/' + file_info.file_path
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            im1 = Image.open(src)
            w,h = im1.size
            if w > h:
                nh = 630
                nw = int((630/h)*w)
            else:
                nw = 600
                nh = int((600/w)*h)
            if nw < 600:
                nw = 600
            if nh < 630:
                nh = 630
            im1 = im1.resize((nw, nh),  Image.ANTIALIAS)
            im3 = Image.open('bot/white1.png')
            im3.paste(im1.convert('RGB'), (490,30))
            im1 = im3
            im1.paste(im0.convert('RGB'), (0,0), im0)
            font = ImageFont.truetype('bot/segoeprint_bold.ttf', size=34)
            draw = ImageDraw.Draw(im1)
            cur = datetime.fromtimestamp(time.time() + 3*3600)
            d = int(cur.day)
            if d < 10:
                d = '0'+str(d)
            else:
                d = str(d)
            md = int(cur.month)
            if md < 10:
                md = '0'+str(md)
            else:
                md = str(md)
            y = str(cur.year)
            old_date = d+'.'+md+'.'+y

            cur = datetime.fromtimestamp(time.time() + 3*3600 + 345600)
            d = int(cur.day)
            if d < 10:
                d = '0'+str(d)
            else:
                d = str(d)
            md = int(cur.month)
            if md < 10:
                md = '0'+str(md)
            else:
                md = str(md)
            y = str(cur.year)
            new_date = d+'.'+md+'.'+y

            text = 'Выдано:  @NekoslaviaBot'
            x, y = 63, 65
            fillcolor = "#FFFFFF"
            shadowcolor = "#242425"

            draw.text((x-2, y), text, font=font, fill=shadowcolor)
            draw.text((x+2, y), text, font=font, fill=shadowcolor)
            draw.text((x, y-2), text, font=font, fill=shadowcolor)
            draw.text((x, y+2), text, font=font, fill=shadowcolor)

            draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

            draw.text((x, y), text, font=font, fill=fillcolor)

            text = 'Кому:  ' + chel
            x, y = 63, 125

            draw.text((x-2, y), text, font=font, fill=shadowcolor)
            draw.text((x+2, y), text, font=font, fill=shadowcolor)
            draw.text((x, y-2), text, font=font, fill=shadowcolor)
            draw.text((x, y+2), text, font=font, fill=shadowcolor)

            draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

            draw.text((x, y), text, font=font, fill=fillcolor)

            text = 'Дата выдачи:  ' + old_date
            x, y = 63, 185

            draw.text((x-2, y), text, font=font, fill=shadowcolor)
            draw.text((x+2, y), text, font=font, fill=shadowcolor)
            draw.text((x, y-2), text, font=font, fill=shadowcolor)
            draw.text((x, y+2), text, font=font, fill=shadowcolor)

            draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

            draw.text((x, y), text, font=font, fill=fillcolor)

            text = 'Действует до:  ' + new_date
            x, y = 63, 245

            draw.text((x-2, y), text, font=font, fill=shadowcolor)
            draw.text((x+2, y), text, font=font, fill=shadowcolor)
            draw.text((x, y-2), text, font=font, fill=shadowcolor)
            draw.text((x, y+2), text, font=font, fill=shadowcolor)

            draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

            draw.text((x, y), text, font=font, fill=fillcolor)

            font = ImageFont.truetype('bot/comicbd.ttf', size=52)
            text = 'ЛИЦЕНЗИЯ НА\nНЕКОДЕВОЧКУ'
            x, y = 95, 500
            fillcolor = "#F6B1CB"

            draw.text((x-2, y), text, font=font, fill=shadowcolor)
            draw.text((x+2, y), text, font=font, fill=shadowcolor)
            draw.text((x, y-2), text, font=font, fill=shadowcolor)
            draw.text((x, y+2), text, font=font, fill=shadowcolor)

            draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
            draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

            draw.text((x, y), text, font=font, fill=fillcolor)

            im1.save('bot/result.png')
            f = open("bot/result.png","rb")
            m = bot.send_photo(message.chat.id, photo=f,caption = 'И самое главное, держи лицензию 🎫 на свою некодевочку. Нужно будет продлить её через 4 дня, если не хочешь платить штраф, конечно')
            fil = m.photo[len(m.photo) - 1].file_id
            os.remove(src)
            cursor.execute("UPDATE neko SET photo_licension = '" + fil + "' WHERE id = " + str(message.from_user.id))
            #conn.commit()
        else:
            bot.send_message(message.chat.id,'Ты уже некослав ебанат')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
@bot.message_handler(commands=["pet"])
def msg_pet(message):
        if message.reply_to_message is None:
            bot.send_message(message.chat.id, 'Ответом на сообщение даун')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
            return
        try:
            r = bot.get_user_profile_photos(message.reply_to_message.from_user.id)
            p = r.photos
            for photo_sizes in p:
                phot = max(photo_sizes, key=lambda x: x.width)
                fil = phot.file_id
                m = bot.send_photo(-1001694727085,photo=fil)
                file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'bot/files/' + file_info.file_path
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                #img = Image.open(src)
                #mean = ImageStat.Stat(img).mean
                #aboba = '{: .0f} {:.0f} {:.0f}'.format(*mean)
                #args = aboba.split()
                #mean = (int(args[0]),int(args[1]),int(args[2]))
                mean = dominant_color(src)
                make(src, 'result.gif',mean)
                f = open("result.gif","rb")
                bot.send_animation(message.chat.id,f)
                os.remove(src)
                f.close()
                break
        except Exception as e:
            bot.send_message(message.chat.id, e)
@bot.message_handler(commands=["sex"])
def msg_sex(message):
        bot.send_animation(message.chat.id,r'https://c.tenor.com/V8cU0yYnehAAAAAM/nosex-sex.gif')
@bot.message_handler(commands=["cmd"])
def msg_cmd(message):
        text = 'Список комманд:\n\n<code>Неко</code> - твоя некодевочка\n<code>Вещи</code> - всякий мусор, твой инвентарь\n<code>Покормить</code> - можно кормить раз в 4 часа\n<code>Выгулять</code> - можно выгуливать раз в 6 часов, от 2-х доверия\n<code>Погладить</code> - название говорит само за себя, от 10-ти доверия\n<code>Имя [текст]</code> - дать имя, от 1-го доверия\n<code>Топ</code> - лучшие некодевочки\n<code>Кладбище</code> - недавно умершие некодевочки\n<code>База</code> - ты здесь живёшь\n<code>Гараж</code> - тут будет стоять твоя машина\n<code>Завод</code> - отработать смену раз в день\n<code>Казино</code> - а здесь можно проебать заработанные деньги\n<code>Донат [N]</code> - перевести деньги ответом на сообщение\n<code>Арена</code> - арена некодевочек, от 20-ти доверия\n<code>Лицензия</code> - получить новую лицензию на некодевочку за 10 💰\n<code>Портал</code> - данж от 50-ти доверия, нужен некомобиль\n<code>Навыки</code> - уникальные боевые способности твоей некодевочки'
        bot.send_message(message.chat.id,text,parse_mode='HTML')
@bot.message_handler(commands=["paint"])
def msg_paint(message):
        try:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            webAppTest = types.WebAppInfo("https://mackaronina.github.io/bibasosina/")
            one_butt = types.KeyboardButton(text="Рисовать письки", web_app=webAppTest) #создаем кнопку типа webapp
            keyboard.add(one_butt)
            bot.send_message(message.chat.id, 'Нажми на кнопку чтобы рисовать письки', reply_markup=keyboard)
        except Exception as e:
            pass
@bot.message_handler(commands=["clear"])
def msg_clear(message):
        try:
            keyboard = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Убрал эту ебучую кнопку', reply_markup=keyboard)
        except Exception as e:
            pass
@bot.message_handler(commands=["test"])
def msg_spin(message):
        try:
            data = cursor.execute('SELECT * FROM neko')
            data = data.fetchall()
            i = 0
            while i < len(data):
                idk = data[i][0]
                skill1 = data[i][30]
                skill2 = data[i][31]
                if skill1 >= 8:
                    skill1 = skill1 - 7 + 100
                if skill2 >= 8:
                    skill2 = skill2 - 7 + 100
                cursor.execute('UPDATE neko SET skill_one = ' + str(skill1) + ',skill_two = ' + str(skill2) + ' WHERE id = ' + str(idk))
                i = i + 1
        except Exception as e:
            bot.send_message(-1001694727085,e)
@bot.message_handler(content_types="web_app_data")
def answer(webAppMes):
        try:
            bot.send_photo(-1001268892138,photo = webAppMes.web_app_data.data)
        except:
            bot.send_message(-1001268892138, 'error')
@bot.message_handler(commands=["fix"])
def msg_fix(message):
        global can
        global dcan
        can = True
        dcan = True
        bot.send_message(message.chat.id,'Допустим',parse_mode='HTML')
@bot.message_handler(commands=["help"])
def msg_help(message):
        text = '<b>Некославия</b> - великая держава, а великая держава должна заботиться о своих гражданах, не так ли? Для этого запуvvщена специальная социальная программа - каждому полагается по некодевочке, без очередей и налогов. К счастью, благодаря новейшим разработкам у нас их достаточно. По закону каждый некослав обязан заботиться о своей некодевочке, а её смерть уголовно наказуема. Основой же нашего государственного строя является социальный рейтинг граждан, который напрямую зависит от доверия питомцев к ним\n\nЕсли тебе этого мало, вот ссылка на канал:\n<a href="https://www.youtube.com/channel/UCGGQGNMYzZqNJSCmmLsqEBg">Nekoslavia</a>\nЗадонатить на развитие бота:\n<i>5375 4141 3075 3857</i>'
        text = 'Полезные ссылки:\n\n<a href="https://t.me/nekoslavia">Беседа с ботом</a>\n\n<a href="https://www.youtube.com/channel/UCGGQGNMYzZqNJSCmmLsqEBg">Наш канал на ютубе</a>\n\n<a href="https://send.monobank.ua/jar/8A79RjcXRM">Задонатить на развитие бота</a>'
        bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsNJi4zRDEZJXRw3LDwsaG18kszXm_wACPbsxG6IdGEsJeCDpoaaZxAEAAwIAA3MAAykE',caption = text,parse_mode='HTML')
@bot.message_handler(commands=["stat"])
def msg_stat(message):
        text = 'Всего некодевочек:  ' + str(len(photos) + len(elite_photos) + len(ero_photos) + len(arc_photos) + len(trap_photos)) + '\nОбычные:  ' + str(len(photos)) + '\nМагазин:  ' + str(len(elite_photos)) + '\nКазино:  ' + str(len(ero_photos)) + '\nНекоарки:  ' + str(len(arc_photos)) + '\nНекомальчики:  ' + str(len(trap_photos))
        bot.send_message(message.chat.id,text)
@bot.message_handler(func=lambda message: True,content_types=["text"])
def repeat_text(message):
        if str(message.from_user.id) in nekosas:
            args = nekosas[str(message.from_user.id)]
            args = args.split()
            dr_day = int(args[0])
            dr_month = int(args[1])
            cur = datetime.fromtimestamp(time.time() + 3*3600)
            if cur.day == dr_day and cur.month == dr_month:
                bot.send_message(message.chat.id, 'Именинника спросить забыли',reply_to_message_id=message.message_id)
                return
        if message.text == 'неко' or message.text == 'Неко' or message.text == '@NekoslaviaBot Неко' or message.text == '@NekoslaviaBot неко':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом ')
                return
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Покормить 🐟', switch_inline_query_current_chat = "Покормить")
            switch_button2 = types.InlineKeyboardButton(text='Выгулять 🚶‍♀️', switch_inline_query_current_chat = "Выгулять")
            switch_button3 = types.InlineKeyboardButton(text='Инвентарь 🎒', switch_inline_query_current_chat = "Вещи")
            markup.add(switch_button1,switch_button2)
            markup.add(switch_button3)
            nam = str(data[1]).rstrip()
            rep = data[2]
            phot = str(data[5]).rstrip()
            new_phot = str(data[38]).rstrip()
            if new_phot != 'None':
                phot = new_phot
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            coins = data[11]
            baza = data[8]
            buff = data[12]
            ch = data[13]
            kormit = int(time.time() - data[4])
            gulat = int(time.time() - data[3])
            car = data[9]
            chel = str(data[16]).rstrip()
            gender = data[33]
            if message.from_user.first_name != chel:
                chel = message.from_user.first_name
                cursor.execute("UPDATE neko SET chel = '"+ str(chel) +"' WHERE id = " + str(message.from_user.id))
                #conn.commit()
            if gulat < 6*3600:
                g = 'Пока не хочет гулять ❌\n'
            else:
                g = 'Хотела бы прогуляться ✅\n'
                if gender == 1:
                    g = 'Хотел бы прогуляться ✅\n'
            if kormit < 4*3600:
                k = '\nПока не хочет есть ❌\n'
            else:
                k = '\nНе отказалась бы от вискаса ✅\n'
                if gender == 1:
                    k = '\nНе отказался бы от вискаса ✅\n'
            if car == 0:
                c = 'Нет некомобиля 🚘\n'
            else:
                c = 'Есть некомобиль 🚘\n'
            if ch != message.chat.id:
                ch = message.chat.id
                cursor.execute('UPDATE neko SET chat = '+ str(ch) +' WHERE id = ' + str(message.from_user.id))
                #conn.commit()
            if nam == 'Некодевочка' or nam == 'Некомальчик':
                txt = 'У неё нет имени'
                if gender == 1:
                    txt = 'У него нет имени'
            else:
                txt = 'Её зовут ' + nam
                if gender == 1:
                    txt = 'Его зовут ' + nam
            text = 'Что ж, это твоя личная некодевочка, чем не повод для гордости?\n\n' + txt + k + g + 'Доверие 💞:  '+str(rep) + '\n\nА вот что касается тебя...\n'
            if gender == 1:
                text = 'Что ж, это твой личный некомальчик, чем не повод для гордости?\n\n' + txt + k + g + 'Доверие 💞:  '+str(rep) + '\n\nА вот что касается тебя...\n'
            text = text + c + 'Уровень некобазы 🏠:  ' + str(baza) + '\nНекогривен 💰:  ' + str(coins)
            if bolnitsa > 0:
                if bolnitsa < 3600:
                    b = 1
                else:
                    b = math.ceil(bolnitsa/3600)
                text = text + '\nТы в больнице 💊\nОсталось лечиться ' + str(b) + ' часов'
            bot.send_photo(message.chat.id,photo=phot,caption = text,reply_markup=markup)
        elif message.text == 'Вещи' or message.text == 'вещи' or message.text == '@NekoslaviaBot Вещи' or message.text == '@NekoslaviaBot вещи':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом ')
                return
            notifed = data[39]
            casino = data[40]
            pilk = data[41]
            days = data[42]
            coins = data[11]
            buff = data[12]
            monsters = data[20]
            heal = data[21]
            boxes = data[34]
            bones = data[43]
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Антипохмелин 🍼', switch_inline_query_current_chat = "Антипохмелин")
            markup.add(switch_button1)
            switch_button2 = types.InlineKeyboardButton(text='Вискас 🍫', switch_inline_query_current_chat = "Вискас")
            markup.add(switch_button2)
            text = 'Это твой инвентарь. Надеюсь, ты сможешь найти всему этому применение\n\nНекогривен 💰:  ' + str(coins) + '\nВискаса 🍫:  ' + str(buff) + '\nМонстров ⚡️:  ' + str(monsters) + '\nАнтипохмелина 🍼:  ' + str(heal) + '\nPilk 🥛: ' + str(pilk)
            if boxes > 0:
                text = text + '\nПосылок 📦:  ' + str(boxes)
            if bones > 0:
                text = text + '\nКостей санса 🦴:  ' + str(bones)
            text = text + '\n\n<code>Антипохмелин</code> - использовать предмет чтобы выйти из больницы\n\n<code>Вискас</code> - включить/выключить автоматическое использование вискаса'
            bot.send_photo(message.chat.id,photo='AgACAgIAAx0CZQN7rQACrNBi2OxzrdcKU1c1LOxqBdGsjRxKDAACn70xG-8HyUoUEuWNwlQYIgEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
        elif message.text == 'Навыки' or message.text == 'навыки' or message.text == '@NekoslaviaBot Навыки' or message.text == '@NekoslaviaBot навыки':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом ')
                return
            skill1 = data[30]
            skill2 = data[31]
            gender = data[33]
            if skill1 > 100:
                sktxt1 = active_skill_list[skill1-100]
            else:
                sktxt1 = passive_skill_list[skill1]
            if skill2 > 100:
                sktxt2 = active_skill_list[skill2-100]
            else:
                sktxt2 = passive_skill_list[skill2]
            text = 'Это навыки и черты характера, которыми обладает твоя некодевочка. Удивительно, но некодевочки обычно не такие слабые, какими кажутся на первый взгляд, а их когти острее бритвы\n\n' + sktxt1 + '\n' + sktxt2
            if gender == 1:
                text = 'Это навыки и черты характера, которыми обладает твой некомальчик. Удивительно, но некомальчики обычно не такие слабые, какими кажутся на первый взгляд, а их когти острее бритвы\n\n' + sktxt1 + '\n' + sktxt2
            bot.send_photo(message.chat.id,photo='AgACAgIAAx0CZQN7rQACzrBjRJTTrokWxq7HNUPeZWB8hwhOAwACy8AxGzDSKUp1KOI5xNQ4_gEAAwIAA3MAAyoE',caption = text, parse_mode='HTML')
        elif message.text == 'антипохмелин' or message.text == 'Антипохмелин' or message.text == '@NekoslaviaBot Антипохмелин' or message.text == '@NekoslaviaBot антипохмелин':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            heal = data[21]
            event = data[10]
            bolnitsa = int(data[6] - time.time())

            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if heal < 1:
                bot.send_message(message.chat.id, 'У тебя нет антипохмелина дегенерат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if message.reply_to_message is None:
                if bolnitsa <= 0:
                    bot.send_message(message.chat.id, 'Ты не в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                bolnitsa = 0
                heal = heal - 1
                cursor.execute('UPDATE neko SET bolnitsa = '+ str(bolnitsa) +',heal = ' + str(heal) + ' WHERE id = ' + str(message.from_user.id))
                bot.send_message(message.chat.id, 'Ты вылетел(а) из больницы на жопной тяге')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFhGti8zHsovf2QjnACCIhNm-mGDTNfgACJhUAAm8UmEppPj8WKn_J6ikE')
                return
            else:
                idk = message.reply_to_message.from_user.id
                if idk == message.from_user.id:
                    bot.send_message(message.chat.id, 'Чет я не понял')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'У этого лоха нет некодевочки')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                b2 = int(data[6] - time.time())
                chel = str(data[16]).rstrip()
                if b2 <= 0:
                    bot.send_message(message.chat.id,'Этот лох не в больнице')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                heal = heal - 1
                b2 = 0
                cursor.execute('UPDATE neko SET heal = ' + str(heal) + ' WHERE id = ' + str(message.from_user.id))
                cursor.execute('UPDATE neko SET bolnitsa = ' + str(b2) + ' WHERE id = ' + str(idk))
                bot.send_message(message.chat.id, '<a href="tg://user?id='+str(idk)+'">'+str(chel)+'</a> вылетел(а) из больницы на жопной тяге',parse_mode='HTML')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFhGti8zHsovf2QjnACCIhNm-mGDTNfgACJhUAAm8UmEppPj8WKn_J6ikE')
                return


        elif message.text == 'топ' or message.text == 'Топ' or message.text == '@NekoslaviaBot Топ' or message.text == '@NekoslaviaBot топ':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            phot = str(data[5]).rstrip()
            event = data[10]
            m = cursor.execute('SELECT MAX(wins) FROM neko')
            m = m.fetchone()
            m = m[0]
            text = 'Питомцы лучших граждан нашей родины, Некославии. Нет, числа это не цена за час, даже не думай об этом\n\n'
            data = cursor.execute('SELECT * FROM neko ORDER BY rep DESC')
            data = data.fetchall()
            i = 0
            if data is not None:
             for d in data:
                if i == 10:
                    break
                if str(d[1]).rstrip() == 'Некодевочка' or str(d[1]).rstrip() == 'Некомальчик':
                    n = 'Безымянная шмароёбина'
                else:
                    n = str(d[1]).rstrip()
                if d[15] == m and m != 0:
                    text = text + '🏆 <b>' + n + '</b>  ' + str(d[2]) + ' 💞\n'
                else:
                    text = text + str(i+1) + '.  ' + n + '  ' + str(d[2]) + ' 💞\n'
                i = i + 1
            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACn9piwJArenxX-o-B5a2xO7AhvSCTlAAC4LUxG5j7EUkOukwyvavLgQEAAwIAA3MAAykE',caption = text,parse_mode='HTML')
        elif message.text == 'топ деньги' or message.text == 'Топ деньги' or message.text == '@NekoslaviaBot Топ деньги' or message.text == '@NekoslaviaBot топ деньги':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            text = 'Это богатейшие граждане Некославии. Когда-нибудь ты станешь одним из них, если, конечно, не будешь проёбывать все деньги в казино\n\n'
            data = cursor.execute('SELECT * FROM neko ORDER BY coins DESC')
            data = data.fetchall()
            i = 0
            if data is not None:
             for d in data:
                if i == 10:
                    break
                n = str(d[16]).rstrip()
                text = text + str(i+1) + '.  ' + n + '  ' + str(d[11]) + ' 💰\n'
                i = i + 1
            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACw-di9rxFH9TpOzq-NFDEthztPu5QdAACprwxG81SuUuSxydRTDvpogEAAwIAA3MAAykE',caption = text,parse_mode='HTML')
        elif message.text == 'погладить' or message.text == 'Погладить' or message.text == '@NekoslaviaBot Погладить' or message.text == '@NekoslaviaBot погладить':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            ch = data[13]
            gladit = data[14]
            gender = data[33]
            gladit = gladit + 1
            phot = str(data[5]).rstrip()
            new_phot = str(data[38]).rstrip()
            if new_phot != 'None':
                phot = new_phot
            gifka = str(data[32]).rstrip()
            if ch != message.chat.id:
                ch = message.chat.id
                cursor.execute('UPDATE neko SET chat = '+ str(ch) +' WHERE id = ' + str(message.from_user.id))
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if rep < 10:
                text = nam + ' даёт понять, что откусит палец если ты попытаешься её погладить'
                if gender == 1:
                    text = nam + ' даёт понять, что откусит палец если ты попытаешься его погладить'
                bot.send_message(message.chat.id,text)
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLY5iwIflAaGLlpw7vXvQvEvJcWilzgACjxEAAqg6WEjqQFCw4uPiwikE')
                return
            text = 'Ты погладил некодевочку, и она довольно помурчала в ответ. Удивительно, но ' + nam + ' уже была поглажена ' + str(gladit) + ' раз'
            if gender == 1:
                text = 'Ты погладил некомальчика, и он довольно помурчал в ответ. Удивительно, но ' + nam + ' уже был поглажен ' + str(gladit) + ' раз'
            try:
              if gifka == 'Nothing':
                m = bot.send_photo(-1001694727085,photo=phot)
                file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'bot/files/' + file_info.file_path
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                im0 = Image.open(src)
                w,h = im0.size
                if w > h:
                    n = h
                else:
                    n = w
                area = (0, 0, n, n)
                im0 = im0.crop(area)
                im0.save(src)
                time.sleep(0.25)
                mean = dominant_color(src)
                make(src, 'bot/result.gif',mean)
                f = open("bot/result.gif","rb")
                m = bot.send_animation(message.chat.id,f,caption = text)
                gifka = m.animation.file_id
                os.remove(src)
                f.close()
              else:
                bot.send_animation(message.chat.id,gifka,caption = text)
              cursor.execute("UPDATE neko SET gladit = "+ str(gladit) +", gifka = '" + gifka + "'  WHERE id = " + str(message.from_user.id))
            except Exception as e:
                bot.send_message(message.chat.id,e)
        elif message.text == 'покормить' or message.text == 'Покормить' or message.text == '@NekoslaviaBot Покормить' or message.text == '@NekoslaviaBot покормить':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            kormit = int(time.time() - data[4])
            buff = data[12]
            ch = data[13]
            automate = data[25]
            gender = data[33]
            if ch != message.chat.id:
                ch = message.chat.id
                cursor.execute('UPDATE neko SET chat = '+ str(ch) +' WHERE id = ' + str(message.from_user.id))
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if kormit < 4*3600:
                text = nam + ' пока не хочет есть'
                bot.send_message(message.chat.id,text)
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW1iwHwF7vKClo5usceHHPCXG_sHxwACKxAAAnazWEhhnVRbfrQa8ikE')
            else:

                if buff > 0 and automate == 1:
                    rep = rep + 2
                    buff = buff - 1
                    if rep < 10:
                        text = 'Ты покормил некодевочку её любимым вискасом 🍫. Уверен, ей это понравилось гараздо больше обычной еды ❤️'
                        if gender == 1:
                            text = 'Ты покормил некомальчика его любимым вискасом 🍫. Уверен, ему это понравилось гараздо больше обычной еды ❤️'
                    else:
                        text = 'Ты покормил некодевочку её любимым вискасом 🍫. Ей это действительно понравилось, и в знак благодарности она предложила погладить себя ❤️'
                        if gender == 1:
                            text = 'Ты покормил некомальчика его любимым вискасом 🍫. Ему это действительно понравилось, и в знак благодарности он предложил погладить себя ❤️'
                else:
                    rep = rep + 1
                    if rep < 10:
                        text = 'Ты покормил некодевочку, продолжай в том же духе и она разрешит тебе себя погладить ❤️'
                        if gender == 1:
                            text = 'Ты покормил некомальчика, продолжай в том же духе и он разрешит тебе себя погладить ❤️'
                    else:
                        text = 'Ты покормил некодевочку, и в знак благодарности она предложила погладить себя. Не советую отказываться ❤️'
                        if gender == 1:
                            text = 'Ты покормил некомальчика, и в знак благодарности он предложил погладить себя. Не советую отказываться ❤️'
                kormit = int(time.time() + random.randint(-1800,1800))
                bot.send_message(message.chat.id,text)
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLXFiwHwWe1jhzAgMe071rTZ4ureX3AACJRAAAhQoWEiDQZVvpXK9GikE')
                cursor.execute('UPDATE neko SET notifed = 0, kormit = '+ str(kormit) +' WHERE id = ' + str(message.from_user.id))
                cursor.execute('UPDATE neko SET rep = '+ str(rep) +' WHERE id = ' + str(message.from_user.id))
                cursor.execute('UPDATE neko SET buff = '+ str(buff) +' WHERE id = ' + str(message.from_user.id))
        elif message.text == 'выгулять' or message.text == 'Выгулять' or message.text == '@NekoslaviaBot Выгулять' or message.text == '@NekoslaviaBot выгулять':
            data = cursor.execute('SELECT * FROM neko WHERE id ='+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            gulat = int(time.time() - data[3])
            coins = data[11]
            ch = data[13]
            baza = data[8]
            gender = data[33]
            if ch != message.chat.id:
                ch = message.chat.id
                cursor.execute('UPDATE neko SET chat = '+ str(ch) +' WHERE id = ' + str(message.from_user.id))
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if rep < 2:
                text = nam + ' тебе не доверяет, продолжай кормить её'
                bot.send_message(message.chat.id, text)
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLY5iwIflAaGLlpw7vXvQvEvJcWilzgACjxEAAqg6WEjqQFCw4uPiwikE')
                return
            if gulat < 6*3600:
                text = nam + ' пока не хочет гулять'
                bot.send_message(message.chat.id, text)
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW1iwHwF7vKClo5usceHHPCXG_sHxwACKxAAAnazWEhhnVRbfrQa8ikE')
            else:
                d = random.randint(1,6)
                gulat = int(time.time() + random.randint(-1800,1800))
                cursor.execute('UPDATE neko SET gulat = '+ str(gulat) +' WHERE id = ' + str(message.from_user.id))
                if d == 1:
                    if coins < 10:
                        text = 'Взор некодевочки упал на старую колоду карт. Было решено сыграть в дурака на раздевание, и ты остался в одних трусах. Удивительно, но некодевочке они понравились ❤️'
                        if gender == 1:
                            text = 'Взор некомальчика упал на старую колоду карт. Было решено сыграть в дурака на раздевание, и ты остался в одних трусах. Удивительно, но некомальчику они понравились ❤️'
                        bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACrPNi2TTbjCTpB2sEekm_cYy69euvVgACYr8xG35hyUq6nUwvpV7fGgEAAwIAA3MAAykE',caption = text)
                        rep = rep + 1
                        cursor.execute('UPDATE neko SET rep = '+ str(rep) +' WHERE id = ' + str(message.from_user.id))
                    else:
                        cost = random.randint(1,10)
                        k = random.randint(1,2)
                        if k == 1:
                            coins = coins - cost
                            text = 'Взор некодевочки упал на старую колоду карт. Было решено сыграть в дурака, и ты проебал ' + str(cost) + ' некогривен 💰. Если не обращать на это внимания, ' + nam + ' весело провела время'
                            if gender == 1:
                                text = 'Взор некомальчика упал на старую колоду карт. Было решено сыграть в дурака, и ты проебал ' + str(cost) + ' некогривен 💰. Если не обращать на это внимания, ' + nam + ' весело провёл время'
                            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACrPVi2TUAAV6ak7zuL9k5SIEEHAYXdUkAAmO_MRt-YclKhliUv3FMpYABAAMCAANzAAMpBA',caption = text)
                            cursor.execute('UPDATE neko SET coins = '+ str(coins) +' WHERE id = ' + str(message.from_user.id))
                        elif k == 2:
                            coins = coins + cost
                            text = 'Взор некодевочки упал на старую колоду карт. Было решено сыграть в дурака, и ты выиграл целых ' + str(cost) + ' некогривен 💰. Повезло, повезло. Если не обращать на это внимания, ' + nam + ' весело провела время'
                            if gender == 1:
                                text = 'Взор некомальчка упал на старую колоду карт. Было решено сыграть в дурака, и ты выиграл целых ' + str(cost) + ' некогривен 💰. Повезло, повезло. Если не обращать на это внимания, ' + nam + ' весело провёл время'
                            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACrPdi2TsB9fVbCZY53iP83RMkWyfu2wACUbsxG35h0UpbeK76av4qSgEAAwIAA3MAAykE',caption = text)
                            cursor.execute('UPDATE neko SET coins = '+ str(coins) +' WHERE id = ' + str(message.from_user.id))
                if d == 2:
                    k = random.randint(1,2)
                    if baza >= 4:
                        k = 2
                    if k == 1:
                        rep = rep - 1
                        cursor.execute('UPDATE neko SET rep = ' + str(rep) + ' WHERE id = ' + str(message.from_user.id))
                        text = 'Ты проснулся в луже блевоты с дичайшим похмельем. Последнее воспоминание - вы заходите в Сильпо и видите Капитана Моргана по скидке. Вчерашние события, к сожалению, остаются тайной. ' + nam + ' теперь тебе доверяет меньше как их следствие 💔'
                        bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACNE1imy-Ri_WnMfD3yi2ud0IAAToM38oAAuy7MRuYt9lIMfj5yYi-9gEBAAMCAANzAAMkBA',caption = text)
                    if k == 2:
                        rep = rep + 1
                        cursor.execute('UPDATE neko SET rep = ' + str(rep) + ' WHERE id = ' + str(message.from_user.id))
                        text = 'Ты проснулся в луже блевоты с дичайшим похмельем. Последнее воспоминание - вы заходите в Сильпо и видите Капитана Моргана по скидке. Вчерашние события, к сожалению, остаются тайной. ' + nam + ' теперь тебе доверяет больше как их следствие ❤️'
                        bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACNE1imy-Ri_WnMfD3yi2ud0IAAToM38oAAuy7MRuYt9lIMfj5yYi-9gEBAAMCAANzAAMkBA',caption = text)
                if d == 3:
                    k = random.randint(1,2)
                    if k == 1:
                        rep = rep + 2
                        cursor.execute('UPDATE neko SET rep = ' + str(rep) + ' WHERE id = ' + str(message.from_user.id))
                        cursor.execute('UPDATE neko SET event = 1 WHERE id = ' + str(message.from_user.id))
                        markup = types.InlineKeyboardMarkup()
                        switch_button1 = types.InlineKeyboardButton(text='Отдать 😔', switch_inline_query_current_chat = "Отдать")
                        switch_button2 = types.InlineKeyboardButton(text='Драться 😡', switch_inline_query_current_chat = "Драться")
                        markup.add(switch_button1,switch_button2)
                        text = '<b>"Эй, пацан, норм тяночка такая. Одолжишь на пару часиков?"</b> - послышалось сзади. Обернувшись, ты увидел медленно приближающихся гопников. Думать нужно быстро\n\n<code>Отдать</code> - отдать некодевочку без боя\n\n<code>Драться</code> - нанести превентивный удар'
                        ph = 'AgACAgIAAx0CZQN7rQACLENimg9vCvzViX185G4iP7oGl72XRQACIrwxG0Xf0Eg9-p59YMy7GwEAAwIAA3MAAyQE'
                        if gender == 1:
                            text = '<b>"Эй, пацан, норм кунчик такой. Одолжишь на пару часиков?"</b> - послышалось сзади. Обернувшись, ты увидел медленно приближающихся гопников. Думать нужно быстро\n\n<code>Отдать</code> - отдать некомальчика без боя\n\n<code>Драться</code> - нанести превентивный удар'
                            ph = 'AgACAgIAAx0CZQN7rQAC1MBjUuUNoGAz-fxdW7ZeYIfUMLbYQQACtNExG0AamErnC56G4DwJHwEAAwIAA3MAAyoE'
                        bot.send_photo(message.chat.id,photo = ph,caption = text,parse_mode='HTML',reply_markup=markup)
                    elif k == 2:
                        cursor.execute('UPDATE neko SET event = 7 WHERE id = ' + str(message.from_user.id))
                        markup = types.InlineKeyboardMarkup()
                        switch_button1 = types.InlineKeyboardButton(text='Откупиться 💸', switch_inline_query_current_chat = "Откупиться")
                        switch_button2 = types.InlineKeyboardButton(text='Показать 👀', switch_inline_query_current_chat = "Показать")
                        markup.add(switch_button1,switch_button2)
                        text = '<b>"Молодой человек, будьте любезны, покажите лицензию на некодевочку"</b> - обратились к тебе. Ничего необычного, просто до тебя решили доебаться менты. К счастью, лицензию 🎫 ты не забыл. Но стоит ли её показывать?\n\n<code>Откупиться</code> - предложить 20 некогривен 💰\n\n<code>Показать</code> - показать свою лицензию'
                        if gender == 1:
                            text = '<b>"Молодой человек, будьте любезны, покажите лицензию на некомальчика"</b> - обратились к тебе. Ничего необычного, просто до тебя решили доебаться менты. К счастью, лицензию 🎫 ты не забыл. Но стоит ли её показывать?\n\n<code>Откупиться</code> - предложить 20 некогривен 💰\n\n<code>Показать</code> - показать свою лицензию'
                        bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACy85jH3o2r1Pxxh53bkPNRvxmMXG6TgACvb0xGzWj-UgBumfJ3Ov7wQEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
                if d == 4:
                    markup = types.InlineKeyboardMarkup()
                    switch_button1 = types.InlineKeyboardButton(text='Открыть ❔', switch_inline_query_current_chat = "Открыть")
                    switch_button2 = types.InlineKeyboardButton(text='Уйти 🚶‍♂️', switch_inline_query_current_chat = "Уйти")
                    markup.add(switch_button1,switch_button2)
                    text = 'Прогуливаясь, вы заметили странную коробку посреди дороги. ' + nam + ' сразу же предложила открыть её. На самом деле, тебе и самому интересно что там внутри\n\n<code>Открыть</code> - открыть коробку\n\n<code>Уйти</code> - не открывать'
                    if gender == 1:
                        text = 'Прогуливаясь, вы заметили странную коробку посреди дороги. ' + nam + ' сразу же предложил открыть её. На самом деле, тебе и самому интересно что там внутри\n\n<code>Открыть</code> - открыть коробку\n\n<code>Уйти</code> - не открывать'
                    bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACoJpiwc-XmJW9JlazZ9GQkiyni6DQfgACVbsxGxyOEUozV-1wOZ04sAEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
                    cursor.execute('UPDATE neko SET event = 2 WHERE id = ' + str(message.from_user.id))
                if d == 5:
                    markup = types.InlineKeyboardMarkup()
                    switch_button1 = types.InlineKeyboardButton(text='Вискас 🍫', switch_inline_query_current_chat = "Вискас")
                    switch_button2 = types.InlineKeyboardButton(text='Монстр ⚡️', switch_inline_query_current_chat = "Монстр")
                    switch_button3 = types.InlineKeyboardButton(text='Коробка 📦', switch_inline_query_current_chat = "Коробка")
                    switch_button4 = types.InlineKeyboardButton(text='Уйти 🚶‍♂️', switch_inline_query_current_chat = "Уйти")
                    markup.add(switch_button1,switch_button2,switch_button3,switch_button4)
                    cursor.execute('UPDATE neko SET event = 3 WHERE id = ' + str(message.from_user.id))
                    text = '<b>"Whiskas, monster, nekogirls – you want it? Its yours, my friend, as long as you have enough nekogrivnas"</b> - услышали вы, заходя в ничем не примечательный ларёк. Ты с детства знаешь это место, ведь здесь продают бухло без паспорта, но на этот раз вы пришли не за этим\n\nСтоит взглянуть на особые товары:\n<code>Вискас</code> - 25 некогривен 💰\n<code>Монстр</code> - 30 некогривен 💰\n<code>Коробка</code> - 50 некогривен 💰\n\n<code>Уйти</code> - ничего не покупать'
                    bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACoh9ixOhAIbV7nzzHybTYBoJOkG2hGAACgb4xGzBhKEomCoej8lEPzgEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
                if d == 6:
                    markup = types.InlineKeyboardMarkup()
                    switch_button1 = types.InlineKeyboardButton(text='Адреналин 💪', switch_inline_query_current_chat = "Адреналин")
                    switch_button2 = types.InlineKeyboardButton(text='Gender changer 🏳️‍🌈', switch_inline_query_current_chat = "Gender changer")
                    switch_button4 = types.InlineKeyboardButton(text='Уйти 🚶‍♂️', switch_inline_query_current_chat = "Уйти")
                    markup.add(switch_button1,switch_button2)
                    markup.add(switch_button4)
                    cursor.execute('UPDATE neko SET event = 8 WHERE id = ' + str(message.from_user.id))
                    text = 'Зайдя в переулок, вы увидели бездомную некодевочку, роющуюся в мусорном баке. Завидев вас, она подпрыгнула и взволнованно заговорила: <b>"Ня, дайте покушать, а я вам блестяшки, ня"</b>. Похоже, она плохо знает человеческий язык\n\nНекодевочка держала странные вещи, найденные на свалке:\n<code>Адреналин</code> - 3 вискаса 🍫\n<code>Gender changer</code> - 20 вискаса 🍫\n\n<code>Уйти</code> - ничего не покупать'
                    bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQAC00ljS2wxdGuJbyZKRPFIhwptU9xbIwACa8AxG7RRWUp-23IUrAnepQEAAwIAA3MAAyoE',caption = text,parse_mode='HTML',reply_markup=markup)
        elif 'имя' in message.text or 'Имя' in message.text:
            args = message.text.split()
            if args[0] == 'Имя' or args[0] == 'имя':
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                    return
                nam = str(data[1]).rstrip()
                rep = data[2]
                event = data[10]
                bolnitsa = int(data[6] - time.time())
                gender = data[33]
                if bolnitsa > 0:
                    bot.send_message(message.chat.id, 'Ты в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if event > 0:
                    bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if len(args) >= 2 and len(message.text) < 54 and len(message.text) > 6:
                    if rep > 0:
                        nam = str(args[1])
                        i = 2
                        while i < len(args):
                            nam = nam + ' ' + str(args[i])
                            i = i + 1
                        nam = nam.capitalize()
                        if emoji.emoji_count(nam) > 0 or '[' in nam or ']' in nam or '<' in nam or '>' in nam:
                            bot.send_message(message.chat.id, 'Неправильное имя пашол нахуй')
                            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                            return
                        cursor.execute("UPDATE neko SET name = '"+ nam +"' WHERE id = "+str(message.from_user.id))
                        text = 'Ты дал имя некодевочке. Без сомнений, она быстро к нему привыкнет'
                        if gender == 1:
                            text = 'Ты дал имя некомальчику. Без сомнений, он быстро к нему привыкнет'
                        bot.send_message(message.chat.id, text)
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLaRiwIk4DRbw0Lap34MSyMpU-1-3KQACSQ8AAt46WUgVZwAB2AjTbT8pBA')
                    else:
                        text = nam + ' тебя не знает, может лучше сначала покормишь её?'
                        if gender == 1:
                            text = nam + ' тебя не знает, может лучше сначала покормишь его?'
                        bot.send_message(message.chat.id, text)
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLY5iwIflAaGLlpw7vXvQvEvJcWilzgACjxEAAqg6WEjqQFCw4uPiwikE')
                else:
                    bot.send_message(message.chat.id, 'Неправильное имя пашол нахуй')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        elif message.text == 'кладбище' or message.text == 'Кладбище' or message.text == '@NekoslaviaBot Кладбище' or message.text == '@NekoslaviaBot кладбище':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            text = 'Ты решил посетить кладбище некодевочек. Здесь покоятся все некодевочки, за которыми, к сожалению, мы не доглядели\n'
            data = cursor.execute('SELECT * FROM dead ORDER BY time DESC')
            data = data.fetchall()
            text = text + 'Последние умершие некодевочки и некомальчики:\n\n'
            i = 0
            if data is not None:
             for dat in data:
                if i == 10:
                    break
                cur = datetime.fromtimestamp(dat[1])
                d = int(cur.day)
                if d < 10:
                    d = '0'+str(d)
                else:
                    d = str(d)
                md = int(cur.month)
                if md < 10:
                    md = '0'+str(md)
                else:
                    md = str(md)
                y = str(cur.year)
                death_date = d+'.'+md+'.'+y

                text = text + str(i+1) + '.  ' + str(dat[0]).rstrip() + ' ☠️   ' + death_date + ' 🗓\n'
                i = i + 1
            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACn-JiwJJAUjK0Czuxv3RBKiKJJ61u_wACjrwxG0oRCEoxH0CUJepbQQEAAwIAA3MAAykE',caption = text)
        elif 'отдать' == message.text or 'Отдать' == message.text or message.text == '@NekoslaviaBot Отдать' or message.text == '@NekoslaviaBot отдать':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            baza = data[8]
            gender = data[33]
            photo = str(data[5]).rstrip()
            if event != 1:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            else:
                if gender == 0:
                    text = '<b>"Еба, все б такие умные были"</b> - сказали гопники, уводя твою некодевочку в неизвестном направлении ☠️. Грустно, конечно, но может оно и к лучшему?'
                    bot.send_message(message.chat.id, text,parse_mode='HTML')
                    bot.send_message(message.chat.id, 'Видимо, придётся выдать тебе новую некодевочку')
                    photka = random.choice(photos)
                    while photo == photka:
                        photka = random.choice(photos)
                    newnam = 'Некодевочка'
                else:
                    text = '<b>"Еба, все б такие умные были"</b> - сказали гопники, уводя твоего некомальчика в неизвестном направлении ☠️. Грустно, конечно, но может оно и к лучшему?'
                    bot.send_message(message.chat.id, text,parse_mode='HTML')
                    bot.send_message(message.chat.id, 'Видимо, придётся выдать тебе нового некомальчика')
                    photka = random.choice(trap_photos)
                    while photo == photka:
                        photka = random.choice(trap_photos)
                    newnam = 'Некомальчик'
                if nam == 'Некодевочка' or nam == 'Некомальчик':
                    cursor.execute("INSERT INTO dead (name,time) VALUES ('Безымянная могила',"+str(int(time.time())) +")")
                else:
                    cursor.execute("INSERT INTO dead (name,time) VALUES ('"+nam+"',"+str(int(time.time())) +")")
                kormit = time.time()
                gulat = time.time()
                cursor.execute("UPDATE neko SET new_phot = 'None', kormit = " + str(kormit) + ", gulat = " + str(gulat) + ", name = '" + newnam + "', gifka = 'Nothing', licension = 0, gladit = 0,photo = '" + photka + "',event = 0 WHERE id = "+str(message.from_user.id))
                if baza >= 2:
                    if gender == 0:
                        bot.send_message(message.chat.id, 'Новой некодевочке, cудя по всему, понравилась твоя база')
                    else:
                        bot.send_message(message.chat.id, 'Новому некомальчику, cудя по всему, понравилась твоя база')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFM5VixNUnaSAzda2fwcrxHsDUdA-caAACJw8AAmVYWEj9O0ji0K4xiikE')
                else:
                    cursor.execute("UPDATE neko SET rep = 0 WHERE id = "+ str(message.from_user.id))
        elif 'драться' == message.text or 'Драться' == message.text or message.text == '@NekoslaviaBot Драться' or message.text == '@NekoslaviaBot драться':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            gender = data[33]
            if event != 1:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            else:
                biba = random.randint(28800,43200)
                b = int(time.time() + biba)
                biba = math.ceil(biba/3600)
                text =  "Твоя некодевочка прибежала и, заливаясь слезами, рассказала мне что случилось. Хоть ты и напал первым, но численное преимущество оказалось на стороне гопников. Сожалею, но ближайшие " + str(biba) + " часов прийдётся провести в больнице 💊. Во всяком случае, "+ nam  + " стала доверять тебе гараздо больше ❤️"
                if gender == 1:
                    text =  "Твой некомальчик прибежал и, заливаясь слезами, рассказал мне что случилось. Хоть ты и напал первым, но численное преимущество оказалось на стороне гопников. Сожалею, но ближайшие " + str(biba) + " часов прийдётся провести в больнице 💊. Во всяком случае, "+ nam  + " стал доверять тебе гараздо больше ❤️"
                bot.send_message(message.chat.id, text)
                cursor.execute('UPDATE neko SET bolnitsa  = '+str(b)+',event = 0 WHERE id = ' + str(message.from_user.id))
        elif 'показать' == message.text or 'Показать' == message.text or message.text == '@NekoslaviaBot Показать' or message.text == '@NekoslaviaBot показать':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            event = data[10]
            licension = data[26]
            gender = data[33]
            if event != 7:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if time.time() > licension:
                biba = random.randint(28800,43200)
                b = int(time.time() + biba)
                biba = math.ceil(biba/3600)
                text = 'Мент пристально посмотрел сначала на лицензию, а потом на некодевочку. <b>"А лицензия-то недействительна. Будьте добры пройти с нами в отделение"</b> - было сказано как итог. Пару часов тебя избивали дубинками в отделении, требуя признания в краже некодевочки. В конце-концов, вас отпустили, и ' + nam + ' помогла доковылять тебе до ближайшей больницы, где ты проведёшь ' + str(biba) + ' часов 💊'
                if gender == 1:
                    text = 'Мент пристально посмотрел сначала на лицензию, а потом на некомальчика. <b>"А лицензия-то недействительна. Будьте добры пройти с нами в отделение"</b> - было сказано как итог. Пару часов тебя избивали дубинками в отделении, требуя признания в краже некодевочки. В конце-концов, вас отпустили, и ' + nam + ' помог доковылять тебе до ближайшей больницы, где ты проведёшь ' + str(biba) + ' часов 💊'
                bot.send_message(message.chat.id, text,parse_mode='HTML')
                cursor.execute('UPDATE neko SET bolnitsa  = '+str(b)+',event = 0 WHERE id = ' + str(message.from_user.id))
            else:
                text = 'Мент пристально посмотрел сначала на лицензию, а потом на некодевочку. <b>"Ладно, всё в полном порядке. Извините за беспокойство"</b> - было сказано с некоторым разочарованием. ' + nam + ' весь оставшийся день расспрашивала тебя что такое лицензия и зачем она нужна, а ты с радостью отвечал на ёё вопросы'
                if gender == 1:
                    text = 'Мент пристально посмотрел сначала на лицензию, а потом на некомальчика. <b>"Ладно, всё в полном порядке. Извините за беспокойство"</b> - было сказано с некоторым разочарованием. ' + nam + ' весь оставшийся день расспрашивал тебя что такое лицензия и зачем она нужна, а ты с радостью отвечал на его вопросы'
                bot.send_message(message.chat.id, text,parse_mode='HTML')
                cursor.execute('UPDATE neko SET event = 0 WHERE id = ' + str(message.from_user.id))
        elif 'откупиться' == message.text or 'Откупиться' == message.text or message.text == '@NekoslaviaBot Откупиться' or message.text == '@NekoslaviaBot откупиться':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            event = data[10]
            coins = data[11]
            gender = data[33]
            cost = 20
            if event != 7:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if coins < cost:
                bot.send_message(message.chat.id, 'А деньги где')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            coins = coins - cost
            text = '<b>"Хорошего вам дня, молодой человек"</b> - ответили тебе менты с насмешливыми улыбками на их лицах. Как можно было догадаться, этот день хорошим уже не будет'
            bot.send_message(message.chat.id, text,parse_mode='HTML')
            cursor.execute('UPDATE neko SET coins  = '+str(coins)+',event = 0 WHERE id = ' + str(message.from_user.id))
        elif 'завод' == message.text or 'Завод' == message.text or message.text == '@NekoslaviaBot Завод' or message.text == '@NekoslaviaBot завод':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            zavod = data[7]
            event = data[10]
            coins = data[11]
            bolnitsa = int(data[6] - time.time())
            version = data[29]
            boxes = data[34]
            reward = data[35]
            rep = data[2]
            gender = data[33]
            days = data[42]
            box = int(rep/100) - reward
            nam = str(data[1]).rstrip()
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            cur = datetime.now()
            d = int(cur.day)
            h = int(cur.hour) + 3
            if h > 17 or h < 7:
                bot.send_message(message.chat.id, 'Работать можно только с 7 до 6')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if h < 8:
                pic = 'AgACAgIAAx0CZQN7rQAC1cRjWHHPqKY27zwSInf6YS46TjgN3wAC3r4xG2_iyEpm4U7RaB2iRQEAAwIAA3MAAyoE'
            else:
                pic = 'AgACAgIAAx0CZQN7rQACn_1iwNZlro5zQzmVqnbvJMQSzhuaCQACLr0xG0oRCEphls-j33z4fQEAAwIAA3MAAykE'
            if zavod == d:
                bot.send_message(message.chat.id, 'Сегодня ты уже работал')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            days = days + 1
            cursor.execute("UPDATE neko SET zavod = "+ str(d) +" WHERE id = "+str(message.from_user.id))
            cursor.execute("UPDATE neko SET days = "+ str(days) +" WHERE id = "+str(message.from_user.id))
            if days <= 3:
                c = 15
                coins = coins + c
                cursor.execute("UPDATE neko SET coins = "+ str(coins) +" WHERE id = "+str(message.from_user.id))
                if days != 3:
                    bot.send_photo(message.chat.id, photo = pic,caption = 'Что ж, самое время идти на завод ебашить за копейки.\n\nЗа эту смену тебе удалось заработать ' + str(c) + ' некогривен 💰. Уверен, у тебя получится всё не пропить')
                else:
                    bot.send_photo(message.chat.id, photo = pic,caption = 'Что ж, самое время идти на завод ебашить за копейки.\n\nЗа эту смену тебе удалось заработать ' + str(c) + ' некогривен 💰. Уверен, у тебя получится всё не пропить\n\nК сожалению, станком тебе отхерачило последний палец, поэтому тебя переводят на новую должность. С завтрашнего дня ты будешь работать на одном из контрольно-пропускных пунктов завода. Можешь считать это повышением')
                if version != patch_version:
                    cursor.execute("UPDATE neko SET version = "+ str(patch_version) +" WHERE id = "+str(message.from_user.id))
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button1 = types.InlineKeyboardButton(text = 'Читать 👀',callback_data = 'read ' + str(message.from_user.id))
                    keyboard.add(callback_button1)
                    callback_button2 = types.InlineKeyboardButton(text = 'Не читать ❌',callback_data = 'dont ' + str(message.from_user.id))
                    keyboard.add(callback_button2)
                    bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACznBjQgABiPsE5FE7am8mfAOKiXsSOEsAAju9MRuS1hFKlyErHhjWQfcBAAMCAANzAAMqBA',caption = 'Возвращаясь с работы, ты заметил свежую газету, торчащую из твоего почтового ящика. Прочитать её?',reply_markup=keyboard)
               #elif box > 0:
               #  boxes = boxes + box
               # reward = reward + box
               #cursor.execute("UPDATE neko SET reward = "+ str(reward) +" WHERE id = "+str(message.from_user.id))
               #     cursor.execute("UPDATE neko SET boxes = "+ str(boxes) +" WHERE id = "+str(message.from_user.id))
               #    keyboard = types.InlineKeyboardMarkup()
               #   callback_button1 = types.InlineKeyboardButton(text = 'Читать 👀',callback_data = 'letter ' + str(message.from_user.id))
               #  keyboard.add(callback_button1)
               # callback_button2 = types.InlineKeyboardButton(text = 'Не читать ❌',callback_data = 'dont ' + str(message.from_user.id))
               # keyboard.add(callback_button2)
               # txt = 'Перебирая почту, ты заметил письмо, выделяющееся среди кучи бесполезных счетов и повесток. Прочитать его?'
               # bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQAC1PhjVwdShxawIYgm_OAkJPMXuOBWiQAClsgxG1hTuEqsn8YQrmq_egEAAwIAA3MAAyoE',caption = txt,reply_markup=keyboard)
               # txt = 'К тому же, у тебя под входной дверью лежала подозрительная коробка 📦. Ты предложил её просто выкинуть, но ' + nam + ', ожидаемо, не согласилась с таким решением\n\nПосылка 📦 добавлена в инвентарь\n\n<code>Донат посылка [N]</code> - передать посылку, ответом на сообщение\n\n<code>Открыть посылку</code> - открыть загадочную посылку\n'
               # if gender == 1:
               #     txt = 'К тому же, у тебя под входной дверью лежала подозрительная коробка 📦. Ты предложил её просто выкинуть, но ' + nam + ', ожидаемо, не согласился с таким решением\n\nПосылка 📦 добавлена в инвентарь\n\n<code>Донат посылка [N]</code> - передать посылку, ответом на сообщение\n\n<code>Открыть посылку</code> - открыть загадочную посылку\n'
               # bot.send_message(message.chat.id, txt,parse_mode='HTML')
            else:
                p1 = random.choice(papers_images)
                p2 = random.choice(papers_images)
                p3 = random.choice(papers_images)
                while p1 == p2 or p1 == p3 or p2 == p3:
                    p1 = random.choice(papers_images)
                    p2 = random.choice(papers_images)
                    p3 = random.choice(papers_images)
                images = [p1,p2,p3]
                images = pack(images)
                txt = 'Ты пришел на рабочее место и готов принять первых некочанов. В твои обязанности входит проверять их документы на подлинность и соответствие правилам, которые можно найти в справке'
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                callback_button1 = types.InlineKeyboardButton(text = 'Начать ▶️',callback_data = 'paper ' + str(message.from_user.id) + ' ' + str(True) + ' '  + str(True) + ' 1')
                keyboard.add(callback_button1)
                m = bot.send_photo(message.chat.id,photo=pic,caption = txt, reply_markup=keyboard)
                wait = int(time.time() + 3600)
                cursor.execute("INSERT INTO papers (id,images,wait,chat,message) VALUES ("+str(message.from_user.id)+",'"+str(images)+"',"+str(wait)+","+str(m.chat.id)+","+str(m.id)+")")


        elif 'отработать' == message.text or 'Отработать' == message.text or message.text == '@NekoslaviaBot Отработать' or message.text == '@NekoslaviaBot отработать8':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            event = data[10]
            coins = data[11]
            bolnitsa = int(data[6] - time.time())
            zavod = data[7]
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if coins >= 0:
                bot.send_message(message.chat.id, 'У тебя нет долгов')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            cur = datetime.now()
            d = int(cur.day)
            if zavod == d:
                bot.send_message(message.chat.id, 'Сегодня ты уже работал')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            cursor.execute("UPDATE neko SET coins = 0 WHERE id = "+str(message.from_user.id))
            cursor.execute("UPDATE neko SET zavod = "+ str(d) +" WHERE id = "+str(message.from_user.id))
            cap = 'Тебя взяли охранником в казино. Ничего интересного не произошло, разве что под конец смены ты помогал санитарам увезти странного мужика, кричащего что-то про другой порядок и запечатанную колоду. Как бы то ни было, долгов у тебя больше нет'
            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACyrNjGc35xHSmb1gR4r9IgIkFXObqRgAC5r0xG0V90EgpsZ5EAAGzE7UBAAMCAANzAAMpBA',caption = cap)

        elif message.text == 'выгнать дебилов' or message.text == 'Выгнать дебилов' or message.text == '@NekoslaviaBot Выгнать дебилов' or message.text == '@NekoslaviaBot выгнать дебилов':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            debil = data[23]
            if debil != 0:
                bot.send_message(message.chat.id, 'Дебилы уже ушли')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            cursor.execute('UPDATE neko SET debil = 1 WHERE id = ' + str(message.from_user.id))
            bot.send_message(message.chat.id, 'Дебилы ушли от тебя, но будут рады вернуться в любой момент')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFi19i9rLE0Zk7bicpKmus0JujKOHZGwACDxEAAoIqUUg7LMMbW4WU6SkE')
            return
        elif message.text == 'вернуть дебилов' or message.text == 'Вернуть дебилов' or message.text == '@NekoslaviaBot Вернуть дебилов' or message.text == '@NekoslaviaBot вернуть дебилов':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            debil = data[23]
            if debil != 1:
                bot.send_message(message.chat.id, 'Дебилы никуда не уходили')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            cursor.execute('UPDATE neko SET debil = 0 WHERE id = ' + str(message.from_user.id))
            bot.send_message(message.chat.id, 'Дебилы наконец-то вернулись к тебе')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFi19i9rLE0Zk7bicpKmus0JujKOHZGwACDxEAAoIqUUg7LMMbW4WU6SkE')
            return
        elif message.text == 'база' or message.text == 'База' or message.text == '@NekoslaviaBot База' or message.text == '@NekoslaviaBot база':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            baza = data[8]
            event = data[10]
            coins = data[11]
            bolnitsa = int(data[6] - time.time())
            debil = data[23]
            gender = data[33]
            gtxt = ' со своей некодевочкой '
            if gender == 1:
                gtxt = ' со своим некомальчиком '
            photo_debil = str(data[24]).rstrip()
            photo_base = str(data[18]).rstrip()
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Улучшить ⏫', switch_inline_query_current_chat = "Улучшить")
            markup.add(switch_button1)
            switch_button101 = types.InlineKeyboardButton(text='Выгнать дебилов 🙁', switch_inline_query_current_chat = "Выгнать дебилов")
            switch_button102 = types.InlineKeyboardButton(text='Вернуть дебилов 🙂', switch_inline_query_current_chat = "Вернуть дебилов")
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if baza == 0:
                text = 'Вау, да это же твоя база. В этом замечательном месте ты живёшь вместе' + gtxt + '\n\nНазвание:  Немного интерьера 🏠\nУлучшение:  +2 💞\nCтоимость:  10 некогривен 💰\n\n<code>Улучшить</code> - улучшить некобазу'
                bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACw35i9oRbhYo6RYn6QAnFSkmZVFkbwgAC27sxG81SuUtfLMdu2vIYnQEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
                return
            if baza == 1:
                text = 'Вау, да это же твоя база. В этом замечательном месте ты живёшь вместе' + gtxt + '\n\nНазвание:  Немного искусства 🏠\nУлучшение:  Восстанавливает 💞 при смене некодевочки\nCтоимость:  30 некогривен 💰\n\n<code>Улучшить</code> - улучшить некобазу'
                bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACw4Bi9oRf18y-g2J1C7J4XNJH1z5oPQAC3LsxG81SuUuJeWcaJ79QMQEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
                return
            if baza == 2:
                text = 'Вау, да это же твоя база. В этом замечательном месте ты живёшь вместе' + gtxt + '\n\nНазвание:  Телевизор со встроенным флексаиром 🏠\nУлучшение:  +4 💞\nCтоимость:  50 некогривен 💰\n\n<code>Улучшить</code> - улучшить некобазу'
                bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACw4Ji9oRk24AR2_u0GfMgyJULde2OdwAC3bsxG81SuUv25H8Ql-DLeQEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
                return
            if baza == 3:
                if debil == 0:
                    p = 'AgACAgIAAx0CZQN7rQACw4Ri9oRpE899uYr2kOPZZo7UShnJrAAC3rsxG81SuUupIFHivmnf4gEAAwIAA3MAAykE'
                    markup.add(switch_button101)
                else:
                    p = 'AgACAgIAAx0CZQN7rQACw7xi9q3o6HZ5SRsY0COlOZBKM4MeeAAC37sxG81SuUujfptgGa8ytAEAAwIAA3MAAykE'
                    markup.add(switch_button102)
                text = 'Вау, да это же твоя база. В этом замечательном месте ты живёшь вместе' + gtxt + '\n\nНазвание:  Стол с бухлом 🏠\nУлучшение:  Событие с Капитаном Морганом всегда даёт ♥️\nCтоимость:  70 некогривен 💰\n\n<code>Улучшить</code> - улучшить некобазу'
                bot.send_photo(message.chat.id,photo = p,caption = text,parse_mode='HTML',reply_markup=markup)
                return
            if baza == 4:
                if debil == 0:
                    p = 'AgACAgIAAx0CZQN7rQACw4hi9oR_awKmG_JB2hPf9UiwDqGabAAC4LsxG81SuUvAsNx2DcKWAgEAAwIAA3MAAykE'
                    markup.add(switch_button101)
                else:
                    p = 'AgACAgIAAx0CZQN7rQACw75i9q3viIx8HSPpBs9hC1w3VcZ1ewACfLwxG81SuUupdL90K43F7wEAAwIAA3MAAykE'
                    markup.add(switch_button102)
                text = 'Вау, да это же твоя база. В этом замечательном месте ты живёшь вместе' + gtxt + '\n\nНазвание:  Всратый туалет 🏠\nУлучшение:  +6 💞 \nCтоимость:  90 некогривен 💰\n\n<code>Улучшить</code> - улучшить некобазу'
                bot.send_photo(message.chat.id,photo = p,caption = text,parse_mode='HTML',reply_markup=markup)
                return
            if baza == 5:
                if debil == 0:
                    p = 'AgACAgIAAx0CZQN7rQACw4pi9oSLHbFGO7zGYnu85rvB4A1JRwAC4bsxG81SuUuML50JHeB4SwEAAwIAA3MAAykE'
                    markup.add(switch_button101)
                else:
                    p = 'AgACAgIAAx0CZQN7rQACw8Bi9q4Vk-OxDDm1FgTcCiHJnGysBwACfbwxG81SuUtb30KJ0lXEhwEAAwIAA3MAAykE'
                    markup.add(switch_button102)
                text = 'Вау, да это же твоя база. В этом замечательном месте ты живёшь вместе' + gtxt + '\n\nНазвание:  Не менее всратая кухня 🏠\nУлучшение:  +1 к получаемому 🍫\nCтоимость:  120 некогривен 💰\n\n<code>Улучшить</code> - улучшить некобазу'
                bot.send_photo(message.chat.id,photo = p,caption = text,parse_mode='HTML',reply_markup=markup)
                return
            if baza == 6:
                text = 'Вау, да это же твоя база. В этом замечательном месте ты живёшь вместе' + gtxt + '\n\nCтоимость:  20 некогривен 💰\n<code>Покрасить базу</code> - изменить цвет стен, обязательно приложить фото'
                mark = types.InlineKeyboardMarkup()
                switch_button2 = types.InlineKeyboardButton(text='Покрасить 🌈', switch_inline_query_current_chat = "Покрасить базу")
                mark.add(switch_button2)
                if debil == 0:
                    p = photo_base
                    mark.add(switch_button101)
                else:
                    p = photo_debil
                    mark.add(switch_button102)
                bot.send_photo(message.chat.id,photo = p,caption = text,parse_mode='HTML',reply_markup=mark)
                return
        elif message.text == 'улучшить' or message.text == 'Улучшить' or message.text == '@NekoslaviaBot Улучшить' or message.text == '@NekoslaviaBot улучшить':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            baza = data[8]
            event = data[10]
            rep = data[2]
            coins = data[11]
            bolnitsa = int(data[6] - time.time())
            gender = data[33]
            nam = str(data[1]).rstrip()
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if baza == 0:
                cost = 10
            if baza == 1:
                cost = 30
            if baza == 2:
                cost = 50
            if baza == 3:
                cost = 70
            if baza == 4:
                cost = 90
            if baza == 5:
                cost = 120
            if baza == 6:
                bot.send_message(message.chat.id, 'У тебя база максимального уровня ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if coins < cost:
                bot.send_message(message.chat.id, 'А деньги где')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            text = nam + ' не очень понимает что это и зачем оно нужно, но ей понравилось'
            if gender == 1:
                text = nam + ' не очень понимает что это и зачем оно нужно, но ему понравилось'
            bot.send_message(message.chat.id, text)
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLYxiwIeP83zV6whMtLqyTygKqGALagAChBAAAh_9WEh3vpYnO2kD1ikE')
            coins = coins - cost
            baza = baza + 1
            if baza == 1:
                rep = rep + 2
            if baza == 3:
                rep = rep + 4
            if baza == 5:
                rep = rep + 6
            cursor.execute("UPDATE neko SET coins = "+ str(coins) +" WHERE id = "+str(message.from_user.id))
            cursor.execute("UPDATE neko SET base = "+ str(baza) +" WHERE id = "+str(message.from_user.id))
            cursor.execute("UPDATE neko SET rep = "+ str(rep) +" WHERE id = "+str(message.from_user.id))
        elif 'уйти' == message.text or 'Уйти' == message.text or message.text == '@NekoslaviaBot Уйти' or message.text == '@NekoslaviaBot уйти':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())

            if event != 2 and event != 3 and event != 8:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event == 2:
                text = "Вы ушли, так и не узнав что находилось внутри загадочной коробки. Могу сказать что это было разумным решением"
                bot.send_message(message.chat.id, text)
                cursor.execute('UPDATE neko SET event = 0 WHERE id = ' + str(message.from_user.id))
            if event == 3:
                text = '<b>"Sorry, nekoslav, I cant give credit! Come back when youre a little...mmmm...richer"</b> - после этих слов окошко ларька закрылось. Мда уж, видимо, ты сильно разочаровал продавщицу'
                bot.send_message(message.chat.id,text,parse_mode='HTML')
                cursor.execute('UPDATE neko SET event = 0 WHERE id = ' + str(message.from_user.id))
            if event == 8:
                text = 'Вы вежливо отказались, и некодевочка с некоторой грустью молча вернулась к своему занятию. Видимо, ей не впервой слышать подобные слова'
                bot.send_message(message.chat.id,text,parse_mode='HTML')
                cursor.execute('UPDATE neko SET event = 0 WHERE id = ' + str(message.from_user.id))
        elif 'купить' == message.text or 'Купить' == message.text or message.text == '@NekoslaviaBot Купить' or message.text == '@NekoslaviaBot купить':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            coins = data[11]
            buff = data[12]
            photo = str(data[5]).rstrip()
            baza = data[8]
            monsters = data[20]
            skill1 = data[30]
            skill2 = data[31]
            gender = data[33]
            if event != 4 and event != 5 and event != 6 and event != 9 and event != 10:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event == 4:
                cost = 25
                if coins < cost:
                    bot.send_message(message.chat.id, 'А деньги где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                coins = coins - cost
                buff = buff + 4
                if baza >= 6:
                    buff = buff + 1
                text = 'Потраченных денег немного жаль, но ' + nam + ' выглядит счастливой, а это главное, не так ли?'
                if gender == 1:
                    text = 'Потраченных денег немного жаль, но ' + nam + ' выглядит счастливым, а это главное, не так ли?'
                bot.send_message(message.chat.id, text)
                cursor.execute('UPDATE neko SET event = 0 WHERE id = ' + str(message.from_user.id))
                cursor.execute('UPDATE neko SET buff = ' + str(buff) + ' WHERE id = ' + str(message.from_user.id))
                cursor.execute('UPDATE neko SET coins = ' + str(coins) + ' WHERE id = ' + str(message.from_user.id))
            if event == 5:
                cost = 30
                if coins < cost:
                    bot.send_message(message.chat.id, 'А деньги где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                coins = coins - cost
                text = 'Вам конечно хотелось выпить содержимое банок, но заправить некомобиль важнее. Надеюсь, ты не жалеешь о потраченных деньгах'
                monsters = monsters + 1
                bot.send_message(message.chat.id, text)
                cursor.execute('UPDATE neko SET event = 0 WHERE id = ' + str(message.from_user.id))
                cursor.execute('UPDATE neko SET monsters = ' + str(monsters) + ' WHERE id = ' + str(message.from_user.id))
                cursor.execute('UPDATE neko SET coins = ' + str(coins) + ' WHERE id = ' + str(message.from_user.id))
            if event == 6:
                cost = 50
                if coins < cost:
                    bot.send_message(message.chat.id, 'А деньги где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                coins = coins - cost
                if gender == 0:
                    photka = random.choice(elite_photos)
                    while True:
                        if photo != photka:
                            break
                        else:
                            photka = random.choice(elite_photos)
                else:
                    photka = random.choice(trap_photos)
                    while True:
                        if photo != photka:
                            break
                        else:
                            photka = random.choice(trap_photos)
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                callback_button1 = types.InlineKeyboardButton(text = 'Взять ✅',callback_data = 'get ' + str(message.from_user.id) + ' ' + str(gender) + ' 0')
                keyboard.add(callback_button1)
                callback_button2 = types.InlineKeyboardButton(text = 'Не брать ❌',callback_data = 'dont ' + str(message.from_user.id))
                keyboard.add(callback_button2)
                bot.send_photo(message.chat.id, photo=photka,reply_markup=keyboard)
                cursor.execute('UPDATE neko SET event = 0 WHERE id = ' + str(message.from_user.id))
                cursor.execute('UPDATE neko SET coins = ' + str(coins) + ' WHERE id = ' + str(message.from_user.id))
            if event == 9:
                cost = 3
                if buff < cost:
                    bot.send_message(message.chat.id, 'А вискас где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                buff = buff - cost
                text = '<b>"Ня, спасибо"</b> - поблагодарила некодевочка и поспешила скрыться, будто боясь, что ты передумаешь'
                bot.send_message(message.chat.id,text,parse_mode='HTML')

                a = random.choice([True,False])
                if a:
                    skill = random.randint(1,10)
                else:
                    skill = random.randint(101,110)

                while skill == skill1 or skill == skill2:
                    a = random.choice([True,False])
                    if a:
                        skill = random.randint(1,10)
                    else:
                        skill = random.randint(101,110)

                if skill1 > 100:
                    sktxt1 = active_skill_list[skill1-100]
                else:
                    sktxt1 = passive_skill_list[skill1]
                if skill2 > 100:
                    sktxt2 = active_skill_list[skill2-100]
                else:
                    sktxt2 = passive_skill_list[skill2]

                keyboard = types.InlineKeyboardMarkup(row_width=3)
                callback_button1 = types.InlineKeyboardButton(text = 'Заменить навык 1️⃣',callback_data = 'skill ' + str(message.from_user.id) + ' 1 ' + str(skill))
                callback_button2 = types.InlineKeyboardButton(text = 'Заменить навык 2️⃣',callback_data = 'skill ' + str(message.from_user.id) + ' 2 ' + str(skill))
                keyboard.add(callback_button1)
                keyboard.add(callback_button2)
                callback_button3 = types.InlineKeyboardButton(text = 'Не менять ❌',callback_data = 'dont ' + str(message.from_user.id))
                keyboard.add(callback_button3)
                text = nam + ', выпив содержимое банки, почуствовала в себе силу, способную свернуть горы. У неё появилось новое умение, выбери какой навык заменить на случайный:\n\n' + sktxt1 + '\n' + sktxt2
                if gender == 1:
                    text = nam + ', выпив содержимое банки, почуствовал в себе силу, способную свернуть горы. У него появилось новое умение, выбери какой навык заменить на случайный:\n\n' + sktxt1 + '\n' + sktxt2
                bot.send_message(message.chat.id,text,parse_mode='HTML',reply_markup=keyboard)

                cursor.execute('UPDATE neko SET event = 0, buff = ' + str(buff) + ' WHERE id = ' + str(message.from_user.id))
            if event == 10:
                cost = 20
                if buff < cost:
                    bot.send_message(message.chat.id, 'А вискас где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                buff = buff - cost
                text = '<b>"Ня, спасибо"</b> - поблагодарила некодевочка и поспешила скрыться, будто боясь, что ты передумаешь'
                bot.send_message(message.chat.id,text,parse_mode='HTML')
                text = nam + 'чувствует себя странно...'
                bot.send_message(message.chat.id,text,parse_mode='HTML')
                if gender == 0:
                    photka = random.choice(trap_photos)
                    while True:
                        if photo != photka:
                            break
                        else:
                            photka = random.choice(trap_photos)
                    gender = 1
                else:
                    photka = random.choice(photos)
                    while True:
                        if photo != photka:
                            break
                        else:
                            photka = random.choice(photos)
                    gender = 0
                cursor.execute("UPDATE neko SET new_phot = 'None', gender = " + str(gender) + ", gifka = 'Nothing', licension = 0, photo = '"+photka+"' WHERE id = "+ str(message.from_user.id))
                cursor.execute('UPDATE neko SET event = 0, buff = ' + str(buff) + ' WHERE id = ' + str(message.from_user.id))
        #elif 'Открыть посылку' == message.text or 'открыть посылку' == message.text or message.text == '@NekoslaviaBot Открыть посылку' or message.text == '@NekoslaviaBot открыть посылку':
        #    data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
        #    data = data.fetchone()
        #    if data is None:
        #        bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
        #        return
        #    nam = str(data[1]).rstrip()
        #    rep = data[2]
        #    event = data[10]
        #    bolnitsa = int(data[6] - time.time())
         #   boxes = data[34]
        #    gender = data[33]
        #    photo = str(data[5]).rstrip()
       #     item1 = data[36]
        #    item2 = data[37]
         #   if event > 0:
        #        bot.send_message(message.chat.id, 'Ты гуляешь дебил')
        #        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #        return
        #    if bolnitsa > 0:
        #        bot.send_message(message.chat.id, 'Ты в больнице дебил')
        #        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #        return
        #    if boxes < 1:
        #        bot.send_message(message.chat.id, 'Открывать нечего')
        #        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #        return
        #    a = random.randint(1,2)
        #    if a == 1:
         #       photka = random.choice(arc_photos)
        #        while True:
        #            if photo != photka:
        #                break
        #            else:
         #               photka = random.choice(arc_photos)
        #        keyboard = types.InlineKeyboardMarkup(row_width=3)
        #       callback_button1 = types.InlineKeyboardButton(text = 'Взять ✅',callback_data = 'get ' + str(message.from_user.id) + ' 0 ')
         #       keyboard.add(callback_button1)
        #        callback_button2 = types.InlineKeyboardButton(text = 'Не брать ❌',callback_data = 'dont ' + str(message.from_user.id))
        #        keyboard.add(callback_button2)
        #        bot.send_photo(message.chat.id, photo=photka,reply_markup=keyboard)
         #   else:
        #        item = random.randint(1,18)
        #        while item == item1 or item == item2:
        #            item = random.randint(1,18)
        #        keyboard = types.InlineKeyboardMarkup(row_width=3)
         #       callback_button1 = types.InlineKeyboardButton(text = 'Заменить предмет 1️⃣',callback_data = 'item ' + str(message.from_user.id) + ' 1 ' + str(item))
         #       callback_button2 = types.InlineKeyboardButton(text = 'Заменить предмет 2️⃣',callback_data = 'item ' + str(message.from_user.id) + ' 2 ' + str(item))
        #        keyboard.add(callback_button1)
        #        keyboard.add(callback_button2)
        #        callback_button3 = types.InlineKeyboardButton(text = 'Да ну нахуй ❌',callback_data = 'dont ' + str(message.from_user.id))
        #        keyboard.add(callback_button3)
        #        f = open("bot/items/" + str(item) + ".png","rb")
        #        bot.send_photo(message.chat.id,photo = f,reply_markup=keyboard)
        #    boxes = boxes - 1
        #    cursor.execute('UPDATE neko SET boxes = ' + str(boxes) + ' WHERE id = ' + str(message.from_user.id))



        elif 'открыть' == message.text or 'Открыть' == message.text or message.text == '@NekoslaviaBot Открыть' or message.text == '@NekoslaviaBot открыть':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            buff = data[12]
            baza = data[8]
            gender = data[33]
            if event != 2:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            d = random.randint(1,2)
            if d == 1:
                text = 'Внутри оказалась бездомная некодевочка. Как только ты открыл коробку, она моментально набросилась на твою, издавая шипящие звуки. К сожалению, ушло время чтобы их разнять. ' + nam + ' обиделась на тебя за это 💔'
                if gender == 1:
                    text = 'Внутри оказалась бездомная некодевочка. Как только ты открыл коробку, она моментально набросилась на твоего некомальчика, издавая шипящие звуки. К сожалению, ушло время чтобы их разнять. ' + nam + ' обиделся на тебя за это 💔'
                rep = rep - 2
                cursor.execute("UPDATE neko SET rep = " + str(rep) + " WHERE id = "+str(message.from_user.id))
                bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACohNixNKGV5unSWPowKZ7Go5lj9An_wACfr4xGzBhKEochCEOh_LDpwEAAwIAA3MAAykE',caption = text)
            if d == 2:
                text = 'Вам повезло, коробка оказалась полностью заполнена вискасом 🍫! Этого должно хватить на три раза, если не больше'
                buff = buff + 3
                if baza >= 6:
                    buff = buff + 1
                    text = 'Вам повезло, коробка оказалась полностью заполнена вискасом 🍫! Этого должно хватить на четыре раза, если не больше'
                cursor.execute("UPDATE neko SET buff = " + str(buff) + " WHERE id = "+str(message.from_user.id))
                bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACoKJiweU_aU7g1olT0b065v9A9dDVXwACqLsxGxyOEUodvpN4YkjBswEAAwIAA3MAAykE',caption = text)
            cursor.execute("UPDATE neko SET event = 0 WHERE id = "+str(message.from_user.id))
        elif 'вискас' == message.text or 'Вискас' == message.text or message.text == '@NekoslaviaBot вискас' or message.text == '@NekoslaviaBot Вискас':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            buff = data[12]
            baza = data[8]
            automate = data[25]
            gender = data[33]
            if event != 3:
                if automate == 1:
                    automate = 0
                    text = 'Ты больше не кормишь свою некодевочку вискасом 🍫, жестоко'
                    if gender == 1:
                        text = 'Ты больше не кормишь своего некомальчика вискасом 🍫, жестоко'
                    bot.send_message(message.chat.id, text)
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGHaljTQMPtoJuC9PyYV2e5g0lGX77-wACIA8AAg7tWEjVrCd9QwTr1ioE')
                else:
                    automate = 1
                    bot.send_message(message.chat.id, 'Ура, ' + nam + ' снова может есть свой любимый вискас 🍫')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGHbFjTQM_ocljKc2-O9GAUVL7Nb60TgACSQ8AAt46WUgVZwAB2AjTbT8qBA')
                cursor.execute("UPDATE neko SET automate = " + str(automate) + " WHERE id = "+str(message.from_user.id))
                return
            d = 1
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
            switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
            markup.add(switch_button1,switch_button2)
            if d == 1:
                cursor.execute('UPDATE neko SET event = 4 WHERE id = ' + str(message.from_user.id))
                text = 'Да это же целый мешок вискаса 🍫! ' + nam + ' облизывается смотря на него. Этого хватит раза на четыре точно\n\nСтоимость:  25 некогривен 💰\n\n<code>Купить</code> - потратить деньги\n\n<code>Назад</code> - присмотреться к другим товарам'
                if baza >= 6:
                    text = 'Да это же целый мешок вискаса 🍫! ' + nam + ' облизывается смотря на него. Этого хватит раз на пять точно\n\nСтоимость:  25 некогривен 💰\n\n<code>Купить</code> - потратить деньги\n\n<code>Назад</code> - присмотреться к другим товарам'
                bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACoiNixPAzHZnqNOrRhTGCLWbDzhdI8QAChr4xGzBhKErbwYUmB-YY7gEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
        elif 'монстр' == message.text or 'Монстр' == message.text or message.text == '@NekoslaviaBot Монстр' or message.text == '@NekoslaviaBot монстр':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            buff = data[12]
            gender = data[33]
            if event != 3:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            d = 2
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
            switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
            markup.add(switch_button1,switch_button2)
            if d == 2:
                cursor.execute('UPDATE neko SET event = 5 WHERE id = ' + str(message.from_user.id))
                text = 'Розовые монстры ⚡️ - единственное топливо, подходящее твоему некомобилю 🚘. Ничего не подумай, пить их тоже никто не запрещал\n\nСтоимость:  30 некогривен 💰\n\n<code>Купить</code> - потратить деньги\n\n<code>Назад</code> - присмотреться к другим товарам'
                bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACoiVixPeSb0E1O4DOFDnx_KZt2KHongACjr4xGzBhKEr2G-QRjbdbnQEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
        elif 'адреналин' == message.text or 'Адреналин' == message.text or 'АДРЕНАЛИН' == message.text or message.text == '@NekoslaviaBot Адреналин' or message.text == '@NekoslaviaBot адреналин':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            buff = data[12]
            gender = data[33]
            if event != 8:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
            switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
            markup.add(switch_button1,switch_button2)
            cursor.execute('UPDATE neko SET event = 9 WHERE id = ' + str(message.from_user.id))
            text = 'Не может быть, это совершенно новая банка АДРЕНАЛИНА! Выпив его, ' + nam + ' определённо сможет стать сильнее\n\nСтоимость:  3 вискаса 🍫\n\n<code>Купить</code> - потратить вискас\n\n<code>Назад</code> - присмотреться к другим вещам'
            bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQAC00djS1wDLAyjAAESNb1iCMbnFm82jQIAAhHAMRu0UVlKwksUd0cuhScBAAMCAANzAAMqBA',caption = text,parse_mode='HTML',reply_markup=markup)
        elif 'gender changer' == message.text or 'Gender changer' == message.text or 'Gender changer' == message.text or message.text == '@NekoslaviaBot Gender changer' or message.text == '@NekoslaviaBot gender changer':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            buff = data[12]

            if event != 8:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
            switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
            markup.add(switch_button1,switch_button2)
            cursor.execute('UPDATE neko SET event = 10 WHERE id = ' + str(message.from_user.id))
            text = 'Кто вообще это выкинул? Не вдаваясь в подробности работы устройства, cкажу лишь, что оно превращает некодевочек в некомальчиков и наоборот. Действительно, удивительная вещь\n\nСтоимость:  20 вискаса 🍫\n\n<code>Купить</code> - потратить вискас\n\n<code>Назад</code> - присмотреться к другим вещам'
            bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQAC00VjS1vzWZ5Yu_jq-nrUCUZwdZlMZAACEMAxG7RRWUqecoNnqMqp6QEAAwIAA3MAAyoE',caption = text,parse_mode='HTML',reply_markup=markup)
        elif 'коробка' == message.text or 'Коробка' == message.text or message.text == '@NekoslaviaBot Коробка' or message.text == '@NekoslaviaBot коробка':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            buff = data[12]
            gender = data[33]
            if event != 3:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            d = 3
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
            switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
            markup.add(switch_button1,switch_button2)
            if d == 3:
                cursor.execute('UPDATE neko SET event = 6 WHERE id = ' + str(message.from_user.id))
                if gender == 0:
                    text = 'Уникальный в своём роде товар, коробка с некодевочкой 🐱. В ней может оказаться кто угодно, но результат точно тебя не разочарует\n\nСтоимость:  50 некогривен 💰\n\n<code>Купить</code> - потратить деньги\n\n<code>Назад</code> - присмотреться к другим товарам'
                else:
                    text = 'Уникальный в своём роде товар, коробка с некомальчиком 🐱. В ней может оказаться кто угодно, но результат точно тебя не разочарует\n\nСтоимость:  50 некогривен 💰\n\n<code>Купить</code> - потратить деньги\n\n<code>Назад</code> - присмотреться к другим товарам'
                bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACoidixPqDuXC6Re6KtTl1Ma87jDMoPgACkL4xGzBhKEremTk6cCni0AEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
        elif 'назад' == message.text or 'Назад' == message.text or message.text == '@NekoslaviaBot Назад' or message.text == '@NekoslaviaBot назад':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            buff = data[12]

            if event != 4 and event != 5 and event != 6 and event != 9 and event != 10:
                bot.send_message(message.chat.id, 'Хуйню сморозил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event == 4 or event == 5 or event == 6:
                markup = types.InlineKeyboardMarkup()
                switch_button1 = types.InlineKeyboardButton(text='Вискас 🍫', switch_inline_query_current_chat = "Вискас")
                switch_button2 = types.InlineKeyboardButton(text='Монстр ⚡️', switch_inline_query_current_chat = "Монстр")
                switch_button3 = types.InlineKeyboardButton(text='Коробка 📦', switch_inline_query_current_chat = "Коробка")
                switch_button4 = types.InlineKeyboardButton(text='Уйти 🚶‍♂️', switch_inline_query_current_chat = "Уйти")
                markup.add(switch_button1,switch_button2,switch_button3,switch_button4)
                cursor.execute('UPDATE neko SET event = 3 WHERE id = ' + str(message.from_user.id))
                text = '<b>"Whiskas, monster, nekogirls – you want it? Its yours, my friend, as long as you have enough nekogrivnas"</b> - услышали вы, заходя в ничем не примечательный ларёк. Ты с детства знаешь это место, ведь здесь продают бухло без паспорта, но на этот раз вы пришли не за этим\n\nСтоит взглянуть на особые товары:\n<code>Вискас</code> - 25 некогривен 💰\n<code>Монстр</code> - 30 некогривен 💰\n<code>Коробка</code> - 50 некогривен 💰\n\n<code>Уйти</code> - ничего не покупать'
                bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACoh9ixOhAIbV7nzzHybTYBoJOkG2hGAACgb4xGzBhKEomCoej8lEPzgEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
            else:
                markup = types.InlineKeyboardMarkup()
                switch_button1 = types.InlineKeyboardButton(text='Адреналин 💪', switch_inline_query_current_chat = "Адреналин")
                switch_button2 = types.InlineKeyboardButton(text='Gender changer 🏳️‍🌈', switch_inline_query_current_chat = "Gender changer")
                switch_button4 = types.InlineKeyboardButton(text='Уйти 🚶‍♂️', switch_inline_query_current_chat = "Уйти")
                markup.add(switch_button1,switch_button2)
                markup.add(switch_button4)
                cursor.execute('UPDATE neko SET event = 8 WHERE id = ' + str(message.from_user.id))
                text = 'Зайдя в переулок, вы увидели бездомную некодевочку, роющуюся в мусорном баке. Завидев вас, она подпрыгнула и взволнованно заговорила: <b>"Ня, дайте покушать, а я вам блестяшки, ня"</b>. Похоже, она плохо знает человеческий язык\n\nНекодевочка держала странные вещи, найденные на свалке:\n<code>Адреналин</code> - 3 вискаса 🍫\n<code>Gender changer</code> - 20 вискаса 🍫\n\n<code>Уйти</code> - ничего не покупать'
                bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQAC00ljS2wxdGuJbyZKRPFIhwptU9xbIwACa8AxG7RRWUp-23IUrAnepQEAAwIAA3MAAyoE',caption = text,parse_mode='HTML',reply_markup=markup)
        elif message.text == 'гараж' or message.text == 'Гараж' or message.text == '@NekoslaviaBot Гараж' or message.text == '@NekoslaviaBot гараж':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            car = data[9]
            event = data[10]
            coins = data[11]
            bolnitsa = int(data[6] - time.time())
            photo_mobile = str(data[19]).rstrip()
            monsters = data[20]
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if car == 0:
                markup = types.InlineKeyboardMarkup()
                switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить машину")
                markup.add(switch_button1)
                text = 'Это твой гараж, но как-то здесь пустовато, ты так не думаешь?\n\nCтоимость:  100 некогривен 💰\n<code>Купить машину</code> - купить свой некомобиль'
                bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACoV5iw21fDMZ4Yb_e1BZ3uIL-IT1xVwACFrwxG-RaGEpQPC9bR_1lwQEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
            if car > 0:
                markup = types.InlineKeyboardMarkup()
                switch_button1 = types.InlineKeyboardButton(text='Отпиздить 😈', switch_inline_query_current_chat = "Отпиздить")
                switch_button3 = types.InlineKeyboardButton(text='Спасти 😇', switch_inline_query_current_chat = "Спасти")
                switch_button4 = types.InlineKeyboardButton(text='Портал 🏳️‍🌈', switch_inline_query_current_chat = "Портал")
                switch_button2 = types.InlineKeyboardButton(text='Покрасить 🌈', switch_inline_query_current_chat = "Покрасить машину")
                markup.add(switch_button1)
                markup.add(switch_button3)
                markup.add(switch_button4)
                markup.add(switch_button2)
                text = 'Это твой собственный некомобиль, разве он не прекрасен? Что ж, выбирай куда ехать\nМонстров ⚡️:  ' + str(monsters) + '\n\n<code>Отпиздить</code> - отправить своего врага в больницу, ответом на сообщение\n\n<code>Спасти</code> - покормить чужую некодевочку, если она не ела четыре дня, ответом на сообщение\n\n<code>Портал</code> - отправиться к загадочному порталу в LGBT мир\n\nCтоимость:  20 некогривен 💰\n<code>Покрасить машину</code> - изменить цвет некомобиля, обязательно приложить фото'
                bot.send_photo(message.chat.id,photo = photo_mobile,caption = text,parse_mode='HTML',reply_markup=markup)
        elif message.text == 'Купить машину' or message.text == 'купить машину' or message.text == '@NekoslaviaBot Купить машину' or message.text == '@NekoslaviaBot купить машину':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            car = data[9]
            event = data[10]
            coins = data[11]
            bolnitsa = int(data[6] - time.time())

            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if car > 0:
                bot.send_message(message.chat.id, 'У тебя уже есть некомобиль ебанько')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            cost = 100
            if coins < cost:
                bot.send_message(message.chat.id, 'А деньги где')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            bot.send_message(message.chat.id, 'Поздравляю с покупкой! Если машина сломается в течении года, мы вернём 1 некогривну на кэшбек счёт')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLYxiwIeP83zV6whMtLqyTygKqGALagAChBAAAh_9WEh3vpYnO2kD1ikE')
            coins = coins - cost
            car = car + 1
            cursor.execute("UPDATE neko SET coins = "+ str(coins) +" WHERE id = "+str(message.from_user.id))
            cursor.execute("UPDATE neko SET car = "+ str(car) +" WHERE id = "+str(message.from_user.id))

        elif message.text == 'спасти' or message.text == 'Спасти' or message.text == '@NekoslaviaBot Спасти' or message.text == '@NekoslaviaBot спасти':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            car = data[9]
            monsters = data[20]
            event = data[10]
            coins = data[11]
            bolnitsa = int(data[6] - time.time())
            nam  = str(data[1]).rstrip()

            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if car == 0:
                bot.send_message(message.chat.id, 'Лох у тебя нет некомобиля')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if monsters < 1:
                bot.send_message(message.chat.id, 'Сначала заправь некомобиль дегенерат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if message.reply_to_message is None:
                bot.send_message(message.chat.id, 'Я же сказал ответом на сообщение даун')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            idk = message.reply_to_message.from_user.id
            if idk == message.from_user.id:
                bot.send_message(message.chat.id, 'Ты сам себе ответил ебан')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'У этого лоха нет некодевочки')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            k2 = int(time.time() - data[4])
            chel = str(data[16]).rstrip()
            n2 = str(data[1]).rstrip()
            gender = data[33]
            if k2 < 4*24*3600:
                text = 'Его некодевочка пока не настолько голодна'
                if gender == 1:
                    text = 'Его некомальчик пока не настолько голоден'
                bot.send_message(message.chat.id,text)
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            text = n2 + ', конечно, испугалась тебя, но от еды не отказалась. Можешь не сомневаться, ты сделал действительно доброе дело. <a href="tg://user?id='+str(idk)+'">'+str(chel)+'</a>, тебе должно быть стыдно'
            if gender == 1:
                text = n2 + ', конечно, испугался тебя, но от еды не отказался. Можешь не сомневаться, ты сделал действительно доброе дело. <a href="tg://user?id='+str(idk)+'">'+str(chel)+'</a>, тебе должно быть стыдно'
            bot.send_message(message.chat.id,text,parse_mode='HTML')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFVF5i2QceOMOx4OUJLMf60d1yFdEnHgACChIAAoCLWUi4Fv-mtr7ecikE')
            monsters = monsters - 1
            k2 = time.time()
            cursor.execute('UPDATE neko SET monsters = '+ str(monsters) +' WHERE id = ' + str(message.from_user.id))
            cursor.execute('UPDATE neko SET notifed = 0, kormit = '+ str(k2) +' WHERE id = ' + str(idk))
        elif 'донат' in message.text or 'Донат' in message.text:
            args = message.text.split()
            if args[0] == 'донат' or args[0] == 'Донат':
              try:
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
                data = data.fetchone()
                if message.from_user.id == 1087968824:
                    bot.send_message(message.chat.id,'Пашол нахуй')
                    return
                if data is None:
                    bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                    return
                bolnitsa = int(data[6] - time.time())
                coins = data[11]
                buff = data[12]
                monsters = data[20]
                boxes = data[34]
                heal = data[21]
                if bolnitsa > 0:
                    bot.send_message(message.chat.id, 'Ты в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if message.reply_to_message is None:
                    bot.send_message(message.chat.id, 'Ответом на сообщение даун')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                idk = message.reply_to_message.from_user.id
                if idk == message.from_user.id:
                    bot.send_message(message.chat.id, 'Ты как себе собрался перевести дегенерат')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'У этого лоха нет некодевочки')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                b2 = int(data[6] - time.time())
                c2 = data[11]
                wh2 = data[12]
                m2 = data[20]
                boxes2 = data[34]
                heal2 = data[21]
                if b2 > 0:
                    bot.send_message(message.chat.id,'Этот лох в больнице')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if len(args) == 2:
                    cost = int(args[1])
                    if coins < cost:
                        bot.send_message(message.chat.id, 'А деньги где')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                        return
                    if cost <= 0:
                        bot.send_message(message.chat.id, 'А ловко ты это придумал')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                        return
                    c2 = c2 + cost
                    coins = coins - cost
                    cursor.execute('UPDATE neko SET coins = '+ str(coins) +' WHERE id = ' + str(message.from_user.id))
                    cursor.execute('UPDATE neko SET coins = '+ str(c2) +' WHERE id = ' + str(idk))
                    bot.send_message(message.chat.id,'Деньги отправлены, комиссия за услуги банка составила ' + str(cost) + ' некогривен 💰')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
                elif len(args) == 3:
                    if args[1] == 'монстры' or args[1] == 'Монстры' or args[1] == 'монстр' or args[1] == 'Монстр':
                        cost = int(args[2])
                        if monsters < cost:
                            bot.send_message(message.chat.id, 'А монстры где')
                            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                            return
                        if cost <= 0:
                            bot.send_message(message.chat.id, 'А ловко ты это придумал')
                            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                            return
                        m2 = m2 + cost
                        monsters = monsters - cost
                        cursor.execute('UPDATE neko SET monsters = '+ str(monsters) +' WHERE id = ' + str(message.from_user.id))
                        cursor.execute('UPDATE neko SET monsters = '+ str(m2) +' WHERE id = ' + str(idk))
                        bot.send_message(message.chat.id,'Монстры ⚡️ отправлены новой почтой')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
                    elif args[1] == 'вискасы' or args[1] == 'Вискасы' or args[1] == 'вискас' or args[1] == 'Вискас':
                        cost = int(args[2])
                        if buff < cost:
                            bot.send_message(message.chat.id, 'А вискас где')
                            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                            return
                        if cost <= 0:
                            bot.send_message(message.chat.id, 'А ловко ты это придумал')
                            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                            return
                        wh2 = wh2 + cost
                        buff = buff - cost
                        cursor.execute('UPDATE neko SET buff = '+ str(buff) +' WHERE id = ' + str(message.from_user.id))
                        cursor.execute('UPDATE neko SET buff = '+ str(wh2) +' WHERE id = ' + str(idk))
                        bot.send_message(message.chat.id,'В️искас 🍫 отправлен новой почтой')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
                    elif args[1] == 'посылка' or args[1] == 'Посылка' or args[1] == 'посылки' or args[1] == 'Посылки':
                        cost = int(args[2])
                        if boxes < cost:
                            bot.send_message(message.chat.id, 'Отправлять нечего')
                            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                            return
                        if cost <= 0:
                            bot.send_message(message.chat.id, 'А ловко ты это придумал')
                            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                            return
                        boxes2 = boxes2 + cost
                        boxes = boxes - cost
                        cursor.execute('UPDATE neko SET boxes = '+ str(boxes) +' WHERE id = ' + str(message.from_user.id))
                        cursor.execute('UPDATE neko SET boxes = '+ str(boxes2) +' WHERE id = ' + str(idk))
                        bot.send_message(message.chat.id,'Коробка 📦 с неведомой хуйней внутри отправлена новой почтой')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
                    elif args[1] == 'антипохмелин' or args[1] == 'Антипохмелин' or args[1] == 'антипохмел' or args[1] == 'Антипохмел':
                        cost = int(args[2])
                        if heal < cost:
                            bot.send_message(message.chat.id, 'Отправлять нечего')
                            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                            return
                        if cost <= 0:
                            bot.send_message(message.chat.id, 'А ловко ты это придумал')
                            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                            return
                        heal2 = heal2 + cost
                        heal = heal - cost
                        cursor.execute('UPDATE neko SET heal = '+ str(heal) +' WHERE id = ' + str(message.from_user.id))
                        cursor.execute('UPDATE neko SET heal = '+ str(heal2) +' WHERE id = ' + str(idk))
                        bot.send_message(message.chat.id,'Бутыль антипохмелина 🍼 отправлен новой почтой')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
                    else:
                        bot.send_message(message.chat.id,'Чет ты хуйню написал')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')

                else:
                    bot.send_message(message.chat.id,'Чет ты хуйню написал')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
              except:
                    bot.send_message(message.chat.id,'Чет ты хуйню написал')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        elif 'бой' in message.text or 'Бой' in message.text:
            args = message.text.split()
            wait = int(time.time() + 360)
            if args[0] == 'бой' or args[0] == 'Бой':
              if len(args) == 2:
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                    return
                bolnitsa = int(data[6] - time.time())
                coins = data[11]
                rep = data[2]
                arena = int(data[17] - time.time())
                chel1 = str(data[16]).rstrip()
                skill1 = data[30]
                skill2 = data[31]
                skills1 = [skill1,skill2]
                sk = pack(skills1)
                gender = data[33]
                if bolnitsa > 0:
                    bot.send_message(message.chat.id, 'Ты в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if rep < 20:
                    text = 'К сожалению, у тебя не получилось убедить некодевочку пойти с тобой на арену'
                    if gender == 1:
                        text = 'К сожалению, у тебя не получилось убедить некомальчика пойти с тобой на арену'
                    bot.send_message(message.chat.id, text)
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFP2VizLFlogiFH1n3Rpg9Hki7DC1y_wACjxEAAqg6WEjqQFCw4uPiwikE')
                    return
                if arena > 0:
                    text = 'Может быть стоит дать некодевочке отдохнуть?'
                    if gender == 1:
                        text = 'Может быть стоит дать некомальчику отдохнуть?'
                    bot.send_message(message.chat.id, text)
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFP2VizLFlogiFH1n3Rpg9Hki7DC1y_wACjxEAAqg6WEjqQFCw4uPiwikE')
                    return
                try:
                    c = args[1]
                    cost = int(c)
                except:
                    bot.send_message(message.chat.id,'Чет ты хуйню написал')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if coins < cost:
                    bot.send_message(message.chat.id, 'А деньги где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if cost < 10:
                    bot.send_message(message.chat.id, 'Ставка на арене от 10 некогривен')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                data = cursor.execute('SELECT * FROM battles WHERE one = '+str(message.from_user.id))
                data = data.fetchone()
                if data is not None:
                    event = data[2]
                    ch = data[5]
                    msg = data[6]
                    if event != 0:
                        bot.send_message(message.chat.id,'Куда столько, cпамер ебаный')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                        return
                    try:
                        bot.delete_message(chat_id=ch, message_id=msg)
                        cursor.execute('DELETE FROM battles WHERE one = '+str(message.from_user.id))
                    except:
                        pass
                if message.reply_to_message is None:
                    idk = 0
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    callback_button1 = types.InlineKeyboardButton(text = 'Принять ✅',callback_data = 'accept ' + str(message.from_user.id) + ' ' + str(idk) + ' ' + str(cost))
                    callback_button3 = types.InlineKeyboardButton(text = 'Отозвать 🚫',callback_data = 'aremove ' + str(message.from_user.id) + ' ' + str(idk))
                    keyboard.add(callback_button1)
                    keyboard.add(callback_button3)
                    text = '<a href="tg://user?id='+str(message.from_user.id)+'">'+str(chel1)+'</a> ищет противника для своей некодевочки! Приймешь вызов или зассал?\nСтавка: ' + str(cost) + ' 💰'
                    if gender == 1:
                        text = '<a href="tg://user?id='+str(message.from_user.id)+'">'+str(chel1)+'</a> ищет противника для своего некомальчика! Приймешь вызов или зассал?\nСтавка: ' + str(cost) + ' 💰'
                    m = bot.send_message(message.chat.id, text,reply_markup=keyboard,parse_mode='HTML')
                    cursor.execute("INSERT INTO battles (one,two,event,wait,cost,chat,message,skillone) VALUES ("+str(message.from_user.id)+","+str(idk)+",0,"+str(wait)+","+str(cost)+","+str(message.chat.id)+","+str(m.id)+",'"+sk+"')")
                else:
                    idk = message.reply_to_message.from_user.id
                    if idk == message.from_user.id:
                        bot.send_message(message.chat.id, 'Ты как с собой воевать собрался')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                        return
                    data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
                    data = data.fetchone()
                    if data is None:
                        bot.send_message(message.chat.id,'У этого лоха нет некодевочки')
                        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                        return
                    b2 = int(data[6] - time.time())
                    c2 = data[11]
                    r2 = data[2]
                    ar2 = int(data[17] - time.time())
                    chel2 = str(data[16]).rstrip()
                    gnd2 = data[33]

                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    callback_button1 = types.InlineKeyboardButton(text = 'Принять ✅',callback_data = 'accept ' + str(message.from_user.id) + ' ' + str(idk) + ' ' + str(cost))
                    callback_button2 = types.InlineKeyboardButton(text = 'Отклонить ❌',callback_data = 'decline ' + str(message.from_user.id) + ' ' + str(idk))
                    callback_button3 = types.InlineKeyboardButton(text = 'Отозвать 🚫',callback_data = 'aremove ' + str(message.from_user.id) + ' ' + str(idk))
                    keyboard.add(callback_button1,callback_button2)
                    keyboard.add(callback_button3)
                    text = '<a href="tg://user?id='+str(idk)+'">'+str(chel2)+'</a>, твоей некодевочке бросили вызов! Приймешь или зассал?\nСтавка: ' + str(cost) + ' 💰'
                    if gender == 1:
                        text = '<a href="tg://user?id='+str(idk)+'">'+str(chel2)+'</a>, твоему некомальчику бросили вызов! Приймешь или зассал?\nСтавка: ' + str(cost) + ' 💰'
                    m = bot.send_message(message.chat.id, text,reply_markup=keyboard,parse_mode='HTML')

                    cursor.execute("INSERT INTO battles (one,two,event,wait,cost,chat,message,skillone) VALUES ("+str(message.from_user.id)+","+str(idk)+",0,"+str(wait)+","+str(cost)+","+str(message.chat.id)+","+str(m.id)+",'"+str(sk)+"')")
        #elif 'трейд' in message.text or 'Трейд' in message.text:
        #    args = message.text.split()
        #    if args[0] == 'трейд' or args[0] == 'Трейд':
        #      if len(args) == 3:
        #       data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
        #        data = data.fetchone()
        #        if data is None:
        #            bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
        #            return
        #        bolnitsa = int(data[6] - time.time())
        #        coins = data[11]
        #        arena = int(data[17] - time.time())
        #        chel = str(data[16]).rstrip()
        #        chat = message.chat.id
        #        idk = message.from_user.id
        #        if bolnitsa > 0:
        #            bot.send_message(message.chat.id, 'Ты в больнице дебил')
         #           bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #            return
        #        try:
        #            cost = int(args[1])
        #            up = (args[2]).lower()
        #        except:
        #            bot.send_message(message.chat.id,'Чет ты хуйню написал')
        #            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #            return
        #        if coins < cost:
         #           bot.send_message(message.chat.id, 'А деньги где')
         #           bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #            return
        #        if cost < 10 or cost > 200:
        #            bot.send_message(message.chat.id, 'Инвестиции от 10 до 200 некогривен')
        #            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #            return
        #        if up == 'вверх':
        #            up = 1
        #        elif up == 'вниз':
        #            up = 0
        #        else:
        #            bot.send_message(message.chat.id, 'Третье слово либо вверх либо вниз еблан')
        #            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #            return
        #        data = cursor.execute('SELECT * FROM trade WHERE id = '+str(message.from_user.id))
        #        data = data.fetchone()
        #        if data is not None:
        #            bot.send_message(message.chat.id,'Ты уже торгуешь говном')
         #           bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #            return
        #        try:
         #           bitcoin_api_url = 'https://api.coingecko.com/api/v3/coins/bitcoin/'
         #           response = requests.get(bitcoin_api_url)
        #            response_json = response.json()
         #           start = int(response_json['market_data']['current_price']['uah'])
         #           text = 'Поздравляю, ты инвестировал ' + str(cost) + ' 💰 в говно\n📊 Начальный курс говна: ' + str(start) + ' грн\nФиксируем прибыль через пару минут 🤑'
        #            bot.send_message(message.chat.id, text,parse_mode='HTML')
        #            cursor.execute("INSERT INTO trade (id,start,chat,chel,cost,up) VALUES ("+str(idk)+","+str(start)+","+str(chat)+",'"+str(chel)+"',"+str(cost)+","+str(up)+")")
        #        except Exception as e:
        #            bot.send_message(message.chat.id,e,parse_mode='HTML')
        elif message.text == 'арена' or message.text == 'Арена' or message.text == '@NekoslaviaBot Арена' or message.text == '@NekoslaviaBot арена':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            rep = data[2]
            phot = str(data[5]).rstrip()
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            wins = data[15]
            gender = data[33]
            if rep < 20:
                text = nam + ' отказалась идти на арену, и я её прекрасно понимаю'
                if gender == 1:
                    text = nam + ' отказался идти на арену, и я его прекрасно понимаю'
                bot.send_message(message.chat.id,text)
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLY5iwIflAaGLlpw7vXvQvEvJcWilzgACjxEAAqg6WEjqQFCw4uPiwikE')
                return
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            text = 'Очевидно, бои некодевочек нелегальны, поэтому опустим лишние подробности. Обязательным условием проведения боя является ставка, часть которой организаторы забирают себе. На входе тебя уверили, что ещё ни одна некодевочка не умерла\nЛучшие некодевочки арены:\n\n'

            m = cursor.execute('SELECT MAX(wins) FROM neko')
            m = m.fetchone()
            m = m[0]

            data = cursor.execute('SELECT * FROM neko ORDER BY wins DESC')
            data = data.fetchall()
            i = 0
            if data is not None:
              for d in data:
                if i == 10:
                    break
                if str(d[1]).rstrip() == 'Некодевочка':
                    n = 'Безымянная шмароёбина'
                else:
                    n = str(d[1]).rstrip()

                if d[15] == m and m != 0:
                    text = text + '🏆 <b>' + n + '</b>  ' + str(d[15]) + ' ⚔️\n'
                else:
                    text = text + str(i+1) + '.  ' + n + '  ' + str(d[15]) + ' ⚔️\n'
                i = i + 1
            text = text + '\nТвоих побед:  ' + str(wins) + ' ⚔️'
            text = text + '\n\n<code>Бой [Ставка]</code> - бросить вызов, ответом на сообщение'
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Бой 🗡', switch_inline_query_current_chat = "Бой 10")
            markup.add(switch_button1)
            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACqQpizlI_XJiCwrzrSCYH47ZtXq9cCwACfLwxG0_FeEqC6_m0bVQSoQEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
        elif 'Лицензия' == message.text or 'лицензия' == message.text:
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом ')
                    return
                event = data[10]
                coins = data[11]
                licension = data[26]
                bolnitsa = int(data[6] - time.time())
                if bolnitsa > 0:
                    bot.send_message(message.chat.id, 'Ты в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                photo_licension = (data[27]).rstrip()
                markup = types.InlineKeyboardMarkup()
                switch_button1 = types.InlineKeyboardButton(text='Продлить 📆', switch_inline_query_current_chat = "Продлить")
                switch_button2 = types.InlineKeyboardButton(text='Дизайн 🌈', switch_inline_query_current_chat = "Дизайн")
                markup.add(switch_button1)
                markup.add(switch_button2)
                text = 'Здесь ты можешь посмотреть на свою лицензию 🎫 и остальные документы, когда они появятся у тебя\n\n10 💰\n<code>Продлить</code> - получить новую лицензию\n\n20 💰\n<code>Дизайн</code> - заказать уникальный дизайн лицензии, обязательно приложить фото'
                bot.send_photo(message.chat.id,photo = photo_licension,caption = text,parse_mode='HTML',reply_markup=markup)
        elif message.text == 'Продлить' or message.text == 'продлить' or message.text == '@NekoslaviaBot Продлить' or message.text == '@NekoslaviaBot продлить':
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом ')
                    return
                event = data[10]
                coins = data[11]
                licension = data[26]
                bolnitsa = int(data[6] - time.time())
                phot = str(data[5]).rstrip()
                new_phot = str(data[38]).rstrip()
                if new_phot != 'None':
                    phot = new_phot
                photo_design = (data[28]).rstrip()
                gender = data[33]
                chel = message.from_user.first_name
                cost = 10
                if coins < cost:
                    bot.send_message(message.chat.id, 'А деньги где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if event > 0:
                    bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if bolnitsa > 0:
                    bot.send_message(message.chat.id, 'Ты в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                coins = coins - cost
                if photo_design == 'Nothing':
                    im0 = Image.open('bot/01.png')
                else:
                    m = bot.send_photo(-1001694727085,photo=photo_design,caption = 'Идёт обработка...')
                    file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    src = 'bot/files/' + file_info.file_path
                    with open(src, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    im0 = Image.open(src)
                    w,h = im0.size
                    if w > h:
                        nh = 630
                        nw = int((630/h)*w)
                    else:
                        nw = 600
                        nh = int((600/w)*h)
                    if nw < 600:
                        nw = 600
                    if nh < 630:
                        nh = 630
                    im0 = im0.resize((nw, nh),  Image.ANTIALIAS)
                    im1 = Image.open('bot/white1.png')
                    im1.paste(im0.convert('RGB'), (40,34))
                    im0 = im1
                    im1 = Image.open('bot/02.png')
                    im0.paste(im1.convert('RGB'), (0,0), im1)
                    im0 = im0.convert('RGBA')
                    pixdata = im0.load()
                    for y in range(im0.size[1]):
                        for x in range(im0.size[0]):
                            if pixdata[x,y][0]==255 and pixdata[x,y][1]==0 and pixdata[x,y][2]==0:
                                pixdata[x, y] = (255, 255, 255,0)


                if len(chel) > 18:
                    chel = (chel[:18] + '..')
                m = bot.send_photo(message.chat.id,photo=phot,caption = 'Идёт обработка...')
                file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'bot/files/' + file_info.file_path
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                im1 = Image.open(src)
                w,h = im1.size
                if w > h:
                    nh = 630
                    nw = int((630/h)*w)
                else:
                    nw = 600
                    nh = int((600/w)*h)
                if nw < 600:
                    nw = 600
                if nh < 630:
                    nh = 630
                im1 = im1.resize((nw, nh),  Image.ANTIALIAS)
                im3 = Image.open('bot/white1.png')
                im3.paste(im1.convert('RGB'), (490,30))
                im1 = im3
                im1.paste(im0.convert('RGB'), (0,0), im0)
                font = ImageFont.truetype('bot/segoeprint_bold.ttf', size=34)
                draw = ImageDraw.Draw(im1)
                cur = datetime.fromtimestamp(time.time() + 3*3600)
                d = int(cur.day)
                if d < 10:
                    d = '0'+str(d)
                else:
                    d = str(d)
                md = int(cur.month)
                if md < 10:
                    md = '0'+str(md)
                else:
                    md = str(md)
                y = str(cur.year)
                old_date = d+'.'+md+'.'+y

                cur = datetime.fromtimestamp(time.time() + 3*3600 + 345600)
                d = int(cur.day)
                if d < 10:
                    d = '0'+str(d)
                else:
                    d = str(d)
                md = int(cur.month)
                if md < 10:
                    md = '0'+str(md)
                else:
                    md = str(md)
                y = str(cur.year)
                new_date = d+'.'+md+'.'+y



                if photo_design == 'Nothing':
                    draw.text((207, 117),str(chel),font=font,fill='#FFFFFF')
                    draw.text((352, 177),str(old_date),font=font,fill='#FFFFFF')
                    draw.text((370, 237),str(new_date),font=font,fill='#FFFFFF')
                else:
                    text = 'Выдано:  @NekoslaviaBot'
                    x, y = 63, 65
                    fillcolor = "#FFFFFF"
                    shadowcolor = "#242425"

                    draw.text((x-2, y), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y), text, font=font, fill=shadowcolor)
                    draw.text((x, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x, y), text, font=font, fill=fillcolor)

                    text = 'Кому:  ' + chel
                    x, y = 63, 125

                    draw.text((x-2, y), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y), text, font=font, fill=shadowcolor)
                    draw.text((x, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x, y), text, font=font, fill=fillcolor)

                    text = 'Дата выдачи:  ' + old_date
                    x, y = 63, 185

                    draw.text((x-2, y), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y), text, font=font, fill=shadowcolor)
                    draw.text((x, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x, y), text, font=font, fill=fillcolor)

                    text = 'Действует до:  ' + new_date
                    x, y = 63, 245

                    draw.text((x-2, y), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y), text, font=font, fill=shadowcolor)
                    draw.text((x, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x, y), text, font=font, fill=fillcolor)

                    font = ImageFont.truetype('bot/comicbd.ttf', size=52)
                    text = 'ЛИЦЕНЗИЯ НА\nНЕКОДЕВОЧКУ'
                    x, y = 95, 500
                    if gender == 1:
                        text = 'ЛИЦЕНЗИЯ НА\nНЕКОМАЛЬЧИКА'
                        x, y = 65, 500
                    fillcolor = "#F6B1CB"

                    draw.text((x-2, y), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y), text, font=font, fill=shadowcolor)
                    draw.text((x, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                    draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                    draw.text((x, y), text, font=font, fill=fillcolor)


                im1.save('bot/result.png')
                f = open("bot/result.png","rb")
                bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
                m = bot.send_photo(message.chat.id, photo=f,caption = 'Вот твоя новая лицензия 🎫, не теряй её и не забывай вовремя продлевать')
                fil = m.photo[len(m.photo) - 1].file_id
                cursor.execute("UPDATE neko SET coins = "+ str(coins) +" WHERE id = "+str(message.from_user.id))
                cursor.execute("UPDATE neko SET licension = "+ str(time.time() + 345600) +" WHERE id = "+str(message.from_user.id))
                cursor.execute("UPDATE neko SET photo_licension = '"+ fil +"' WHERE id = "+str(message.from_user.id))
                os.remove(src)
        elif message.text == 'войти' or message.text == 'Войти' or message.text == '@NekoslaviaBot Войти' or message.text == '@NekoslaviaBot войти':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            car = data[9]
            monsters = data[20]
            dungeon = int(data[22] - time.time())
            rep = data[2]
            gender = data[33]
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event < 0:
                bot.send_message(message.chat.id, 'Твоя некодевочка в данже или на арене')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if car == 0:
                bot.send_message(message.chat.id, 'Тебе нужен некомобиль еблана кусок')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if monsters <= 0:
                bot.send_message(message.chat.id, 'Тебе нужны монстры дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if dungeon > 0:
                bot.send_message(message.chat.id, 'Харош, дай отдохнуть своей некодевочке хотя бы день')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFP2VizLFlogiFH1n3Rpg9Hki7DC1y_wACjxEAAqg6WEjqQFCw4uPiwikE')
                return
            if rep < 50:
                text = nam + ' отказалась входить, не стоит её заставлять'
                if gender == 1:
                    text = nam + ' отказался входить, не стоит его заставлять'
                bot.send_message(message.chat.id,text)
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLY5iwIflAaGLlpw7vXvQvEvJcWilzgACjxEAAqg6WEjqQFCw4uPiwikE')
                return
            dungeon = int(time.time()+72000)
            event = -1
            monsters = monsters - 1
            cursor.execute("UPDATE neko SET dungeon = "+ str(dungeon) +" WHERE id = "+str(message.from_user.id))
            #cursor.execute("UPDATE neko SET event = "+ str(event) +" WHERE id = "+str(message.from_user.id))
            cursor.execute("UPDATE neko SET monsters = "+ str(monsters) +" WHERE id = "+str(message.from_user.id))

            mas = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
            generation = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
            generator = [2,2,2,3,3,3,4,4,5,5,6,7,8,8,8,8,8,8,8]
            stack = []
            mas[0][0] = 2
            generation[0][0] = 1
            cur_x = 0
            cur_y = 0
            while True:
              found = 0
              dirs = [1,2,3,4]
              if generation[cur_y][cur_x] == 0 and len(generator) > 0:
                d = random.choice(generator)
                generator.remove(d)
                generation[cur_y][cur_x] = d
              while len(dirs) != 0:
                d = random.choice(dirs)
                dirs.remove(d)
                if d == 1:
                    if (cur_y-3) >= 0:
                        if mas[cur_y-3][cur_x] == 0:
                            mas[cur_y-1][cur_x] = 1
                            mas[cur_y-2][cur_x] = 1
                            stack.append(str(cur_x) + ' ' + str(cur_y))
                            cur_y = cur_y - 3
                            mas[cur_y][cur_x] = 2
                            found = 1
                            break
                if d == 2:
                    if (cur_x+3) < len(mas[cur_y]):
                        if mas[cur_y][cur_x+3] == 0:
                            mas[cur_y][cur_x+1] = 1
                            mas[cur_y][cur_x+2] = 1
                            stack.append(str(cur_x) + ' ' + str(cur_y))
                            cur_x = cur_x + 3
                            mas[cur_y][cur_x] = 2
                            found = 1
                            break
                if d == 3:
                    if (cur_y+3) < len(mas):
                        if mas[cur_y+3][cur_x] == 0:
                            mas[cur_y+1][cur_x] = 1
                            mas[cur_y+2][cur_x] = 1
                            stack.append(str(cur_x) + ' ' + str(cur_y))
                            cur_y = cur_y + 3
                            mas[cur_y][cur_x] = 2
                            found = 1
                            break
                if d == 4:
                    if (cur_x-3) >= 0:
                        if mas[cur_y][cur_x-3] == 0:
                            mas[cur_y][cur_x-1] = 1
                            mas[cur_y][cur_x-2] = 1
                            stack.append(str(cur_x) + ' ' + str(cur_y))
                            cur_x = cur_x - 3
                            mas[cur_y][cur_x] = 2
                            found = 1
                            break
              if found == 1:
                continue
              else:
                if len(stack) == 0:
                    break
                st = stack[len(stack)-1]
                stack.remove(st)
                args = st.split()
                cur_x = int(args[0])
                cur_y = int(args[1])
            txt = ''
            mas[0][1] = 1
            mas[0][2] = 1
            mas[1][0] = 1
            mas[2][0] = 1
            mas[0][0] = 3
            for i in range(0, len(mas)):
              for j in range(0, len(mas[i])):
                if mas[i][j] == 0:
                    txt = txt + '◼️'
                if mas[i][j] == 1:
                    txt = txt + '▫️'
                if mas[i][j] == 2:
                    txt = txt + '🟥'
                if mas[i][j] == 3:
                    txt = txt + '🟢'
                if mas[i][j] == 4:
                    txt = txt + '🟩'
              txt = txt + '\n'
            maxhp = 5 + int((rep-50)/10)
            if maxhp > 8:
                maxhp = 8
            hp = maxhp
            keyboard = types.InlineKeyboardMarkup(row_width=4)
            callback_button1 = types.InlineKeyboardButton(text = '⬆️',callback_data = 'move ' + str(message.from_user.id) + ' 1')
            callback_button2 = types.InlineKeyboardButton(text = '⬅️',callback_data = 'move ' + str(message.from_user.id) + ' 4')
            callback_button3 = types.InlineKeyboardButton(text = '⏺',callback_data = 'nothing')
            callback_button4 = types.InlineKeyboardButton(text = '➡️',callback_data = 'move ' + str(message.from_user.id) + ' 2')
            callback_button5 = types.InlineKeyboardButton(text = '⬇️',callback_data = 'move ' + str(message.from_user.id) + ' 3')
            callback_button6 = types.InlineKeyboardButton(text = 'Уйти 🔚',callback_data = 'back ' + str(message.from_user.id))
            keyboard.add(callback_button1,callback_button5,callback_button2,callback_button4)
            keyboard.add(callback_button6)
            ms = [a for b in mas for a in b]
            gs = [a for b in generation for a in b]
            md = pack(ms)
            gn = pack(gs)
            text = nam + ' сразу же почуствовала прохладу и сырость, а её нога вступила во что-то мокрое. Да это же огромная пещера! Исходящее отовсюду разноцветное свечение прогоняет темноту даже с самых отдалённых уголков. Что ж, это место не выглядит опасным, но надолго ли?\n\n' + 'Добыча:  0💰 0🍫 0⚡️ 0🍼\n'+'Карта:\n'+txt
            if gender == 1:
                text = nam + ' сразу же почуствовал прохладу и сырость, а его нога вступила во что-то мокрое. Да это же огромная пещера! Исходящее отовсюду разноцветное свечение прогоняет темноту даже с самых отдалённых уголков. Что ж, это место не выглядит опасным, но надолго ли?\n\n' + 'Добыча:  0💰 0🍫 0⚡️ 0🍼\n'+'Карта:\n'+txt
            m = bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACwxZi8uNUoMtUGP6J96D7X-pveAGj3wAC374xGxy_mEsWdB1RBPi4nQEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=keyboard)
            wait = int(time.time() + 3600)
            cursor.execute("INSERT INTO dungeons (id,map,message,chat,wait,generation,co,wh,mo,he,selected,hp,maxhp) VALUES ("+str(message.from_user.id)+",'"+str(md)+"',"+str(m.id)+","+str(message.chat.id)+","+str(wait)+",'"+str(gn)+"',0,0,0,0,-1,"+str(hp)+","+str(maxhp)+")")
        elif message.text == 'портал' or message.text == 'Портал' or message.text == '@NekoslaviaBot Портал' or message.text == '@NekoslaviaBot портал':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            car = data[9]
            monsters = data[20]
            gender = data[33]
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return

            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return

            text = 'Это военный объект, но благодаря связям тебе удалось попасть сюда. Место, куда ведёт портал, принятно называть LGBT миром, и про него практически ничего неизвестно. Попасть туда могут только некодевочки с некомальчиками, обычные же люди даже не могут прикоснуться к порталу. К тому же, последняя исследовательская экспедиция считается пропавшей без вести\n\n<code>Войти</code> - отправить некодевочку в портал'
            if gender == 1:
                text = 'Это военный объект, но благодаря связям тебе удалось попасть сюда. Место, куда ведёт портал, принятно называть LGBT миром, и про него практически ничего неизвестно. Попасть туда могут только некодевочки с некомальчиками, обычные же люди даже не могут прикоснуться к порталу. К тому же, последняя исследовательская экспедиция считается пропавшей без вести\n\n<code>Войти</code> - отправить некомальчика в портал'
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Войти 🏳️‍🌈', switch_inline_query_current_chat = "Войти")
            markup.add(switch_button1)
            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsRxi5CVwxElzGR26h0_tTvU6R5cFmAACHb8xG38aIEs12xAgGvf_ugEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
        elif message.text == 'отпиздить' or message.text == 'Отпиздить' or message.text == '@NekoslaviaBot Отпиздить' or message.text == '@NekoslaviaBot отпиздить':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            car = data[9]
            event = data[10]
            coins = data[11]
            bolnitsa = int(data[6] - time.time())
            nam  = str(data[1]).rstrip()
            monsters = data[20]
            gender = data[33]

            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if car == 0:
                bot.send_message(message.chat.id, 'Лох у тебя нет некомобиля')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if monsters < 1:
                bot.send_message(message.chat.id, 'Сначала заправь некомобиль дегенерат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if message.reply_to_message is None:
                bot.send_message(message.chat.id, 'Я же сказал ответом на сообщение даун')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            idk = message.reply_to_message.from_user.id
            if idk == message.from_user.id:
                bot.send_message(message.chat.id, 'Вот сам себя и пизди, а мне больше не пиши')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'У этого лоха нет некодевочки')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            b = int(data[6] - time.time())
            chel = str(data[16]).rstrip()
            if b > 0:
                bot.send_message(message.chat.id,'Этот лох уже в больнице')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            biba = random.randint(21600,36000)
            b = int(time.time()+biba)
            biba = math.ceil(biba/3600)
            txt = 'Прохожие видели, как кого-то силой затолкали в розовую буханку без номеров и увезли в неизвестном направлении. Обходясь без подробностей, <a href="tg://user?id='+str(idk)+'">'+str(chel)+'</a> отправился в больницу на ' + str(biba) + ' часов 💊'
            bot.send_message(message.chat.id,txt,parse_mode='HTML')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGKY5jU0Mm9xVPCdaaFU7LHYBXnA4o3gACyiQAAp0NSEv_PF-UBc--kioE')
            monsters = monsters - 1
            cursor.execute('UPDATE neko SET monsters = '+ str(monsters) +' WHERE id = ' + str(message.from_user.id))
            cursor.execute('UPDATE neko SET bolnitsa = '+ str(b) +' WHERE id = ' + str(idk))
        elif message.text == 'казино' or message.text == 'Казино' or message.text == '@NekoslaviaBot Казино' or message.text == '@NekoslaviaBot казино':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            casino = data[40]
            pilk = data[41]
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event < 0:
                bot.send_message(message.chat.id, 'Твоя некодевочка в данже или на арене')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            text = 'Чтобы не платить деньги, казино Некославии часто предлагают в качестве выигрыша некодевочек и прочий мусор. Это, базирующееся в глубинах подвала твоего дома, не оказалось исключением\n\nСлоты 🎰\n10 💰\n<code>Пуск</code> - запустить слоты\n\nПокер 🃏\nОт 20 💰\n<code>Покер</code> - сыграть с такими же полупокерами'
            markup = types.InlineKeyboardMarkup()
            switch_button1 = types.InlineKeyboardButton(text='Пуск 🎰', switch_inline_query_current_chat = "Пуск")
            switch_button2 = types.InlineKeyboardButton(text='Покер ♠️', switch_inline_query_current_chat = "Покер")
            switch_button3 = types.InlineKeyboardButton(text = 'Комбинации ❓',callback_data = 'comb ' + str(message.from_user.id))
            markup.add(switch_button1)
            markup.add(switch_button2)
            markup.add(switch_button3)
            bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsadi5sd8T9_OueoaHagCng-OXhWKYQACmrsxG5NIMEuXRTxWMN6TQwEAAwIAA3MAAykE',caption = text,parse_mode='HTML',reply_markup=markup)
        #elif message.text == 'колесо' or message.text == 'Колесо' or message.text == '@NekoslaviaBot Колесо' or message.text == '@NekoslaviaBot колесо':
        #    data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
        #    data = data.fetchone()
        #    if data is None:
        #        bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
        #        return
        #    nam = str(data[1]).rstrip()
        #    event = data[10]
        #    bolnitsa = int(data[6] - time.time())
        #    coins = data[11]
        #    nam = str(data[1]).rstrip()
        #    casino = data[40]
        #    photo = str(data[5]).rstrip()
        #    if bolnitsa > 0:
        #        bot.send_message(message.chat.id, 'Ты в больнице дебил')
        #        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #        return
        #    if event > 0:
        #        bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
        #        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #        return
        #    if casino < 200:
        #        bot.send_message(message.chat.id, 'Хуй тебе, ты потратил недостаточно')
        #        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
        #        return
        #    keyboard = types.InlineKeyboardMarkup(row_width=2)
        #    callback_button1 = types.InlineKeyboardButton(text = 'Остановить ⛔️',callback_data = 'spinner ' + str(message.from_user.id))
        #    keyboard.add(callback_button1)
        #    bot.send_animation(message.chat.id,'CgACAgIAAx0CZQN7rQAC3FNjwFjfJDXiyZlObH8tlPA5dDBpfQACXiMAAiEsCEqlbaCDYfSigi0E',reply_markup=keyboard)
        #    cursor.execute('UPDATE neko SET casino = 0 WHERE id = ' + str(message.from_user.id))



        elif message.text == 'пуск' or message.text == 'Пуск' or message.text == '@NekoslaviaBot Пуск' or message.text == '@NekoslaviaBot пуск':
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
            data = data.fetchone()
            if data is None:
                bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                return
            nam = str(data[1]).rstrip()
            event = data[10]
            bolnitsa = int(data[6] - time.time())
            coins = data[11]
            nam = str(data[1]).rstrip()
            casino = data[40]
            photo = str(data[5]).rstrip()
            gender = data[33]
            if bolnitsa > 0:
                bot.send_message(message.chat.id, 'Ты в больнице дебил')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event < 0:
                bot.send_message(message.chat.id, 'Твоя некодевочка в данже или на арене')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            if event > 0:
                bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            cost = 10
            if coins < 0:
                bot.send_message(message.chat.id, 'А деньги где')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                return
            coins = coins - cost
            casino = casino + cost
            mas = ['🍉','🍓','🍒','🍋']
            first = random.choice(mas)
            second = random.choice(mas)
            third = random.choice(mas)
            text = 'Ты ничего не выиграл, лох\n\n<code>Пуск</code> - запустить слоты'
            nek = False
            # '\n\nВозможные комбинации:\n🍓🍓 - 20 некогривен 💰\n🍒🍒 - 20 некогривен 💰\n🍓🍓🍓 - 50 некогривен 💰\n🍒🍒🍒 - 70 некогривен 💰\n🍉🍉🍉 - 100 некогривен 💰\n🍋🍋🍋 - хорни некодевочка 🐱'
            # '\n\nВозможные комбинации:\n🍓🍓 - 10 некогривен 💰\n🍒🍒 - 10 некогривен 💰\n🍓🍓🍓 - 25 некогривен 💰\n🍒🍒🍒 - 35 некогривен 💰\n🍉🍉🍉 - 45 некогривен 💰\n🍋🍋🍋 - хорни некодевочка 🐱'
            if first == '🍒' and second == '🍒' and third == '🍒':
                text = 'Ты выиграл целых 70 некогривен 💰, мои поздравления!\n\n<code>Пуск</code> - запустить слоты'
                coins = coins + 80
            elif first == '🍓' and second == '🍓' and third == '🍓':
                text = 'Ты выиграл целых 40 некогривен 💰, мои поздравления!\n\n<code>Пуск</code> - запустить слоты'
                coins = coins + 50
            elif first == '🍉' and second == '🍉' and third == '🍉':
                text = 'Ты выиграл целых 100 некогривен 💰, мои поздравления!\n\n<code>Пуск</code> - запустить слоты'
                coins = coins + 110
            elif first == '🍋' and second == '🍋' and third == '🍋':

                nek = True
                if gender == 0:
                    text = 'Ты выиграл уникальную некодевочку 🐱! Конечно, тебе решать, брать её или нет\n\n<code>Пуск</code> - запустить слоты'
                    photka = random.choice(ero_photos)
                    while True:
                        if photo != photka:
                            break
                        else:
                            photka = random.choice(ero_photos)
                else:
                    text = 'Ты выиграл уникального некомальчика 🐱! Конечно, тебе решать, брать его или нет\n\n<code>Пуск</code> - запустить слоты'
                    photka = random.choice(trap_photos)
                    while True:
                        if photo != photka:
                            break
                        else:
                            photka = random.choice(trap_photos)
            elif first == second == '🍓' or first == third == '🍓' or second == third == '🍓':
                text = 'Ты выиграл 10 некогривен 💰, это мало, но лучше чем ничего\n\n<code>Пуск</code> - запустить слоты'
                coins = coins + 20
            elif first == second == '🍒' or first == third == '🍒' or second == third == '🍒':
                text = 'Ты выиграл 10 некогривен 💰, это мало, но лучше чем ничего\n\n<code>Пуск</code> - запустить слоты'
                coins = coins + 20
            elif first == second == '🍉' or first == third == '🍉' or second == third == '🍉':
                text = 'Ты вышел в ноль, попробуй ещё раз если не зассал\n\n<code>Пуск</code> - запустить слоты'
                coins = coins + 10
            cursor.execute('UPDATE neko SET casino = ' + str(casino) + ', coins = '+ str(coins) +' WHERE id = ' + str(message.from_user.id))
            markup = types.InlineKeyboardMarkup()
            switch_button2 = types.InlineKeyboardButton(text='Пуск 🎰', switch_inline_query_current_chat = "Пуск")
            markup.add(switch_button2)
            key = first + ' ' + second + ' ' + third
            f = casino_pics[key]
            bot.send_photo(message.chat.id, photo = f,caption = text,parse_mode='HTML',reply_markup=markup)
            if nek == True:
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                if gender == 0:
                    callback_button1 = types.InlineKeyboardButton(text = 'Взять некодевочку 🐱',callback_data = 'get ' + str(message.from_user.id) + ' 0 1')
                else:
                    callback_button1 = types.InlineKeyboardButton(text = 'Взять некомальчика 🐱',callback_data = 'get ' + str(message.from_user.id) + ' 1 1')
                keyboard.add(callback_button1)
                callback_button2 = types.InlineKeyboardButton(text = 'Взять 50 некогривен 💰',callback_data = 'money ' + str(message.from_user.id))
                keyboard.add(callback_button2)
                bot.send_photo(message.chat.id, photo=photka,reply_markup=keyboard)
        elif message.text == 'покер' or message.text == 'Покер' or message.text == '@NekoslaviaBot Покер' or message.text == '@NekoslaviaBot покер':
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                    return
                bolnitsa = int(data[6] - time.time())
                coins = data[11]
                event = data[10]
                if bolnitsa > 0:
                    bot.send_message(message.chat.id, 'Ты в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if coins < 20:
                    bot.send_message(message.chat.id, 'А деньги где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if event > 0:
                    bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if check_poker(message.from_user.id):
                    bot.send_message(message.chat.id,'Куда столько, cпамер ебаный')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                callback_button1 = types.InlineKeyboardButton(text = 'Присоединиться ➕',callback_data = 'pjoin ' + str(message.from_user.id))
                callback_button2 = types.InlineKeyboardButton(text = 'Старт ✅',callback_data = 'pstart ' + str(message.from_user.id))
                callback_button3 = types.InlineKeyboardButton(text = 'Отмена ❌',callback_data = 'pend ' + str(message.from_user.id))
                keyboard.add(callback_button1)
                keyboard.add(callback_button2,callback_button3)
                m = bot.send_message(message.chat.id, text = 'Идёт набор в покер, кто не отзовётся тот лох\nВход от 20 некогривен 💰\n1 из 2 игроков',reply_markup=keyboard)
                players = [message.from_user.id]
                names = [message.from_user.first_name]
                bank = [5]
                money = [coins]
                dead = []
                vabank = []
                pd = pack(players)
                nd = pack(names)
                bd = pack(bank)
                md = pack(money)
                dd = pack(dead)
                vb = pack(vabank)
                wait = int(time.time() + 600)
                cursor.execute("INSERT INTO poker (id,event,wait,chat,message,players,names,bank,money,dead,vabank) VALUES ("+str(message.from_user.id)+",-1,"+str(wait)+","+str(message.chat.id)+","+str(m.id)+",'"+str(pd)+"','"+str(nd)+"','"+str(bd)+"','"+str(md)+"','"+str(dd)+"','"+str(vb)+"')")
        elif 'фото' in message.text or 'Фото' in message.text:
            args = message.text.split()
            try:
                a = int(args[1])
                i = int(args[2])
                if a == 0:
                    bot.send_photo(message.chat.id, photo = photos[i])
                elif a == 1:
                    bot.send_photo(message.chat.id, photo = elite_photos[i])
                elif a == 2:
                    bot.send_photo(message.chat.id, photo = ero_photos[i])
                elif a == 3:
                    bot.send_photo(message.chat.id, photo = trap_photos[i])
            except:
                pass
        elif '!set' in message.text:
            args = message.text.split(' ')
            if message.reply_to_message is None:
                bot.send_message(message.chat.id, 'Ответом на сообщение')
                return
            if message.from_user.id != 738931917:
                bot.send_message(message.chat.id, 'Лол нет')
                return
            try:
                column = args[1]
                value = args[2]
                cursor.execute("UPDATE neko SET " + column + " = " + value + " WHERE id = " + str(message.reply_to_message.from_user.id))
                bot.send_message(message.chat.id, 'Допустим')
            except Exception as e:
                bot.send_message(message.chat.id, e)
        elif 'Давид' in message.text or 'давид' in message.text  or 'ДАВИД' in message.text:
            bot.send_message(message.chat.id, 'Давид шедевр',reply_to_message_id=message.message_id)
        elif message.reply_to_message is not None and message.reply_to_message.from_user.id == 5388861642 and message.reply_to_message.text is not None and 'Кто-то высрал:' not in message.reply_to_message.text:
            bot.send_message(message.chat.id, 'Хохла спросить забыли',reply_to_message_id=message.message_id)
        elif message.chat.id == message.from_user.id:
            bot.send_message(-1001268892138, 'Кто-то высрал: '+ message.text)
@bot.message_handler(func=lambda message: True,content_types=["photo"])
def msg_photo_bot(message):
        if message.chat.id ==  -1001694727085:
            bot.send_message(message.chat.id,str(message.photo[0].file_id) + ' ' + str(message.photo[0].file_size),reply_to_message_id=message.message_id)
        if message.caption is not None:
            if 'Покрасить базу' in message.caption or 'покрасить базу' in message.caption:
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                    return
                event = data[10]
                bolnitsa = int(data[6] - time.time())
                coins = data[11]
                base = data[8]
                if bolnitsa > 0:
                    bot.send_message(message.chat.id, 'Ты в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if event > 0:
                    bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if coins < 20:
                    bot.send_message(message.chat.id, 'А деньги где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if base != 6:
                    bot.send_message(message.chat.id, 'Нужна база максимального уровня')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                bot.send_message(message.chat.id,'Ты успешно нанял таджиков, которые покрасили тебе стены. Полюбуйся результатом')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'bot/files/' + file_info.file_path
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                im1 = Image.open(src)
                im1 = im1.resize((1000, 667),  Image.ANTIALIAS)
                im2 = Image.open('bot/rm228.png')
                im1.paste(im2.convert('RGB'), (0,0), im2)
                im1.save('bot/result.png')
                im1 = Image.open(src)
                im1 = im1.resize((1000, 667),  Image.ANTIALIAS)
                im2 = Image.open('bot/rm229.png')
                im1.paste(im2.convert('RGB'), (0,0), im2)
                im1.save('bot/result2.png')
                f = open("bot/result.png","rb")
                m = bot.send_photo(message.chat.id, photo=f)
                n = m.photo[len(m.photo) - 1].file_id
                cursor.execute("UPDATE neko SET photo_base = '"+ str(n) +"' WHERE id = "+str(message.from_user.id))
                f = open("bot/result2.png","rb")
                m = bot.send_photo(message.chat.id, photo=f)
                n = m.photo[len(m.photo) - 1].file_id
                cursor.execute("UPDATE neko SET photo_debil = '"+ str(n) +"' WHERE id = "+str(message.from_user.id))
                coins = coins - 20
                cursor.execute("UPDATE neko SET coins = "+ str(coins) +" WHERE id = "+str(message.from_user.id))
                os.remove(src)
            elif 'Покрасить машину' in message.caption or 'покрасить машину' in message.caption:
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом')
                    return
                event = data[10]
                bolnitsa = int(data[6] - time.time())
                coins = data[11]
                car = data[9]
                if bolnitsa > 0:
                    bot.send_message(message.chat.id, 'Ты в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if event > 0:
                    bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if coins < 20:
                    bot.send_message(message.chat.id, 'А деньги где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if car != 1:
                    bot.send_message(message.chat.id, 'Тебе нужен некомобиль')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                bot.send_message(message.chat.id,'Ты успешно нанял таджиков, которые покрасили тебе машину. Полюбуйся результатом')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'bot/files/' + file_info.file_path
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                im1 = Image.open(src)
                im1 = im1.resize((500, 300),  Image.ANTIALIAS)
                im3 = Image.open('bot/white.png')
                im3.paste(im1.convert('RGB'), (150,200))
                im1 = im3
                im2 = Image.open('bot/garag228.png')
                im1.paste(im2.convert('RGB'), (0,0), im2)
                im1.save('bot/result.png')
                f = open("bot/result.png","rb")
                m = bot.send_photo(message.chat.id, photo=f)
                n = m.photo[len(m.photo) - 1].file_id
                coins = coins - 20
                cursor.execute("UPDATE neko SET coins = "+ str(coins) +" WHERE id = "+str(message.from_user.id))
                cursor.execute("UPDATE neko SET photo_mobile = '"+ str(n) +"' WHERE id = "+str(message.from_user.id))
                os.remove(src)

            elif 'Дизайн' == message.caption or 'дизайн' == message.caption or '@NekoslaviaBot дизайн' == message.caption or '@NekoslaviaBot Дизайн' == message.caption:
                data = cursor.execute('SELECT * FROM neko WHERE id = '+str(message.from_user.id))
                data = data.fetchone()
                if data is None:
                    bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом ')
                    return
                event = data[10]
                coins = data[11]
                licension = data[26]
                bolnitsa = int(data[6] - time.time())
                phot = str(data[5]).rstrip()
                new_phot = str(data[38]).rstrip()
                if new_phot != 'None':
                    phot = new_phot
                photo_design = (data[28]).rstrip()
                gender = data[33]
                chel = message.from_user.first_name
                cost = 20
                if coins < cost:
                    bot.send_message(message.chat.id, 'А деньги где')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if event > 0:
                    bot.send_message(message.chat.id, 'Ты гуляешь ебанат')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                if bolnitsa > 0:
                    bot.send_message(message.chat.id, 'Ты в больнице дебил')
                    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW9iwHwLLVxr-1f5AAG6VRQQwGfiJ1kAAjoSAAIiZ1hI6TCE3lJaV4EpBA')
                    return
                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'bot/files/' + file_info.file_path
                with open(src, 'wb') as new_file:
                        new_file.write(downloaded_file)
                im0 = Image.open(src)
                w,h = im0.size
                if w > h:
                        nh = 630
                        nw = int((630/h)*w)
                else:
                        nw = 600
                        nh = int((600/w)*h)
                if nw < 600:
                        nw = 600
                if nh < 630:
                        nh = 630
                im0 = im0.resize((nw, nh),  Image.ANTIALIAS)
                im1 = Image.open('bot/white1.png')
                im1.paste(im0.convert('RGB'), (40,34))
                im0 = im1
                im1 = Image.open('bot/02.png')
                im0.paste(im1.convert('RGB'), (0,0), im1)
                im0 = im0.convert('RGBA')
                pixdata = im0.load()
                for y in range(im0.size[1]):
                        for x in range(im0.size[0]):
                            if pixdata[x,y][0]==255 and pixdata[x,y][1]==0 and pixdata[x,y][2]==0:
                                pixdata[x, y] = (255, 255, 255,0)


                if len(chel) > 18:
                    chel = (chel[:18] + '..')
                m = bot.send_photo(message.chat.id,photo=phot,caption = 'Идёт обработка...')
                file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'bot/files/' + file_info.file_path
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                im1 = Image.open(src)
                w,h = im1.size
                if w > h:
                    nh = 630
                    nw = int((630/h)*w)
                else:
                    nw = 600
                    nh = int((600/w)*h)
                if nw < 600:
                    nw = 600
                if nh < 630:
                    nh = 630
                im1 = im1.resize((nw, nh),  Image.ANTIALIAS)
                im3 = Image.open('bot/white1.png')
                im3.paste(im1.convert('RGB'), (490,30))
                im1 = im3
                im1.paste(im0.convert('RGB'), (0,0), im0)
                font = ImageFont.truetype('bot/segoeprint_bold.ttf', size=35)
                draw = ImageDraw.Draw(im1)
                cur = datetime.fromtimestamp(time.time() + 3*3600)
                d = int(cur.day)
                if d < 10:
                    d = '0'+str(d)
                else:
                    d = str(d)
                md = int(cur.month)
                if md < 10:
                    md = '0'+str(md)
                else:
                    md = str(md)
                y = str(cur.year)
                old_date = d+'.'+md+'.'+y

                cur = datetime.fromtimestamp(time.time() + 3*3600 + 345600)
                d = int(cur.day)
                if d < 10:
                    d = '0'+str(d)
                else:
                    d = str(d)
                md = int(cur.month)
                if md < 10:
                    md = '0'+str(md)
                else:
                    md = str(md)
                y = str(cur.year)
                new_date = d+'.'+md+'.'+y

                text = 'Выдано:  @NekoslaviaBot'
                x, y = 63, 65
                fillcolor = "#FFFFFF"
                shadowcolor = "#242425"

                draw.text((x-2, y), text, font=font, fill=shadowcolor)
                draw.text((x+2, y), text, font=font, fill=shadowcolor)
                draw.text((x, y-2), text, font=font, fill=shadowcolor)
                draw.text((x, y+2), text, font=font, fill=shadowcolor)

                draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                draw.text((x, y), text, font=font, fill=fillcolor)

                text = 'Кому:  ' + chel
                x, y = 63, 125

                draw.text((x-2, y), text, font=font, fill=shadowcolor)
                draw.text((x+2, y), text, font=font, fill=shadowcolor)
                draw.text((x, y-2), text, font=font, fill=shadowcolor)
                draw.text((x, y+2), text, font=font, fill=shadowcolor)

                draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                draw.text((x, y), text, font=font, fill=fillcolor)

                text = 'Дата выдачи:  ' + old_date
                x, y = 63, 185

                draw.text((x-2, y), text, font=font, fill=shadowcolor)
                draw.text((x+2, y), text, font=font, fill=shadowcolor)
                draw.text((x, y-2), text, font=font, fill=shadowcolor)
                draw.text((x, y+2), text, font=font, fill=shadowcolor)

                draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                draw.text((x, y), text, font=font, fill=fillcolor)

                text = 'Действует до:  ' + new_date
                x, y = 63, 245

                draw.text((x-2, y), text, font=font, fill=shadowcolor)
                draw.text((x+2, y), text, font=font, fill=shadowcolor)
                draw.text((x, y-2), text, font=font, fill=shadowcolor)
                draw.text((x, y+2), text, font=font, fill=shadowcolor)

                draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                draw.text((x, y), text, font=font, fill=fillcolor)

                font = ImageFont.truetype('bot/comicbd.ttf', size=52)
                text = 'ЛИЦЕНЗИЯ НА\nНЕКОДЕВОЧКУ'
                x, y = 95, 500
                if gender == 1:
                    text = 'ЛИЦЕНЗИЯ НА\nНЕКОМАЛЬЧИКА'
                    x, y = 65, 500
                fillcolor = "#F6B1CB"

                draw.text((x-2, y), text, font=font, fill=shadowcolor)
                draw.text((x+2, y), text, font=font, fill=shadowcolor)
                draw.text((x, y-2), text, font=font, fill=shadowcolor)
                draw.text((x, y+2), text, font=font, fill=shadowcolor)

                draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x-2, y+2), text, font=font, fill=shadowcolor)

                draw.text((x, y), text, font=font, fill=fillcolor)


                im1.save('bot/result.png')
                f = open("bot/result.png","rb")
                bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
                m = bot.send_photo(message.chat.id, photo=f,caption = 'Вот твоя новая лицензия 🎫, не теряй её и не забывай вовремя продлевать')
                fil = m.photo[len(m.photo) - 1].file_id
                fil2 = message.photo[len(message.photo) - 1].file_id
                coins = coins - cost
                cursor.execute("UPDATE neko SET coins = "+ str(coins) +" WHERE id = "+str(message.from_user.id))
                cursor.execute("UPDATE neko SET licension = "+ str(time.time() + 345600) +" WHERE id = "+str(message.from_user.id))
                cursor.execute("UPDATE neko SET photo_licension = '"+ fil +"' WHERE id = "+str(message.from_user.id))
                cursor.execute("UPDATE neko SET photo_design = '"+ fil2 +"' WHERE id = "+str(message.from_user.id))
                os.remove(src)
@bot.message_handler(func=lambda message: True,content_types=["animation"])
def msg_anim_bot(message):
        if message.chat.id ==  -1001694727085:
            try:
                bot.send_message(message.chat.id,str(message.animation.file_id),reply_to_message_id=message.message_id)
                bot.send_animation(message.chat.id,message.animation.file_id)
            except Exception as e:
                bot.send_message(-1001694727085,e)

def pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,blocks1,blocks2,skills1,skills2):
    txt = nam1 + ' \n[ '
    i = 1
    while i <= maxhp1:
        if (i <= hp1):
            txt = txt + '🟩'
        else:
            txt = txt + '🟥'
        i = i + 1
    txt = txt + ' ]'
    if blocks1 > 0:
        for i in range(blocks1):
            txt = txt + '🛡 '
    if 8 in skills1 or 88 in skills1 or 6 in skills1:
        txt = txt + '\n'
        if 8 in skills1:
            txt = txt + '☘️☘️'
        elif 88 in skills1:
            txt = txt + '☘️'
        if 6 in skills1:
            txt = txt + '✝️'
        txt = txt + '\n\n'
    else:
        txt = txt + '\n\n'


    txt = txt + nam2 + '\n[ '
    i = 1
    while i <= maxhp2:
        if i <= hp2:
            txt = txt + '🟩'
        else:
            txt = txt + '🟥'
        i = i + 1
    txt = txt + ' ]'
    if blocks2 > 0:
        for i in range(blocks2):
            txt = txt + '🛡 '
    if 8 in skills2 or 88 in skills2 or 6 in skills2:
        txt = txt + '\n'
        if 8 in skills2:
            txt = txt + '☘️☘️'
        elif 88 in skills2:
            txt = txt + '☘️'
        if 6 in skills2:
            txt = txt + '✝️'
        txt = txt + '\n\n'
    else:
        txt = txt + '\n\n'

    return txt

def poker_image(cards,event):
    im1 = Image.open('bot/table.png')
    im2 = Image.open('bot/cardback.png')
    im3 = Image.open('bot/cards.png')
    for i in range(5):
        card = cards[i]
        b = round((card%1)*10)
        a = round(card)
        if i > event:
            im1.paste(im2.convert('RGB'), (82+i*215,203), im2)
        else:
            x = 215*(a-2)
            y = 295*(b-1)
            crop = im3.crop((x, y, x+215, y+295))
            im1.paste(crop.convert('RGB'), (82+i*215,203), crop)

    im1.save('bot/result.png')
    f = open("bot/result.png","rb")
    return f
def notify_callback_query(call,txt):
    try:
        bot.answer_callback_query(call.id,text = txt,show_alert = True)
    except:
        try:
            bot.send_message(call.from_user.id, text = txt, parse_mode='HTML')
        except:
            pass
def answer_callback_query(call,txt):
    try:
        bot.answer_callback_query(call.id,text = txt)
    except:
        pass
def bone_atack(field,atack,bone):
    if bone == 0 or atack == 0:
        return
    #if atack == 1:
    #    a1 = random.randint(0,35)
    #    while field[a1] == 6:
    #        a1 = random.randint(0,35)
    #    field[a1] = 6
    #    return
    a1 = random.randint(0,35)
    a2 = random.randint(0,35)
    while a1 == a2 or field[a1] == 6 or field[a2] == 6:
        a1 = random.randint(0,35)
        a2 = random.randint(0,35)
    field[a1] = 6
    field[a2] = 6
    return
    # elif atack >= 3:
    #    a1 = random.randint(0,35)
    #    a2 = random.randint(0,35)
    #    a3 = random.randint(0,35)
    #    while a1 == a2 or a1 == a3 or a2 == a3 or field[a1] == 6 or field[a2] == 6 or field[a3] == 6:
    #        a1 = random.randint(0,35)
    #        a2 = random.randint(0,35)
    #        a3 = random.randint(0,35)
    #    field[a1] = 6
    #    field[a2] = 6
    #    field[a3] = 6
    #    return
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
      if call.data == "no":
        answer_callback_query(call,'Лох')
      elif "decline" in call.data:
        args = call.data.split()
        one = int(args[1])
        two = int(args[2])
        if call.from_user.id != two:
            answer_callback_query(call,'Пашол нахуй')
            return
        cursor.execute("DELETE FROM battles WHERE one = "+str(one)+" AND two = " + str(two))
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(two))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        answer_callback_query(call,'Успешно')
        chel = str(data[16]).rstrip()
        txt = '<a href="tg://user?id='+str(two)+'">'+str(chel)+'</a> оказался ссыклом...'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=txt,parse_mode='HTML')
      elif "aremove" in call.data:
        args = call.data.split()
        one = int(args[1])
        two = int(args[2])
        if call.from_user.id != one:
            answer_callback_query(call,'Пашол нахуй')
            return
        answer_callback_query(call,'Успешно')
        cursor.execute("DELETE FROM battles WHERE one = "+str(one)+" AND two = " + str(two))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

      elif "accept" in call.data:
        args = call.data.split()
        one = int(args[1])
        two = int(args[2])
        cost = int(args[3])
        if call.from_user.id == one:
            answer_callback_query(call,'Пашол нахуй')
            return
        if call.from_user.id != two and two != 0:
            answer_callback_query(call,'Пашол нахуй')
            return
        data = cursor.execute('SELECT * FROM neko WHERE id = ' + str(one))
        data = data.fetchone()
        rep1 = data[2]
        nam1 = str(data[1]).rstrip()
        arena1 = int(data[17] - time.time())
        b1 = int(data[6] - time.time())
        c1 = data[11]
        phot1 = str(data[5]).rstrip()
        new_phot = str(data[38]).rstrip()
        if new_phot != 'None':
            phot1 = new_phot
        skill1 = data[30]
        skill2 = data[31]
        gender1 = data[33]
        bones1 = data[43]
        skills1 = [skill1,skill2]
        if rep1 < 20 or arena1 > 0 or b1 > 0 or c1 < cost:
            answer_callback_query(call,'Проблема на стороне отправителя')
            return
        data = cursor.execute('SELECT * FROM neko WHERE id = ' + str(call.from_user.id))
        data = data.fetchone()
        rep2 = data[2]
        nam2 = str(data[1]).rstrip()
        arena2 = int(data[17] - time.time())
        b2 = int(data[6] - time.time())
        c2 = data[11]
        phot2 = str(data[5]).rstrip()
        new_phot = str(data[38]).rstrip()
        if new_phot != 'None':
            phot2 = new_phot
        skill1 = data[30]
        skill2 = data[31]
        gender2 = data[33]
        bones2 = data[43]
        skills2 = [skill1,skill2]
        if rep2 < 20:
            txt = 'Некодевочка недостаточно доверяет тебе'
            if gender2 == 1:
                txt = 'Некомальчик недостаточно доверяет тебе'
            answer_callback_query(call,txt)
            return
        if arena2 > 0:
            txt = 'Дай некодевочке отдохнуть'
            if gender2 == 1:
                txt = 'Дай некомальчику отдохнуть'
            answer_callback_query(call,txt)
            return
        if b2 > 0:
            answer_callback_query(call,'Ты в больнице')
            return
        if c2 < cost:
            answer_callback_query(call,'А деньги где')
            return
        answer_callback_query(call,'Успешно')
        field1 = []
        field2 = []
        sym = ['🟥','🟧','🟡','🟢','💙','⭐️','🦴']
        b = [0,1,2,3,4]
        if 2 in skills1:
            b.append(2)
        if 3 in skills1:
            b.append(4)
        for i in range(36):
            s = random.choice(b)
            field1.append(s)
        b = [0,1,2,3,4]
        if 2 in skills2:
            b.append(2)
        if 3 in skills2:
            b.append(4)
        for i in range(36):
            s = random.choice(b)
            field2.append(s)
        fielder(field1,skills1[0],skills1[1],False)
        fielder(field2,skills2[0],skills2[1],False)
        fd1 = pack(field1)
        fd2 = pack(field2)
        m = bot.send_photo(-1001694727085,photo=phot1)
        file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'bot/files/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        im1 = Image.open(src)
        w,h = im1.size
        if w > h:
            nh = 800
            nw = int((800/h)*w)
        else:
            nw = 781
            nh = int((781/w)*h)
        if nw < 781:
            nw = 781
        if nh < 800:
            nh = 800
        im1 = im1.resize((nw, nh),  Image.ANTIALIAS)
        im3 = Image.open('bot/white2.png')
        im3.paste(im1.convert('RGB'), (0,0))
        im1 = im3
        if bones2 > 0:
            im2 = Image.open('bot/bone_hands.png')
        else:
            im2 = Image.open('bot/hands.png')
        im1.paste(im2.convert('RGBA'), (0,0),im2)
        im1.save('bot/result.png')
        f = open("bot/result.png","rb")
        m = bot.send_photo(-1001694727085, photo=f)
        image1 = m.photo[len(m.photo) - 1].file_id
        os.remove(src)

        m = bot.send_photo(-1001694727085,photo=phot2)
        file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'bot/files/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        im1 = Image.open(src)
        w,h = im1.size
        if w > h:
            nh = 800
            nw = int((800/h)*w)
        else:
            nw = 781
            nh = int((781/w)*h)
        if nw < 781:
            nw = 781
        if nh < 800:
            nh = 800
        im1 = im1.resize((nw, nh),  Image.ANTIALIAS)
        im3 = Image.open('bot/white2.png')
        im3.paste(im1.convert('RGB'), (0,0))
        im1 = im3
        if bones1 > 0:
            im2 = Image.open('bot/bone_hands.png')
        else:
            im2 = Image.open('bot/hands.png')
        im1.paste(im2.convert('RGBA'), (0,0),im2)
        im1.save('bot/result.png')
        f = open("bot/result.png","rb")
        m = bot.send_photo(-1001694727085, photo=f)
        image2 = m.photo[len(m.photo) - 1].file_id
        os.remove(src)
        arena = int(time.time()+1800)
        cursor.execute('UPDATE neko SET arena = ' + str(arena) + ' WHERE id = ' + str(one) + ' OR id = ' + str(call.from_user.id))
        wait = int(time.time()+1200)
        cursor.execute("UPDATE battles SET bone_one = " + str(bones1) + ", bone_two = " + str(bones2) + ", imageone = '" + image1 + "',imagetwo = '" + image2 + "',event = 1,selected = -1,nameone = '" + nam1 + "',nametwo = '" + nam2 + "', wait = " + str(wait) + ",two = " + str(call.from_user.id) + ",fieldone = '" + str(fd1) + "',fieldtwo = '" + str(fd2) + "' WHERE one = " + str(one) + " AND two = " + str(two))
        two = call.from_user.id
        txt = 'Некодевочки выйдут на арену через 15 секунд, собирайте символы по 4 в ряд чтобы поддерживать своих некодевочек с трибун\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
        if gender1 == 1 or gender2 == 1:
            txt = 'Некодевочки и некомальчики выйдут на арену через 15 секунд, собирайте символы по 4 в ряд чтобы поддерживать своих неко с трибун\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
        if gender1 == 1 and gender2 == 1:
            txt = 'Некомальчики выйдут на арену через 15 секунд, собирайте символы по 4 в ряд чтобы поддерживать своих некомальчиков с трибун\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=txt,parse_mode='HTML')
        b = [one,two]
        turn = random.choice(b)
        if turn == one:
            field = field1
            skills = skills1
        else:
            field = field2
            skills = skills2
        blocks1 = 0
        blocks2 = 0
        turns = 1
        if 7 in skills:
            turns = 4
            skills.remove(7)
            skills.append(0)
        if rep1 > rep2:
            maxhp1 = 8
            hp1 = 8
            d = rep1/8
            maxhp2 = math.ceil(rep2/d)
            hp2 = maxhp2
        if rep1 < rep2:
            maxhp2 = 8
            hp2 = 8
            d = rep2/8
            maxhp1 = math.ceil(rep1/d)
            hp1 = maxhp1
        if rep1 == rep2:
            maxhp2 = 8
            hp2 = 8
            maxhp1 = 8
            hp1 = 8

        keyboard = types.InlineKeyboardMarkup(row_width=6)
        stack = []
        dat = 'pvp ' + str(one) + ' ' + str(two) + ' ' + str(turn) + ' ' + str(hp1) + ' ' + str(hp2) + ' ' + str(maxhp1) + ' ' + str(maxhp2) + ' ' + str(turns) + ' ' + str(blocks1) + ' ' + str(blocks2)
        for i in range(36):
            callback_button = types.InlineKeyboardButton(text = sym[field[i]],callback_data = dat + ' ' + str(i) + ' 1 1 1')
            stack.append(callback_button)
            if len(stack) == 6:
                keyboard.add(stack[0],stack[1],stack[2],stack[3],stack[4],stack[5])
                stack = []
        if skills[0] > 100:
            reroll = types.InlineKeyboardButton(text = skill_names[skills[0]-100],callback_data = dat + ' ' + str(-skills[0]) + ' 0 1 1')
            keyboard.add(reroll)
        if skills[1] > 100:
            reroll = types.InlineKeyboardButton(text = skill_names[skills[1]-100],callback_data = dat + ' ' + str(-skills[1]) + ' 1 0 1')
            keyboard.add(reroll)
        txt = pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,0,0,skills1,skills2)
        if turn == one:
            nam = nam1
        else:
            nam = nam2
        txt = txt + 'Ходит <a href="tg://user?id='+str(turn)+'">'+str(nam)+'</a>\n'
        txt = txt + 'Осталось ходов до атаки врага:  ' + str(turns)
        time.sleep(15)
        sk1 = pack(skills1)
        sk2 = pack(skills2)
        if turn == one:
            image = image2
        else:
            image = image1
        m = bot.send_photo(call.message.chat.id, photo=image,caption = txt,reply_markup=keyboard,parse_mode='HTML')
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        cursor.execute("UPDATE battles SET event = 2, chat = " + str(m.chat.id) + ", skillone = '" + str(sk1) + "',skilltwo = '" + str(sk2) + "', message = " + str(m.id) + " WHERE one = " + str(one) + " AND two = " + str(two))

      elif "pvp" in call.data:
        args = call.data.split()
        one = int(args[1])
        two = int(args[2])
        turn = int(args[3])
        hp1 = int(args[4])
        hp2 = int(args[5])
        maxhp1 = int(args[6])
        maxhp2 = int(args[7])
        turns = int(args[8])
        blocks1 = int(args[9])
        blocks2 = int(args[10])
        pos = int(args[11])
        rer1 = int(args[12])
        rer2 = int(args[13])
        starter = int(args[14])
        if call.from_user.id != turn:
            answer_callback_query(call,'Не твой ход')

            return
        time.sleep(0.25)
        data = cursor.execute('SELECT * FROM battles WHERE one = '+str(one)+' AND two = ' + str(two))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')

            return
        cost = data[4]
        field1 = unpack(data[7])
        field2 = unpack(data[8])
        selected = data[9]
        nam1 = (data[10]).rstrip()
        nam2 = (data[11]).rstrip()
        image1 = (data[12]).rstrip()
        image2 = (data[13]).rstrip()
        skills1 = unpack(data[14])
        skills2 = unpack(data[15])
        bone1 = data[16]
        bone2 = data[17]
        atack = 0
        ability = 0
        if turn == one:
            field = field1
            skills = skills1
            hp = hp1
            maxhp = maxhp1
        else:
            field = field2
            skills = skills2
            hp = hp2
            maxhp = maxhp2
        if pos < 0:
            ability = abs(pos)
            if ability == 101:
                if selected == -1:
                    answer_callback_query(call,'Сначала выбери фигуру')
                    return
                if field[selected] == 5:
                    answer_callback_query(call,'Это уже звезда')
                    return
                field[selected] = 5
            elif ability == 102:
                if selected == -1:
                    answer_callback_query(call,'Сначала выбери фигуру')
                    return
                field[selected] = -1
            elif ability == 103:
                random.shuffle(field)
            elif ability == 104:
                turns -= 1
                atack += 1
            elif ability == 105:
                turns -= 1
                if turn == one:
                    blocks1 += 1
                else:
                    blocks2 += 1
            elif ability == 106:
                a1 = random.randint(0,35)
                a2 = random.randint(0,35)
                while a1 == a2 or field[a1] == 5 or field[a2] == 5:
                    a1 = random.randint(0,35)
                    a2 = random.randint(0,35)
                field[a1] = 5
                field[a2] = 5
            elif ability == 107:
                if selected == -1:
                    answer_callback_query(call,'Сначала выбери фигуру')
                    return
                if field.count(field[selected]) < 11:
                    answer_callback_query(call,'Недостаточно фигур')
                    return
                figa = field[selected]
                for i in range(36):
                    if field[i] == figa:
                        field[i] = -1
                if figa == 0 or figa == 1:
                    if turn == one:
                        blocks1 += 1
                    else:
                        blocks2 += 1
                elif figa == 2 or figa == 3:
                    atack = atack + 1
                elif figa == 4:
                    turns = turns + 1
            elif ability == 108:
                if selected == -1:
                    answer_callback_query(call,'Сначала выбери фигуру')
                    return
                res = math.ceil(selected/6 + 0.1)
                for i in range((res-1)*6,res*6):
                    field[i] = -1
            if ability == 109:
                if selected == -1:
                    answer_callback_query(call,'Сначала выбери фигуру')
                    return
                if field[selected] != 5:
                    answer_callback_query(call,'Это не звезда')
                    return
                field[selected] = -1
                turns = turns + 1
            elif ability == 110:
                if selected == -1:
                    answer_callback_query(call,'Сначала выбери фигуру')
                    return
                figa = field[selected]
                a1 = random.randint(0,35)
                a2 = random.randint(0,35)
                while a1 == a2 or field[a1] == figa or field[a2] == figa:
                    a1 = random.randint(0,35)
                    a2 = random.randint(0,35)
                field[a1] = figa
                field[a2] = figa
            selected = -1
            answer_callback_query(call,'Успешно')
        else:
                if selected == -1:
                    answer_callback_query(call,'Выбрано')
                    selected = pos
                    cursor.execute("UPDATE battles SET selected = " + str(selected) + " WHERE one = "+ str(one) + " AND two = " + str(two))

                    return
                if selected == pos:
                    answer_callback_query(call,'Выбор отменен')
                    selected = -1
                    cursor.execute("UPDATE battles SET selected = " + str(selected) + " WHERE one = "+ str(one) + " AND two = " + str(two))

                    return
                d = selected - pos
                if d != 1 and d != -1 and d != 6 and d != -6:
                    answer_callback_query(call,'Можно менять только соседние, выбор отменен')
                    selected = -1
                    cursor.execute("UPDATE battles SET selected = " + str(selected) + " WHERE one = "+ str(one) + " AND two = " + str(two))

                    return
                if field[pos] == field[selected]:
                    answer_callback_query(call,'Клетки одинаковые, выбор отменен')
                    selected = -1
                    cursor.execute("UPDATE battles SET selected = " + str(selected) + " WHERE one = "+ str(one) + " AND two = " + str(two))

                    return
                answer_callback_query(call,'Меняю...')
                d = field[pos]
                field[pos] = field[selected]
                field[selected] = d
                turns = turns - 1
                selected = -1

        result = fielder(field,skills[0],skills[1],True)
        atack += result[0]
        if turn == one:
            blocks1 = blocks1 + result[1]
            if 1 in skills and ability != 105:
                hp1 = hp1 + blocks1
                blocks1 = 0
                if hp1 > maxhp1:
                    hp1 = maxhp1
        else:
            blocks2 = blocks2 + result[1]
            if 1 in skills and ability != 105:
                hp2 = hp2 + blocks2
                blocks2 = 0
                if hp2 > maxhp2:
                    hp2 = maxhp2
        turns = turns + result[2]
        if blocks1 > 3:
            blocks1 = 3
        if blocks2 > 3:
            blocks2 = 3

        if 5 in skills and hp == maxhp and atack != 0:
            atack = atack + 1
        if 4 in skills and hp <= 2 and atack != 0:
            atack = atack + 1
        if 10 in skills and turns == 0 and atack != 0:
            if turn == one and blocks1 == 0:
                atack = atack + 1
            elif turn == two and blocks2 == 0:
                atack = atack + 1

        if turn == one and atack != 0:
            r = True
            bone_atack(field2,atack,bone1)
            if 8 in skills2 or 88 in skills2:
                k = random.randint(1,20)
                if k == 1:
                    r = False
            if r:
                if blocks2 >= atack:
                    blocks2 = blocks2 - atack
                else:
                    atack = atack - blocks2
                    blocks2 = 0
                    hp2 = hp2 - atack
            else:
                if 8 in skills2:
                    skills2.remove(8)
                    skills2.append(88)
                else:
                    skills2.remove(88)
                    skills2.append(0)
            if hp2 <= 0:
                if 6 in skills2:
                    skills2.remove(6)
                    skills2.append(0)
                    hp2 = 1
                else:
                    hp2 = 0
                    txt = pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,blocks1,blocks2,skills1,skills2)
                    bot.edit_message_media(media=telebot.types.InputMedia(media=call.message.photo[len(call.message.photo) - 1].file_id,caption = txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
                    time.sleep(1)
                    newcost = cost
                    cursor.execute('DELETE FROM battles WHERE one = '+str(one)+' AND two = ' + str(two))
                    data = cursor.execute('SELECT * FROM neko WHERE id = ' + str(one))
                    data = data.fetchone()
                    c1 = data[11]
                    w1 = data[15]
                    gender1 = data[33]
                    c1 = c1 + newcost
                    w1 = w1 + 1
                    cursor.execute('UPDATE neko SET wins = ' + str(w1) + ',coins = ' + str(c1) + ' WHERE id = ' + str(one))
                    txt = 'Победила дружба, наебал, победила <a href="tg://user?id='+str(one)+'">'+str(nam1)+'</a>. Выигрыш составил ' + str(newcost) + ' 💰, владельцам арены понравился бой и они не взяли процентов. Не забудьте дать некодевочкам отдохнуть'
                    if gender1 == 1:
                        txt = 'Победила дружба, наебал, победил <a href="tg://user?id='+str(one)+'">'+str(nam1)+'</a>. Выигрыш составил ' + str(newcost) + ' 💰, владельцам арены понравился бой и они не взяли процентов. Не забудьте дать некодевочкам отдохнуть'
                    bot.send_message(call.message.chat.id, txt ,parse_mode='HTML')
                    data = cursor.execute('SELECT * FROM neko WHERE id = ' + str(two))
                    data = data.fetchone()
                    c2 = data[11]
                    c2 = c2 - cost
                    cursor.execute('UPDATE neko SET coins = ' + str(c2) + ' WHERE id = ' + str(two))
                    cursor.execute('UPDATE neko SET bones = bones - 1 WHERE id = ' + str(one) + ' AND bones > 0')
                    cursor.execute('UPDATE neko SET bones = bones - 1 WHERE id = ' + str(two) + ' AND bones > 0')
                    return
        if turn == two and atack != 0:
            r = True
            bone_atack(field1,atack,bone2)
            if 8 in skills1 or 88 in skills1:
                k = random.randint(1,20)
                if k == 1:
                    r = False
            if r:
                if blocks1 >= atack:
                    blocks1 = blocks1 - atack
                else:
                    atack = atack - blocks1
                    blocks1 = 0
                    hp1 = hp1 - atack
            else:
                if 8 in skills1:
                    skills1.remove(8)
                    skills1.append(88)
                else:
                    skills1.remove(88)
                    skills1.append(0)

            if hp1 <= 0:
                if 6 in skills1:
                    skills1.remove(6)
                    skills1.append(0)
                    hp1 = 1
                else:
                    hp1 = 0
                    txt = pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,blocks1,blocks2,skills1,skills2)

                    bot.edit_message_media(media=telebot.types.InputMedia(media=call.message.photo[len(call.message.photo) - 1].file_id,caption = txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
                    time.sleep(1)
                    newcost = cost
                    cursor.execute('DELETE FROM battles WHERE one = '+str(one)+' AND two = ' + str(two))
                    data = cursor.execute('SELECT * FROM neko WHERE id = ' + str(two))
                    data = data.fetchone()
                    c1 = data[11]
                    w1 = data[15]
                    gender2 = data[33]
                    c1 = c1 + newcost
                    w1 = w1 + 1
                    cursor.execute('UPDATE neko SET wins = ' + str(w1) + ',coins = ' + str(c1) + ' WHERE id = ' + str(two))
                    txt = 'Победила дружба, наебал, победила <a href="tg://user?id='+str(two)+'">'+str(nam2)+'</a>. Выигрыш составил ' + str(newcost) + ' 💰, владельцам арены понравился бой и они не взяли процентов. Не забудьте дать некодевочкам отдохнуть'
                    if gender2 == 1:
                        txt = 'Победила дружба, наебал, победил <a href="tg://user?id='+str(two)+'">'+str(nam2)+'</a>. Выигрыш составил ' + str(newcost) + ' 💰, владельцам арены понравился бой и они не взяли процентов. Не забудьте дать некодевочкам отдохнуть'
                    bot.send_message(call.message.chat.id, txt,parse_mode='HTML')
                    data = cursor.execute('SELECT * FROM neko WHERE id = ' + str(one))
                    data = data.fetchone()
                    c2 = data[11]
                    c2 = c2 - cost
                    cursor.execute('UPDATE neko SET coins = ' + str(c2) + ' WHERE id = ' + str(one))
                    cursor.execute('UPDATE neko SET bones = bones - 1 WHERE id = ' + str(one) + ' AND bones > 0')
                    cursor.execute('UPDATE neko SET bones = bones - 1 WHERE id = ' + str(two) + ' AND bones > 0')
                    return
        if turns == 0:
            rer1 = 1
            rer2 = 1
            turns = 2

            if turn == one:
                turn = two
                field = field2
                skills = skills2
                if 9 in skills and hp2 < hp1:
                    turns += 1
            else:
                turn = one
                field = field1
                skills = skills1
                if 9 in skills and hp1 < hp2:
                    turns += 1
            if starter == 1:
                starter = 0
                turns = 1
            if 7 in skills:
                turns = 4
                skills.remove(7)
                skills.append(0)

        if turn == one:
            image = image2
        else:
            image = image1

        keyboard = types.InlineKeyboardMarkup(row_width=6)
        stack = []
        sym = ['🟥','🟧','🟡','🟢','💙','⭐️','🦴']
        dat = 'pvp ' + str(one) + ' ' + str(two) + ' ' + str(turn) + ' ' + str(hp1) + ' ' + str(hp2) + ' ' + str(maxhp1) + ' ' + str(maxhp2) + ' ' + str(turns) + ' ' + str(blocks1) + ' ' + str(blocks2)
        for i in range(36):
            callback_button = types.InlineKeyboardButton(text = sym[field[i]],callback_data = dat + ' ' + str(i) + ' ' + str(rer1) + ' ' + str(rer2) + ' ' + str(starter))
            stack.append(callback_button)
            if len(stack) == 6:
                keyboard.add(stack[0],stack[1],stack[2],stack[3],stack[4],stack[5])
                stack = []
        if skills[0] > 100 and rer1 == 1:
            reroll = types.InlineKeyboardButton(text = skill_names[skills[0]-100],callback_data = dat + ' ' + str(-skills[0]) + ' ' + str(0) + ' ' + str(rer2) + ' ' + str(starter))
            keyboard.add(reroll)
        if skills[1] > 100 and rer2 == 1:
            reroll = types.InlineKeyboardButton(text = skill_names[skills[1]-100],callback_data = dat + ' ' + str(-skills[1]) + ' ' + str(rer1) + ' ' + str(0) + ' ' + str(starter))
            keyboard.add(reroll)

        txt = pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,blocks1,blocks2,skills1,skills2)
        if turn == one:
            nam = nam1
        else:
            nam = nam2
        txt = txt + 'Ходит <a href="tg://user?id='+str(turn)+'">'+str(nam)+'</a>\n'
        txt = txt + 'Осталось ходов до атаки врага:  ' + str(turns)
        fd1 = pack(field1)
        fd2 = pack(field2)
        sk1 = pack(skills1)
        sk2 = pack(skills2)
        cursor.execute("UPDATE battles SET selected = " + str(selected) + ",skillone = '" + str(sk1) + "',skilltwo = '" + str(sk2) + "', fieldone = '" + str(fd1) + "',fieldtwo = '" + str(fd2) + "' WHERE one = "+ str(one) + " and two = " + str(two))
        time.sleep(2)
        bot.edit_message_media(media=telebot.types.InputMedia(media=image,caption = txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)



      elif "pve" in call.data:
        sym = ['🟥','🟧','🟡','🟢','💙']
        args = call.data.split()
        idk = int(args[1])
        turns = int(args[2])
        blocks = int(args[3])
        pos = int(args[4])
        rer = int(args[5])
        targ = int(args[6])
        enemy1 = int(args[7])
        enemy2 = int(args[8])
        enemy3 = int(args[9])
        hpe1 = int(args[10])
        hpe2 = int(args[11])
        hpe3 = int(args[12])
        enems = [enemy1,enemy2,enemy3]
        hpes = [hpe1,hpe2,hpe3]
        atack = 0

        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return

        time.sleep(0.25)
        data = cursor.execute('SELECT * FROM dungeons WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')

            return
        field = unpack(data[10])
        selected = data[11]
        next_x = data[12]
        next_y = data[13]
        hp = data[14]
        maxhp = data[15]
        try:
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
            data = data.fetchone()
            nam = str(data[1]).rstrip()
            rep = data[2]
            gender = data[33]
        except:
            nam = 'Некодевочка'
            rep = 0
            gender = 0
        if pos == -2:
            answer_callback_query(call,'Меняю')
            field = []
            sym = ['🟥','🟧','🟡','🟢','💙']
            for i in range(36):
                s = random.randint(0,4)
                field.append(s)
            while True:

                found = False
                for j in range(6):
                    for i in range(3):
                        if field[j*6+i] != -1 and field[j*6+i] == field[j*6+i+1] and field[j*6+i+1] == field[j*6+i+2] and field[j*6+i+2] == field[j*6+i+3]:
                            field[j*6+i] = -1
                            field[j*6+i+1] = -1
                            field[j*6+i+2] = -1
                            field[j*6+i+3] = -1
                            found = True
                for j in range(3):
                    for i in range(6):
                        if field[j*6+i] != -1 and field[j*6+i] == field[(j+1)*6+i] and field[(j+1)*6+i] == field[(j+2)*6+i] and field[(j+2)*6+i] == field[(j+3)*6+i]:
                            field[j*6+i] = -1
                            field[(j+1)*6+i] = -1
                            field[(j+2)*6+i] = -1
                            field[(j+3)*6+i] = -1
                            found = True
                if found == False:
                    break
                while True:
                    f = False
                    for i in range(36):
                        if field[i] == -1:
                            f = True
                            if i < 6:
                                field[i] = random.randint(0,4)
                            else:
                                field[i] = field[i-6]
                                field[i-6] = -1
                    if f == False:
                        break
        elif pos == -3:
                if selected == -1:
                    answer_callback_query(call,'Сначала выбери фигуру')

                    return
                field[selected] = -1
                answer_callback_query(call,'Успешно')
        elif pos == -4 or pos == -5 or pos == -6:
                newtarg = abs(pos) - 4
                if newtarg == targ:
                    answer_callback_query(call,'Эта цель уже выбрана')

                    return
                if enems[newtarg] == -1:
                    answer_callback_query(call,'На этой позиции никого нет')

                    return
                answer_callback_query(call,'Меняю цель')
                targ = newtarg
        else:
                if selected == -1:
                    answer_callback_query(call,'Успешно выбрано')
                    selected = pos
                    cursor.execute("UPDATE dungeons SET selected = " + str(selected) + " WHERE id = "+ str(idk))

                    return
                if selected == pos:
                    answer_callback_query(call,'Выбор отменен')
                    selected = -1
                    cursor.execute("UPDATE dungeons SET selected = " + str(selected) + " WHERE id = "+ str(idk))

                    return
                d = selected - pos
                if d != 1 and d != -1 and d != 6 and d != -6:
                    answer_callback_query(call,'Менять можно только соседние, выбор отменен')
                    selected = -1
                    cursor.execute("UPDATE dungeons SET selected = " + str(selected) + " WHERE id = "+ str(idk))

                    return
                if field[pos] == field[selected]:
                    answer_callback_query(call,'Клетки одинаковые, выбор отменен')
                    selected = -1
                    cursor.execute("UPDATE dungeons SET selected = " + str(selected) + " WHERE id = "+ str(idk))

                    return
                answer_callback_query(call,'Меняю...')
                d = field[pos]
                field[pos] = field[selected]
                field[selected] = d
                turns = turns - 1
        while True:
                found = False
                for i in range(36):
                    if field[i] == -1:
                        found = True
                for j in range(6):
                    i = 0
                    if field[j*6+i] != -1 and field[j*6+i] == field[j*6+i+1] and field[j*6+i+1] == field[j*6+i+2] and field[j*6+i+2] == field[j*6+i+3] and field[j*6+i+3] == field[j*6+i+4] and field[j*6+i+4] == field[j*6+i+5]:
                        if field[j*6+i] == 0 or field[j*6+i] == 1:
                            blocks = blocks + 3
                        elif field[j*6+i] == 2 or field[j*6+i] == 3:
                            atack = atack + 3
                        else:
                            turns = turns + 3
                        field[j*6+i] = -1
                        field[j*6+i+1] = -1
                        field[j*6+i+2] = -1
                        field[j*6+i+3] = -1
                        field[j*6+i+4] = -1
                        field[j*6+i+5] = -1
                        found = True
                for i in range(6):
                    j = 0
                    if field[j*6+i] != -1 and field[j*6+i] == field[(j+1)*6+i] and field[(j+1)*6+i] == field[(j+2)*6+i] and field[(j+2)*6+i] == field[(j+3)*6+i] and field[(j+3)*6+i] == field[(j+4)*6+i] and field[(j+4)*6+i] == field[(j+5)*6+i]:
                        if field[j*6+i] == 0 or field[j*6+i] == 1:
                            blocks = blocks + 3
                        elif field[j*6+i] == 2 or field[j*6+i] == 3:
                            atack = atack + 3
                        else:
                            turns = turns + 3
                        field[j*6+i] = -1
                        field[(j+1)*6+i] = -1
                        field[(j+2)*6+i] = -1
                        field[(j+3)*6+i] = -1
                        field[(j+4)*6+i] = -1
                        field[(j+5)*6+i] = -1
                        found = True
                for j in range(6):
                    for i in range(2):
                        if field[j*6+i] != -1 and field[j*6+i] == field[j*6+i+1] and field[j*6+i+1] == field[j*6+i+2] and field[j*6+i+2] == field[j*6+i+3] and field[j*6+i+3] == field[j*6+i+4]:
                            if field[j*6+i] == 0 or field[j*6+i] == 1:
                                blocks = blocks + 2
                            elif field[j*6+i] == 2 or field[j*6+i] == 3:
                                atack = atack + 2
                            else:
                                turns = turns + 2
                            field[j*6+i] = -1
                            field[j*6+i+1] = -1
                            field[j*6+i+2] = -1
                            field[j*6+i+3] = -1
                            field[j*6+i+4] = -1
                            found = True
                for j in range(2):
                    for i in range(6):
                        if field[j*6+i] != -1 and field[j*6+i] == field[(j+1)*6+i] and field[(j+1)*6+i] == field[(j+2)*6+i] and field[(j+2)*6+i] == field[(j+3)*6+i] and field[(j+3)*6+i] == field[(j+4)*6+i]:
                            if field[j*6+i] == 0 or field[j*6+i] == 1:
                                blocks = blocks + 2
                            elif field[j*6+i] == 2 or field[j*6+i] == 3:
                                atack = atack + 2
                            else:
                                turns = turns + 2
                            field[j*6+i] = -1
                            field[(j+1)*6+i] = -1
                            field[(j+2)*6+i] = -1
                            field[(j+3)*6+i] = -1
                            field[(j+4)*6+i] = -1
                            found = True
                for j in range(6):
                    for i in range(3):
                        if field[j*6+i] != -1 and field[j*6+i] == field[j*6+i+1] and field[j*6+i+1] == field[j*6+i+2] and field[j*6+i+2] == field[j*6+i+3]:
                            if field[j*6+i] == 0 or field[j*6+i] == 1:
                                blocks = blocks + 1
                            elif field[j*6+i] == 2 or field[j*6+i] == 3:
                                atack = atack + 1
                            else:
                                turns = turns + 1
                            field[j*6+i] = -1
                            field[j*6+i+1] = -1
                            field[j*6+i+2] = -1
                            field[j*6+i+3] = -1
                            found = True
                for j in range(3):
                    for i in range(6):
                        if field[j*6+i] != -1 and field[j*6+i] == field[(j+1)*6+i] and field[(j+1)*6+i] == field[(j+2)*6+i] and field[(j+2)*6+i] == field[(j+3)*6+i]:
                            if field[j*6+i] == 0 or field[j*6+i] == 1:
                                blocks = blocks + 1
                            elif field[j*6+i] == 2 or field[j*6+i] == 3:
                                atack = atack + 1
                            else:
                                turns = turns + 1
                            field[j*6+i] = -1
                            field[(j+1)*6+i] = -1
                            field[(j+2)*6+i] = -1
                            field[(j+3)*6+i] = -1
                            found = True
                if found == False:
                    break
                while True:
                    f = False
                    for i in range(36):
                        if field[i] == -1:
                            f = True
                            if i < 6:
                                field[i] = random.randint(0,4)
                            else:
                                field[i] = field[i-6]
                                field[i-6] = -1
                    if f == False:
                        break
        if blocks > 3:
            blocks = 3
        if atack > 3:
            blocks = 3
        if turns > 5:
            turns = 5
        hpes[targ] = hpes[targ] - atack
        if hpes[targ] <= 0:
            hpes[targ] = 0
            if enems[targ] == 3:
                enems[targ] = 4
                turns = turns + 2
                hpes[targ] = 1
            elif enems[targ] == 4:
                turns = 0
                rer = 1
            else:
                enems[targ] = -1
                if enems[0] != -1:
                    targ = 0
                if enems[1] != -1:
                    targ = 1
                if enems[2] != -1:
                    targ = 2
        if turns == 0:
            turns = 2
            rer = 1
            for i in range(3):
                if enems[i] != -1:
                    if enems[i] == 1:
                        enems[i] = 2
                    elif enems[i] == 2:
                        enems[i] = 1
                        if blocks > 0:
                            blocks = blocks - 1
                        else:
                            hp = hp - 1
                    elif enems[i] == 4:
                        enems[i] = -1
                        if blocks > 1:
                            blocks = blocks - 2
                        else:
                            if blocks > 0:
                                blocks = blocks - 1
                                hp = hp - 1
                            else:
                                hp = hp - 2
                        if enems[0] != -1:
                            targ = 0
                        if enems[1] != -1:
                            targ = 1
                        if enems[2] != -1:
                            targ = 2
                    elif enems[i] == 5:
                        pass
                    else:
                        if blocks > 0:
                            blocks = blocks - 1
                        else:
                            hp = hp - 1
            for i in range(3):
                if enems[i] == 5:
                    if enems[0] == -1:
                        enems[0] = 6
                        hpes[0] = 1
                    elif enems[1] == -1:
                        enems[1] = 6
                        hpes[1] = 1
                    elif enems[2] == -1:
                        enems[2] = 6
                        hpes[2] = 1

        if hp <= 0:
                    txt = nam + ' вышла из портала вся покрытая синяками и странной белой жидкостью. Боюсь даже представить, что с ней произошло. Как можно было ожидать, она отказалась говорить об этом. Будь осторожнее в следующий раз'
                    if gender == 1:
                        txt = nam + ' вышел из портала весь покрытый синяками и странной белой жидкостью. Боюсь даже представить, что с ним произошло. Как можно было ожидать, он отказался говорить об этом. Будь осторожнее в следующий раз'
                    cursor.execute("DELETE FROM dungeons WHERE id = "+str(idk))
                    bot.edit_message_media(media=telebot.types.InputMedia(media='AgACAgIAAx0CZQN7rQACwxZi8uNUoMtUGP6J96D7X-pveAGj3wAC374xGxy_mEsWdB1RBPi4nQEAAwIAA3MAAykE',caption=txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
                    time.sleep(1)

                    return
        if enems[0] == -1 and enems[1] == -1 and enems[2] == -1:
            txt = nam + '\n[ '
            i = 1
            while i <= maxhp:
                if i <= hp:
                    txt = txt + '🟩'
                else:
                    txt = txt + '🟥'
                i = i + 1
            txt = txt + ' ] '
            if blocks > 0:
                for i in range(blocks):
                    txt = txt + '🛡 '

            txt = txt + '\n\nТвоя некодевочка победила!'
            if gender == 1:
                txt = txt + '\n\nТвой некомальчик победил!'
            keyboard = types.InlineKeyboardMarkup(row_width=4)
            data = cursor.execute('SELECT * FROM dungeons WHERE id = ' + str(idk))
            data = data.fetchone()
            mas = unpack(data[1])
            generation = unpack(data[5])
            co = data[6]
            wh = data[7]
            mo = data[8]
            he = data[9]
            generation[next_y*10+next_x] = 0
            gd = pack(generation)
            cursor.execute("UPDATE dungeons SET generation = '" + str(gd) + "',hp = " + str(hp) + " WHERE id = " + str(idk))
            txt = txt + '\n\n' + 'Добыча:  ' + str(co) + '💰 ' + str(wh) + '🍫 ' + str(mo) + '⚡️ ' + str(he) + '🍼\n'+'Карта:\n'
            for a in range(0, 13):
             for b in range(0, 10):
                if mas[a*10+b] == 0:
                    txt = txt + '◼️'
                if mas[a*10+b] == 1:
                    txt = txt + '▫️'
                if mas[a*10+b] == 2:
                    txt = txt + '🟥'
                if mas[a*10+b] == 3:
                    txt = txt + '🟢'
                if mas[a*10+b] == 4:
                    txt = txt + '🟩'
                if mas[a*10+b] == 5:
                    txt = txt + '🟧'
             txt = txt + '\n'
            callback_button1 = types.InlineKeyboardButton(text = '⬆️',callback_data = 'move ' + str(idk) + ' 1 ')
            callback_button2 = types.InlineKeyboardButton(text = '⬅️',callback_data = 'move ' + str(idk) + ' 4 ')
            callback_button3 = types.InlineKeyboardButton(text = '⏺',callback_data = 'nothing')
            callback_button4 = types.InlineKeyboardButton(text = '➡️',callback_data = 'move ' + str(idk) + ' 2 ')
            callback_button5 = types.InlineKeyboardButton(text = '⬇️',callback_data = 'move ' + str(idk) + ' 3 ')
            callback_button6 = types.InlineKeyboardButton(text = 'Уйти 🔚',callback_data = 'back ' + str(idk))
            keyboard.add(callback_button1,callback_button5,callback_button2,callback_button4)
            keyboard.add(callback_button6)
            bot.edit_message_media(media=telebot.types.InputMedia(media='AgACAgIAAx0CZQN7rQACwsFi8ct1qI3M_i1Bt1Tk_WvAbq7BWAACqcQxG-SBkUvkDVBnBMaohgEAAwIAA3MAAykE',caption=txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
            time.sleep(1)

            return

        keyboard = types.InlineKeyboardMarkup(row_width=6)
        if targ == 0:
            target1 = types.InlineKeyboardButton(text = '[Цель выбрана]',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -4 ' + str(rer) + ' ' + str(targ) + ' ' + str(enems[0]) + ' ' + str(enems[1]) + ' ' + str(enems[2]) + ' ' + str(hpes[0]) + ' ' + str(hpes[1]) + ' ' + str(hpes[2]))
        else:
            target1 = types.InlineKeyboardButton(text = 'Цель 1 ⚔️',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -4 ' + str(rer) + ' ' + str(targ) + ' ' + str(enems[0]) + ' ' + str(enems[1]) + ' ' + str(enems[2]) + ' ' + str(hpes[0]) + ' ' + str(hpes[1]) + ' ' + str(hpes[2]))
        if targ == 1:
            target2 = types.InlineKeyboardButton(text = '[Цель выбрана]',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -5 ' + str(rer) + ' ' + str(targ) + ' ' + str(enems[0]) + ' ' + str(enems[1]) + ' ' + str(enems[2]) + ' ' + str(hpes[0]) + ' ' + str(hpes[1]) + ' ' + str(hpes[2]))
        else:
            target2 = types.InlineKeyboardButton(text = 'Цель 2 ⚔️',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -5 ' + str(rer) + ' ' + str(targ) + ' ' + str(enems[0]) + ' ' + str(enems[1]) + ' ' + str(enems[2]) + ' ' + str(hpes[0]) + ' ' + str(hpes[1]) + ' ' + str(hpes[2]))
        if targ == 2:
            target3 = types.InlineKeyboardButton(text = '[Цель выбрана]',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -6 ' + str(rer) + ' ' + str(targ) + ' ' + str(enems[0]) + ' ' + str(enems[1]) + ' ' + str(enems[2]) + ' ' + str(hpes[0]) + ' ' + str(hpes[1]) + ' ' + str(hpes[2]))
        else:
            target3 = types.InlineKeyboardButton(text = 'Цель 3 ⚔️',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -6 ' + str(rer) + ' ' + str(targ) + ' ' + str(enems[0]) + ' ' + str(enems[1]) + ' ' + str(enems[2]) + ' ' + str(hpes[0]) + ' ' + str(hpes[1]) + ' ' + str(hpes[2]))
        keyboard.add(target1,target2,target3)
        stack = []
        for i in range(36):
            callback_button = types.InlineKeyboardButton(text = sym[field[i]],callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' ' + str(i) + ' ' + str(rer) + ' ' + str(targ) + ' ' + str(enems[0]) + ' ' + str(enems[1]) + ' ' + str(enems[2]) + ' ' + str(hpes[0]) + ' ' + str(hpes[1]) + ' ' + str(hpes[2]))
            stack.append(callback_button)
            if len(stack) == 6:
                keyboard.add(stack[0],stack[1],stack[2],stack[3],stack[4],stack[5])
                stack = []
        if rer == 1:
            reroll = types.InlineKeyboardButton(text = '🔄 Перемешать',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -2 0 ' + str(targ) + ' ' + str(enems[0]) + ' ' + str(enems[1]) + ' ' + str(enems[2]) + ' ' + str(hpes[0]) + ' ' + str(hpes[1]) + ' ' + str(hpes[2]))
            keyboard.add(reroll)
           # deleter = types.InlineKeyboardButton(text = '💥 Разрушить фигуру',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -3 0 ' + str(targ) + ' ' + str(enems[0]) + ' ' + str(enems[1]) + ' ' + str(enems[2]) + ' ' + str(hpes[0]) + ' ' + str(hpes[1]) + ' ' + str(hpes[2]))
            #keyboard.add(deleter)
        md = pack(field)
        cursor.execute("UPDATE dungeons SET field = '" + str(md) + "',selected = -1,hp = " + str(hp) + " WHERE id = " + str(idk))

        txt = ''
        for j in range(3):
            if enems[j] != -1:
                txt = txt + enemies[enems[j]][0] + '\n[ '
                i = 1

                while i <= enemies[enems[j]][1]:
                    if (i <= hpes[j]):
                        txt = txt + '🟩'
                    else:
                        txt = txt + '🟥'
                    i = i + 1
                txt = txt + ' ]\n'
        txt = txt + '\n' + nam + '\n[ '
        i = 1
        while i <= maxhp:
            if i <= hp:
                txt = txt + '🟩'
            else:
                txt = txt + '🟥'
            i = i + 1
        txt = txt + ' ] '
        if blocks > 0:
            for i in range(blocks):
                txt = txt + '🛡 '
        txt = txt + '\n\n'
        im1 = Image.open('bot/back.png')
        if enems[0] != -1:
            im2 = Image.open('bot/enemy'+str(enems[0])+'.png')
            im1.paste(im2.convert('RGB'), (enemies[enems[0]][2]-233,enemies[enems[0]][3]), im2)
        if enems[1] != -1:
            im2 = Image.open('bot/enemy'+str(enems[1])+'.png')
            im1.paste(im2.convert('RGB'), (enemies[enems[1]][2],enemies[enems[1]][3]), im2)
        if enems[2] != -1:
            im2 = Image.open('bot/enemy'+str(enems[2])+'.png')
            im1.paste(im2.convert('RGB'), (enemies[enems[2]][2]+233,enemies[enems[2]][3]), im2)
        time.sleep(2)
        im1.save('bot/result.png')
        f = open("bot/result.png","rb")
        bot.edit_message_media(media=telebot.types.InputMedia(media=f,caption=txt + "Осталось ходов до атаки врага:  " + str(turns),type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
        f.close()

      elif "drop" in call.data:
        args = call.data.split()
        idk = int(args[1])



        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        time.sleep(0.25)
        answer_callback_query(call,'Успешно')
        data = cursor.execute('SELECT * FROM dungeons WHERE id = ' + str(idk))
        data = data.fetchone()
        mas = unpack(data[1])
        generation = unpack(data[5])
        co = data[6]
        wh = data[7]
        mo = data[8]
        he = data[9]
        next_x = data[12]
        next_y = data[13]
        hp = data[14]
        maxhp = data[15]
        d = random.randint(1,10)
        if d != 10:
            co = co - 2
            phot = 'AgACAgIAAx0CZQN7rQACwwRi8t920_InxPRHCFJRBhJHi609NAAC274xGxy_mEtJHCxhP9SvfQEAAwIAA3MAAykE'
            new_txt = 'Удивительно, но ничего не произошло. А на что ты вообще надеялся?'
        else:
            co = co - 2
            mo = mo + 1
            phot = 'AgACAgIAAx0CZQN7rQACwwJi8t1lkPUz0QvhDBUeUT7KBUQJgQAC2b4xGxy_mEtae5LvKUzKfgEAAwIAA3MAAykE'
            new_txt = 'Что ж, это можно назвать чудом. Вместо воды в фонтане начал течь розовый монстр ⚡️! Лучше будет взять с собой немного'
        generation[next_y*10+next_x] = 0
        gd = pack(generation)
        cursor.execute("UPDATE dungeons SET generation = '" + str(gd) + "',co = " + str(co) + ",wh = " + str(wh) + ",mo = " + str(mo) + ",he = " + str(he) + " WHERE id = " + str(idk))
        txt = new_txt + '\n\n' + 'Добыча:  ' + str(co) + '💰 ' + str(wh) + '🍫 ' + str(mo) + '⚡️ ' + str(he) + '🍼\n'+'Карта:\n'
        for a in range(0, 13):
            for b in range(0, 10):
                if mas[a*10+b] == 0:
                    txt = txt + '◼️'
                if mas[a*10+b] == 1:
                    txt = txt + '▫️'
                if mas[a*10+b] == 2:
                    txt = txt + '🟥'
                if mas[a*10+b] == 3:
                    txt = txt + '🟢'
                if mas[a*10+b] == 4:
                    txt = txt + '🟩'
                if mas[a*10+b] == 5:
                    txt = txt + '🟧'
            txt = txt + '\n'
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        callback_button1 = types.InlineKeyboardButton(text = '⬆️',callback_data = 'move ' + str(idk) + ' 1 ')
        callback_button2 = types.InlineKeyboardButton(text = '⬅️',callback_data = 'move ' + str(idk) + ' 4 ')
        callback_button3 = types.InlineKeyboardButton(text = '⏺',callback_data = 'nothing')
        callback_button4 = types.InlineKeyboardButton(text = '➡️',callback_data = 'move ' + str(idk) + ' 2 ')
        callback_button5 = types.InlineKeyboardButton(text = '⬇️',callback_data = 'move ' + str(idk) + ' 3 ')
        callback_button6 = types.InlineKeyboardButton(text = 'Уйти 🔚',callback_data = 'back ' + str(idk))
        keyboard.add(callback_button1,callback_button5,callback_button2,callback_button4)
        keyboard.add(callback_button6)
        bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo"),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

      elif "eat" in call.data:
        args = call.data.split()
        idk = int(args[1])

        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        time.sleep(0.25)
        answer_callback_query(call,'Успешно')
        data = cursor.execute('SELECT * FROM dungeons WHERE id = ' + str(idk))
        data = data.fetchone()
        mas = unpack(data[1])
        generation = unpack(data[5])
        co = data[6]
        wh = data[7]
        mo = data[8]
        he = data[9]
        next_x = data[12]
        next_y = data[13]
        hp = data[14]
        maxhp = data[15]
        try:
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
            data = data.fetchone()
            nam = str(data[1]).rstrip()
            gender = data[33]
        except:
            nam = 'Некодевочка'
            gender = 0
        hp = hp + 3
        if hp > maxhp:
            hp = maxhp
        phot = 'AgACAgIAAx0CZQN7rQACwgZi7aTwuv6M-OsOvCsRGijo6gohwwACZb8xG3RJaUufsVKea9BUKAEAAwIAA3MAAykE'
        new_txt = nam + ' поела немного пиццы и теперь чувствует себя заметно лучше!'
        if gender == 1:
            new_txt = nam + ' поел немного пиццы и теперь чувствует себя заметно лучше!'
        generation[next_y*10+next_x] = 0
        gd = pack(generation)
        cursor.execute("UPDATE dungeons SET generation = '" + str(gd) + "',co = " + str(co) + ",wh = " + str(wh) + ",mo = " + str(mo) + ",he = " + str(he) + ",hp = " + str(hp) + " WHERE id = " + str(idk))
        txt = new_txt + '\n\n' + 'Добыча:  ' + str(co) + '💰 ' + str(wh) + '🍫 ' + str(mo) + '⚡️ ' + str(he) + '🍼\n'+'Карта:\n'
        for a in range(0, 13):
            for b in range(0, 10):
                if mas[a*10+b] == 0:
                    txt = txt + '◼️'
                if mas[a*10+b] == 1:
                    txt = txt + '▫️'
                if mas[a*10+b] == 2:
                    txt = txt + '🟥'
                if mas[a*10+b] == 3:
                    txt = txt + '🟢'
                if mas[a*10+b] == 4:
                    txt = txt + '🟩'
                if mas[a*10+b] == 5:
                    txt = txt + '🟧'
            txt = txt + '\n'
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        callback_button1 = types.InlineKeyboardButton(text = '⬆️',callback_data = 'move ' + str(idk) + ' 1 ')
        callback_button2 = types.InlineKeyboardButton(text = '⬅️',callback_data = 'move ' + str(idk) + ' 4 ')
        callback_button3 = types.InlineKeyboardButton(text = '⏺',callback_data = 'nothing')
        callback_button4 = types.InlineKeyboardButton(text = '➡️',callback_data = 'move ' + str(idk) + ' 2 ')
        callback_button5 = types.InlineKeyboardButton(text = '⬇️',callback_data = 'move ' + str(idk) + ' 3 ')
        callback_button6 = types.InlineKeyboardButton(text = 'Уйти 🔚',callback_data = 'back ' + str(idk))
        keyboard.add(callback_button1,callback_button5,callback_button2,callback_button4)
        keyboard.add(callback_button6)
        bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo"),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

      elif "anti" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        time.sleep(0.25)
        answer_callback_query(call,'Успешно')
        data = cursor.execute('SELECT * FROM dungeons WHERE id = ' + str(idk))
        data = data.fetchone()
        mas = unpack(data[1])
        generation = unpack(data[5])
        co = data[6]
        wh = data[7]
        mo = data[8]
        he = data[9]
        next_x = data[12]
        next_y = data[13]
        try:
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
            data = data.fetchone()
            nam = str(data[1]).rstrip()
            rep = data[2]
            gender = data[33]
        except:
            nam = 'Некодевочка'
            rep = 0
            gender = 0
        d = random.randint(1,3)
        if d != 3:
            he = he + 1
            phot = 'AgACAgIAAx0CZQN7rQACwd1i7HKMaDbODOjA7IV5RYxI01bcTAACwMAxG3RJYUvRcTOFHbiG3QEAAwIAA3MAAykE'
            new_txt = nam + ' как можно быстрее набрала бутыль антипохмелина 🍼 и отошла от берега. К счастью, ничего опасного не произошло, но будет ли так и впредь?'
            if gender == 1:
                new_txt = nam + ' как можно быстрее набрал бутыль антипохмелина 🍼 и отошел от берега. К счастью, ничего опасного не произошло, но будет ли так и впредь?'
        else:
            phot = 'AgACAgIAAx0CZQN7rQACwfxi7Zem-ltmGFEQZvc-sg97JYwNewACTb8xG3RJaUs9wsxj9zofxwEAAwIAA3MAAykE'
            new_txt = 'Оказалось, что в озере живёт огромный тентаклевый монстр! К сожалению, все мы знаем, что делают тентаклевые монстры с маленькими некодевочками... ' + nam + ' стала доверять тебе меньше 💔, не стоило посылать её туда'
            if gender == 1:
                new_txt = 'Оказалось, что в озере живёт огромный тентаклевый монстр! К сожалению, все мы знаем, что делают тентаклевые монстры с маленькими некомальчиками... ' + nam + ' стал доверять тебе меньше 💔, не стоило посылать его туда'
            if rep != 0:
                rep = rep - 2
                cursor.execute("UPDATE neko SET rep = '" + str(rep) + "' WHERE id = " + str(idk))
        generation[next_y*10+next_x] = 0
        gd = pack(generation)
        cursor.execute("UPDATE dungeons SET generation = '" + str(gd) + "',co = " + str(co) + ",wh = " + str(wh) + ",mo = " + str(mo) + ",he = " + str(he) + " WHERE id = " + str(idk))
        txt = new_txt + '\n\n' + 'Добыча:  ' + str(co) + '💰 ' + str(wh) + '🍫 ' + str(mo) + '⚡️ ' + str(he) + '🍼\n'+'Карта:\n'
        for a in range(0, 13):
            for b in range(0, 10):
                if mas[a*10+b] == 0:
                    txt = txt + '◼️'
                if mas[a*10+b] == 1:
                    txt = txt + '▫️'
                if mas[a*10+b] == 2:
                    txt = txt + '🟥'
                if mas[a*10+b] == 3:
                    txt = txt + '🟢'
                if mas[a*10+b] == 4:
                    txt = txt + '🟩'
                if mas[a*10+b] == 5:
                    txt = txt + '🟧'
            txt = txt + '\n'
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        callback_button1 = types.InlineKeyboardButton(text = '⬆️',callback_data = 'move ' + str(idk) + ' 1 ')
        callback_button2 = types.InlineKeyboardButton(text = '⬅️',callback_data = 'move ' + str(idk) + ' 4 ')
        callback_button3 = types.InlineKeyboardButton(text = '⏺',callback_data = 'nothing')
        callback_button4 = types.InlineKeyboardButton(text = '➡️',callback_data = 'move ' + str(idk) + ' 2 ')
        callback_button5 = types.InlineKeyboardButton(text = '⬇️',callback_data = 'move ' + str(idk) + ' 3 ')
        callback_button6 = types.InlineKeyboardButton(text = 'Уйти 🔚',callback_data = 'back ' + str(idk))
        keyboard.add(callback_button1,callback_button5,callback_button2,callback_button4)
        keyboard.add(callback_button6)
        bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo"),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

      elif "move" in call.data:
        args = call.data.split()
        idk = int(args[1])
        d = int(args[2])


        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        time.sleep(0.25)
        data = cursor.execute('SELECT * FROM dungeons WHERE id = ' + str(idk))
        data = data.fetchone()
        mas = unpack(data[1])
        generation = unpack(data[5])
        co = data[6]
        wh = data[7]
        mo = data[8]
        he = data[9]
        cur_x = data[12]
        cur_y = data[13]
        hp = data[14]
        maxhp = data[15]
        if d == 1:
            if (cur_y-3) < 0 or mas[(cur_y-1)*10+cur_x] == 0:
                answer_callback_query(call,'Тупик')

                return
        if d == 2:
            if (cur_x+3) > 9 or mas[cur_y*10+cur_x+1] == 0:
                answer_callback_query(call,'Тупик')

                return
        if d == 3:
            if (cur_y+3) > 12 or mas[(cur_y+1)*10+cur_x] == 0:
                answer_callback_query(call,'Тупик')

                return
        if d == 4:
            if (cur_x-3) < 0 or mas[cur_y*10+cur_x-1] == 0:
                answer_callback_query(call,'Тупик')

                return
        mas[cur_y*10+cur_x] = 4
        if d == 1:
            next_x = cur_x
            next_y = cur_y-3
        if d == 2:
            next_x = cur_x+3
            next_y = cur_y
        if d == 3:
            next_x = cur_x
            next_y = cur_y+3
        if d == 4:
            next_x = cur_x-3
            next_y = cur_y
        mas[next_y*10+next_x] = 3
        if generation[cur_y*10+cur_x] != 0 and generation[cur_y*10+cur_x] != 1:
            mas[cur_y*10+cur_x] = 5
        next_gen = generation[next_y*10+next_x]
        try:
            data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
            data = data.fetchone()
            nam = str(data[1]).rstrip()
            rep = data[2]
            gender = data[33]
        except:
            nam = 'Некодевочка'
            rep = 0
            gender = 0
        phot = 'AgACAgIAAx0CZQN7rQACsTdi5aOWZGH8r_RsZ4ZDXbGXHwZZxwACz8AxG2fEKUv9PoikvhKaVgEAAwIAA3MAAykE'
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        answer_callback_query(call,'Успешно')
        time.sleep(2)
        if next_gen == 1:
            phot = 'AgACAgIAAx0CZQN7rQACwxZi8uNUoMtUGP6J96D7X-pveAGj3wAC374xGxy_mEsWdB1RBPi4nQEAAwIAA3MAAykE'
            new_txt = 'К счастью, портал никуда не делся. Может быть, самое время вернуться? Не думаю, что твоей некодевочки ещё надолго хватит'
            if gender == 1:
                new_txt = 'К счастью, портал никуда не делся. Может быть, самое время вернуться? Не думаю, что твоего некомальчика ещё надолго хватит'
        elif next_gen == 2:
            wh = wh + 1
            generation[next_y*10+next_x] = 0
            phot = 'AgACAgIAAx0CZQN7rQACwvRi8tr6ixHXhD5-CLOdFikGnPqDcgACzb4xGxy_mEvGxDZ1JQABuSIBAAMCAANzAAMpBA'
            new_txt = nam + ' обратила внимание на странную коробку, лежавшую в углу. Похоже, это часть припасов пропавшей экспедиции. Только вот где всё остальное? Внутри лежало несколько пустых бутылок водки и совсем немного вискаса 🍫'
            if gender == 1:
                new_txt = nam + ' обратил внимание на странную коробку, лежавшую в углу. Похоже, это часть припасов пропавшей экспедиции. Только вот где всё остальное? Внутри лежало несколько пустых бутылок водки и совсем немного вискаса 🍫'
        elif next_gen == 3:
            co = co + 15
            generation[next_y*10+next_x] = 0
            phot = 'AgACAgIAAx0CZQN7rQACwvhi8tv5UTGRY0Ly30leGF-iVeph4AAC074xGxy_mEtCwi5QjU5PowEAAwIAA3MAAykE'
            new_txt = 'Странный кристалл, переливающийся всеми цветами радуги, преградил вам путь. К счастью, весит он не так много, как могло показаться с первого взгляда. Похоже, его можно хорошо продать 💰, если, конечно, удастся вынести'
        elif next_gen == 4:
            callback_button0 = types.InlineKeyboardButton(text = 'Бросить монетку 💸',callback_data = 'drop ' + str(idk))
            keyboard.add(callback_button0)
            phot = 'AgACAgIAAx0CZQN7rQACwwRi8t920_InxPRHCFJRBhJHi609NAAC274xGxy_mEtJHCxhP9SvfQEAAwIAA3MAAykE'
            new_txt = 'Весьма изысканный фонтан стоял посреди небольшого озера. Кто и зачем его сюда поставил? Как бы то ни было, ' + nam + ' не увидела ничего подозрительного и предложила кинуть туда монетку'
            if gender == 1:
                new_txt = 'Весьма изысканный фонтан стоял посреди небольшого озера. Кто и зачем его сюда поставил? Как бы то ни было, ' + nam + ' не увидел ничего подозрительного и предложил кинуть туда монетку'
        elif next_gen == 5:
            callback_button0 = types.InlineKeyboardButton(text = 'Набрать а-похмелина 🍼',callback_data = 'anti ' + str(idk))
            keyboard.add(callback_button0)
            phot = 'AgACAgIAAx0CZQN7rQACwd1i7HKMaDbODOjA7IV5RYxI01bcTAACwMAxG3RJYUvRcTOFHbiG3QEAAwIAA3MAAykE'
            new_txt = 'Не может быть, да это же целое озеро антипохмелина! На протяжении многих веков эта жидкость использовалась от похмелья, и лишь недавние исследования показали, что она лечит остальные болезни тоже. К сожалению, рецепт антипохмелина был безвозвратно утерян. Нельзя упускать возможность взять с собой немного'
        elif next_gen == 6:
            callback_button0 = types.InlineKeyboardButton(text = 'Съесть пиццу 🍕',callback_data = 'eat ' + str(idk))
            keyboard.add(callback_button0)
            phot = 'AgACAgIAAx0CZQN7rQACwwABYvLc79baJMP4YDV4iM_6n0U1Y0kAAte-MRscv5hL2-WMSvjaptEBAAMCAANzAAMpBA'
            new_txt = 'Вам повезло, вы нашли несколько кустов пиццы. Найти дикорастущую пиццу - большая удача в нашем мире, но не здесь. ' + nam + ' может съесть плоды и восстановить свои силы, конечно, если ты ей разрешишь'
            if gender == 1:
                new_txt = 'Вам повезло, вы нашли несколько кустов пиццы. Найти дикорастущую пиццу - большая удача в нашем мире, но не здесь. ' + nam + ' может съесть плоды и восстановить свои силы, конечно, если ты ему разрешишь'
        elif next_gen == 7:
            phot = 'AgACAgIAAx0CZQN7rQACwvZi8tuNp4bk85D-ypnCu5OUalrZwwAC0L4xGxy_mEvzEzdkcbipPgEAAwIAA3MAAykE'
            generation[next_y*10+next_x] = 0
            letters = ['<b>"День 1. LGBT мир находится под землёй на глубине примерно 50 км, и официальной целью нашей экспедиции является поиск залежей антипохмелина, обнаруженных при последнем геосканировании. Однако, наша настоящая цель - доказать существование LGBTQ+ мира"</b>',
            '<b>"День 2. Размеры этой сети пещер и запутанность её тоннелей действительно удивляют. Мы в пути уже целый день, однако, снова и снова каким-то образом возвращаемся обратно к порталу! К счастью, кто-то додумался начать рисовать карту"</b>',
            '<b>"День 3. Наши припасы стремительно заканчиваются. Возможно, не стоило брать водки больше, чем еды. К тому же, заканчивается топливо для огнемётов, которыми мы отбиваемся от полчищ фурри. Надеюсь, скоро я смогу вернуться домой"</b>',
            '<b>"День 4. Мы нашли целое озеро антипохмелина! Никто не верил в то, что где-то ещё осталась хотя бы капля, но вот же он! Что ж, самое время выпить оставшиеся запасы водки - разве не для этого и нужен антипохмелин?"</b>',
            '<b>"День 5. Остались только я и Лёха... Мы бухали на берегу, пока остальные пошли купаться в озере. Это звучит невообразимо, но спустя пару минут на моих глазах их всех мгновенно что-то утащило под воду. Я сразу же поплыл чтобы помочь им, но никого не нашёл..."</b>']
            let = random.choice(letters)
            new_txt = 'Похоже, здесь экспедиция остановилась для привала, но было это очень давно. Среди пустых упаковок вискаса и прочего мусора ' + nam + ' нашла пожелтевший клочок бумаги. Видимо, это отрывок из журнала экспедиции:\n' + let
            if gender == 1:
                new_txt = 'Похоже, здесь экспедиция остановилась для привала, но было это очень давно. Среди пустых упаковок вискаса и прочего мусора ' + nam + ' нашел пожелтевший клочок бумаги. Видимо, это отрывок из журнала экспедиции:\n' + let
        elif next_gen == 8:

            md = pack(mas)
            gd = pack(generation)
            cursor.execute("UPDATE dungeons SET map = '" + str(md) + "',generation = '" + str(gd) + "',cur_x = " + str(next_x) + ",cur_y = " + str(next_y) + " WHERE id = " + str(idk))

            c = random.randint(0,2)
            if c == 0:
                enemy1 = -1
                enemy2 = 0
                enemy3 = 1
                hpe1 = 0
                hpe2 = 3
                hpe3 = 2
            if c == 1:
                enemy1 = -1
                enemy2 = 3
                enemy3 = -1
                hpe1 = 0
                hpe2 = 3
                hpe3 = 0
            if c == 2:
                enemy1 = -1
                enemy2 = 5
                enemy3 = -1
                hpe1 = 0
                hpe2 = 3
                hpe3 = 0

            im1 = Image.open('bot/back.png')
            if enemy1 != -1:
                im2 = Image.open('bot/enemy'+str(enemy1)+'.png')
                im1.paste(im2.convert('RGB'), (90,130), im2)
            if enemy2 != -1:
                im2 = Image.open('bot/enemy'+str(enemy2)+'.png')
                im1.paste(im2.convert('RGB'), (300,130), im2)
            if enemy3 != -1:
                im2 = Image.open('bot/enemy'+str(enemy3)+'.png')
                im1.paste(im2.convert('RGB'), (530,130), im2)
            im1.save('bot/result.png')
            f = open("bot/result.png","rb")
            new_txt = 'Тишину оборвал звук быстро приближающихся шагов. Кто бы это ни был, идёт он явно не с добрыми намерениями. Похоже, боя не избежать\n\nБой начнётся через 15 секунд, собирай символы по 4 в ряд чтобы поддерживать некодевочку\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
            if gender == 1:
                new_txt = 'Тишину оборвал звук быстро приближающихся шагов. Кто бы это ни был, идёт он явно не с добрыми намерениями. Похоже, боя не избежать\n\nБой начнётся через 15 секунд, собирай символы по 4 в ряд чтобы поддерживать некомальчика\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
            mdk = bot.edit_message_media(media=telebot.types.InputMedia(media='AgACAgIAAx0CZQN7rQACwsFi8ct1qI3M_i1Bt1Tk_WvAbq7BWAACqcQxG-SBkUvkDVBnBMaohgEAAwIAA3MAAykE',caption=new_txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
            field = []
            sym = ['🟥','🟧','🟡','🟢','💙']
            for i in range(36):
                s = random.randint(0,4)
                field.append(s)
            while True:
             found = False
             for j in range(6):
              for i in range(3):
                if field[j*6+i] != -1 and field[j*6+i] == field[j*6+i+1] and field[j*6+i+1] == field[j*6+i+2] and field[j*6+i+2] == field[j*6+i+3]:
                    field[j*6+i] = -1
                    field[j*6+i+1] = -1
                    field[j*6+i+2] = -1
                    field[j*6+i+3] = -1
                    found = True
             for j in range(3):
              for i in range(6):
                if field[j*6+i] != -1 and field[j*6+i] == field[(j+1)*6+i] and field[(j+1)*6+i] == field[(j+2)*6+i] and field[(j+2)*6+i] == field[(j+3)*6+i]:
                    field[j*6+i] = -1
                    field[(j+1)*6+i] = -1
                    field[(j+2)*6+i] = -1
                    field[(j+3)*6+i] = -1
                    found = True
             if found == False:
                break
             while True:
                f = False
                for i in range(36):
                    if field[i] == -1:
                        f = True
                        if i < 6:
                            field[i] = random.randint(0,4)
                        else:
                            field[i] = field[i-6]
                            field[i-6] = -1
                if f == False:
                    break
            blocks = 0
            turns = 2
            targ = 1
            keyboard = types.InlineKeyboardMarkup(row_width=6)
            target1 = types.InlineKeyboardButton(text = 'Цель 1 ⚔️',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -4 1 ' + str(targ) + ' ' + str(enemy1) + ' ' + str(enemy2) + ' ' + str(enemy3) + ' ' + str(hpe1) + ' ' + str(hpe2) + ' ' + str(hpe3))
            target2 = types.InlineKeyboardButton(text = '[Цель выбрана]',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -5 1 ' + str(targ) + ' ' + str(enemy1) + ' ' + str(enemy2) + ' ' + str(enemy3) + ' ' + str(hpe1) + ' ' + str(hpe2) + ' ' + str(hpe3))
            target3 = types.InlineKeyboardButton(text = 'Цель 3 ⚔️',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -6 1 ' + str(targ) + ' ' + str(enemy1) + ' ' + str(enemy2) + ' ' + str(enemy3) + ' ' + str(hpe1) + ' ' + str(hpe2) + ' ' + str(hpe3))
            keyboard.add(target1,target2,target3)
            stack = []

            for i in range(36):
                callback_button = types.InlineKeyboardButton(text = sym[field[i]],callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' ' + str(i) + ' 1 ' + str(targ) + ' ' + str(enemy1) + ' ' + str(enemy2) + ' ' + str(enemy3) + ' ' + str(hpe1) + ' ' + str(hpe2) + ' ' + str(hpe3))
                stack.append(callback_button)
                if len(stack) == 6:
                    keyboard.add(stack[0],stack[1],stack[2],stack[3],stack[4],stack[5])
                    stack = []
            reroll = types.InlineKeyboardButton(text = '🔄 Перемешать',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -2 0 ' + str(targ) + ' ' + str(enemy1) + ' ' + str(enemy2) + ' ' + str(enemy3) + ' ' + str(hpe1) + ' ' + str(hpe2) + ' ' + str(hpe3))
            keyboard.add(reroll)
            #deleter = types.InlineKeyboardButton(text = '💥 Разрушить фигуру',callback_data = 'pve ' + str(idk) + ' ' + str(turns) + ' ' + str(blocks) + ' -3 0 ' + str(targ) + ' ' + str(enemy1) + ' ' + str(enemy2) + ' ' + str(enemy3) + ' ' + str(hpe1) + ' ' + str(hpe2) + ' ' + str(hpe3))
            #keyboard.add(deleter)
            md = pack(field)
            cursor.execute("UPDATE dungeons SET field = '" + str(md) + "',selected = -1 WHERE id = " + str(idk))
            txt = ''
            if enemy1 != -1:
                txt = txt + enemies[enemy1][0] + '\n[ '
                i = 1

                while i <= enemies[enemy1][1]:
                    if (i <= hpe1):
                        txt = txt + '🟩'
                    else:
                        txt = txt + '🟥'
                    i = i + 1
                txt = txt + ' ]\n'
            if enemy2 != -1:
                txt = txt + enemies[enemy2][0] + '\n[ '
                i = 1

                while i <= enemies[enemy2][1]:
                    if (i <= hpe2):
                        txt = txt + '🟩'
                    else:
                        txt = txt + '🟥'
                    i = i + 1
                txt = txt + ' ]\n'
            if enemy3 != -1:
                txt = txt + enemies[enemy3][0] + '\n[ '
                i = 1

                while i <= enemies[enemy3][1]:
                    if (i <= hpe3):
                        txt = txt + '🟩'
                    else:
                        txt = txt + '🟥'
                    i = i + 1
                txt = txt + ' ]\n'
            txt = txt + '\n'  + nam + '\n[ '
            i = 1
            while i <= maxhp:
                if i <= hp:
                    txt = txt + '🟩'
                else:
                    txt = txt + '🟥'
                i = i + 1
            txt = txt + ' ]\n\n'
            time.sleep(15)
            im1 = Image.open('bot/back.png')
            enems = [enemy1,enemy2,enemy3]
            if enems[0] != -1:
                im2 = Image.open('bot/enemy'+str(enems[0])+'.png')
                im1.paste(im2.convert('RGB'), (enemies[enems[0]][2]-233,enemies[enems[0]][3]), im2)
            if enems[1] != -1:
                im2 = Image.open('bot/enemy'+str(enems[1])+'.png')
                im1.paste(im2.convert('RGB'), (enemies[enems[1]][2],enemies[enems[1]][3]), im2)
            if enems[2] != -1:
                im2 = Image.open('bot/enemy'+str(enems[2])+'.png')
                im1.paste(im2.convert('RGB'), (enemies[enems[2]][2]+233,enemies[enems[2]][3]), im2)
            im1.save('bot/result.png')
            f = open("bot/result.png","rb")
            bot.edit_message_media(media=telebot.types.InputMedia(media=f,caption=txt + "Осталось ходов до атаки врага:  " + str(turns),type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)

            f.close()
            return
        else:
            phot = 'AgACAgIAAx0CZQN7rQACsTdi5aOWZGH8r_RsZ4ZDXbGXHwZZxwACz8AxG2fEKUv9PoikvhKaVgEAAwIAA3MAAykE'
            new_txt = 'Масштабы этих пещер действительно удивляют, а их красота завораживает. Здесь же нет абсолютно ничего примечательного, а тишину лишь изредка нарушает падение капель воды'
        md = pack(mas)
        gd = pack(generation)
        cursor.execute("UPDATE dungeons SET map = '" + str(md) + "',generation = '" + str(gd) + "',co = " + str(co) + ",wh = " + str(wh) + ",mo = " + str(mo) + ",he = " + str(he) + ",cur_x = " + str(next_x) + ",cur_y = " + str(next_y) + " WHERE id = " + str(idk))
        txt = new_txt + '\n\n' + 'Добыча:  ' + str(co) + '💰 ' + str(wh) + '🍫 ' + str(mo) + '⚡️ ' + str(he) + '🍼\n'+'Карта:\n'
        for a in range(0, 13):
            for b in range(0, 10):
                if mas[a*10+b] == 0:
                    txt = txt + '◼️'
                if mas[a*10+b] == 1:
                    txt = txt + '▫️'
                if mas[a*10+b] == 2:
                    txt = txt + '🟥'
                if mas[a*10+b] == 3:
                    txt = txt + '🟢'
                if mas[a*10+b] == 4:
                    txt = txt + '🟩'
                if mas[a*10+b] == 5:
                    txt = txt + '🟧'
            txt = txt + '\n'
        callback_button1 = types.InlineKeyboardButton(text = '⬆️',callback_data = 'move ' + str(idk) + ' 1')
        callback_button2 = types.InlineKeyboardButton(text = '⬅️',callback_data = 'move ' + str(idk) + ' 4')
        callback_button3 = types.InlineKeyboardButton(text = '⏺',callback_data = 'nothing')
        callback_button4 = types.InlineKeyboardButton(text = '➡️',callback_data = 'move ' + str(idk) + ' 2')
        callback_button5 = types.InlineKeyboardButton(text = '⬇️',callback_data = 'move ' + str(idk) + ' 3')
        callback_button6 = types.InlineKeyboardButton(text = 'Уйти 🔚',callback_data = 'back ' + str(idk))
        keyboard.add(callback_button1,callback_button5,callback_button2,callback_button4)
        keyboard.add(callback_button6)
        bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

      elif "back" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        answer_callback_query(call,'Успешно')
        time.sleep(0.25)
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        coins = data[11]
        buff = data[12]
        monsters = data[20]
        heal = data[21]
        gender = data[33]
        baza = data[8]
        data = cursor.execute('SELECT * FROM dungeons WHERE id = '+str(idk))
        data = data.fetchone()
        co = data[6]
        wh = data[7]
        mo = data[8]
        he = data[9]
        coins = coins + co
        buff = buff + wh
        if wh != 0 and baza >= 6:
            buff = buff + 1
        monsters = monsters + mo
        heal = heal + he
        cursor.execute("UPDATE neko SET coins = "+ str(coins) +",buff = "+str(buff)+",monsters = "+str(monsters)+",heal = "+str(heal)+" WHERE id = " + str(idk))
        cursor.execute("DELETE FROM dungeons WHERE id = "+str(idk))


        txt = 'Твоя некодевочка вернулась обратно и принесла всё, что нашла в этом загадочном мире. Может стоит наградить её вискасом?'
        if gender == 1:
            txt = 'Твой некомальчик вернулась обратно и принёс всё, что нашёл в этом загадочном мире. Может стоит наградить его вискасом?'
        bot.edit_message_media(media=telebot.types.InputMedia(media='AgACAgIAAx0CZQN7rQACwxZi8uNUoMtUGP6J96D7X-pveAGj3wAC374xGxy_mEsWdB1RBPi4nQEAAwIAA3MAAykE',caption=txt,type="photo"),chat_id=call.message.chat.id, message_id=call.message.message_id)

      elif "nothing" in call.data:
        answer_callback_query(call,'Эта кнопка для красоты')

      elif "get" in call.data:
        args = call.data.split()
        idk = int(args[1])
        gndr = int(args[2])
        cs = int(args[3])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')

            return
        answer_callback_query(call,'Успешно')
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        callback_button1 = types.InlineKeyboardButton(text = 'ТОЧНО БЛЯТЬ ВЗЯТЬ? ✅',callback_data = 'fuck ' + str(idk) + ' ' + str(gndr))
        keyboard.add(callback_button1)
        if cs == 0:
            callback_button2 = types.InlineKeyboardButton(text = 'Не брать ❌',callback_data = 'dont ' + str(idk))
        else:
            callback_button2 = types.InlineKeyboardButton(text = 'Взять 50 некогривен 💰',callback_data = 'money ' + str(idk))
        keyboard.add(callback_button2)
        bot.edit_message_media(media=telebot.types.InputMedia(media=call.message.photo[0].file_id,type="photo"),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
        time.sleep(1)

      elif "wear" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')

            return

        answer_callback_query(call,'Успешно')
        photka = call.message.photo[0].file_id
        cursor.execute("UPDATE neko SET gifka = 'Nothing',new_phot = '"+photka+"' WHERE id = "+ str(idk))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        time.sleep(1)

      elif "fuck" in call.data:
        args = call.data.split()
        idk = int(args[1])
        gndr = int(args[2])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')

            return

        answer_callback_query(call,'Успешно')
        nam = str(data[1]).rstrip()
        baza = data[8]
        gender = data[33]
        if gndr == 0:
            text = 'Поздравляю, это твоя новая некодевочка! Старую мы сами выкинем в ближайшую канаву, тебе не нужно об этом беспокоиться ☠️'
            if gender == 1:
                text = 'Поздравляю, это твоя новая некодевочка! Старого некомальчика мы сами выкинем в ближайшую канаву, тебе не нужно об этом беспокоиться ☠️'
        else:
            text = 'Поздравляю, это твой новый некомальчик! Старую некодевочку мы сами выкинем в ближайшую канаву, тебе не нужно об этом беспокоиться ☠️'
            if gender == 1:
                text = 'Поздравляю, это твой новый некомальчик! Старого мы сами выкинем в ближайшую канаву, тебе не нужно об этом беспокоиться ☠️'
        bot.send_message(call.message.chat.id,text)
        photka = call.message.photo[0].file_id
        if nam == 'Некодевочка' or nam == 'Некомальчик':
            cursor.execute("INSERT INTO dead (name,time) VALUES ('Безымянная могила',"+str(int(time.time())) +")")
        else:
            cursor.execute("INSERT INTO dead (name,time) VALUES ('"+nam+"',"+str(int(time.time())) +")")
        if gndr == 0:
            newnam = 'Некодевочка'
        else:
            newnam = 'Некомальчик'
        kormit = time.time()
        gulat = time.time()
        cursor.execute("UPDATE neko SET new_phot = 'None', gender = " + str(gndr) + ", name = '" + newnam + "', gifka = 'Nothing', gulat = " + str(gulat) + ",kormit = " + str(kormit) + ", gladit = 0, licension = 0, photo = '"+photka+"' WHERE id = "+ str(idk))
        if baza >= 2:
            if gndr == 0:
                text = 'Новой некодевочке, cудя по всему, понравилась твоя база'
            else:
                text = 'Новому некомальчику, cудя по всему, понравилась твоя база'
            bot.send_message(call.message.chat.id, text)
            bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAEFM5VixNUnaSAzda2fwcrxHsDUdA-caAACJw8AAmVYWEj9O0ji0K4xiikE')
        else:
            cursor.execute("UPDATE neko SET rep = 0 WHERE id = "+ str(idk))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        time.sleep(1)

      elif "dont" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')

            return
        answer_callback_query(call,'Успешно')
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        time.sleep(1)

      elif "skill" in call.data:
        args = call.data.split()
        idk = int(args[1])
        turn = int(args[2])
        sk = int(args[3])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')
            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        skill1 = data[30]
        skill2 = data[31]
        if turn == 1:
            cursor.execute("UPDATE neko SET skill_one = " + str(sk) + " WHERE id = "+ str(idk))
            skill1 = sk
        else:
            cursor.execute("UPDATE neko SET skill_two = " + str(sk) + " WHERE id = "+ str(idk))
            skill2 = sk
        if skill1 > 100:
            sktxt1 = active_skill_list[skill1-100]
        else:
            sktxt1 = passive_skill_list[skill1]
        if skill2 > 100:
            sktxt2 = active_skill_list[skill2-100]
        else:
            sktxt2 = passive_skill_list[skill2]

        answer_callback_query(call,'Успешно')
        time.sleep(2)
        txt = 'Навыки изменены:\n\n' + sktxt1 + '\n' + sktxt2
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text = txt,parse_mode='HTML')



      elif "item" in call.data:
        args = call.data.split()
        idk = int(args[1])
        turn = int(args[2])
        it = int(args[3])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')

            return

        answer_callback_query(call,'Успешно')
        if turn == 1:
            cursor.execute("UPDATE neko SET new_phot = 'None', item_one = " + str(it) + " WHERE id = "+ str(idk))
        else:
            cursor.execute("UPDATE neko SET new_phot = 'None', item_two = " + str(it) + " WHERE id = "+ str(idk))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        time.sleep(1)

      elif "money" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')

            return
        answer_callback_query(call,'Успешно')
        coins = data[11]
        bot.send_message(call.message.chat.id,'Деньги отправлены почтовым голубем')
        bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
        coins = coins + 50
        cursor.execute("UPDATE neko SET coins = " + str(coins) + " WHERE id = "+ str(idk))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        time.sleep(1)

      elif "pend" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')
            return
        answer_callback_query(call,'Успешно')
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        cursor.execute("DELETE FROM poker WHERE id = "+str(idk))

      elif "pjoin" in call.data:
        args = call.data.split()
        idk = int(args[1])
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(call.from_user.id))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        bolnitsa = int(data[6] - time.time())
        coins = data[11]
        event = data[10]
        if coins < 20:
            answer_callback_query(call,'А деньги где')
            return
        if bolnitsa > 0:
            answer_callback_query(call,'Ты в больнице')
            return
        if event > 0:
            answer_callback_query(call,'Ты гуляешь')
            return
        if check_poker(call.from_user.id):
            answer_callback_query(call,'Ты уже присоединился')
            return
        data = cursor.execute('SELECT * FROM poker WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        event = data[2]
        players = unpack(data[7])
        bank = unpack(data[8])
        names = unpack(data[9])
        money = unpack(data[10])
        if len(players) == 6:
            answer_callback_query(call,'Максимум игроков')
            return
        answer_callback_query(call,'Успешно')
        players.append(call.from_user.id)
        bank.append(5)
        names.append(call.from_user.first_name)
        money.append(coins)
        pd = pack(players)
        bd = pack(bank)
        nd = pack(names)
        md = pack(money)
        cursor.execute("UPDATE poker SET players = '" + str(pd) + "',bank = '" + str(bd) + "',names = '" + str(nd) + "',money = '" + str(md) + "' WHERE id = " + str(idk))
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        callback_button1 = types.InlineKeyboardButton(text = 'Присоединиться ➕',callback_data = 'pjoin ' + str(idk))
        callback_button2 = types.InlineKeyboardButton(text = 'Старт ✅',callback_data = 'pstart ' + str(idk))
        callback_button3 = types.InlineKeyboardButton(text = 'Отмена ❌',callback_data = 'pend ' + str(idk))
        keyboard.add(callback_button1)
        keyboard.add(callback_button2,callback_button3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text = 'Идёт набор в покер, кто не отзовётся тот лох\nВход от 20 некогривен 💰\n'+str(len(players))+' из 2 игроков',parse_mode='HTML',reply_markup=keyboard)

      elif "pstart" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')
            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        bolnitsa = int(data[6] - time.time())
        coins = data[11]
        event = data[10]
        if coins < 20:
            answer_callback_query(call,'А деньги где')
            return
        if bolnitsa > 0:
            answer_callback_query(call,'Ты в больнице')
            return
        if event > 0:
            answer_callback_query(call,'Ты гуляешь')
            return
        data = cursor.execute('SELECT * FROM poker WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        event = data[2]
        players = unpack(data[7])
        bank = unpack(data[8])
        names = unpack(data[9])
        money = unpack(data[10])
        if len(players) < 2:
            answer_callback_query(call,'Недостаточно игроков')
            return
        if event != -1:
            answer_callback_query(call,'Пашол нахуй')
            return
        answer_callback_query(call,'Успешно')
        deck = [2.1,3.1,4.1,5.1,6.1,7.1,8.1,9.1,10.1,11.1,12.1,13.1,14.1,2.2,3.2,4.2,5.2,6.2,7.2,8.2,9.2,10.2,11.2,12.2,13.2,14.2,2.3,3.3,4.3,5.3,6.3,7.3,8.3,9.3,10.3,11.3,12.3,13.3,14.3,2.4,3.4,4.4,5.4,6.4,7.4,8.4,9.4,10.4,11.4,12.4,13.4,14.4]
        cards = []
        hand = []
        for i in range(5):
            d = random.choice(deck)
            deck.remove(d)
            cards.append(d)
        for j in range(len(players)):
            for i in range(2):
                d = random.choice(deck)
                deck.remove(d)
                hand.append(d)
        turn = players[0]
        pos = 0
        r = 1
        txt = ''
        for i in range(len(players)):
            txt = txt + names[i] + '  ' + str(bank[i]) + '💰\n'
        txt = txt + '\nХод <a href="tg://user?id='+str(turn)+'">'+str(names[pos])+'</a>',

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        m = 5
        callback_button1 = types.InlineKeyboardButton(text = '🆗 Пропуск',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 1 ' + str(r))
        callback_button2 = types.InlineKeyboardButton(text = '❌ Сдаться',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 2 ' + str(r))
        callback_button4 = types.InlineKeyboardButton(text = '🔼 Ставка ('+str(m)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 3 ' + str(r) + ' ' + str(m))
        callback_button5 = types.InlineKeyboardButton(text = '⏫ Ставка ('+str(2*m)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 4 ' + str(r) + ' ' + str(2*m))
        callback_button3 = types.InlineKeyboardButton(text = 'Мои карты',callback_data = 'hand ' + str(idk) + ' ' + str(turn) + ' ' + str(pos))
        keyboard.add(callback_button1,callback_button2)
        keyboard.add(callback_button4,callback_button5)
        keyboard.add(callback_button3)
        f = poker_image(cards,-1)
        m = bot.send_photo(call.message.chat.id, photo=f,caption = txt,reply_markup=keyboard,parse_mode='HTML')
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        cd = pack(cards)
        hd = pack(hand)
        wait = int(time.time() + 600)
        cursor.execute("UPDATE poker SET cards = '" + str(cd) + "',hand = '" + str(hd) + "',event = 2, wait = " + str(wait) + ", message = " + str(m.id) + " WHERE id = " + str(idk))

      elif 'poker' in call.data:
        args = call.data.split()
        idk = int(args[1])
        turn = int(args[2])
        pos = int(args[3])
        action = int(args[4])
        r = int(args[5])
        if call.from_user.id != turn:
            answer_callback_query(call,'Не твой ход')
            return
        data = cursor.execute('SELECT * FROM poker WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        answer_callback_query(call,'Успешно')
        cards = unpack(data[1])
        event = data[2]
        hand = unpack(data[6])
        players = unpack(data[7])
        bank = unpack(data[8])

        names = unpack(data[9])
        money = unpack(data[10])
        dead = unpack(data[11])
        vabank = unpack(data[12])
        end = False
        if action == 1:
            act_txt = names[pos] + ' зассал и пропустил ход\n\n'
        elif action == 2:
            act_txt = names[pos] + ' слился, ну и хуй с ним\n\n'
            names[pos] = '☠️☠️☠️'
            dead.append(turn)
            dd = pack(dead)
            nd = pack(names)
            cursor.execute("UPDATE poker SET dead = '" + str(dd) + "',names = '" + str(nd) + "' WHERE id = " + str(idk))
        elif action == 3 or action == 4:
            act_txt = names[pos] + ' не зассал и сделал ставку\n\n'
            m = int(args[6])
            bank[pos] = bank[pos] + m
            if bank[pos] >= money[pos]:
                vabank.append(turn)
                act_txt = names[pos] + ' ставит душу своей матери\n\n'
            vd = pack(vabank)
            bd = pack(bank)
            cursor.execute("UPDATE poker SET vabank = '" + str(vd) + "', bank = '" + str(bd) + "' WHERE id = " + str(idk))
        #уравнивание банка для расчетов
        true_bank = bank.copy()
        for i in range(len(bank)):
            if players[i] in dead:
                bank[i] = max(bank)
            if players[i] in vabank:
                bank[i] = max(bank)
        balance = max(bank) == min(bank)
        #условия конца игры
        if len(dead) == len(players) - 1:
            end = True
        if len(vabank) >= len(players) - len(dead) - 1 and balance:
            end = True
        #смена ходящего игрока
        if r == 1:
            pos = pos + 1
            while pos != len(players) and (players[pos] in dead or players[pos] in vabank):
                pos = pos + 1
        #новая стадия или конец
        if (r == 1 and pos == len(players) and balance) or (r == 2 and balance) or end == True:
            if end == True:
                event = 5
            pos = 0
            r = 1
            while pos != len(players) and (players[pos] in dead or players[pos] in vabank):
                pos = pos + 1
            f = poker_image(cards,event)
            event = event + 1
            if event == 6:
                #ПРОСЧЕТ КОМБИНАЦИЙ
                combinations = ['Старшая карта','Пара','Две пары','Сет','Стрит','Флеш','Фулл хаус','Каре','Стрит флеш','Флеш рояль']
                colors = ['♦️','♥️','♠️','♣️']
                numbers = ['J','Q','K','A']
                player_combs = []
                for j in range(len(players)):
                    crd = cards.copy()
                    crd.append(hand[j*2])
                    crd.append(hand[j*2+1])
                    player_combs.append(combinator(crd))
                #ГЕНЕРАЦИЯ ТЕКСТА
                txt = act_txt
                for i in range(len(players)):
                    hd = [hand[i*2],hand[i*2+1]]
                    txt = txt + names[i] + '  ' + str(true_bank[i]) + '💰\n'
                    a = round(hd[0])
                    b = round((hd[0]%1)*10)
                    if a > 10:
                        a = numbers[a-11]
                    txt = txt + colors[b-1] + str(a) + '   '
                    a = round(hd[1])
                    b = round((hd[1]%1)*10)
                    if a > 10:
                        a = numbers[a-11]
                    txt = txt + colors[b-1] + str(a) + '\n'
                    txt = txt + str(combinations[round(player_combs[i])]) + '\n\n'
                #ВЫБОР ПОБЕДИТЕЛЯ
                for i in range(len(players)):
                    if players[i] in dead:
                        player_combs[i] = -1
                max_comb = max(player_combs)
                if player_combs.count(max_comb) == 1:
                    winners = [player_combs.index(max_comb)]
                else:
                    for i in range(len(players)):

                            if math.isclose(player_combs[i],max_comb):
                                hd = [hand[i*2],hand[i*2+1]]
                                player_combs[i] = round(max(hd))
                            else:
                                player_combs[i] = -1
                    max_comb = max(player_combs)
                    winners = []
                    for i in range(len(players)):
                        if math.isclose(player_combs[i],max_comb):
                            winners.append(i)
                #ГЕНЕРАЦИЯ ТЕКСТА
                if len(winners) == 1:
                    txt = txt + 'Победитель <a href="tg://user?id='+str(players[winners[0]])+'">'+str(names[winners[0]])+'</a>, остальные сосут бибу'
                else:
                    txt = txt + 'Победители '
                    for j in winners:
                        txt = txt + '<a href="tg://user?id='+str(players[j])+'">'+str(names[j])+'</a>, '
                    txt = txt + 'остальные сосут бибу'
                #РАСПРЕДЕЛЕНИЕ ДЕНЕГ
                max_cash = []
                for j in winners:
                    max_cash.append(true_bank[j])
                max_cash = max(max_cash)
                money = 0
                for i in range(len(players)):
                    if i in winners:
                        continue
                    if true_bank[i] > max_cash:
                        money += max_cash
                        cursor.execute("UPDATE neko SET coins = coins - " + str(max_cash) + " WHERE id = " + str(players[i]))
                    else:
                        money += true_bank[i]
                        cursor.execute("UPDATE neko SET coins = coins - " + str(true_bank[i]) + " WHERE id = " + str(players[i]))
                money = int(money/len(winners))
                for j in winners:
                    cursor.execute("UPDATE neko SET coins = coins + " + str(money) + " WHERE id = " + str(players[j]))
                time.sleep(2)
                bot.edit_message_media(media=telebot.types.InputMedia(media=f,caption = txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
                cursor.execute("DELETE FROM poker WHERE id = "+str(idk))
                return
            cursor.execute("UPDATE poker SET event = " + str(event) + " WHERE id = " + str(idk))
            turn = players[pos]
            txt = act_txt
            for i in range(len(players)):
                txt = txt + names[i] + '  ' + str(true_bank[i]) + '💰\n'
            txt = txt + '\nХод <a href="tg://user?id='+str(turn)+'">'+str(names[pos])+'</a>'
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            callback_button1 = types.InlineKeyboardButton(text = '🆗 Пропуск',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 1 ' + str(r))
            callback_button2 = types.InlineKeyboardButton(text = '❌ Сдаться',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 2 ' + str(r))
            m = 5
            #МИН СТАВКА
            if money[pos] < bank[pos] + m:
                a = money[pos] - bank[pos]
                callback_button4 = types.InlineKeyboardButton(text = '🔼 Ставка ('+str(a)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 3 ' + str(r) + ' ' + str(a))
            else:
                callback_button4 = types.InlineKeyboardButton(text = '🔼 Ставка ('+str(m)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 3 ' + str(r) + ' ' + str(m))
            #МАКС СТАВКА
            if money[pos] <= bank[pos] + m:
                callback_button5 = types.InlineKeyboardButton(text = '🛑 Недоступно',callback_data = 'nothing')
            elif money[pos] < bank[pos] + 2*m:
                a = money[pos] - bank[pos]
                callback_button5 = types.InlineKeyboardButton(text = '⏫ Ставка ('+str(a)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 4 ' + str(r) + ' ' + str(a))
            else:
                callback_button5 = types.InlineKeyboardButton(text = '⏫ Ставка ('+str(2*m)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 4 ' + str(r) + ' ' + str(2*m))




            callback_button3 = types.InlineKeyboardButton(text = 'Мои карты',callback_data = 'hand ' + str(idk) + ' ' + str(turn) + ' ' + str(pos))
            keyboard.add(callback_button1,callback_button2)
            keyboard.add(callback_button4,callback_button5)
            keyboard.add(callback_button3)
            time.sleep(2)
            bot.edit_message_media(media=telebot.types.InputMedia(media=f,caption = txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)

        else:
            if (r == 1 and pos == len(players)) or r == 2:
                r = 2
                pos = bank.index(min(bank))
            turn = players[pos]
            txt = act_txt
            for i in range(len(players)):
                txt = txt + names[i] + '  ' + str(true_bank[i]) + '💰\n'
            txt = txt + '\nХод <a href="tg://user?id='+str(turn)+'">'+str(names[pos])+'</a>'
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            if r == 1 and balance:
                callback_button1 = types.InlineKeyboardButton(text = '🆗 Пропуск',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 1 ' + str(r))
            else:
                callback_button1 = types.InlineKeyboardButton(text = '🛑 Недоступно',callback_data = 'nothing')
            callback_button2 = types.InlineKeyboardButton(text = '❌ Сдаться',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 2 ' + str(r))
            if balance:
                m = 5
            else:
                m = max(bank) - bank[pos]
            #МИН СТАВКА
            if money[pos] < bank[pos] + m:
                a = money[pos] - bank[pos]
                callback_button4 = types.InlineKeyboardButton(text = '🔼 Ставка ('+str(a)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 3 ' + str(r) + ' ' + str(a))
            else:
                callback_button4 = types.InlineKeyboardButton(text = '🔼 Ставка ('+str(m)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 3 ' + str(r) + ' ' + str(m))
            #МАКС СТАВКА
            if money[pos] <= bank[pos] + m or len(vabank) >= len(players) - len(dead) - 1:
                callback_button5 = types.InlineKeyboardButton(text = '🛑 Недоступно',callback_data = 'nothing')
            elif money[pos] < bank[pos] + 2*m:
                a = money[pos] - bank[pos]
                callback_button5 = types.InlineKeyboardButton(text = '⏫ Ставка ('+str(a)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 4 ' + str(r) + ' ' + str(a))
            else:
                callback_button5 = types.InlineKeyboardButton(text = '⏫ Ставка ('+str(2*m)+' 💰)',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 4 ' + str(r) + ' ' + str(2*m))

            callback_button3 = types.InlineKeyboardButton(text = 'Мои карты',callback_data = 'hand ' + str(idk) + ' ' + str(turn) + ' ' + str(pos))
            keyboard.add(callback_button1,callback_button2)
            keyboard.add(callback_button4,callback_button5)
            keyboard.add(callback_button3)
            time.sleep(2)
            bot.edit_message_media(media=telebot.types.InputMedia(media=call.message.photo[len(call.message.photo) - 1].file_id,caption = txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)

      elif 'hand' in call.data:
        args = call.data.split()
        idk = int(args[1])
        turn = int(args[2])
        pos = int(args[3])
        if call.from_user.id != turn:
            answer_callback_query(call,'Не твой ход')
            return

        data = cursor.execute('SELECT * FROM poker WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        cards = unpack(data[1])
        event = data[2]
        hand = unpack(data[6])
        hand = [hand[pos*2],hand[pos*2+1]]
        if event == 2:
            event = 0
        for i in range(5-event):
            cards.pop()
        combinations = ['Старшая карта','Пара','Две пары','Сет','Стрит','Флеш','Фулл хаус','Каре','Стрит флеш','Флеш рояль']
        percents = ['100%','43.8%','23.5%','4.8%','4.6%','3%','2.6%','0.16%','0.03%','0.003%']
        cards.append(hand[0])
        cards.append(hand[1])
        comb = combinator(cards)
        colors = ['♦️','♥️','♠️','♣️']
        numbers = ['J','Q','K','A']
        txt = 'Карты у тебя в руке:\n'
        a = round(hand[0])
        b = round((hand[0]%1)*10)
        if a > 10:
            a = numbers[a-11]
        txt = txt + colors[b-1] + str(a) + '   '
        a = round(hand[1])
        b = round((hand[1]%1)*10)
        if a > 10:
            a = numbers[a-11]
        txt = txt + colors[b-1] + str(a)
        txt = txt + '\n\nТекущая комбинация:\n'
        txt = txt + combinations[round(comb)]

        notify_callback_query(call,txt)
      elif 'read' in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        answer_callback_query(call,'Успешно')
        bot.edit_message_media(media=telebot.types.InputMedia(media=patch_image,type="photo"),chat_id=call.message.chat.id, message_id=call.message.message_id)

      elif 'letter' in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')

            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        answer_callback_query(call,'Успешно')
        nam = str(data[1]).rstrip()
        rep = data[2]
        reward_rep = int(rep/100) * 200
        letter_title = 'ПОЗДРАВЛЯЕМ С ' + str(reward_rep) + ' ДОВЕРИЯ'
        letter_text = 'Вы и ' + nam + ', безусловно, уже довольно долго вместе. Надеемся, в Некославии будущего все граждане смогут построить такие же крепкие отношения со своими некодевочками, и вы являетесь прекрасным тому доказательством. Партия гордится тобой, в связи с чем подготовила небольшой, но приятный подарок. Славься Некославия!'

        lines = textwrap.wrap(letter_text, width=35)
        ptxt = ''
        for line in lines:
            ptxt = ptxt + line + '\n'
        im0 = Image.open('bot/letter.png')
        font = ImageFont.truetype('bot/times-new-roman.ttf', size=50)
        draw = ImageDraw.Draw(im0)
        draw.text((70, 130), ptxt, font=font, fill=(71, 66, 66))
        w = font.getlength(letter_title)
        draw.text(((924-w)/2,50), letter_title, font=font, fill=(71, 66, 66))
        im0.save('bot/result.png')
        f = open("bot/result.png","rb")
        bot.edit_message_media(media=telebot.types.InputMedia(media=f,type="photo"),chat_id=call.message.chat.id, message_id=call.message.message_id)
      elif "spinner" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')
            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(call.from_user.id))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        coins = data[11]
        pilk = data[41]
        answer_callback_query(call,'Успешно')
        d = random.randint(0,6)
        texts = ['Ты выиграл 30 некогривен 💰, неплохо',
        'Ты выиграл стакан странной белой жидкости 🥛',
        'Вау, ты выиграл целое нихуя',
        'Ты выиграл 20 некогривен 💰, неплохо',
        'Ты выиграл 15 некогривен 💰, неплохо',
        'Вау, ты выиграл целое нихуя',
        'Ты выиграл 40 некогривен 💰, неплохо']
        gifs = ['CgACAgIAAx0CZQN7rQAC3G5jwMhPiQwlkRYiMKeeS8-CZcqOgAACVyQAAiEsCEpAqdma088Iry0E',
        'CgACAgIAAx0CZQN7rQAC3HFjwMhwvuJEY8e_yAgTQkJeVjKoGAACWCQAAiEsCEpHsvBSvT-v6C0E',
        'CgACAgIAAx0CZQN7rQAC3HRjwMiE2qyJF3dTF0m5EZ9dg-IFRgACWSQAAiEsCErxfueDukAhXy0E',
        'CgACAgIAAx0CZQN7rQAC3HdjwMiJF3_WaVj6h2986oTl5RpikQACWiQAAiEsCEqfKMMNyTg2-y0E',
        'CgACAgIAAx0CZQN7rQAC3HpjwMiaGehstXo-1qug40koUCrjGAACWyQAAiEsCEo-mEGYHqHwCC0E',
        'CgACAgIAAx0CZQN7rQAC3H1jwMiTA3C7WIZLwMYQvcW74pVohwACXCQAAiEsCEqR-AVp9dE_Bi0E',
        'CgACAgIAAx0CZQN7rQAC3IBjwMiDEyr1BFXw3hie2gzTjHkFcwACXSQAAiEsCEqjTiGYFjksry0E']
        if d == 0:
            coins = coins + 30
        elif d == 1:
            pilk = pilk + 1
        elif d == 3:
            coins = coins + 20
        elif d == 4:
            coins = coins + 15
        elif d == 6:
            coins = coins + 40
        time.sleep(2)
        bot.edit_message_media(media=telebot.types.InputMedia(media=gifs[d],type="animation"),chat_id=call.message.chat.id, message_id=call.message.message_id)
        time.sleep(12)
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,caption=texts[d])
        cursor.execute('UPDATE neko SET coins = ' + str(coins) + ', pilk = ' + str(pilk) + ' WHERE id = '+str(call.from_user.id))
      elif "paper" in call.data:
        args = call.data.split()
        idk = int(args[1])
        b1 = eval(args[2])
        b2 = eval(args[3])
        starter = int(args[4])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')
            return
        data = cursor.execute('SELECT * FROM neko WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        coins = data[11]
        version = data[29]
        data = cursor.execute('SELECT * FROM papers WHERE id = '+str(idk))
        data = data.fetchone()
        if data is None:
            answer_callback_query(call,'Пашол нахуй')
            return
        images = unpack(data[1])
        stage = data[5]
        mistakes = data[6]
        if starter == 1:
            answer_callback_query(call,'Успешно')
        else:
            if b1 == b2:
                answer_callback_query(call,'Правильно 👍')
            else:
                answer_callback_query(call,'Неправильно 👎')
                mistakes += 1
            stage += 1
        if stage == 3:
            phot = 'AgACAgIAAx0CZQN7rQAC3fFj7PN2eIWEEvqIJy3vH2FBpAUl1AACKsUxG7OiaUu7MhScqwbHIAEAAwIAA3MAAy4E'
            c = 15 - 5*mistakes
            coins += c
            cursor.execute("UPDATE neko SET coins = "+ str(coins) +" WHERE id = "+str(idk))
            cursor.execute("DELETE FROM papers WHERE id = "+str(idk))
            time.sleep(2)
            if mistakes == 0:
                txt = 'За эту смену тебе удалось заработать ' + str(c) + ' некогривен 💰. Ты не совершил ни единой ошибки, руководство завода гордится тобой!'
            elif mistakes == 1 or mistakes == 2:
                txt = 'За эту смену тебе удалось заработать ' + str(c) + ' некогривен 💰. К сожалению, сегодня твоя работа не была идеальной, и руководство завода запомнит это'
            elif mistakes == 3:
                txt = 'За эту смену тебе ничего не удалось заработать. Партия всё чаще подумывает о том, что ты недостоин своей некодевочки'
            r = random.randint(1,10)
            if r == 10:
                biba = random.randint(10800,21600)
                b = int(time.time() + biba)
                biba = math.ceil(biba/3600)
                cursor.execute('UPDATE neko SET bolnitsa  = '+str(b)+' WHERE id = ' + str(idk))
                txt += '\n\nК сожалению, непрошедшие проверку некочаны сговорились и отпиздили тебя после работы, благодаря чему ' + str(biba) + ' часов ты проведёшь в больнице 💊'
            bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo"),chat_id=call.message.chat.id, message_id=call.message.message_id)
            if version != patch_version:
                cursor.execute("UPDATE neko SET version = "+ str(patch_version) +" WHERE id = "+str(idk))
                keyboard = types.InlineKeyboardMarkup()
                callback_button1 = types.InlineKeyboardButton(text = 'Читать 👀',callback_data = 'read ' + str(idk))
                keyboard.add(callback_button1)
                callback_button2 = types.InlineKeyboardButton(text = 'Не читать ❌',callback_data = 'dont ' + str(idk))
                keyboard.add(callback_button2)
                bot.send_photo(call.message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACznBjQgABiPsE5FE7am8mfAOKiXsSOEsAAju9MRuS1hFKlyErHhjWQfcBAAMCAANzAAMqBA',caption = 'Возвращаясь с работы, ты заметил свежую газету, торчащую из твоего почтового ящика. Прочитать её?',reply_markup=keyboard)
        else:
            args = images[stage]
            args = args.split()
            phot = str(args[0])
            propusk = eval(args[1])
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            callback_button1 = types.InlineKeyboardButton(text = 'Пропустить ✅',callback_data = 'paper ' + str(idk) + ' ' + str(True) + ' ' + str(propusk) + ' 0')
            callback_button2 = types.InlineKeyboardButton(text = 'Дать пизды ❌',callback_data = 'paper ' + str(idk) + ' ' + str(False) + ' ' + str(propusk) + ' 0')
            callback_button3 = types.InlineKeyboardButton(text = 'Справка ❔',callback_data = 'spravka ' + str(idk))
            keyboard.add(callback_button1,callback_button2)
            keyboard.add(callback_button3)
            cursor.execute("UPDATE papers SET stage = "+ str(stage) +",mistakes = " + str(mistakes) + " WHERE id = "+str(idk))
            time.sleep(2)
            bot.edit_message_media(media=telebot.types.InputMedia(media=phot,type="photo"),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)


      elif "spravka" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            answer_callback_query(call,'Пашол нахуй')
            return
        prof_text = ['монтажникам','электрикам','токарям','сварщикам','охранникам']
        p = prof_text[prof.index(bad_prof)]
        txt = 'Каждый день через твой пункт будет проходить 3 некочана. Для принятия окончательного решения проверь фото, печать, дату выдачи и срок действия\n\nСегодня запрещен проход ' + str(p)
        notify_callback_query(call,txt)
      elif "comb" in call.data:
        args = call.data.split()
        idk = int(args[1])
        if call.from_user.id != idk:
            bot.answer_callback_query(call.id,text = 'Пашол нахуй')
            return
        txt = 'Возможные комбинации:\n🍉🍉 - 0 некогривен 💰\n🍓🍓 - 10 некогривен 💰\n🍒🍒 - 10 некогривен 💰\n🍓🍓🍓 - 40 некогривен 💰\n🍒🍒🍒 - 70 некогривен 💰\n🍉🍉🍉 - 100 некогривен 💰\n🍋🍋🍋 - хорни некодевочка 🐱'
        notify_callback_query(call,txt)





@app.route('/' + token, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok', 200
@app.route('/')
def get_ok():
    return 'ok', 200
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)