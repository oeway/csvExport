import csv
try:
    import Tkinter              # Python 2
    import ttk
except ImportError:
    import tkinter as Tkinter   # Python 3
    import tkinter.ttk as ttk
import tkFileDialog
import tkMessageBox
import os,sys
import threading

import_delimiter = ','
export_delimiter = '\t'

FileName = False
def openFile():
    options = {}
    options['initialdir'] = '.'
    options['parent'] = root
    options['title'] = 'Open a csv or xls file'
    # get filename
    global FileName
    FileName = tkFileDialog.askopenfilename(**options)
    if FileName:
        print("Open file:"+FileName)
    f = open(FileName,'r')
    header = f.readline()
    if '\t' in header:
        importDelimiterVar.set('\\t')
    elif ',' in header:
        importDelimiterVar.set(',')
    print(header)
    #headerVar.set(header)
    f.close()
    
def exportFile():
    global FileName
    if not FileName:
        print("please select file")
        tkMessageBox.showinfo("Eorror", "Please select file")
        return
    options = {}
    options['initialdir'] = os.path.dirname(FileName)
    options['parent'] = root
    options['title'] = 'Save as'
    exportfilename = tkFileDialog.asksaveasfilename(**options)
    if not exportfilename:
        print("export file not selected!")
        return
    print("Save as:"+exportfilename)
    
    eformat = exportFormatVar.get().split(',')#['x','y','z','intensity','frame']
    mythread = exportThread(FileName, exportfilename, eformat)
    mythread.start()

class exportThread (threading.Thread):
    def __init__(self, fromFile, toFile, export_format):
        threading.Thread.__init__(self)
        self.fromFile = fromFile
        self.toFile = toFile
        self.export_format = export_format
    def run(self):
        print "Starting "
        pb_hd.start(50)
        with open(self.fromFile, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=importDelimiterVar.get().decode("string_escape"), quotechar='|')
            header = reader.next()
            f = open(self.toFile, 'wb')
            writer = csv.writer(f, delimiter=exportDelimiterVar.get().decode("string_escape"))
            selection = []
            for e in self.export_format:
                for i,h in enumerate(header):
                    if e.strip().lower() in h.lower():
                        selection.append(i)
                        break;
            if not len(selection) == len(self.export_format):
                tkMessageBox.showinfo("Eorror", "bad format!")
                pb_hd.stop()
                return
            #newRow = [header[i] for i in selection]
            print({i:header[i] for i in range(len(header))})
            #writer.writerow(newRow)
            j=0
            for row in reader:
                #print row
                newRow = [row[i].replace("Infinity","Inf") for i in selection]
                writer.writerow(newRow)
                j+=1
                if j%1000==0:
                    print(j)
            print(str(j)+ " rows exported.")
            print(newRow)
            f.close()
        print "Exiting "
        pb_hd.stop()
        tkMessageBox.showinfo("Finished", "Export complete!")
        
if __name__ == '__main__':
    root = Tkinter.Tk()
    root.title("CSV Export")
    ft = ttk.Frame()
    ft.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    
    L0 = ttk.Label(ft, text="Input File:")
    #L0.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    L0.grid(row=0, column=0,sticky=Tkinter.W)
    
    openBtn = ttk.Button(ft,text ="Select", command = openFile)
    #openBtn.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    openBtn.grid(row=0, column=1)
    #headerVar = Tkinter.StringVar()
    #Headers = ttk.Label(ft, textvariable=headerVar)
    #Headers.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    
    L1 = ttk.Label(ft, text="Import Delimiter:")
    #L1.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    L1.grid(row=1, column=0,sticky=Tkinter.W)
    
    importDelimiterVar = Tkinter.StringVar()
    importDelimiterVar.set(",")
    e = ttk.Entry(ft, textvariable=importDelimiterVar)
    #e.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    e.grid(row=1, column=1)
    
    L2 = ttk.Label(ft, text="Export Format:")
    #L2.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    L2.grid(row=2,column=0,sticky=Tkinter.W)
    
    exportFormatVar = Tkinter.StringVar()
    exportFormatVar.set("x,y,z,intensity,frame")
    e = ttk.Entry(ft, textvariable=exportFormatVar)
    #e.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    e.grid(row=2,column=1)
    
    L3 = ttk.Label(ft, text="Export Delimiter:")
    #L3.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    L3.grid(row=3,column=0,sticky=Tkinter.W)
    
    exportDelimiterVar = Tkinter.StringVar()
    exportDelimiterVar.set("\\t")
    e = ttk.Entry(ft, textvariable=exportDelimiterVar)
    #e.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    e.grid(row=3,column=1)

    exportBtn = ttk.Button(ft,text ="Export", command = exportFile)
    #exportBtn.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    exportBtn.grid(row=4,column=0,columnspan=2,sticky=Tkinter.W+Tkinter.E)
    
    pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='determinate')
    #pb_hd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    pb_hd.grid(row=5,column=0,columnspan=2, sticky=Tkinter.W+Tkinter.E)
    
    root.mainloop()
