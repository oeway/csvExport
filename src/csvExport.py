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
    print header.split('\t')
    f.close()
    if '\t' in header:
        importDelimiterVar.set('\\t')
    elif ',' in header:
        importDelimiterVar.set(',')
    print(header)

    importDelimiterChanged()

def importDelimiterChanged(*args):
    if 1:#try:
        global FileName
        f = open(FileName,'rb')
        reader = csv.reader(f, delimiter=importDelimiterVar.get().decode("string_escape"), quotechar='|')
        header = reader.next()
        HeaderListbox.delete(0, Tkinter.END)
        for i,h in enumerate(header):
            HeaderListbox.insert(Tkinter.END, str(i+1)+": "+h.strip('"'))
        f.close()
        headerSelectChanged()
        #except:
        #pass

def headerSelectChanged(*args):
    try:
        format = exportFormatVar.get()
        si = int(HeaderListbox.curselection()[0])
        if si>=0 and si<HeaderListbox.size():
            si = si+1
            format +=  (", "+str(si))
            exportFormatVar.set(format.strip(","))
            
        #update header    
        ef = exportFormatVar.get().split(',')#['x','y','z','intensity','frame']
        ef = [int(e.strip())-1 for e in ef ] # remove empty
        eformat = [e for e in ef if e>=0 and e<HeaderListbox.size()]
        global FileName
        f = open(FileName,'rb')
        reader = csv.reader(f, delimiter=importDelimiterVar.get().decode("string_escape"), quotechar='|')
        reader = csv.reader(f, delimiter=importDelimiterVar.get().decode("string_escape"), quotechar='|')
        header = reader.next()
        f.close()
        outputDelimiter = exportDelimiterVar.get()
        tmp = ""
        for i,h in enumerate(header):
            if i in eformat:
                tmp += (h.strip('"') + outputDelimiter)
        headerVar.set(tmp.rstrip(outputDelimiter))
    except:
        pass

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

    ef = exportFormatVar.get().split(',')#['x','y','z','intensity','frame']

    ef = [int(e.strip())-1 for e in ef ] # remove empty

    eformat = [e for e in ef if e>=0 and e<HeaderListbox.size()]
    if len(ef)!=len(eformat) and len(eformat)>0:
        tkMessageBox.showinfo("Bad format", "Please select the right column numbers")
        return

    if len(eformat)>0:
        mythread = exportThread(FileName, exportfilename, eformat)
        mythread.start()


class exportThread (threading.Thread):
    def __init__(self, fromFile, toFile, export_format):
        threading.Thread.__init__(self)
        self.fromFile = fromFile
        self.toFile = toFile
        self.export_format = export_format
    def run(self):
        if 1:
            print "Starting "
            pb_hd.start(50)
            with open(self.fromFile, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=importDelimiterVar.get().decode("string_escape"), quotechar='|')
                header = reader.next()
                
                selection = []
                for ix in self.export_format:
                    if ix>=0 and ix<len(header):
                        selection.append(ix)
                if not len(selection) == len(self.export_format):
                    print self.export_format
                    print selection
                    tkMessageBox.showinfo("Eorror", "bad format!")
                    pb_hd.stop()
                    return
                if len(selection)<=0:
                    return
                #newRow = [header[i] for i in selection]
                print({i:header[i] for i in range(len(header))})
                j=0
                exportDelimiter = exportDelimiterVar.get().decode("string_escape")
                f = open(self.toFile, 'wb')
                writer = csv.writer(f, delimiter=exportDelimiter)
                if includeHeaderVar.get():
                    newRow = headerVar.get().decode("string_escape").split(exportDelimiter) # [header[i].strip('"') for i in selection]
                    writer.writerow(newRow)
                for row in reader:
                    #print row
                    newRow = [row[i].replace("Infinity","Inf") for i in selection]
                    writer.writerow(newRow)
                    j+=1
                    if j%1000==0:
                        print(j)
                print(str(j)+ " rows exported.")
                #print(newRow)
                f.close()
            print "Done! "
            pb_hd.stop()
            tkMessageBox.showinfo("Finished", "Export complete!")
            #except:
            #print "Error! "
            pb_hd.stop()

        
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
    HeaderListbox = Tkinter.Listbox(ft)
    HeaderListbox.grid(row=1,column=0,columnspan=2,sticky=Tkinter.W+Tkinter.E)

    HeaderListbox.bind("<Double-Button-1>", headerSelectChanged)
    
    L1 = ttk.Label(ft, text="Input Delimiter:")
    #L1.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    L1.grid(row=2, column=0,sticky=Tkinter.W)
    
    importDelimiterVar = Tkinter.StringVar()
    importDelimiterVar.set(",")
    e = ttk.Entry(ft, textvariable=importDelimiterVar)
    #e.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    e.grid(row=2, column=1)
    importDelimiterVar.trace("w", importDelimiterChanged)
    
    L2 = ttk.Label(ft, text="Selected Columns:")
    #L2.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    L2.grid(row=3,column=0,sticky=Tkinter.W)
    
    exportFormatVar = Tkinter.StringVar()
    exportFormatVar.set(" 1, 2")
    e = ttk.Entry(ft, textvariable=exportFormatVar)
    #e.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    e.grid(row=3,column=1)
    
    L3 = ttk.Label(ft, text="Output Delimiter:")
    #L3.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    L3.grid(row=4,column=0,sticky=Tkinter.W)
    
    exportDelimiterVar = Tkinter.StringVar()
    exportDelimiterVar.set("\\t")
    e = ttk.Entry(ft, textvariable=exportDelimiterVar)
    #e.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    e.grid(row=4,column=1)
    
    L4 = ttk.Label(ft, text="Header:")
    #L3.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    L4.grid(row=5,column=0,sticky=Tkinter.W)
    
    headerVar = Tkinter.StringVar()
    headerVar.set("")
    e = ttk.Entry(ft, textvariable=headerVar)
    #e.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    e.grid(row=5,column=1)
    
    includeHeaderVar = Tkinter.IntVar()
    cb = ttk.Checkbutton(ft, text="Include Header", variable=includeHeaderVar)
    cb.grid(row=6,column=0,columnspan=2,sticky=Tkinter.W+Tkinter.E)
    
    #replaceInfVar = Tkinter.IntVar()
    #cb2 = ttk.Checkbutton(ft, text="Include Header", variable=replaceInfVar)
    #cb2.grid(row=6,column=0,columnspan=2,sticky=Tkinter.W+Tkinter.E)

    exportBtn = ttk.Button(ft,text ="Export", command = exportFile)
    #exportBtn.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    exportBtn.grid(row=7,column=0,columnspan=2,sticky=Tkinter.W+Tkinter.E)
    
    pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='determinate')
    #pb_hd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    pb_hd.grid(row=8,column=0,columnspan=2, sticky=Tkinter.W+Tkinter.E)
    
    root.mainloop()
