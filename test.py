from Tkinter import * #for gui
from time import sleep

root=Tk()

frame= Frame(root)

img=['New-Delhi.gif','narendra-modi-2016-592.gif','New_Delhi_government_block_03-2016_img3.gif','india-pension.gif']
imga = PhotoImage(file='New-Delhi.gif')
label=Label(frame,image=imga)
label.pack()
frame.pack();
root.mainloop()
    
   

