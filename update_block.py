import datetime 
import csv
import plot_graph 

now=datetime.datetime.now()

def update_block(id1,name1,gen1,total1,avail_list1,bal_list1,index1):       #Main update block
    global name,gen,bal_list,index,avail_list,Id,total_list                 #Globalising the variables
    Id=id1
    index=index1
    total_list=total1                                               
    avail_list=avail_list1
    name=name1
    gen=gen1
    bal_list=bal_list1
    update()

def update_spl_leaves(t_leave):                                             #Updating record for special leaves
    if t_leave=='pl':
        leaves[index+1][0]=int(leaves[index+1][0])-1
       
    elif t_leave=='ml':
        leaves[index+1][0]=int(leaves[index+1][0])-1

    else:
        leaves[index+1][1]=int(leaves[index+1][1])-1

    key=open('s_leaves.csv','wb')
    writer=csv.writer(key) 
    for i in range(len(leaves)):
        writer.writerow(leaves[i]) 
    key.close()        

def leave_update(l_type,ref):                                               #Updating the main record(i.e.,login.csv)    global leaves
    leaves=[]
    key=open('s_leaves.csv','rb')
    reader=csv.reader(key)
    for row in reader:
        leaves.append(row)
    if ref in [1,2,3,4]:
        bal_list[ref-1]-=nod
        avail_list[ref-1]+=nod
                                            
    elif ref==5:
        if int(leaves[index+1][0])>0 and int(leaves[index+1][0])!=1:
            avail_list[4]+=15
        else: 
            avail_list[4]+=15
            bal_list[4]-=15
        update_spl_leaves('pl')
        
    elif ref==6:
        if int(leaves[index+1][0])>0 and int(leaves[index+1][0])!=1:
            avail_list[4]+=90
            
        else:
            avail_list[4]+=90
            bal_list[4]-=90
        update_spl_leaves('ml')
        
    elif ref==7:
        if int(leaves[index+1][1])>0 and int(leaves[index+1][1])!=1:
            avail_list[5]+=30
            
        else:
            avail_list[5]+=30
            bal_list[5]-=30
        update_spl_leaves('cc')
        
    key.close()
    f_open=open('login.csv','rb')
    reader=csv.reader(f_open)
    l=[]
    
    for row in reader:
        l.append(row)
    
    f_open.close()
    final_list=[]
    for k in range(len(total_list)):
        final_list.append(total_list[k])
        final_list.append(avail_list[k])
        final_list.append(bal_list[k])
       
    for k in range(4,len(avail_list)):
        final_list.append(avail_list[k])
        final_list.append(bal_list[k])

    if gen=='Male':
        for i in range(4):
            final_list.append(0)
            
    elif gen=='Female':
        temp=[]
        for i in range(12):
            temp.append(final_list[i])
        temp.append(0)
        temp.append(0)
        for i in range(12,len(final_list)):
                temp.append(final_list[i])
        final_list=temp
        
    for i in range(5,len(l[index+1])):
        l[index+1][i]=final_list[i-5]
    
    f_open=open('login.csv','wb')
    writer=csv.writer(f_open)
    for i in range(len(l)):
        writer.writerow(l[i])
    f_open.close()
    
    option=raw_input('\nDo you want to confirm your leave?(y/n): ')    
    if option=='y' or option=='Y' or option=='Yes' or option=='yes' or option=='YES':
        plot_graph.plot_bar(gen,avail_list,bal_list,name)
        leave_record()
        leave_page()
    else:
        exit_page(name,1)
    
def leave_page():                                           #final leave page
    for i in range(20):
        print '\n'
    print 'Leave has been updated..!!'
    if ref==2 and nod>=3:
        print '\nPlease submit your medical certificate in the office'
    
    exit_page(name,1)
    

def leave_record():                                     #Storing the leave data in our data base
    key=open('leave_record.csv','rb')  
    reader=csv.reader(key)
    f_open=open('leave_record.csv','ab')
    writer=csv.writer(f_open)
    row=next(reader)
    sno=[]
    try:
        for row in reader:
            sno.append(int(row[0]))
        max_sno=max(sno)    
    except:
        max_sno=0
    l=[max_sno+1,Id,name,leave_type,From,To,now]
    writer.writerow(l)
    f_open.close()
    key.close()
    
def update():                                               #Updatee page
         try:
                 print '\n\t\t\tSelect the type of leave'
                 option1=int(input('\n1.Normal leave\n2.Special leave\n3.exit\noption: '))
                 if option1==3:
                     exit_page(name,1)
                     
                 elif option1== 1:
                         option2=int(input('\n1.CL(Casual leave-Max 2 per leave)\n2.SL(Sick leave-Max 2 with medical certificaate 3)\n3.EL(Earn leave-Jan to June or July to December)\n4.PDL(Physical disability leave)\noption: '))
                         leave(option1,option2)
                 elif option1== 2:
                            if gen=='Male':
                                option2=int(input('1.PL(Previlage leave)\noption: '))
        
                            else:
                                option2=int(input('1.ML(Maternity leave)\n2.CC(Childcare leave)\noption: '))
                 
                            leave(option1,option2)
                 else:
                     print '\nInvalid option...!!'
                     option=exit_page(name,0)
                     if option:
                         update()

              
         except:
                     print '\nSomething went wrong..!!'
                     option=exit_page(name,0)
                     if option==True:
                         update()

def leave(option1,option2):                             #checking the validity for the requested leaves
         global nod,leave_type,ref
         nod=int(input('Enter the number of days: '))
         value= check_ft()
         f= datetime.date(f_year,f_mon,f_day)           #checking the number of days chosen is equal to the difference
         t= datetime.date(t_year,t_mon,t_day)           #between from and to dates
         difference= t-f
         if (nod>1 and difference.days==nod-1) or (nod==1 and difference.days==0) :
                     if value==True:
                         val,leave_type,ref= check_avail(option1,option2,nod)
                         if val == 1:
                             leave_update(leave_type,ref)
                         elif val==2:
                             print '\nInvalid option..!'
                             option=exit_page(name,0)
                             if option:
                                 leave(option1,option2)
                         elif val==0:
                            print '\nNot enough days or Max crossed'
                            option=exit_page(name,0)                           
                            if option:
                                leave(option1,option2)
                         else:
                            print '\nSorry couldn\'t update. Something went wrong..!'
                            option=exit_page(name,0)
                            if option:
                                leave(option1,option2)
                     else:
                         print '\nInvalid From and To dates..!'
                         option=exit_page(name,0)
                         if option:
                             leave(option1,option2)
                             
                

         else:
             print '\nNumber of days given and difference between the dates are not equal..!!'
             option=exit_page(name,0)
             if option:
                 leave(option1,option2)
             

                               



def exit_page(name,i):                                  #Exiting from the code
    while True:
        if i==0:
            option=raw_input('Try once again(y/n)?\ny=Yes\tn=Exit\noption:')
            if option=='y' or option=='Y' or option=='Yes' or option=='yes' or option=='YES':
                return True
                break
            elif option=='n' or option=='N' or option == 'NO' or option=='No' or option =='no':
                if name==None:
                    print 'Thank you. Have a nice day..!!'
                else:
                    print 'Thank you',name,'.Have a nice day..!!'
                break
                exit
        else:
            print 'Thank you',name,'.Have a nice day.!!'
            break
            exit


def check_avail(opt1,opt2,nod):                         # checking the availability of different leaves
    if opt1==1:
        if opt2==1:
            if nod<=bal_list[0] and nod<=2:
                    return 1,'CL',1
            else:
                return 0,0,0
                
        elif opt2==2:
            if nod<=bal_list[1] and nod<=3:
                return 1,'SL',2
            elif nod<bal_list[1] and nod>=3:
                print '\nMaximum 3 days without medical certificate'
                option = raw_input('Do you have medical certificate(y/n): ')
                if option=='y' or option=='Y' or option=='Yes' or option=='yes':
                    return 1,'SL',2
            else:
                return 0,0,0
                
        elif opt2==3:
          months1=[1,2,3,4,5,6]
          months2=[7,8,9,10,11,12]
          if nod<=bal_list[2] and nod<=15:  
             if From[1] in months1 and To[1] in months1:
                 return 1,'EL',3
             elif From[1] in months2 and To[1] in months2:
                 return 1,'EL',3
             else:
                 return 0,0,0
          else:
              return 0,0,0
              

        elif opt2==4:
            if nod<=bal_list[3]:
                    return 1,'PDL',4
            else:
                return 0,0,0            
            
        else:
            return 2,2,2
        
        
    else:
        if gen=='Male':
            if nod<=bal_list[4]:
                return 1,'PL',5
            else:
                return 0,0,0
        
        if gen=='Female':
            if opt2==1:
                if nod<=bal_list[4]:
                    return 1,'ML',6
                else:
                    return 0,0,0
            
            elif opt2==2:
                if nod<=bal_list[5]:
                    return 1,'CC',7
                else:
                    return 0,0,0

            else:
                return 2,2,2             
                    
            

def check_ft():                                     # Checking the from and to dates
    try:
        global f_day,f_mon,f_year,t_day,t_mon,t_year
        print '\nPlease enter the FROM and TO dates:'
        print '\nCaution:If day or month is 08 or 09 just type 8 or 9 only..!!'
        print '\nFrom:'
        f_day=int(input('\tDay  : '))
        f_mon=int(input('\tMonth: '))
        f_year=int(input('\tYear: '))
        print 'To: '
        t_day=int(input('\tDay  : '))
        t_mon=int(input('\tMonth: '))
        t_year=int(input('\tYear: '))
        global From,To
        From=[f_day,f_mon,f_year]
        To=[t_day,t_mon,t_year]

        
        if From[0]<=31 and From[1]<=12 and To[0]<=31 and To[1]<=12:
                if From[2] == now.year and To[2]==now.year:
                   if From[1] >= now.month and To[1] >= From[1]:
                      if From[1]== now.month:
                         if From[0]>now.day:
                            if To[1]==now.month:
                               if To[0]>=From[0]:
                                 return True
                                 
                            else:
                                return True
                            
                    
                      else:                  
                          return True
                          
    except:
        print 'Something wrong..!!'


                          
