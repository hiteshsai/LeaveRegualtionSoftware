import csv 
import datetime


def reader_writer():                            #Function to read the data from csv files
    f_open=open('login.csv','rb')
    reader=csv.reader(f_open)
    global genderlist,dojlist
    id_list=[]
    genderlist=[]
    dojlist=[]
    name_list=[]
    l_size=[]
    row=next(reader)
    
    for row in reader:
        l_size.append(row)
        id_list.append(row[1])
        name_list.append(row[2])
        genderlist.append(row[3])
        dojlist.append(row[4])
     
    f_open.close()
    for i in range(len(l_size)):
        if len(l_size[i])==5:    
            first_update_record()
            break
    return id_list,name_list,genderlist,dojlist
    
    
def first_update_record():                      #First time updating the record
                                                #this code only runs once for the whole project  
    for i in range(len(dojlist)):
            bal_list=[]
            final_list=[]
            avail_list=[]
            total_list=[]       
            now= datetime.datetime.now()
            if now.year == int(dojlist[i][6]+dojlist[i][7]+dojlist[i][8]+dojlist[i][9]):
                month=int(dojlist[i][3]+dojlist[i][4])     
                cl=(13-month)*8/12
                sl=(13-month)*10/12
                el=(13-month)*30/12
                pdl=(13-month)*24/12
            else:
                cl=8
                sl=10
                el=30
                pdl=24
            pl=15
            ml=90
            cc=30
            
            if genderlist[i]=='Male':
                total_list=[cl,sl,el,pdl,pl,0,0]
                avail_list=[0,0,0,0,0,0,0]
                slist=[2]
                
            elif genderlist[i]=='Female':
                total_list=[cl,sl,el,pdl,0,ml,cc]
                avail_list=[0,0,0,0,0,0,0]
                slist=[2,2]
                
            for k in range(len(total_list)):
                    bal_list.append(total_list[k]-avail_list[k])
            
            for k in range(len(total_list)-3):
                final_list.append(total_list[k])
                final_list.append(avail_list[k])
                final_list.append(bal_list[k])
                    
            for k in range(3):
                final_list.append(0)
                final_list.append(total_list[k+4])
                
               
            f_open=open('login.csv','rb')
            reader=csv.reader(f_open)
            l=[]
            for row in reader:
                l.append(row)
                
            f_open.close()
            
            for j in range(len(final_list)):
                    l[i+1].append(final_list[j])
            
            f_open=open('login.csv','wb')
            writer=csv.writer(f_open)
            
            for i in range(len(l)):
                writer.writerow(l[i])
            f_open.close()
            
            f_open1=open('s_leaves.csv','ab')               #updating information of special leaves
            writer=csv.writer(f_open1)
            writer.writerow(slist)
            f_open.close()
      
            
    