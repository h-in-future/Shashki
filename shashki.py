
import tkinter
import tkinter.messagebox
import random
import time
import copy

gl_okno=tkinter.Tk()
gl_okno.title('Shashki')
doska=tkinter.Canvas(gl_okno, width=800,height=800,bg='#FFFFFF')
doska.pack()

n2_spisok=()
ur=3
k_rez=0
o_rez=0
poz1_x=-1
f_hi=True

def izobrazheniya_peshek():
    global peshki
    i1=tkinter.PhotoImage(file="1b.gif")
    i2=tkinter.PhotoImage(file="1bk.gif")
    i3=tkinter.PhotoImage(file="1h.gif")
    i4=tkinter.PhotoImage(file="1hk.gif")
    peshki=[0,i1,i2,i3,i4]

def novaya_igra():
    global pole
    pole=[[0,3,0,3,0,3,0,3],
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]

def vivod(x_poz_1,y_poz_1,x_poz_2,y_poz_2):
    global peshki
    global pole
    global kr_ramka,zel_ramka
    k=100
    x=0
    doska.delete('all')
    kr_ramka=doska.create_rectangle(-5, -5, -5, -5,outline="red",width=5)
    zel_ramka=doska.create_rectangle(-5, -5, -5, -5,outline="green",width=5)

    while x<8*k:
        y=1*k
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    x=1*k
    while x<8*k:
        y=0
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    
    for y in range(8):
        for x in range(8):
            z=pole[y][x]
            if z:  
                if (x_poz_1,y_poz_1)!=(x,y):
                    doska.create_image(x*k,y*k, anchor=tkinter.NW, image=peshki[z])
          
    z=pole[y_poz_1][x_poz_1]
    if z:
        doska.create_image(x_poz_1*k,y_poz_1*k, anchor=tkinter.NW, image=peshki[z],tag='ani')
    
    kx = 1 if x_poz_1<x_poz_2 else -1
    ky = 1 if y_poz_1<y_poz_2 else -1
    for i in range(abs(x_poz_1-x_poz_2)):
        for ii in range(33):
            doska.move('ani',0.03*k*kx,0.03*k*ky)
            doska.update()
            time.sleep(0.01)

def soobsenie(s):
    global f_hi
    z='Игра завершена'
    if s==1:
        i=tkinter.messagebox.askyesno(title=z, message='Вы победили!\nНажми "Да" что бы начать заново.',icon='info')
    if s==2:
        i=tkinter.messagebox.askyesno(title=z, message='Вы проиграли!\nНажми "Да" что бы начать заново.',icon='info')
    if s==3:
        i=tkinter.messagebox.askyesno(title=z, message='Ходов больше нет.\nНажми "Да" что бы начать заново.',icon='info')
    if i:
        novaya_igra()
        vivod(-1,-1,-1,-1)
        f_hi=True
    if not(i):
        quit()
   

def pozici_1(event):
    x,y=(event.x)//100,(event.y)//100
    doska.coords(zel_ramka,x*100,y*100,x*100+100,y*100+100)

def pozici_2(event):
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    x,y=(event.x)//100,(event.y)//100
    if pole[y][x]==1 or pole[y][x]==2:
        doska.coords(kr_ramka,x*100,y*100,x*100+100,y*100+100)
        poz1_x,poz1_y=x,y
    else:
        if poz1_x!=-1:
            poz2_x,poz2_y=x,y
            if f_hi:
                hod_igroka()
                if not(f_hi):
                    time.sleep(0.5)
                    hod_kompjutera()
            poz1_x=-1
            doska.coords(kr_ramka,-5,-5,-5,-5)

             
     
def hod_kompjutera():
    global f_hi
    global n2_spisok
    proverka_hk(1,(),[])
    if n2_spisok:
        kh=len(n2_spisok)
        th=random.randint(0,kh-1)
        dh=len(n2_spisok[th])
        for h in n2_spisok:
            h=h
        for i in range(dh-1):
            spisok=hod(1,n2_spisok[th][i][0],n2_spisok[th][i][1],n2_spisok[th][1+i][0],n2_spisok[th][1+i][1])
        n2_spisok=[]
        f_hi=True

    #определяем победителя 
    s_k,s_i=skan()
    if not(s_i):
            soobsenie(2)
    elif not(s_k):
            soobsenie(1)
    elif f_hi and not(spisok_hi()):
            soobsenie(3)
    elif not(f_hi) and not(spisok_hk()):
            soobsenie(3)

def spisok_hk():
    spisok=prosmotr_hodov_k1([])
    if not(spisok):
        spisok=prosmotr_hodov_k2([])
    return spisok

def proverka_hk(tur,n_spisok,spisok):
    global pole
    global n2_spisok
    global l_rez,k_rez,o_rez
    if not(spisok):
        spisok=spisok_hk()

    if spisok:
        k_pole=copy.deepcopy(pole)
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:
            t_spisok=hod(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:
                proverka_hk(tur,(n_spisok+((poz1_x,poz1_y),)),t_spisok)
            else:
                proverka_hi(tur,[])
                if tur==1:
                    t_rez=o_rez/k_rez
                    if not(n2_spisok):
                        n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        l_rez=t_rez
                        if t_rez==l_rez:
                            n2_spisok=n2_spisok+(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        if t_rez>l_rez:
                            n2_spisok=()
                            n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                            l_rez=t_rez
                    o_rez=0
                    k_rez=0

            pole=copy.deepcopy(k_pole)
    else:
        s_k,s_i=skan()
        o_rez+=(s_k-s_i)
        k_rez+=1

def spisok_hi():
    spisok=prosmotr_hodov_i1([])
    if not(spisok):
        spisok=prosmotr_hodov_i2([])
    return spisok
    
def proverka_hi(tur,spisok):
    global pole,k_rez,o_rez
    global ur
    if not(spisok):
        spisok=spisok_hi()

    if spisok:
        k_pole=copy.deepcopy(pole)
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:                    
            t_spisok=hod(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:
                proverka_hi(tur,t_spisok)
            else:
                if tur<ur:
                    proverka_hk(tur+1,(),[])
                else:
                    s_k,s_i=skan()
                    o_rez+=(s_k-s_i)
                    k_rez+=1

            pole=copy.deepcopy(k_pole)
    else:
        s_k,s_i=skan()
        o_rez+=(s_k-s_i)
        k_rez+=1

def skan():
    global pole
    s_i=0
    s_k=0
    for i in range(8):
        for ii in pole[i]:
            if ii==1:s_i+=1
            if ii==2:s_i+=3
            if ii==3:s_k+=1
            if ii==4:s_k+=3
    return s_k,s_i

def hod_igroka():
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    f_hi=False
    spisok=spisok_hi()
    if spisok:
        if ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:
            t_spisok=hod(1,poz1_x,poz1_y,poz2_x,poz2_y)          
            if t_spisok:
                f_hi=True
        else:
            f_hi=True
    doska.update()

def hod(f,poz1_x,poz1_y,poz2_x,poz2_y):
    global pole
    if f:vivod(poz1_x,poz1_y,poz2_x,poz2_y)
   
    if poz2_y==0 and pole[poz1_y][poz1_x]==1:
        pole[poz1_y][poz1_x]=2

    if poz2_y==7 and pole[poz1_y][poz1_x]==3:
        pole[poz1_y][poz1_x]=4
            
    pole[poz2_y][poz2_x]=pole[poz1_y][poz1_x]
    pole[poz1_y][poz1_x]=0

    #рубим пешку игрока
    kx=ky=1
    if poz1_x<poz2_x:kx=-1
    if poz1_y<poz2_y:ky=-1
    x_poz,y_poz=poz2_x,poz2_y
    while (poz1_x!=x_poz) or (poz1_y!=y_poz):
        x_poz+=kx
        y_poz+=ky
        if pole[y_poz][x_poz]!=0:
            pole[y_poz][x_poz]=0
            if f:vivod(-1,-1,-1,-1)
            if pole[poz2_y][poz2_x]==3 or pole[poz2_y][poz2_x]==4:
                return prosmotr_hodov_k1p([],poz2_x,poz2_y)
            elif pole[poz2_y][poz2_x]==1 or pole[poz2_y][poz2_x]==2:
                return prosmotr_hodov_i1p([],poz2_x,poz2_y)
    if f:vivod(poz1_x,poz1_y,poz2_x,poz2_y)

def prosmotr_hodov_k1(spisok):
    for y in range(8):
        for x in range(8):
            spisok=prosmotr_hodov_k1p(spisok,x,y)
    return spisok

def prosmotr_hodov_k1p(spisok,x,y):
    if pole[y][x]==3:
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))
    if pole[y][x]==4:
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))
                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                        osh+=1
                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2:
                        if osh>0:spisok.pop()
                        break
    return spisok

def prosmotr_hodov_k2(spisok):
    for y in range(8):
        for x in range(8):
            if pole[y][x]==3:
                for ix,iy in (-1,1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))
                        if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))                 
            if pole[y][x]==4:
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2:
                                break
    return spisok

def prosmotr_hodov_i1(spisok):
    spisok=[]
    for y in range(8):
        for x in range(8):
            spisok=prosmotr_hodov_i1p(spisok,x,y)
    return spisok

def prosmotr_hodov_i1p(spisok,x,y):
    if pole[y][x]==1:
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))
    if pole[y][x]==2:
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))
                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                        osh+=1
                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2:
                        if osh>0:spisok.pop()
                        break
    return spisok

def prosmotr_hodov_i2(spisok):
    for y in range(8):
        for x in range(8):
            if pole[y][x]==1:
                for ix,iy in (-1,-1),(1,-1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))
                        if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))                 
            if pole[y][x]==2:
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2:
                                break
    return spisok

izobrazheniya_peshek()
novaya_igra()
vivod(-1,-1,-1,-1)
doska.bind("<Motion>", pozici_1)#движение мышки по полю
doska.bind("<Button-1>", pozici_2)#нажатие левой кнопки (действие движение битьё)
doska.bind("<Double-Button-1>", pozici_3)#двойное нажатие левой кнопки (выкл полностью)
tkinter.mainloop()
