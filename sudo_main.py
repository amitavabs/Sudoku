#sudo_ main Ver 1.1 amitavabs@yahoo.com
#Generates at least one solution if there are multiple solutions
#Verfies and reports if the Sudoku data is invalid

from sudo_config import  *
from sudo_solver import  *
from tkinter import  *


def reg_data_chk(input): #exclude 00 as width 2
    if (input.isdigit() and int(input) < 10) and len(input) == 1 \
          or input is "": return True   
    return False       

  
def solver_start():
    global t
    global entry_tab_list   
    global s_all
    global s_udo_arr
    
    #Initialise internal t list data from screen, and set all, as possible values s_udo_arr
    for mndx,i in enumerate(entry_tab_list) :
        t[mndx]   = enteries[i].get()
        if enteries[i].get() != "" : enteries[i].configure(state='disabled')
        if not bool(t[mndx]) :  s_udo_arr[mndx] = s_all
        else : s_udo_arr[mndx].add(t[mndx])

    #s_debug()
    i = sudo_solver_engine()
    
    if (i == 0) : i = sudo_solver_chkpnt()
    if (i != 1) : print ("SUDOKU Data Invalid")
     
    update_screen(enteries)
    
    return


root = Tk()
root.geometry("500x600+700+100")
root.config(bg = '#F2B33D')
root.option_add("*font", "lucida 25 bold ")
root.title("SUDOKU")

#register background update handlers that are polled while the application is idle.
data_chk = root.register(reg_data_chk)

#Validation container for entries - only after root is defined
md = [StringVar()]*81
#important otherwise all point to same address place
for i in range(0,81) : md[i] = str(i)

frame = Frame(root)
frame.config(bg = '#F2B33D', bd = 10, relief = RIDGE)
frame.grid( row=0,column=0, padx=47, pady=40)

frame_but = Frame(root)
frame_but.config(bg = '#F2B33D', bd = 10, )
frame_but.grid( row=1,column=0, padx=2, pady=2)

frame_arr = []
mcount = 0
for i in range(0,3):
    for j in range(0,3):
        frame_element =  Frame(frame)       
        frame_element.grid( row=i,column=j,padx=1, pady=1)
        frame_arr.append(frame_element)

enteries = []
mcount = 0
mi = 0
mj = 0
for i in range(0,9):
    for j in range(0,9):
        b = Entry(frame_arr[i], width=2,textvariable=md[mcount])
        mcount += 1
        
        b.grid( row = mi, column = mj,)
        mj += 1
        if mj == 3 :
            mj = 0
            mi += 1
        b.config(validate ="key", validatecommand =(data_chk, '%P'))

        b.delete(0,"end")
        b.insert(0,"")

        enteries.append(b)

#Populate screen 
populate_sudo(enteries)

button1 = Button(frame_but, text='Solve',command= solver_start, padx=10, pady=10)
button1.grid(row=0, column=0, pady=0, padx=50,ipadx=5)
button1.config(font=('helvetica', 15))

button2 = Button(frame_but, text='Quit', command=root.destroy,padx=10, pady=10)
button2.grid(row=0, column=5, pady=0, padx=50,ipadx=10)
button2.config(font=('helvetica', 15))

mainloop()
