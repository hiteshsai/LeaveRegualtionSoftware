import csv
import datetime
import module1
import plot_graph
import update_block


def home():                                 #Home page
    while True:
        try:
            option= int(input('Select from the following\n\n1.Add a new member\n2.Faculty page for leaves\n3.Exit\n\noption:'))
            if option==1:
                return 1,1
                break
            elif option==2:
                log_id  = raw_input('Enter your ID    : ')
                gen     = raw_input('Enter your Gender: ')
                if gen=='Male' or gen=='M' or gen=='m' or gen=='male':
                    log_gen='Male'
                elif gen=='Female' or gen=='F' or gen=='f' or gen=='female':
                    log_gen='Female'
                else:
                    log_gen='other'
                return log_id,log_gen
            elif option==3:
                return 0,0
                break
            else:
                print '\nInvalid option..!!'
        except:
             print '\nInvalid option..!!'



def login(Id,gender):                   #checking for valid ID and Gender
     if Id in idlist:
        if gender in genderlist:
            for i in range(len(idlist)):
                if Id==idlist[i]:
                    break

            if gender== genderlist[i]:
                    return 1,i      # Both are present
            else:
                    return 2,2      # gender doesn't match
        else:
             return 2,2             # gender doesn't match

     else :
        return 0,0                  # Not registered


def admin():                                #checking Administrator name and password
    print '\n\t\t\t\tADMINISTRATOR(Confidential)'
    admin_name =raw_input('Enter Admin name:     ')
    admin_pass =raw_input('Enter Admin password: ')
    
    f_open =open('CSV_Files/admin.csv','rb')
    reader= csv.reader(f_open)
    name=[]
    pas=[]
    for row in reader:
        name.append(row[0])
        pas.append(row[1])
    if admin_name in name and admin_pass in pas:
        for i in range(len(name)):
            if admin_name==name[i]:
                break
        if pas[i]==admin_pass:
              return True
    else:
        return False
    

def add_mem():                          #Adding a new member after checking the Admin's permission
    c=3
    while True:
        val= admin()
        if val==True:
            f_open =open('CSV_Files/login.csv','ab')
            writer = csv.writer(f_open)
            print '\nHello sir!'
            ID = raw_input('Enter the ID                         : ')   
            while ID in idlist:                                          #checking for unique ID
                print 'ID already exists.Please enter a different ID'
                option=raw_input('Try once again(y/n)')
                if option=='y' or option=='Y' or option=='Yes' or option=='yes':
                    ID = raw_input('Enter the ID                         : ')
                else:
                    break
            
            name=raw_input('Enter the Name                       : ')
            gen=raw_input('Enter the gender                      : ')
            if gen=='Male' or gen=='M' or gen=='m' or gen=='male':
                gender='Male'
            elif gen=='Female' or gen=='F' or gen=='f' or gen=='female':
                gender='Female'
            else:
                gender='other'

            while True:                        
                    doj=raw_input('Enter the Date of Joining (dd-mm-yyyy): ')   
                    
                    val=check_doj(doj)                              #checking for valid date of joining
                    if val==True:
                        DOJ=doj
                        total_list= recordnew(DOJ,gender)           #calling function for calculating the leaves
                        f_open=open('CSV_Files/login.csv','rb')
                        reader=csv.reader(f_open)
                        row=next(reader)
                        sno=[]
                        for row in reader:
                            sno.append(int(row[0]))
                        max_sno= max(sno)
                        
                        l=[max_sno+1,ID,name,gender,DOJ]
                        
                        for i in total_list:                    #writing the record into the .csv file
                            l.append(i)
                        writer.writerow(l)
                        f_open.close()
                        key=open('CSV_Files/s_leaves.csv','ab')
                        writer=csv.writer(key)
                        if gender=='Male':
                            sleaves=[2]
                        elif gender=='Female':
                            sleaves=[2,2]
                        writer.writerow(sleaves)
                        key.close()                  
                        
                        print 'Thankyou.',name,'has been added to the list'
                        option=raw_input('Go to the HOMEPAGE(y/n)\noption: ')
                        if option=='y' or option=='Y' or option=='Yes' or option=='yes':
                            main()
                        else:
                            exit
                        break
                        break
                        
                    else:
                        option=raw_input('Do you want to exit? (y/n)')
                        if option=='y' or option=='Y' or option=='Yes' or option=='yes':
                            print '\n Thank you sir. Have a nice day..!!'
                            break
                            break
                            exit
        
            break
            
        else:
            c-=1                                    #If the admin name and password didn't match
            print '\nWrong Credentials..!!',c,'chance(s) left'
            if c==0:
                print 'Sorry, Maximum tries reached. ABORTING..!!'
                break
        exit
def recordnew(doj,gender):                              #calculating leaves for new member
    if now.year == int(doj[6]+doj[7]+doj[8]+doj[9]):
        month=int(doj[3]+doj[4])
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
    if gender=='Male':
        total=[cl,0,cl,sl,0,sl,el,0,el,pdl,0,pdl,0,pl,0,0,0,0]
    elif gender=='Female':
        total=[cl,0,cl,sl,0,sl,el,0,el,pdl,0,pdl,0,0,0,ml,0,cc]
   
    return total
    
    
def record(index):                              #segregating the leaves into availed and balance leaves
    global avail_list,bal_list,total_list
    f_open=open('CSV_Files/login.csv','rb')
    reader=csv.reader(f_open)
    row=next(reader)
    l=[]
    avail_list1=[]
    bal_list1=[]
    avail_list=[]
    bal_list=[]
    total_list=[]
    for row in reader:
        l.append(row)
        
    for i in range(5,15,3):                         #Total leaves alloted
        total_list.append(int(l[index][i]))        
                                                    #common leaves
    for i in range(6,16,3):
        avail_list1.append(int(l[index][i]))
    for i in range(7,17,3):
        bal_list1.append(int(l[index][i]))
   
    for i in range(17,22,2):                        #special leaves
        avail_list1.append(int(l[index][i]))
    for i in range(18,23,2):
        bal_list1.append(int(l[index][i]))

    for i in range(4):
            avail_list.append(avail_list1[i])
            bal_list.append(bal_list1[i])
    if gen=='Male':
        avail_list.append(int(avail_list1[4]))
        bal_list.append(int(bal_list1[4]))
    elif gen=='Female':
        for i in range(5,7):
            avail_list.append(int(avail_list1[i]))
            bal_list.append(int(bal_list1[i]))
        

def fac_page():                                         #Faculty page: For information of leaves
    while True:
            print '\nHello',name,'..!!'
        
            option = int(input('\n1.Query mode\n2.Update mode\n3.Exit\n\noption:'))
            
            if option==3:
                break
                exit
            
            if option==1:
                query()
                break
           
            elif option==2:
                record(index)
                update_block.update_block(ID,name,gen,total_list,avail_list,bal_list,index) #updating the record

                break
            else:
                print 'Invalid option1..!!'
                option2=raw_input('Do you want to exit?(y/n):')
                if option2=='y' or option2=='Y' or option2=='Yes' or option2=='yes':
                    print 'Thankyou',name,'Have a nice day..!!'
                    break


def check_doj(doj):                 #function to check for valid date of joining
       try:
         if len(doj)==10: 
            if int(doj[0]+doj[1])<=31:
                if int(doj[3]+doj[4])<=12:
                    if int(doj[6]+doj[7]+doj[8]+doj[9])<=now.year:
                            if int(doj[3]+doj[4])==2:
                                if int(doj[0]+doj[1])<=29:
                                    return True
                                else:
                                    print 'February doesn\'t have more than 29 days'
                                    return False
                            else:
                                return True
                    else:
                        print 'Year can\'t be more than',now.year
                        return False
                else:
                    
                    print 'Months can\'t be more than 12 or Can\'t exceed current month'
                    return False

            else:
                print 'Days can\'t be more than 31'
                return False
         else:
             print 'Invalid date of joining'
             return False

       except:
            print 'Invalid Date of Joining'
            return False





def query():                                    #To display bar graph of the leaves 
    record(index)
    plot_graph.plot_bar(gen,avail_list,bal_list,name)
     
"""
    #The following statements shouldn't be used in Spyder. If running in cmd or other python 
    #console they can be un commented..!!

    option=raw_input('Do you want to update the record?(y/n): ')
    if option=='y' or option=='Y' or option=='Yes' or option=='yes':
               update_block.update_block(ID,name,gen,total_list,avail_list,bal_list,index)
    else:
        print 'Thank you',name,'. Have a nice day.!!'
        exit

"""  
def exit_page(name):                               #Exiting from the code
    while True:
        option=raw_input('Try once again(y/n)\ny=Yes\tn=Exit\noption:')
        if option=='y' or option=='Y' or option=='Yes' or option=='yes' or option=='YES':
            return True
            break
        elif option=='n' or option=='N' or option == 'NO' or option=='No' or option =='no':
            if name==None:
                print 'Thankyou.Have a nice day..!!'
            else:
                print 'Thankyou',name,'.Have a nice day..!!'
            break
            exit


def main():                                         #Where everything starts
        Id,gender = home()
        global idlist,namelist,genderlist,dojlist
        if Id==0:
            print 'Thank you. Have a nice day.!'
            exit
        elif Id==1:
            idlist,namelist,genderlist,dojlist = module1.reader_writer()    #for getting data from .csv file
            add_mem()
        else:
            
            idlist,namelist,genderlist,dojlist = module1.reader_writer()
            global index,ID,gen,doj,name                                    #globalising the variables
            
            val,index=login(Id,gender)
            
            ID=idlist[index]                
            gen=genderlist[index]
            doj=dojlist[index]
            name=namelist[index]

            if val==1:
                    fac_page()
                    exit
            elif val==2:
                    print '\nID and Gender didn\'t match...'
                    option = exit_page(None)
                    if option:
                            main()
            else:
                    print '\nFaculty not registered..'
                    option=exit_page(None)
                    if option:
                            main()
now=datetime.datetime.now()                                 #Main function
print '\t\t\tWelcome to LEAVE AUTOMATION software'
main()
