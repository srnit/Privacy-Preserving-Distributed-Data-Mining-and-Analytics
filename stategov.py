from Tkinter import * #for gui
import MySQLdb
#import mysql.connector #for database connectivity
import unittest #for shamir library
from SSSA import sssa #for shamir library


statesName=['andaman_and_nicobar_islands','andhra_pradesh','arunachal_pradesh','assam','bihar','chandigarh','chhattisgarh','dadra_and_nagar_haveli','daman_and_diu','national_capital_territory_of_delhi','goa','gujarat','haryana','himachal_pradesh','jammu_and_kashmir','jharkhand','karnataka','kerala','lakshadweep','madhya_pradesh','maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim','tamil_nadu','telangana','tripura','uttar_pradesh','uttarakhand','west_bengal']
totalState=len(statesName);
varState=[None]*totalState;
### Main GUI frame
root=Tk(); 
mainFrame=Frame(root);


####### Secret sharing Library used
sss=sssa();


''''
def checkedState(*varState):

     for i in range(totalState):
         if(varState[i].get()==1):
             ####print statesName[i];
'''
################################################################################################################################################################
###########################################                                                     ################################################################
###########################################         FUNCTIONS DEFINED USED IN PROGRAMS          ################################################################
###########################################                                                     ################################################################
################################################################################################################################################################

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
    global cur,totalStates,tables,states,statesName,totalStates
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
        #varState=[None]*totalState;
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




########## generatekey() function generate secret key and distribute to the selected state
########## parameters used:
##########                  1) state: name of state which generate secret
##########                  2) threshold: minimum key needed to unlock secret
##########                  3) secret : secret information
##########                  4) cluster : what type of secret 
##########                  5) infoL : information obtain in this infoL Frame

def generateKey(state,threshold,secret,cluster,infoL):

    #if(str(state.get())!="" or str(threshold.get())!="" or str(secret.get())!=""):

    ##### CONVERTING INFORMATION TO STRING
    sta=str(state);
    thr=int(threshold);
    sec=str(secret);
    cluster=str(cluster);
    #####print cluster+"   ss";


    ####  QUERY FOR TOTAL STATES  
    cur=con.cursor()
    cur.execute("SELECT COUNT(*) From state");
    fetch=cur.fetchone();
    totalStates=int(fetch[0])
    #####print totalStates;


    ###### EXTRACT NAME OF SELECTED STATES IN CHECKBOX
    countState=0;
    states=[None]*(totalState);
    j=0;
    for i in range(totalState):
        if(varState[i].get()==1):
            #####print statesName[i];
            states[j]=statesName[i];
            countState=countState+1;
            j=j+1;   

    #####GENERATE SECRET FOR TOTAL SELECTED STATES (library we used for generating secret.Shami secret sharing algorithm is used)
    ##### parameter is used 
    #####                   1) thr: Minimum key to unlock secret
    #####                   2) countState: Number of secret key generated
    #####                   3) sec : secret information which we want to encrypted
    #####                   out in keys is like this ["secret_1","secret_2","secret_3","secret_4",................"secret_countState"]

    keys=sss.create(thr,countState,sec)
    #####print keys
    #####print keys
    

    #### generated secret in selected states and added in there key[checkedStateName] tables
    i=0;
    for stat in states:
        #####print stat;
        if(stat==None):
            break;
        #Query to add the secret in key[statesName] table
        keyState="key"+stat;
        query = "INSERT INTO "+keyState+"(state,cluster,keyss) VALUES(%s,%s,%s)";
        args = (str(sta),str(cluster),str(keys[i]))
        #####print query;
        cur1=con.cursor()
        cur1.execute(query,args)
        con.commit()
        i=i+1;


########## generateSecret() function generate secret with help of generateKey() function
########## parameters used:
##########                  1) state: name of state which generate secret
##########                  2) threshold: minimum key needed to unlock secret
##########                  3) infoL : information obtain in this infoL Frame

def generateSecret(state,threshold,infoL,databaseNameE,databasePassE):

    databaseNameE=databaseNameE.get();
    databasePassE=databasePassE.get();
    check=databases(databaseNameE,databasePassE)
    check=int(check)
    if(check==0):
        ### this if condition check whether all fields are filled or not
        ###     if filled then generate secret
        if(str(state.get())!="" or str(threshold.get())!=""):
            ##### converting information into string
            state=str(state.get())
            threshold=str(threshold.get())
            
            ###### this part check wheither the state already generate there secret or not if generate then no extra secret generate
            ###### we did this by checking minimum key is there in minkey[state] if it is there it means it already generate secret if not then generate secret
            curM=con.cursor()
            query="SELECT number FROM minkey"+state;
            curM.execute(query);
            minS=curM.fetchone();
            if(minS==None):


                cur=con.cursor()

                ####  QUERY FOR TOTAL STATES  
                cur.execute("SELECT COUNT(*) From state");
                fetch=cur.fetchone();
                totalStates=int(fetch[0])
                #####print totalStates;


                ###### EXTRACT NAME OF SELECTED STATES IN CHECKBOX
                countState=0;
                states=[None]*(totalState);
                j=0;
                for i in range(totalState):
                    if(varState[i].get()==1):
                        #####print statesName[i];
                        states[j]=statesName[i];
                        countState=countState+1;
                        j=j+1;
                


                ############ this part is enter the name of state which is checked to take secret for the states
                i=0;
                for stat in states:
                    #####print stat;
                    if(stat==None):
                        break;
                    shareState="sharestate_"+state;
                    query = "INSERT INTO "+shareState+"(indices,state) VALUES(%s,%s)";
                    args = (str(i),str(stat))
                    i=i+1;
                    #####print query;
                    
                    cur1=con.cursor()
                    cur1.execute(query,args)
                    con.commit()
                
                
                ##### population cluster is created and generate encrypted key for cluster
                curp=con.cursor()

                #query to extract total population
                query="Select count(*) from "+state+"information";
                curp.execute(query);
                table=curp.fetchone();

                #####print table[0]
                secret=str(table[0])
                
                #####print secret
                
                cluster="population" #type of cluster

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                #################################

                ##### Age cluster is created and generate encrypted key for cluster
                curA=con.cursor()

                #young age (0-13 years)
                #query to find number of young aged person(0-13)
                query="select count(*) from "+state+"information where (datediff(curdate(),dob)/365.25)<=13";
               # ####print query;
                curA.execute(query);
                table=curA.fetchone();
                #####print table;
                ####print "ssss-------"+str(table[0])
                secret=str(table[0])
               # ####print secret
                cluster="youngage"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                ###########

                #teen age (0-13 years)
                #query to find number of teen aged person(14-18)
                query="select count(*) from "+state+"information where (datediff(curdate(),dob)/365.25)>13 and (datediff(curdate(),dob)/365.25)<=18";
                curA.execute(query);
                table=curA.fetchone();
                #####print table[0]
                secret=str(table[0])
                ####print secret
                cluster="teenage"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                ###########

                #Adult age (19-39 years)
                #query to find number of Adult aged person(19-39)
                query="select count(*) from "+state+"information where (datediff(curdate(),dob)/365.25)>18 and (datediff(curdate(),dob)/365.25)<=39";
                curA.execute(query);
                table=curA.fetchone();
                #####print table[0]
                secret=str(table[0])
               # ####print secret
                cluster="adultage"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                ###########
                
                #Middle age (39-65 years)
                #query to find number of Middle aged person(39-65)
                query="select count(*) from "+state+"information where (datediff(curdate(),dob)/365.25)>39 and (datediff(curdate(),dob)/365.25)<=65";
                curA.execute(query);
                table=curA.fetchone();
                #####print table[0]
                secret=str(table[0])
                ######print secret
                cluster="middleage"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                ###########
                
                #Old age (65 above years)
                #query to find number of old aged person(65 above)
                query="select count(*) from "+state+"information where (datediff(curdate(),dob)/365.25)>65";
                curA.execute(query);
                table=curA.fetchone();
                ######print table[0]
                secret=str(table[0])
                #####print secret
                cluster="oldage"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                ###########

                #Income wise cluster is made and encrypted the cluster information and send to selected states
                curI=con.cursor()
                #### below incBA is BPL and above This APL
                incBA=str(1000000)
                #### below incAR is APL and above This Rich
                incAR=str(5000000)

                #below poverty line
                query="select count(*) from "+state+"information where income<"+incBA;
                curI.execute(query);
                table=curI.fetchone();
                secret=str(table[0])
                #####print "below="+secret
                cluster="bpl"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                ###########

                #Middle class
                query="select count(*) from "+state+"information where income>="+incBA+" and income<"+incAR;
                curI.execute(query);
                table=curI.fetchone();
                secret=str(table[0])
                #####print "below="+secret
                cluster="middleclass"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                ###########

                #Rich class
                query="select count(*) from "+state+"information where income>="+incAR;
                curI.execute(query);
                table=curI.fetchone();
                secret=str(table[0])
                #####print "below="+secret
                cluster="richclass"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                ###########

                #genders
                #male
                curp=con.cursor()
                query="Select count(*) from "+state+"information where gender='m'";
                ######print query;
                curp.execute(query);
                table=curp.fetchone();
                #####print table[0]
                secret=str(table[0])
                ####print secret
                cluster="genderMale"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                #################################

                #Female
                curp=con.cursor()
                query="Select count(*) from "+state+"information where gender='f'";
                #####print query;
                curp.execute(query);
                table=curp.fetchone();
                #####print table[0]
                secret=str(table[0])
                ####print secret
                cluster="genderFemale"

                #### this function generate key and add to database
                generateKey(state,threshold,secret,cluster,infoL)
                #################################


                #### this query add the information what the minimum key require to unlock there cluster secrets
                minState="minkey"+state;
                query= "INSERT INTO "+minState+"(number) VALUES("+threshold+")";
                cur2=con.cursor()
                cur2.execute(query)

                ####finally commit all the changes which we done
                con.commit()

                ###### Display the informatin in new windows(or pop up box)
                infoL.config(text="your record succesfully entered");
            else:
                #####this part run only when minimum key for state is already available in the database

                ###### Display the informatin in new windows(or pop up box)
                infoL.config(text="sorry your record already entered");


        else:
            ########This part run only when some field is not filled

            infoL.config(text="Please fill all the fields",fg="red");

            

########## THis funcion is used to select all the checkbox of states
def selectAll(*varState):
    totalState=len(statesName);
    for i in range(totalState):
        varState[i].set(1)
    

########## This function is used to create checkbox for selection of states
def multiState(frame1):

    ####Select all button or check all the states
    selectAllB=Button(frame1,text="select ALL");
    selectAllB.pack();

    ####scrollbar 
    vsb=Scrollbar(frame1,orient="vertical")
        
    cb=[None]*totalState
        
    text=Text(frame1,width=60,height=10,yscrollcommand=vsb.set)
    vsb.config(command=text.yview)
    vsb.pack(side="right", fill="y")
    text.pack(side="left", fill="both", expand=True)
        
    for i in range(totalState):
        varState[i] = IntVar()
        cb[i] = Checkbutton(frame1, text=statesName[i],variable=varState[i])
        #cb[i].grid(row=i,sticky=W)
        text.window_create("end",window=cb[i])
        text.insert("end", "\n")
    selectAllB.config(command=lambda: selectAll(*varState));






################################################################################################################################################################
###########################################                                                     ################################################################
###########################################                 FUNCTIONS ENDED                     ################################################################
###########################################                                                     ################################################################
################################################################################################################################################################






################################################################################################################################################################
###########################################                                                     ################################################################
###########################################         GUI CREATION FOR STATE GOVERMNET            ################################################################
###########################################                                                     ################################################################
################################################################################################################################################################



mainFrame=Frame(root);
### main title 
headL=Label(mainFrame,text="State Directorate", fg="#922b21" ,font=("Helvetica", 50));
line="--------------------------";

###### labels
lineL=Label(mainFrame,text=line,font=("Helvetica", 50));
stateL=Label(mainFrame,text="State",font=("Times", 24));
thresholdL=Label(mainFrame,text="Minimum Key",font=("Times", 24));

infoL=Label(mainFrame,font=("Times", 24));
stateE=Entry(mainFrame,font=("Times", 24));
thresholdE=Entry(mainFrame,font=("Times", 24));

buttonF=Frame(mainFrame);
checkF=Frame(mainFrame);
sharesParticularL=Label(mainFrame,text="shares for states",font=("Times", 24));

databaseNameL=Label(mainFrame,text="enter database name:",font=("Times", 24))
databaseNameL.grid(row=7,column=0)
databaseNameE=Entry(mainFrame,font=("Times", 24))
databaseNameE.grid(row=7,column=1)
databasePassL=Label(mainFrame,text="enter database password:",font=("Times", 24))
databasePassL.grid(row=8,column=0)
databasePassE=Entry(mainFrame,font=("Times", 24),show="*")
databasePassE.grid(row=8,column=1)

#This button genertate secret by calling generateSecret() function
generate=Button(buttonF,text="generate key",command= lambda: generateSecret(stateE,thresholdE,infoL,databaseNameE,databasePassE),bg="#a1dbcd",font=("Times", 20))
#generate=Button(buttonF,text="generate key",command= lambda: checkedState(*varState),bg="#a1dbcd",font=("Times", 20))

### creating checkbox of states through this function
multiState(checkF)
headL.grid(row=0,columnspan=2);
lineL.grid(row=1,columnspan=2);
stateL.grid(row=2,column=0);
stateE.grid(row=2,column=1);
thresholdL.grid(row=3,column=0);
thresholdE.grid(row=3,column=1);

buttonF.grid(row=9,columnspan=2);
infoL.grid(row=10,columnspan=2);
#checkF.grid(row=6,columnspan=2);
sharesParticularL.grid(row=5,column=0)
#sharesParticularB.grid(row=5,column=1);
checkF.grid(row=5,column=1);
generate.grid(row=1,pady=5);


root.geometry("1000x700")

mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop();

################################################################################################################################################################
###########################################                                                     ################################################################
###########################################                 END OF GUI                          ################################################################
###########################################                                                     ################################################################
################################################################################################################################################################
