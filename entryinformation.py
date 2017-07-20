import mysql.connector
import random

statesName=['Andaman_and_Nicobar_Islands','Andhra_Pradesh','Arunachal_Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra_and_Nagar_Haveli','Daman_and_Diu','National_Capital_Territory_of_Delhi','Goa','Gujarat','Haryana','Himachal_Pradesh','Jammu_and_Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Madhya_Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil_Nadu','Telangana','Tripura','Uttar_Pradesh','Uttarakhand','West_Bengal']

con=mysql.connector.connect(user="root",password="",host="localhost",database="test")

name=['abc','def','ghi','jkl','mno','pqr','stu','vwx','yz','za'];
gender=['m','f'];
dob=['2010-10-21','2000-04-03','1996-02-17','1970-03-13','1950-02-09',];
occupation=['student','housewife','farmer','doctor','enginner','teacher','politican','shopkeeper'];
address=['asd','sdf','asdf','sdf','sdfc','ad3c','ddfa','sdfwe'];

cur=con.cursor()
i=1

ln=len(name)
gn=len(gender)
dn=len(dob);
on=len(occupation);
an=len(address);
r=random.sample(range(0,ln ), 4)
for state in statesName:
    for i in range (1000):
        r=random.sample(range(0,ln ), 1)
        n=name[r[0]]
        r=random.sample(range(0,ln ), 1)
        fn=name[r[0]]
        r=random.sample(range(0,ln ), 1)
        mn=name[r[0]]
        r=random.sample(range(0,gn ), 1)
        g=gender[r[0]]
        r=random.sample(range(0,dn ), 1)
        d=dob[r[0]]
        r=random.sample(range(0,on ), 1)
        o=occupation[r[0]]
        r=random.sample(range(0,an ), 1)
        a=address[r[0]]
        r=random.sample(range(0,10000000 ), 1)
        inc=r[0];

        print str(n)+" "+str(fn)+" "+str(mn)+" "+str(g)+" "+str(d)+" "+str(inc)+" "+str(o)+" "+str(a)
        query = "INSERT INTO "+state+"Information (UIDAI,Name,FName,MName,Gender,DOB,Income,Occupation,Address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        args = (str(i),str(n),str(fn),str(mn),str(g),str(d),str(inc),str(o),str(a))
        cur.execute(query,args)
        con.commit()

print "done"
    
