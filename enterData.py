import mysql.connector

statesName=['Andaman_and_Nicobar_Islands','Andhra_Pradesh','Arunachal_Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra_and_Nagar_Haveli','Daman_and_Diu','National_Capital_Territory_of_Delhi','Goa','Gujarat','Haryana','Himachal_Pradesh','Jammu_and_Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Madhya_Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil_Nadu','Telangana','Tripura','Uttar_Pradesh','Uttarakhand','West_Bengal']

con=mysql.connector.connect(user="root",password="",host="localhost",database="test")

cur=con.cursor()
i=1
'''
cur.execute("SELECT number FROM minKeyLakshadweep");
tables=cur.fetchone()
if(tables==None):
    print tables;
'''
for state in statesName:
    #cur.execute("CREATE TABLE shareState_"+state+"(indices int(5),state varchar(1000))");
    #cur.execute("CREATE TABLE minkey"+state+"(number int(4))");
    #cur.execute("insert into state values("+str(i)+",'"+str(state)+"')");
    #print "drop table "+state+"Information";
    #cur.execute("drop table "+state+"Information");
    
    #print "CREATE TABLE "+state+"Information(UIDAI int(12),Name varchar(50),FName varchar(50),MName varchar(50),Gender varchar(7),DOB date,Income double(15),Occupation varchar(50),Address varchar(100))";

    #cur.execute("CREATE TABLE "+state+"Information(UIDAI int(12),Name varchar(50),FName varchar(50),MName varchar(50),Gender varchar(7),DOB date,Income double(11,3),Occupation varchar(50),Address varchar(100))");
        
    #cur.execute("delete from key"+state+"");
    cur.execute("delete from key"+state+"");
    cur.execute("delete from minkey"+state+"");
    cur.execute("delete from shareState_"+state+"");
    #cur.execute("drop table "+state+"Information")
    #cur.execute("drop table key"+state+"")
    con.commit();
    #cur.execute("CREATE TABLE key"+state+"(state varchar(50),cluster varchar(50),keyss varchar(1000))");
    
    con.commit();
    print "created table "+state+"";
    i=i+1;

