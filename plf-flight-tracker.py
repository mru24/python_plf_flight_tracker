# https://pyflightdata.readthedocs.io/en/latest/pyflightdata.html

from pyflightdata import FlightData
import datetime
import tkinter as tk
import tkinter.font as TkFont

root = tk.Tk()
root.geometry('800x400')
root.title('Flight tracker')
lf = TkFont.Font(family='Helvetica', size=12, weight='normal')

def readData():
    api = FlightData()
    flight = entry.get()
    flights = api.get_all_available_history_by_flight_number(flight,delay=2)
    displayData(flights)

def insertData(data):
    entry.delete(0,tk.END)
    entry.insert(0,data)

def displayData(data):
    list.delete(0,tk.END)
    print(len(data))
    if len(data):
        for flight in data:
            try:
                date = flight['status']['generic']['eventTime']['utc_millis']
                dateFormated = datetime.datetime.fromtimestamp(date / 1000)
            except KeyError:
            # Key is not present
                dateFormated = ''
                # pass
            statusText = flight['status']['text']
            status = flight['status']['live']
            origin = flight['airport']['origin']['name']
            dest = flight['airport']['destination']['name']
            if status!=0:
                list.itemconfig(tk.END,{'bg':'green','fg':'white'})
            else:
                status = ''
            line = (f"{ dateFormated }  { statusText }  {status} FROM: {origin} TO: {dest}")
            list.insert(tk.END,line)
    else:
        line = ("No data")
        list.insert(tk.END,line)
        

topFrame = tk.Frame(root,pady=5)
midFrame = tk.Frame(root,pady=5)
content = tk.Frame(root)

list = tk.Listbox(content,selectmode=tk.MULTIPLE,width=800,font=lf)
list.pack(fill=tk.BOTH, expand=True)
scroll = tk.Scrollbar(list)
scroll.pack(side=tk.RIGHT,fill=tk.BOTH)
list.config(yscrollcommand = scroll.set)
scroll.config(command = list.yview) 

entry = tk.Entry(master=midFrame,font=lf)
entry.pack(fill=tk.BOTH,side=tk.LEFT)

button = tk.Button(master=midFrame,text='Submit',command = readData,font=lf,padx=20)
button.pack(fill=tk.BOTH,side=tk.LEFT,padx=10)

for _ in range(1,7):
    b = tk.Button(master=topFrame,text=f"PLF10{_}",command = lambda v=_:insertData(f"PLF10{v}"),font=lf,padx=20)
    b.pack(fill=tk.BOTH,side=tk.LEFT)

topFrame.pack(fill=tk.BOTH,padx=5,pady=5)
midFrame.pack(fill=tk.BOTH,padx=5,pady=5)
content.pack(fill=tk.BOTH,expand=True,padx=5,pady=5)

root.mainloop()
    