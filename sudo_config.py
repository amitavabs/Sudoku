#sudo_config Ver 1.1 amitavabs@yahoo.com
#Intial configuration program for Sudoku solving
#Edit  here (see comments below) if Sudoku input data mode needs to be changed

INPUT_SCREEN = 0

INPUT_FILE = 1
INPUT_FILE_NAME = "sudo_data.txt"
INPUT_FILE_REC = 11

INPUT_PROGRAM = 3

#Change comment here if you want to change input mode 
INPUT_MODE = INPUT_SCREEN
#INPUT_MODE = INPUT_FILE
#INPUT_MODE = INPUT_PROGRAM

global input_program_data
#apparently most difficult Sudoku
input_program_data = [ 0,0,5,  3,0,0,  0,0,0,  \
                       8,0,0,  0,0,0,  0,2,0,  \
                       0,7,0,  0,1,0,  5,0,0,  \
                                               \
                       4,0,0,  0,0,5,  3,0,0,  \
                       0,1,0,  0,7,0,  0,0,6,  \
                       0,0,3,  2,0,0,  0,8,0,  \
                                               \
                       0,6,0,  5,0,0,  0,0,9,  \
                       0,0,4,  0,0,0,  0,3,0,  \
                       0,0,0,  0,0,9,  7,0,0   ]
    
global t
t = ["" for i in range(81)]

global t_chk
t_chk = ["" for i in range(81)]

global s_all
s_all = {"1","2","3","4","5","6","7","8","9"}

global entry_tab_list
#####################################################
entry_tab_list = [  0, 1, 2,  9,10,11, 18,19,20,  \
                    3, 4, 5, 12,13,14, 21,22,23,  \
                    6, 7, 8, 15,16,17, 24,25,26,  \
                                                  \
                    27,28,29, 36,37,38, 45,46,47, \
                    30,31,32, 39,40,41, 48,49,50, \
                    33,34,35, 42,43,44, 51,52,53, \
                                                  \
                    54,55,56, 63,64,65, 72,73,74, \
                    57,58,59, 66,67,68, 75,76,77, \
                    60,61,62, 69,70,71, 78,79,80  ]          
                       
#####################################################

global row_list
row_list = []
row_list.append([ 0,1,2,3,4,5,6,7,8])
row_list.append([ 9,10,11,12,13,14,15,16,17])
row_list.append([ 18,19,20,21,22,23,24,25,26])
row_list.append([ 27,28,29,30,31,32,33,34,35])
row_list.append([ 36,37,38,39,40,41,42,43,44])
row_list.append([ 45,46,47,48,49,50,51,52,53])
row_list.append([ 54,55,56,57,58,59,60,61,62])
row_list.append([ 63,64,65,66,67,68,69,70,71])
row_list.append([ 72,73,74,75,76,77,78,79,80])


global col_list
col_list = []
col_list.append( [ 0,9,18,27,36,45,54,63,72] )
col_list.append( [ 1,10,19,28,37,46,55,64,73] )
col_list.append( [ 2,11,20,29,38,47,56,65,74] )
col_list.append( [ 3,12,21,30,39,48,57,66,75] )
col_list.append( [ 4,13,22,31,40,49,58,67,76] )
col_list.append( [ 5,14,23,32,41,50,59,68,77] )
col_list.append( [ 6,15,24,33,42,51,60,69,78] )
col_list.append( [ 7,16,25,34,43,52,61,70,79] )
col_list.append( [ 8,17,26,35,44,53,62,71,80] )


global grid_list
grid_list = []
grid_list.append( [ 0,1,2,9,10,11,18,19,20] )
grid_list.append( [ 3,4,5,12,13,14,21,22,23] )
grid_list.append( [ 6,7,8,15,16,17,24,25,26] )
grid_list.append( [ 27,28,29,36,37,38,45,46,47] )
grid_list.append( [ 30,31,32,39,40,41,48,49,50] )
grid_list.append( [ 33,34,35,42,43,44,51,52,53] )
grid_list.append( [ 54,55,56,63,64,65,72,73,74] )
grid_list.append( [ 57,58,59,66,67,68,75,76,77] )
grid_list.append( [ 60,61,62,69,70,71,78,79,80] )

#gr8 example of diff between append and extend
global master_row_col_grid_list
master_row_col_grid_list = []
master_row_col_grid_list.extend(row_list)
master_row_col_grid_list.extend(col_list)
master_row_col_grid_list.extend(grid_list)

global s_udo_arr
s_udo_arr = [set() for i in range(81)]

#Nested array list
global row_lookup_list
row_lookup_list = []
row_lookup_list.append( [  [0], [12,21,15,24,12,15,21,24] ] )
row_lookup_list.append( [  [3], [9,18,15,24,9,15,18,24] ] )
row_lookup_list.append( [  [6], [9,18,12,21,9,12,18,21] ] )
row_lookup_list.append( [  [9], [3,21,6,24,3,6,21,24] ] )
row_lookup_list.append( [  [12], [0,18,6,24,0,6,18,24] ] )
row_lookup_list.append( [  [15], [0,18,3,21,0,3,18,21] ] )
row_lookup_list.append( [  [18], [6,15,3,12,3,6,12,15] ] )
row_lookup_list.append( [  [21], [0,9,6,15,0,6,9,15] ] )
row_lookup_list.append( [  [24], [0,9,3,12,0,3,9,12] ] )

#Stack for iterative values
global s_ckpt
s_ckpt = []

#Sudoko populate modes
#11- User Input 2- Stored flat file  - Checkpoint start
def populate_sudo(enteries):
    global input_program_data
    global entry_tab_list
    
    update_mode = INPUT_MODE
    
    if   update_mode ==  INPUT_SCREEN  : return
    elif update_mode ==  INPUT_FILE    : populate_sudo_file(enteries)
    elif update_mode ==  INPUT_PROGRAM : 
        for mndx, i in enumerate(entry_tab_list)  :
            j = str(input_program_data[mndx])
            if j== "0" : j= ""
            enteries[i].insert(0,j)
    return


def populate_sudo_file(enteries):
    global entry_tab_list
    
    mrec_use = INPUT_FILE_REC
    f = open(INPUT_FILE_NAME, "r")
    for mdata in f: 
        mfield = mdata.split(",")
        mrec = int(mfield[0][:])
        if mrec_use == mrec :
            for mndx,i in enumerate(entry_tab_list)  :
                mfield1 = mfield[1][mndx]
                if mfield1 == "0" : mfield1 = ""
                enteries[i].insert(0, mfield1)
    f.close
    return


def update_screen(enteries) :
    global t
    global entry_tab_list   

    for mndx,i in enumerate(entry_tab_list) :
        enteries[i].delete(0,"end")
        enteries[i].insert(0,t[mndx])
    return

