import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("..\Anaconda2\Lib\site-packages\\matplotlib")

def plot_bar(gen,avail_list,bal_list,name):             #plotting bar graph

    if gen=='Male':
            label=['CL\n(Casual leave)','SL\n(Sick leave)','EL\n(Earn leave)','PDL\n(Physical disability leave)','PL*\n(Privilage leave)']
    elif gen=='Female':
        
        label=['CL\n(Casual leave)','SL\n(Sick leave)','EL\n(Earn leave)','PDL\n(Physical Disability leave)','ML*\n(Maternity leave)','CC*\n(Child care leave)']
    max1=max(avail_list)
    max2=max(bal_list)
    if max1>=max2:
        fmax=max1
    else:
        fmax=max2
    
    x=np.arange(len(label))
    plt.bar(x,avail_list,color='red',align='center',width=0.35)
    plt.bar(x+0.35,bal_list,color='green',align='center',width=0.35)
    plt.xticks(x+0.15,label,fontsize=15)
    name1= name+'-Leave graphs'
    plt.title(name1,fontsize=15)
    plt.xlabel('\nType(* Special leaves per kid)',fontsize=15)
    plt.ylabel('Number of leaves',fontsize=15)
    plt.legend(['Availed','Balance'])
    plt.xlim(-0.5,len(x))
    plt.ylim(0,fmax+5)
    plt.grid(axis='y',linestyle='--',color='black')
    for a,b in zip(x,avail_list):
        plt.text(a,b+0.5,str(b),fontsize=15,horizontalalignment='center',bbox=dict(facecolor='white',alpha=0.5))
    for a,b in zip(x,bal_list):
        plt.text(a+0.32,b+0.5,str(b),fontsize=15,bbox=dict(facecolor='white',alpha=0.5))
    plt.show()


