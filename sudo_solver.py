#sudo_solver Ver 1.1 amitavabs@yahoo.com
#sudo_solver_engine works conventional way by eliminating possible choices of a cell
#sudo_solver_chkpnt works by partial brute force method if above fails.

from sudo_config import  *


def sudo_solver_engine() :
    #0 - Incompelete processing 
    #1 - Solution complete
    #2 - Invalid Sudoku data
 
    while True :

        while(sudo_solver_exclude()) :pass
        
        i = sudo_solver_validate()
        if ( i == 1) or ( i == 2) : return i
    
        mprocessd1 = sudo_solver_lookup()
        mprocessd2 = sudo_solver_exclude()
       
        i = sudo_solver_validate()
        if ( i == 1) or ( i == 2) : return i
    
        if not( mprocessd1) and  not( mprocessd2): return 0
        else : continue    

    return 0
 
 
#Processes by excluding values of element already
#present in applicable row, col and minigrid
#Generates partial list of possible values of an element, even if not fully solved
def sudo_solver_exclude() :
    
    global t
    global s_all
    global s_udo_arr
    global master_row_col_grid_list

    melement_solved = False

    # Get list of possible values of an uncomputed element
    for i in range(81) :
        if t[i] == "" :
            for j in master_row_col_grid_list :
                for k in j :
                    if i == k :
                        for l in j :
                            if t[l] != "" :
                                 s_udo_arr[i] = s_udo_arr[i] - set(t[l])
                                 
    # Solve for converged cases of only one possible value                      
    for i in range(81) :
        if t[i] == "" :                        
            if len(s_udo_arr[i]) == 1 :
                melement_solved = True
                t[i] = list(s_udo_arr[i])[0]
                

    return melement_solved


#Every element belongs to distinct  row and column
#There are four minigrids(3x3) excluding the one in which the 
#element belongs , present in the row and column of the element
#which we name as external minigrid. Each element must also be present
#in the  external minigrid excluding  row/ column which it belongs.
#An unascertained element in external minigrid related to an element, are named as external elements.
#An element with its one external minigrid has maximum six external elements .
#Earlier processing will  reduce possible  values of each uncomputed element. 
#For a computed element that matches with one and only one of the possible vales of
#external element, then that uncomputed element will be same as element.
# The reverse also is true and a element in grid is used to check row/ column wise
#Lookup Tables  used to speed up processing
#sudo_solver_exclude() should have executed before to get possible values.
#First proceed rowise and do a transpose, to use same code for columnwise check

def sudo_solver_lookup() :
    order = 0 #row process
    if ( sudo_solver_lookup_row(order) ) : return True
    order = 1 #col process transpose elements
    if ( sudo_solver_lookup_row(order) ) : return True
    return False


def sudo_solver_lookup_row(order)  :    
    global t
    global col_list
    global s_udo_arr    
    global row_lookup_list

    melement_solved = False
    
    if order == 0:
        mt = ["" for i in range(81)]        
        for i in range(81) : mt[i] = t[i]
        ms_udo_arr = s_udo_arr
    else :
        mt = ["" for i in range(81)]
        ms_udo_arr = [set() for i in range(81)]
        k = 0
        for i in col_list :
            for j in i :
                mt[j] = t[k]
                ms_udo_arr[j] = s_udo_arr[k]
                k += 1
    
    k = 0;
    for i in range(1,81) :
        if mt[i] != "" :
            tquot = int(i/9)
            trem = i - tquot*9
            if trem in (0,1,2) : rlook = 0
            if trem in (3,4,5) : rlook = 3
            if trem in (6,7,8) : rlook = 6
            rlook = 9*tquot + rlook

            roffset = 0
            if rlook > 53 :
                rlook =  rlook - 54
                roffset = 54
            elif rlook > 26 :
                rlook  =  rlook - 27
                roffset = 27

            for j in row_lookup_list :
                if j[0][0] == rlook : break

            melement_solved = sudo_solver_row_match(mt,ms_udo_arr,i,j[1][0],j[1][1],roffset,order)
            if melement_solved : break
            melement_solved = sudo_solver_row_match(mt,ms_udo_arr,i,j[1][2],j[1][3],roffset,order)
            if melement_solved : break
            melement_solved = sudo_solver_row_match(mt,ms_udo_arr,i,j[1][4],j[1][5],roffset,order)
            if melement_solved : break
            melement_solved = sudo_solver_row_match(mt,ms_udo_arr,i,j[1][6],j[1][7],roffset,order)
            if melement_solved : break
            
    if melement_solved : return True
                
    return False


#Checks and populates element if single external element match in row found 
def sudo_solver_row_match(mt,ms_udo_arr,pos,j1,j2,offset,order) :

    global t
    global col_list
    global s_udo_arr

    mx = mt[pos]
    j1 = j1 + offset
    j2 = j2 + offset
    
    process_list = []
    for i in range(3) :
        if mt[j1 +i] == "" :
            process_list.append(j1+i)
    for i in range(3) :
        if mt[j2 +i] == "" :
            process_list.append(j2+i)
            
    j=0
    lastindex = 0
    for i in process_list :        
        if mx in ms_udo_arr[i] :
            lastindex = i
            j += 1
 
    if  j == 1 :
        # Row element
        if order == 0 :
            t[lastindex] = mx
            s_udo_arr[lastindex] = set(t[lastindex])         
        # Transposed col element
        else :
            k= 0
            for i1 in col_list :
                for i2 in i1 :
                    if lastindex == i2 :
                        break
                    k +=1
                if lastindex == i2 : break
            t[k] = mx
            s_udo_arr[k] = set(t[k])         
        return True

    return  False


def sudo_solver_chkpnt() :
    global t
    global t_chk
    global s_udo_arr
    global s_ckpt
    global s_all
    
    mstat = 0
    s_ckpt = []

    #Take Checkpoint
    for i in range(81) : t_chk[i] = t[i]

    i = sudo_solver_ckpt_stat0()
    if (i) : return 2
    
    while mstat != 1 :
        #Restore Checkpoint
        for i in range(81) : t[i] = t_chk[i]
        for i in s_ckpt : t[i[0]] = i[2]
        for i in range(81) :
            if t[i] == "" : s_udo_arr[i] = s_all
            else : s_udo_arr[i] = set(t[i])

        #s_debug()
        mstat = sudo_solver_engine()
        #solved
        if mstat == 1 : return 1
        
        #s_debug()
        if mstat == 0 :
            i = sudo_solver_ckpt_stat0()
            if (i)  : return 2
            continue
        else :
            i = sudo_solver_ckpt_stat1()
            if (i)  : return 2
            continue

    return False


#Begins new set of iteration with possible value of unsolved element 
def sudo_solver_ckpt_stat0() :
    global t
    global s_udo_arr
    global s_ckpt
    
    mlenmin = 100
    #Get uncomputed element, with least possible values
    for ndx, i in enumerate(s_udo_arr) :
        mlen =  len(i)     
        if  mlen > 1 and mlen < mlenmin :
            mndx = ndx
            mlenmin = mlen
            for j in i :
                mfirstval = j
                break
    if mlenmin == 100 :
        s_debug()
        print ("Warning: Array to assign exhausted")
 
    s1=[]
    s1.append(mndx)
    s1.append(list(s_udo_arr[mndx]))
    s1.append(mfirstval)
    s_ckpt.append(s1)
    
    t[mndx] = mfirstval
    s_udo_arr[mndx] = set(t[mndx])
    
    return False


#Iterates with next posible data for solution, excluding previous one
def sudo_solver_ckpt_stat1() :
    global t
    global s_udo_arr
    global s_ckpt
    global s_all
 
    #Current element used was the end choice of list of possibilities  
    mend_choice = True
    while  mend_choice :
        #last sublist
        s_ckpt_data = s_ckpt[-1:][0]
        
        #If possible values of an element checked and exhausted, pop and exclude it.
        if (s_ckpt_data[1][-1] == s_ckpt_data[2]) :
            tndx =   s_ckpt_data[0]  
            t[tndx] = ""
            s_udo_arr[tndx] = s_all
            s_ckpt.pop()
            if not s_ckpt: return True
        else :
            mend_choice = False          
        
    s_ckpt_data = s_ckpt[-1:][0]
                         
    mfound =  False
    msetdatapresent = False

    for i in s_ckpt_data[1] :
        if i == str(s_ckpt_data[2]) :
            mfound = True
            continue
        if mfound :
            msetdatapresent = True
            ndx = s_ckpt_data[0]
            t[ndx] = i
            s_udo_arr[ndx] = set(t[ndx])
            s_ckpt[-1][2] = i
            break
        
    if not mfound  or not msetdatapresent :
        print("Warning: Invalid set data creation")
        return True
 
    return False


def sudo_solver_validate() :
    
    #Invalid Data, Can arise during iterative check
    if (sudo_solver_invalid()) : return 2
    
    if (sudo_solver_solved() ) :
        print ("Sudoku solved !")
        return 1
    
    return 0      


def sudo_solver_invalid() :
    global t
    global master_row_col_grid_list

    #Count occurance of element in row/col/mimigrid  ,shoul be 0 or 1            
    for i in master_row_col_grid_list :
        t_count = [0 for i in range(10)]
        for j in i :
            if  (t[j] != "") :
                k = int(t[j])
                t_count[k] += 1
                
        for j in range(1,10)  :
             if t_count[j] > 1 : return True
             
    #Exclusion processing left no possible values of element
    for i in range(0,81)  :
            if not(s_udo_arr[i]) : return True
            
    return False


def sudo_solver_solved() :
    global t
    for i in range(81) :
        if t[i] == "" : return False
    return True


def s_debug() :
    global t

    for i in range(9) :
        for j in range(9) :
            k = i*9 +j
            if t[k] == "" : print(" ", end="|")
            else : print(t[k], end="|")
            if j == 8 : print(" ")
    print("===========================")
    return            

