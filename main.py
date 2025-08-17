from google import genai
from tkinter import *
from PIL import Image
import nname, tkinter.font, time, threading, make_data, random

app = Tk()
app.title('Merchant')
app.resizable(False, False)
screenWidth = 1280
screenHeight = 760
fps = 0.012


#---------------------------------------

# 본인의 API KEY 작성
API_KEY = "AIzaSyBZpFAmAevbIbzSA21HBomWLo16j60fJsE"

#---------------------------------------


app.geometry(str(screenWidth) + 'x' + str(screenHeight))
client = genai.Client(api_key=API_KEY)
canvas = Canvas(width=screenWidth, height=screenHeight, bg='black')
canvas.place(x=-2, y=-2)

boldFont = tkinter.font.Font(family="Pyeojin Gothic", size=16)


guestName = random.choice(nname.nnamesList)

guestName_text = None
itemName_text = None
itemDes_text = None
itemCost_text = None
item_photo = None
frame_photo = None

item_i = None
frame_i = PhotoImage(file='images/frames/0.png')
blank_i = PhotoImage(file="images/blank.png")

myMoney = 1000
myMoney_text = None

history_of_itemName = "토끼풀,"

def Awake():
    global guestName_text, itemName_text, itemDes_text, itemCost_text, myMoney_text, item_photo, frame_photo
    guestName_text = canvas.create_text(360, 50, text="손님 오시는 중..", font=tkinter.font.Font(family="이사만루체 Medium", size=22), anchor=NW, fill='white')
    itemName_text = canvas.create_text(370, 160, text="손님 오시는 중..", font=tkinter.font.Font(family="이사만루체 Bold", size=42), anchor=NW, fill='white')
    itemDes_text = canvas.create_text(53, 470, text="손님 오시는 중..", font=tkinter.font.Font(family="이사만루체 Light", size=22), anchor=NW, fill='white')
    itemCost_text = canvas.create_text(180, 350, text="손님 오시는 중..", font=tkinter.font.Font(family="이사만루체 Medium", size=22), anchor=CENTER, fill='white')
    myMoney_text = canvas.create_text(1240, 680, text="자산 : " + str(myMoney) + "G", font=tkinter.font.Font(family="이사만루체 Medium", size=16), anchor=NE, fill='white')
    item_photo = canvas.create_image(180, 180, image=blank_i, anchor=CENTER)
    frame_photo = canvas.create_image(180, 180, image=frame_i, anchor=CENTER)

def Update():
    global pressReturn, response, guestName_text, guestName, itemName_text, itemDes_text, itemCost_text, myMoney_text
    while True:
        
        if pressReturn == True: # 엔터 키를 눌렀을 때
            threading.Thread(target=spawn_guest, daemon=True).start()
            response = False
            guestName = random.choice(nname.nnamesList)
            pressReturn = False

        if response == False:
            canvas.itemconfig(guestName_text, text="손님 오시는 중..")
            canvas.itemconfig(itemName_text, text="")
            canvas.itemconfig(itemDes_text, text="")
            canvas.itemconfig(itemCost_text, text="")
            canvas.itemconfig(item_photo, image=blank_i)
        elif response == True:
            canvas.itemconfig(guestName_text, text="ㅣ " + guestName + "님의 상품")
            canvas.itemconfig(itemName_text, text="< " + current_name + " >")
            canvas.itemconfig(itemDes_text, text=current_des)
            canvas.itemconfig(itemCost_text, text="구매 가격 : " + str(current_cost) + "G")
            canvas.itemconfig(item_photo, image=item_i)
        canvas.itemconfig(myMoney_text, text="자산 : " + str(myMoney) + "G")
        time.sleep(fps)


pressReturn = False
def pressed_return(key):
    global pressReturn
    if allow_enter == True and response == True:
        pressReturn = True
        threading.Thread(target=enter_cooltime, daemon=True).start()
app.bind('<Return>', pressed_return)

def pressed_b(key):
    global myMoney
    if response == True and allow_enter == True:
        myMoney -= current_cost
        pressed_return(2)
app.bind('<b>', pressed_b)

response = False
current_name = ""
current_des = ""
current_rare = 0
current_cost = 0
def spawn_guest():
    print("아이템 생성 시작")
    global response, current_cost, current_des, current_name, history_of_itemName, item_i, frame_i
    frame_i = PhotoImage(file="images/frames/0.png")
    canvas.itemconfig(frame_photo, image=frame_i)

    rp_list = client.models.generate_content(model="gemini-2.0-flash", contents="아이템을 생성할 때 다음과 같은 이름은 80% 확률로 금지 : " + history_of_itemName + ",  " + make_data.new_question).text.split('/')

    current_name = rp_list[0]
    history_of_itemName += current_name + ','
    current_des = ""
    index_des = rp_list[1]

    im_pixel_list = client.models.generate_content(model="gemini-2.0-flash", contents="[그려야 하는 아이템 이름 : " + current_name + "], [그려야 하는 아이템의 설명 : " + current_des + "]," + make_data.new_image_question).text

    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    im_pixel_list = eval(im_pixel_list)

    for pixel in im_pixel_list:
        img.putpixel(*pixel)
    
    
    img = img.resize((230, 230), Image.NEAREST)
    img.save("images/item.png")

    item_i = PhotoImage(file='images/item.png')

    count = 0
    for oneText in index_des:
        count += 1
        current_des += oneText
        if count == 35:
            current_des += "\n"
            count = 0

    current_rare = rp_list[2]

    try:
        current_cost.replace("\n", "")
    except:
        pass

    current_cost = int(random.uniform(int(current_rare) ** 2.5, int(current_rare) ** 2.5 + 2) * random.uniform(5, 6))

    if current_cost > 950:
        frame_i = PhotoImage(file="images/frames/5.png")
    elif current_cost > 750:
        frame_i = PhotoImage(file="images/frames/4.png")
    elif current_cost > 550:
        frame_i = PhotoImage(file="images/frames/3.png")
    elif current_cost > 350:
        frame_i = PhotoImage(file="images/frames/2.png")
    elif current_cost > 180:
        frame_i = PhotoImage(file="images/frames/1.png")
    else:
        frame_i = PhotoImage(file="images/frames/0.png")

    canvas.itemconfig(frame_photo, image=frame_i)
    response = True

allow_enter = True
def enter_cooltime():
    global allow_enter
    allow_enter = False
    time.sleep(4)
    allow_enter = True


Awake()
threading.Thread(target=Update, daemon=True).start()
pressReturn = True
app.mainloop()