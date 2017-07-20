from Tkinter import * #for gui
import MySQLdb
#import mysql.connector #for database connectivity
import unittest #for shamir library
from SSSA import sssa #for shamir library
import random # for random number generation
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np



### Main GUI frame
root=Tk(); 
counts=0


####### Secret sharing Library used
sss=sssa();

######################################################################################################################################################
##########################################             FUNCTIONS                ######################################################################
######################################################################################################################################################
    
########################################
####### this function will close gui 
########################################
def close(frame):
    frame.destroy()

#####   Start connection with mysql     ###############
#con=mysql.connector.connect(user="root",password="",host="localhost",database="test")
def databases(name,password):
    name=str(name)
    password=str(password)
    global con
    global cur,totalStates,tables,states,statesName,totalStates,varState
    try:
        con=MySQLdb.connect("localhost","root",password,name );
        #con=mysql.connector.connect(user="root",password="",host="localhost",database="test")

        cur=con.cursor()

        ########## total states
        cur.execute("SELECT COUNT(*) From state");
        fetch=cur.fetchone();
        totalStates=int(fetch[0])
        
        ######States are available
        cur.execute("SELECT * FROM state");
        tables=cur.fetchone()

            
        states=[None]*(totalStates);
        statesName=[None]*(totalStates);
        totalState=len(statesName);
        varState=[None]*totalState;
        i=0;
        while tables is not None:
            states[i]=tables[1]
            statesName[i]=tables[1]
            i=i+1;
            tables=cur.fetchone()

        return 0;
    except MySQLdb.Error, e:
        print MySQLdb.Error;
        create=Tk();
        create.title("error");
        Label(create,text="please check database name \nand password",font=("Times", 20),fg="red").pack()
        Button(create,text="OK",command=lambda:close(create),fg="red").pack();
        create.geometry("400x100");
        create.mainloop();
        return 1;



########################################
####
#### this function will extract the clusters from encrpyted cluster and make the new cluster
####            parameters: 
####                        1) cluster: what type of cluster we want to extract
############################

def getInfo(cluster):

    
    ####    state cluster array
    statePopulation=[None]*(totalStates);
    ####    total population initially
    totalPopulation=0;

    total=0
    maxState=None
    minState=None
    
    ####    change to string
    cluster=str(cluster)
    c=0;
    #####loop run for all the states
    for stat in states:
        curM=con.cursor()

        #### extract the minimum key require to decrypt the encrypted cluster 
        query="SELECT number FROM minkey"+stat;
        #print query+"-"
        
        curM.execute(query);
        minS=curM.fetchone();
        ### if minimum key is not there means no cluster and if minimum key then cluster is there
        if(minS!=None):
            #print minS;
            curS=con.cursor()

            #### query to find in the state from which we find cluster
            query="SELECT state FROM sharestate_"+stat+"";
            curS.execute(query);
            shareCount=0;
            #print totalStates;
            ###shareState is array which store all the share state
            shareState=[None]*(totalStates);
            table=curS.fetchone()
            while(table):
               # #print table[0];
                shareState[shareCount]=table[0];
                shareCount=shareCount+1;
                table=curS.fetchone()
            ##print shareCount;
            #print query;

            # this will generate minS random number for the selection of state from which we unlock the cluster information
            selectS=random.sample(range(0,(shareCount) ), int(minS[0]))
            #print selectS
            
            ## secret encrypted key array
            secret=[None]*(int(minS[0]));
            j=0;
            curS=con.cursor()
            for i in selectS:
                #print i
                ### query to find the encrypted cluster for the state
                query="SELECT keyss FROM key"+shareState[i]+" where state='"+stat+"' and cluster='"+cluster+"'";
                #print query;
                curS.execute(query);
                sec=curS.fetchone();
                #key is store in secret[j]
                secret[j]=sec[0];
                #print "llll==="+secret[j]
                j=j+1;

            ###this is a shamir secret library function 
            ### from this we extract our secret and store the secret cluster in sec
            sec=sss.combine(secret);
            
            #print str(sec)+"-----";

            ##this StatePopulation will store the cluster information of state
            statePopulation[c]=int(sec);

            ###initial conditon when first time loop run
            if(minState==None):
                minState=statePopulation[c]
            #### minState will store the minimum of cluster after each cluster    
            minState=min(minState,statePopulation[c]);
            #### maxState will store the maximum of cluster after each cluster 
            maxState=max(maxState,statePopulation[c]);
            ##TotalPopulation will store the total population after each cluster is adding
            totalPopulation=totalPopulation+statePopulation[c];
            c=c+1;

            ###counting states
            total=total+1

    #print totalPopulation

    ###this part will find average
    average=0;
    if(total!=0):
        average=totalPopulation/total;

    ##then finally return the totalpopulation ,average ,maxstate,minstate
    return totalPopulation,average,maxState,minState;



##############################################################################################################################
##############          This getAnalysis() function used for analysis phase
##############              Parameter used:
##############                              1)varPop: population checkbox is checked or not 
##############                              2)varAvg: average checkbox is checked or not
##############                              3)varMax: maximum checkbox is checked or not
##############                              4)varMin: minimum checkbox is checked or not

def getAnalaysis(varPop,varAvg,varMax,varMin,databaseNameE,databasePassE):
    ########info is new window for information which we get
    databaseNameE=databaseNameE.get();
    databasePassE=databasePassE.get();
    correct=databases(databaseNameE,databasePassE)
    correct=int(correct)
    if(correct==0):
        info=Tk()
        info.title("Analysis");
        #cluster is a type of cluster we want to knnow
        cluster="population"
        #messge is variabl which we want to display initially none
        message=""

        ####from getInfo() function we get totalPopulation,average,maxState,minState 
        totalPopulation,average,maxState,minState=getInfo(cluster)

        #checking atleast on box is checked or not
        if(varPop.get()!=1 and varAvg.get()!=1 and varMax.get()!=1 and varMin.get()!=1):
            message=message+"Atleast select one field";
        else:
            #if population is checked then add to message for display
            if(varPop.get()==1):
                message=message+"total population="+str(totalPopulation);
            #if Average is checked then add to message for display
            if(varAvg.get()==1):
                message=message+"\nAverage Population="+str(average)
            #if Maximum is checked then add to message for display
            if(varMax.get()==1):
                message=message+"\nMax="+str(maxState)
            #if Minimum is checked then add to message for display
            if(varMin.get()==1):
                message=message+"\nMin="+str(minState);

        #gui of new window with information
        Label(info,font=("Times", 20),text=message).pack()
        Button(info,font=("Times", 20),text='ok',bg='red',command=lambda:close(info)).pack(side=BOTTOM)
        info.geometry("400x200")
        info.mainloop()

##############################################################################################################################
##############          This getAMiningInfo() function used for analysis phase
##############              Parameter used:
##############                              1)varRadio: store which radio button is selected 

def getMiningInfo(varRadio,databaseNameE,databasePassE):
    databaseNameE=databaseNameE.get();
    databasePassE=databasePassE.get();

    check=databases(databaseNameE,databasePassE)
    check=int(check)
    if(check==0):
        select=int(varRadio.get())
        #if gender is selected
        if(select==1):

            cluster="genderMale"
            #get male combine cluster
            totalMale,average,maxState,minState=getInfo(cluster)


            cluster="genderFemale"
            #get female combine cluster
            totalFemale,average,maxState,minState=getInfo(cluster)


            # Data to plot
            
            labels = 'Male', 'Female'
            sizes = [totalMale, totalFemale]
            colors = ['gold', 'yellowgreen']
            explode = (0, 0)
     
            # Plot pichart
            
            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
            
           
            plt.axis('equal')
            #message="male/female\nmale="+str(totalMale)+"\nfemale="+str(totalFemale);
            plt.title("Male/Female");
            plt.show()




            
            #if gender is selected
        elif(select==2):

            cluster="bpl"
            #get bpl combine cluster
            bpl,average,maxState,minState=getInfo(cluster)

            cluster="middleclass"
            #get middleclass combine cluster
            middleclass,average,maxState,minState=getInfo(cluster)

            cluster="richclass"
            #get richclass combine cluster
            richclass,average,maxState,minState=getInfo(cluster)



            #message="bpl="+str(bpl)+"\nmiddleclass="+str(middleclass)+"\nrichclass="+str(richclass);
               # Data to plot

            labels = 'Bpl' , 'Middleclass','Richclass' #
            sizes = [bpl,middleclass,richclass]#, 245, 210]
            colors = ['gold', 'yellowgreen', 'lightcoral']#, 'lightskyblue']
            explode = (0,0,0)#, 0)  # explode 1st slice
     
            # Plot pichart
            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
     
            plt.axis('equal')
            plt.title("Income");
            plt.show()



        elif(select==3):

            cluster="youngage"
            #get youngage combine cluster
            youngage,average,maxState,minState=getInfo(cluster)
            


            cluster="teenage"
            #get teenage combine cluster
            teenage,average,maxState,minState=getInfo(cluster)


            cluster="adultage"
            #get adultage combine cluster
            adultage,average,maxState,minState=getInfo(cluster)

            
            cluster="middleage"
            #get middleage combine cluster
            middleage,average,maxState,minState=getInfo(cluster)

            
            cluster="oldage"
            #get oldage combine cluster
            oldage,average,maxState,minState=getInfo(cluster)

            # Data to plot
            labels = 'Childhood' , 'Adolescence','Young_Adult','Adult','Elderly' #
            sizes = [youngage,teenage,adultage,middleage,oldage]#, 245, 210]
            colors = ['gold', 'yellowgreen', 'lightcoral','lightskyblue','red']
            explode = (0,0,0,0,0)  # explode 1st slice
     
            # Plot pichart
            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
     
            plt.axis('equal')
            plt.title("Age");
            plt.show()



##############################################################################################################################################################
##############          This checked() used in analysis phase for particulat state it check which state is checked and according to this generate information
##############              Parameter used:
##############                              1)varPop: population checkbox is checked or not 
##############                              2)varAvg: average checkbox is checked or not
##############                              3)varMax: maximum checkbox is checked or not
##############                              4)varMin: minimum checkbox is checked or not


def checked(varPop,varAvg,varMax,varMin,*varState):
    ###information window create
    info=Tk()
    info.title("Analysis")

    c=0;
    ###statePopulation is array for state popluation cluster
    statePopulation=[None]*(totalStates);
    totalState=len(statesName);
    totalPopulation=0;
    total=0;
    maxState=None
    minState=None

    ###this loop checking for all state if it checked then do operation
    for i in range(0,totalState):
        #print statesName[i]+"  "+str(varState[i].get())

        ##check state is checked or not
        if(varState[i].get()==1):
            #print statesName[i];
            curM=con.cursor()
            ## query to obtain minimum key
            query="SELECT number FROM minkey"+statesName[i];
            curM.execute(query);
            minS=curM.fetchone();

            #if minkey is there then the must have secret 
            if(minS!=None):
                #print minS;
                curS=con.cursor()

                ### obtain the state which have the key to unlock
                query="SELECT state FROM sharestate_"+statesName[i]+"";
                curS.execute(query);
                shareCount=0;
                shareState=[None]*(totalStates);
                table=curS.fetchone()
                
                ### put all the state which have in array shareState for the stateName[i]
                while(table):
                    #print table[0];
                    shareState[shareCount]=table[0];
                    shareCount=shareCount+1;
                    table=curS.fetchone()
                #print shareCount;
                #print query;

                #genereate random number equal to minimum key
                selectS=random.sample(range(0,(shareCount) ), int(minS[0]))
                #print selectS

                ##Secret is array to obtain secret
                secret=[None]*(int(minS[0]));
                j=0;

                curS=con.cursor()

                ##### loop for state which having a key and selectS is random number for the state which having a key
                for k in selectS:

                    ##query to obtain a key for stateName[i]
                    query="SELECT keyss FROM key"+shareState[k]+" where state='"+statesName[i]+"' and cluster='population'";
                    print query;
                    curS.execute(query);
                    sec=curS.fetchone();
                    #store key in secret[j]
                    secret[j]=sec[0];
                    #print "llll==="+secret[j]
                    j=j+1;

                #get result by passing all the key
                statePopulation[c]=int(sss.combine(secret));
                
                if(minState==None):
                    minState=statePopulation[c]
                
                minState=min(minState,statePopulation[c]);
                maxState=max(maxState,statePopulation[c]);
                totalPopulation=totalPopulation+statePopulation[c];
                c=c+1;

            total=total+1
    
    #print totalPopulation
    average=0;
    #messge is variabl which we want to display initially none
    message=""
    if(total!=0):
        average=totalPopulation/total;

    #checking atleast on box is checked or not
    if(varPop.get()!=1 and varAvg.get()!=1 and varMax.get()!=1 and varMin.get()!=1):
        message=message+"Atleast select one field";
    else:
        #if population is checked then add to message for display
        if(varPop.get()==1):
            message=message+"total population="+str(totalPopulation);
        #if Average is checked then add to message for display
        if(varAvg.get()==1):
            message=message+"\nAverage Population="+str(average)
        #if Average is checked then add to message for display
        if(varMax.get()==1):
            message=message+"\nMax="+str(maxState)
        #if Average is checked then add to message for display 
        if(varMin.get()==1):
            message=message+"\nMin="+str(minState);

    #gui of new window with information
    Label(info,font=("Times", 20),text=message).pack()
    Button(info,font=("Times", 20),text='ok',bg='red',command=lambda:close(info)).pack(side=BOTTOM)
    info.geometry("400x200")
    info.mainloop()


##############################################################################################################################################################
##############          multiState() function used checked() function used in analysis phase for particulat state to check 
##############          which state is checked and according to this generate information
##############              Parameter used:
##############                              1)frame1: is root frame
##############                              2)window: frame in where this checked state is placed
##############                              3)varPop: population checkbox is checked or not 
##############                              4)varAvg: average checkbox is checked or not
##############                              5)varMax: maximum checkbox is checked or not
##############                              6)varMin: minimum checkbox is checked or not

global text;
def multiState(frame1,window,varPop,varAvg,varMax,varMin,databaseNameE,databasePassE):
    databaseNameE=databaseNameE.get();
    databasePassE=databasePassE.get();
    databases(databaseNameE,databasePassE);
    global counts
    global text;
    #for scrolling effect
    vsb=Scrollbar(frame1,orient="vertical")

    #for checkbox state we put all in text
    text=Text(width=20,height=10,yscrollcommand=vsb.set)
    #this if is for if more than multistate button is clicked then only first time it will display states
    if(counts==0):
        totalState=len(statesName);


        ##adding some property in scrollbar
        vsb.config(command=text.yview)
        vsb.pack(side="right", fill="y")
        text.pack(side="bottom", fill="both", expand=True)

        ##checkbox state array
        cb=[None]*totalState

        ##checkbox state variable inforamtion array(checked or not if checked it 1 else 0)
        varState=[None]*totalState;

        #this will put checkbox atate in text
        for i in range(totalState):
            varState[i] = IntVar()
            cb[i] = Checkbutton(frame1, text=statesName[i],variable=varState[i])
            text.window_create("end", window=cb[i])
            text.insert("end", "\n") # to force one checkbox per line

        #button is added to obtain result
        click=Button(window,text="Get Result for Selected State")
        click.config(command=lambda: checked(varPop,varAvg,varMax,varMin,*varState));

        #display position
        click.grid(row=8)

        counts=1;



#################################################################################################################################################
#####################################             FUNCTION END             ######################################################################
#################################################################################################################################################

#set the window background to hex code '#a1dbcd'
root.configure(background="#a1dbcd")

window=Frame(root)
home=Frame(root)
mining=Frame(root)

root.title("central government")

countHome=0;

##################################################################################################################################
###########################             HOME                ######################################################################
##################################################################################################################################

def displayHome(home):
    global countHome;
    window.pack_forget()
    home.pack_forget()
    mining.pack_forget()
    global text
    text=Text()
    text.pack();
    text.pack_forget();
    if(countHome==0):
         x=Label(home,text="Registrar General and Census Commissioner", fg="#922b21", bg="#a1dbcd",font=("Helvetica", 30))
         info= Label(home,text="---------Under Ministry of Home Affairs, Government of India---------", fg="#922b21", bg="#a1dbcd", font=("Helvetica", 20))
         x.grid(row=0);
         info.grid(row=1);
         countHome=1;
    home.pack();

displayHome(home)



##################################################################################################################################
###########################          MINING GUI             ######################################################################
##################################################################################################################################


countMining=0;
def displayMining(mining):
    global countMining;
    window.pack_forget()
    home.pack_forget()
    mining.pack_forget()
    text.pack_forget();
    if(countMining==0):
        #Label(mining,text="Mining",font=("Helvetica", 50)).pack();
        mining.configure(background="#a1dbcd")
        x=Label(mining,text="Registrar General and Census Commissioner", fg="#922b21", bg="#a1dbcd",font=("Helvetica", 30))
        info= Label(mining,text="---------Under Ministry of Home Affairs, Government of India---------", fg="#922b21", bg="#a1dbcd", font=("Helvetica", 20))
        x.grid(row=0);
        info.grid(row=1);
        info = Label(mining,text="Mining Area:K-mean Clustering", fg="#922b21", bg="#a1dbcd", font=("Helvetica", 20))
        #and pack it into the window
        #lblInst.grid(row=0)
        info.grid(row=2)
        #create the widgets for entering a username

        frameL=Frame(mining,pady=10)
        frameL.configure(background="#a1dbcd")
        databaseNameL=Label(frameL,text="enter database name:",padx=20)
        databaseNameL.grid(row=0,column=0,sticky='W')
        databaseNameE=Entry(frameL)
        databaseNameE.grid(row=0,column=1,sticky='W')
        databasePassL=Label(frameL,text="enter database password:",padx=20)
        databasePassL.grid(row=0,column=2,sticky='E')
        databasePassE=Entry(frameL,show="*")
        databasePassE.grid(row=0,column=3,sticky='E')
        frameL.grid(row=3,sticky='W')

        frameR=Frame(mining,pady=10)
        frameR.configure(background="#a1dbcd")
        lblOption = Label(frameR,font=("Times", 25), text="Select The Options", fg="#383a39", bg="#a1dbcd")
        #and pack them into the window
        lblOption.grid(row=3)
        varRadio=IntVar()
        MaleFemaleRadio = Radiobutton(frameR,font=("Times", 24), text="Male/Female", fg="#383a39", bg="#a1dbcd",variable=varRadio, value=1)
        MaleFemaleRadio.grid(row=4,column=0,sticky='W')
        
        incomeRadio = Radiobutton(frameR,font=("Times", 24), text="Income", fg="#383a39", bg="#a1dbcd",variable=varRadio, value=2)
        incomeRadio.grid(row=5,sticky='W')
        
        ageRadio = Radiobutton(frameR,font=("Times", 24), text="Age", fg="#383a39", bg="#a1dbcd",variable=varRadio, value=3)
        ageRadio.grid(row=6,sticky='W')
        frameR.grid(row=4,sticky='W')

        #create the widgets for entering a username

        #create a button widget called btn
        btn = Button(mining, text="Get All states details", fg="#a1dbcd", bg="#383a39",command=lambda:getMiningInfo(varRadio,databaseNameE,databasePassE))
        #pack the widget into the window
        btn.grid(row=9)

        
        countMining=1;
    mining.pack();








##################################################################################################################################
###################################           ANALYSIS   GUI        ##############################################################
##################################################################################################################################






countWindow=0;
def displayWindow(window):
    global countWindow;
    window.pack_forget()
    home.pack_forget()
    mining.pack_forget()
    #text.pack_forget();
    if(countWindow==0):
        window.configure(background="#a1dbcd")

        #create a label for the instructions
        x=Label(window,text="Registrar General and Census Commissioner", fg="#922b21", bg="#a1dbcd",font=("Helvetica", 30))
        info= Label(window,text="---------Under Ministry of Home Affairs, Government of India---------", fg="#922b21", bg="#a1dbcd", font=("Helvetica", 20))
        x.grid(row=0);

        info.grid(row=1);
        frameR=Frame(window,pady=10)
        frameR.configure(background="#a1dbcd")
        databaseNameL=Label(frameR,text="enter database name:",padx=20)
        databaseNameL.grid(row=0,column=0,sticky='W')
        databaseNameE=Entry(frameR)
        databaseNameE.grid(row=0,column=1,sticky='W')
        databasePassL=Label(frameR,text="enter database password:",padx=20)
        databasePassL.grid(row=0,column=2,sticky='E')
        databasePassE=Entry(frameR,show="*")
        databasePassE.grid(row=0,column=3,sticky='E')
        frameR.grid(row=3,column=0,sticky='W')

        #create the widgets for entering a username
        lblOption = Label(window,font=("Times", 35), text="Select The options", fg="#383a39", bg="#a1dbcd")
        #and pack them into the window
        lblOption.grid(row=4)
        

        frameL=Frame(window)
        frameL.configure(background="#a1dbcd",width=100)
        varPop=IntVar()
        populationCheck = Checkbutton(frameL,font=("Times", 25), text="population", fg="#383a39", bg="#a1dbcd",variable=varPop)
        populationCheck.grid(row=0,column=0,sticky='W')
        varAvg=IntVar()
        averageCheck = Checkbutton(frameL,font=("Times", 24), text="Average", fg="#383a39", bg="#a1dbcd",variable=varAvg)
        averageCheck.grid(row=1,sticky='W')
        varMax=IntVar()
        maxCheck =Checkbutton(frameL,font=("Times", 24), text="Maximum", fg="#383a39", bg="#a1dbcd",variable=varMax)
        maxCheck.grid(row=2,sticky='W')
        varMin=IntVar()
        minCheck = Checkbutton(frameL,font=("Times", 24), text="Minimum", fg="#383a39", bg="#a1dbcd",variable=varMin)
        minCheck.grid(row=3,sticky='W')
        frameL.grid(row=5,column=0,sticky='W')




        #create the widgets for entering a username
        cluster="population"
        #create a button widget called btn
        btn = Button(window, text="Get All states details", fg="#a1dbcd", bg="#383a39",command=lambda:getAnalaysis(varPop,varAvg,varMax,varMin,databaseNameE,databasePassE))
        btn2 = Button(window, text="click for particulat states", fg="#a1dbcd", bg="#383a39",command=lambda:multiState(root,window,varPop,varAvg,varMax,varMin,databaseNameE,databasePassE))

        #pack the widget into the window
        btn.grid(row=8)
        btn2.grid(row=9)

        
        countWindow=1;

    window.pack()


#displayHome()

##################################################################################################################################
###########################             MENU GUI            ######################################################################
##################################################################################################################################


menubar = Menu(root)
def end(root):
    root.destroy();

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Home", command=lambda: displayHome(home),font=("Times", 15))
filemenu.add_command(label="Analysis", command=lambda:displayWindow(window),font=("Times", 15))
filemenu.add_command(label="Mining", command=lambda:displayMining(mining),font=("Times", 15))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=lambda: end(root),font=("Times", 15))
menubar.add_cascade(label="Options",font=("Times", 15), menu=filemenu)

# display the menu
root.config(menu=menubar)
##################################################################################################################################
###########################             MENU END            ######################################################################
##################################################################################################################################

#draw the window, and start the 'application'
root.geometry("800x600")
root.mainloop()

