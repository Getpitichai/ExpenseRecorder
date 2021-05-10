#GUIBasic2-Expense.py
from tkinter import *
from tkinter import ttk, messagebox # ttk is theme of Tk และ เพิ่ม messagebox
from datetime import datetime #import วันเวลา
import csv


GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Uncle')
GUI.geometry('600x700+500+50')

# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=50, ipady=20) #.pack() ติดปุ่มเข้า GUI หลัก


##########---------สร้างเมนูใหม่---------
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')
# Help
def About():
	messagebox.showinfo('About','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม? ขอ 1 BTC ก็พอแล้ว\nBTC Address: abc')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)





#####################################










#สร้าง tab-------------------------------------
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab) #สามารถใช้ width=500,height=500 เพื่อ fix ขนาด frame ได้
T2 = Frame(Tab)
Tab.pack(fill='both', expand = True)  #fill สามารถใช้ x หรือ y ก็ได้ แต่มันจะขนาดแค่ฝั่งเดียว ถ้าใช้ both จะขยายทั้งหมด


expenseicon = PhotoImage(file='add.png') #.subsample(2) = ย่อรูป
listicon = PhotoImage(file='list.png')

Tab.add(T1,text=f'{"Add Expense":^{30}}' ,image=expenseicon,compound='top')
Tab.add(T2,text=f'{"Expense List":^{30}}',image=listicon,compound='top')

#-----------------------------------------------

F1 = Frame(T1)
F1.pack()
#F1.place(x=100,y=50)

#เพิ่ม Dictionary
days = {'Mon':'จันทร์',
		'Tue':'อังคาร',
		'Wed':'พุธ',
		'Thu':'พฤหัสบดี',
		'Fri':'ศุกร์',
		'Sat':'เสาร์',
		'Sun':'อาทิตย์'}

def Save(event=None):
	expense = v_expense.get()
	price = v_price.get()
	quantity = v_quantity.get()
	

	if expense == '':
		print('No data')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
		return #ทำให้จบฟังก์ชั่น
	elif price == '':
		messagebox.showwarning('Error','กรุณากรอกราคา')
		return #ทำให้จบฟังก์ชั่น
	elif quantity == '':
		messagebox.showwarning('Error','กรุณากรอกจำนวน')
		return #ทำให้จบฟังก์ชั่น


	try:
		total = float(price) * float(quantity)
		today = datetime.now().strftime('%a') #days['Mon'] = จันทร์

		print(today)
		dt = datetime.now().strftime("%y/%m/%d-%H:%M:%S")
		dt = days[today] + '-' + dt
		# .get() ดึงมาจาก v_expense = StringVar()
		print('รายการ: {} ราคา: {} บาท'.format(expense,price))
		print(f'จำนวน: {quantity} บาท รวมทั้งหมด: {total} บาท savetime: {dt}')
		text = 'รายการ: {} ราคา: {} บาท\n'.format(expense,price)
		text = text + f'จำนวน: {quantity} ชิ้น รวมทั้งหมด: {total} บาท\nsavetime: {dt}'
		v_result.set(text)
		# clear ข้อมูลเก่า
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')


		#บันทึกข้อมูลลง csv อย่าลืม import csv ด้วยนะ
		with open('savedata.csv','a',encoding='utf-8',newline='') as f:
			# with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
			# 'a' การบันทึกเรื่อย ๆ เพิ่มต่อจากข้อมูลเก่า แต่ถ้าเป็น
			# newline = '' ทำให้ข้อมูลไม่มีบันทัดว่าง
			fw = csv.writer(f) #สร้างฟังก์ชั่นสำหรับเขียนข้อมูล
			data = [dt,expense,price,quantity,total]
			fw.writerow(data)
		E1.focus() # ทำให้ cursor กลับไปตำแหน่งช่องกรอก E1
		update_table() #เอาไว้อัพเดทเวลากด save
	except Exception as e:
		print('ERROR',e)
		#messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')
		#กรอกผิดแล้วเกิด error ให้ set clear

#ทำให้สามารถกด enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def save(event=None)

FONT1 = (None,20) #None เปลี่ยนเป็น Angsana new


#เพิ่มรูปเข้าไป--------------------------------------
centerimg = PhotoImage(file='wallet.png')
logo = ttk.Label(F1, image=centerimg)
logo.pack()
#-----------------------------------------------


#---text1---
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#----------

#---text2---
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#----------

#---text3---
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#----------

#สร้างปุ่ม แบบมี icon-------
saveicon = PhotoImage(file='save.png')
B2 = ttk.Button(F1,text=f'{"Save": >{10}}',command=Save,image=saveicon,compound ='left')
B2.pack(ipadx=50, ipady=20, pady=20) #ipad = internal padding ,,, pady = external
#----------------------

v_result = StringVar()
v_result.set('--------ผลลัพธ์-------')
result = ttk.Label(F1,textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=20)



#-------------------------------------------------------------------------
#tab2!!!

rs = []
def read_csv():
	with open('savedata.csv',newline='',encoding='utf-8') as f:    #with = เปิดไฟล์แล้วปิดให้อัตโนมัติ(ป้องกันลืม)
		fr = csv.reader(f) #fr = file reader
		data = list(fr)
	return data #ถ้าต้องการใช้งานค่าต่อให้ใช้คำสั่ง return ด้วย


L = ttk.Label(T2,text='ตารางแสดงผลลัพธ์ทั้งหมด',font=FONT1).pack(pady=20)
# table
header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resulttable.pack()

# for i in range(len(header)):
#     resulttable.heading(header[i],text=header[i])

for h in header:
	resulttable.heading(h,text=h)

headerwidth = [150,170,80,80,80]
for h,w in zip(header,headerwidth):
	resulttable.column(h,width=w)


# resulttable.insert('',0,value=['จันทร์','น้ำ',30,5,150])  >>>> ล่าสุดไว้ด้านบน
# resulttable.insert('','end',value=['อังคาร','น้ำ',30,5,150])   >>>> ล่าสุดไว้ด้านล่าง

def update_table():
	resulttable.delete(*resulttable.get_children()) #ทำซ้ำบันทัดนี้  #*(ดอกจันทร์) คือการทำแบบรัวๆ
	# for c in resulttable.get_children():
	#     resulttable.delete(c)
	data = read_csv()
	for d in data:
		resulttable.insert('',0,value=d)
update_table()

print('Get Child:',resulttable.get_children())



GUI.bind('<Tab>',lambda x: E2.focus()) ##กด tab.
GUI.mainloop()