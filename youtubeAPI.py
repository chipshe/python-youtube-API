from io import BytesIO
from googleapiclient.discovery import build
from tkinter import *
import webbrowser
import requests
from PIL import Image, ImageTk

#API Key'inizi girin..
api_key = ''

root = Tk()
root.geometry("600x600+410+50")
root.title("Youtube API")
root.resizable(False,False)
root.configure(bg="white")

frame = Frame(root,width=350,height=350,bg='white')
frame.pack(expand=True,fill=BOTH)

secondFrame = Frame(frame,width=350,height=45,bg='white')
secondFrame.pack(expand=True,fill=BOTH)

terimAra = Entry(secondFrame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
terimAra.place(x = 200,y = 0)


Frame(frame,width=200,height=2,bg='black').place(x=195,y=27)

def on_enter(e):
    terimAra.delete(0,'end')
def on_leave(e):
    name = terimAra.get()
    if name =="":
        terimAra.insert(0,'Aranacak Terimi Girin..')
terimAra.insert(0,'Aranacak Terimi Girin..')
terimAra.bind('<FocusIn>',on_enter)
terimAra.bind('<FocusOut>',on_leave)

def ara():
    a = str(terimAra.get())
    
    youtube = build('youtube', 'v3', developerKey = api_key)
    request = youtube.search().list(
            q = a,
            part = 'snippet',
            type = 'video',
            videoDuration = 'any',
            maxResults = 6
        )

    response = request.execute()

    

    y = 80
    for item in response['items']:
        video_link = f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
        video_thumbnail = item['snippet']['thumbnails']['default']['url']
        video_title = f'{item["snippet"]["title"]}'

        image_data = requests.get(video_thumbnail).content
        image = Image.open(BytesIO(image_data))
        image = image.resize((60, 60), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)

        video_thumbnail_label = Label(frame,image=image)
        video_thumbnail_label.image = image
        video_thumbnail_label.place(x=5, y=y)

        sonuc = Label(frame,text=video_title,fg='black',bg='white',font=('Microsoft YaHei UI Light',10,'bold'))
        sonuc.place(x=85,y=y+5)

        def open_link(event):
            link = event.widget.cget("text")
            event.widget['fg'] = 'blue'
            webbrowser.open_new_tab(link)
        
        links = []

        link = Label(frame, text=video_link, fg='black',bg='white',font=('Microsoft YaHei UI Light',10,'bold'), cursor="hand2")
        link.pack_forget()
        links.append(link)
        link.place(x=85,y=y+35)
        link.bind("<Button-1>", open_link)

        Frame(frame,width=590,height=3,bg='black').place(x=5,y=y+67)

        y +=80
        
button = Button(frame,width=9,pady=1,text='Ara',bg='#57a1f8',fg='white',border=1,command=ara, cursor="hand2")
button.place(x = 420, y = 0)


root.mainloop()
