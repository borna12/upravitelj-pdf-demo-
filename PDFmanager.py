from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.filedialog, os, shutil, PyPDF2, datetime
from PyPDF2.generic import NameObject, createStringObject
from PIL import Image

global prozor_meta
def doSomething():
    # check if saving
    # if not:
    prozor.destroy()
    try:
        prozor_meta.destroy()
    except:
        return

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
global filename
#ucitaj privitak
def ucitaj_privitak():
    global filename
    filename =  tkinter.filedialog.askopenfilename(parent=prozor, initialdir='/', title = "Odaberi dokument",filetypes = [("pdf dokumenti","*.pdf")])
    print (filename)
    lista=filename.split("/")
    cwd = os.getcwd()
    lokacija=str(cwd)+"/dokumenti/"+str(lista[-1])
    shutil.copyfile(filename, lokacija, follow_symlinks=True)  
    oznaka_ucitavanje["text"]=str(lista[-1])
    br_str["text"]= "Broj stranica: "+ str(PyPDF2.PdfFileReader(open(filename,"rb")).getNumPages())
    prouci_metapodatke["state"]='normal'
    postavi_digitalni["state"]='normal'


#provjeri je li polje popunjeno
def toggle_state(*_):
    if unesi_sifru.var.get():
        postavi_sifru['state'] = 'normal'
    else:
        postavi_sifru['state'] = 'disabled'
def sifriraj():
    if oznaka_ucitavanje["text"]=="...":
        messagebox.showerror("","Niste učitali PDF dokument.")
    else:  
        try:  
            pdffile = open(r"dokumenti/"+oznaka_ucitavanje["text"], "rb")
            pdfReader = PyPDF2.PdfFileReader(pdffile)
            pdfWriter = PyPDF2.PdfFileWriter()
            for pageNum in range(pdfReader.numPages):
                pdfWriter.addPage(pdfReader.getPage(pageNum))
            pdfWriter.encrypt(str(unesi_sifru.get()),use_128bit=True)
            resultPDF = open(r"sifrirani/"+oznaka_ucitavanje["text"][:-4]+"_sifriran.pdf", "wb")
            pdfWriter.write(resultPDF)
            resultPDF.close()
            cwd = os.getcwd()
            f = tkinter.filedialog.asksaveasfile(parent=prozor, initialdir='/', title = "Odaberi lokaciju",filetypes = [("pdf dokumenti","*.pdf")], defaultextension=".pdf", mode = 'wb')
            if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            shutil.copyfile("sifrirani/"+oznaka_ucitavanje["text"][:-4]+"_sifriran.pdf", str(f.name), follow_symlinks=True)  
            messagebox.showinfo("Šifriranje gotovo.","Vaš dokument je šifriran na željenoj lokaciji.")
        except:
            messagebox.showerror("Nemoguće šifrirati.","Vaš dokument ne možemo šifrirati. Vjerojano je već zaštičen.")
global rows
broj=1      
def izmijenametapodataka():
    dokument=open(r"dokumenti/"+oznaka_ucitavanje["text"], "rb")
    pdfmerge = PyPDF2.PdfFileMerger()
    pdfmerge.append(dokument)
    lista=[]
    global rows
    for x in rows:
        for y in x:
            if type(y)==tkinter.Entry:
                lista.append(y.get())
            else:
                lista.append(y)
    pdfmerge.addMetadata({"/Author":str(lista[0]),'/CreationDate':str(lista[1]), '/Creator':str(lista[2]),'/Producer':str(lista[3]), '/ModDate':str(lista[4]), '/Title':str(lista[5])})
    pdffilefinal = open(filename, "wb")
    pdfmerge.write(pdffilefinal)
    pdffilefinal.close()
    pdffilefinal = PyPDF2.PdfFileReader(open(filename, "rb"))
    pdfWriter = PyPDF2.PdfFileWriter()
    for pageNum in range(pdffilefinal.numPages):
        pdfWriter.addPage(pdffilefinal.getPage(pageNum))
    prozor_meta.destroy()
    print(pdffilefinal.getDocumentInfo())


def metapodatke():
    if oznaka_ucitavanje["text"]=="...":
        messagebox.showerror("","Niste učitali PDF dokument.")
    else:
        try:  
            global rows
            rows=[]
            pdffile = open(filename, "rb")
            pdfReader = PyPDF2.PdfFileReader(pdffile)
            info=pdfReader.getDocumentInfo()
            global prozor_meta
            prozor_meta=Tk()
            global broj
            items = ["","","","","",""]
            items2=["","","","","",""]
            var = IntVar()
            l= Label(prozor_meta,text="Autor: ")
            l.grid(row=1,column=0, sticky=W)
            b = Entry(prozor_meta,width=50)
            b.insert(0, "")
            b.grid(row=1, column=1)

            l= Label(prozor_meta,text="Datum stvaranja: ")
            l.grid(row=2,column=0, sticky=W)
            b = Entry(prozor_meta,width=50)
            b.insert(0, "")
            b.grid(row=2, column=1)
         
            l= Label(prozor_meta,text="Proizvedeno s: ")
            l.grid(row=3,column=0, sticky=W)
            b = Entry(prozor_meta,width=50)
            b.insert(0, "")
            b.grid(row=3, column=1)

            l= Label(prozor_meta,text="Producirano s: ")
            l.grid(row=4,column=0, sticky=W)
            b = Entry(prozor_meta,width=50)
            b.insert(0, "")
            b.grid(row=4, column=1)


            l= Label(prozor_meta,text="Datum izmjene: ")
            l.grid(row=5,column=0, sticky=W)
            b = Entry(prozor_meta,width=50)
            b.insert(0, "")
            b.grid(row=5, column=1)

            l= Label(prozor_meta,text="Naziv dokumenta: ")
            l.grid(row=6,column=0, sticky=W)
            b = Entry(prozor_meta,width=50)
            b.insert(0, "")
            b.grid(row=6, column=1)

            for x,y in info.items():
                if str(x)=="/Author":
                    b = Entry(prozor_meta,width=50)
                    b.insert(0, str(y))
                    b.grid(row=1, column=1)
                    items[0]=b.get()
                    items2[0]=b
                elif str(x)=="/CreationDate":
                    b = Entry(prozor_meta,width=50)
                    b.insert(0, str(y))
                    b.grid(row=2, column=1)
                    items[1]=b.get()
                    items2[1]=b
                elif str(x)=="/Creator":
                    b = Entry(prozor_meta,width=50)
                    b.insert(0, str(y))
                    b.grid(row=3, column=1)
                    items[2]=b.get()
                    items2[2]=b
                elif str(x)=="/Producer":
                    b = Entry(prozor_meta,width=50)
                    b.insert(0, str(y))
                    b.grid(row=4, column=1)
                    items[3]=b.get()
                    items2[3]=b
                elif str(x)=="/ModDate":
                    b = Entry(prozor_meta,width=50)
                    b.insert(0, str(y))
                    b.grid(row=5, column=1)
                    items[4]=b.get()
                    items2[4]=b
                elif str(x)=="/Title":
                    b = Entry(prozor_meta,width=50)
                    b.insert(0, str(y))
                    b.grid(row=6, column=1)
                    items[5]=b.get()
                    items2[5]=b
                broj=broj+1
            azur_metapodataka=ttk.Button(prozor_meta,text="izmijeni", command=izmijenametapodataka)
            azur_metapodataka.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
            rows.append(items2)
            prozor_meta.title("Metapodatci")
            prozor_meta.iconbitmap(r"favicon.ico")
            center(prozor_meta)
            prozor_meta.mainloop()
            return prozor_meta
        except:
            messagebox.showerror("Nemoguće učitati metapodatke.","Iz vašega dokumenta ne možemo pročitati metapodatke.")

def digitalni():
    filename2 =  tkinter.filedialog.askopenfilename(parent=prozor, initialdir='/', title = "Odaberi sliku",filetypes = [("jpg slika","*.jpg"),("png slika","*.png")])
    im=Image.open(filename2).convert("RGB")
    #im.putalpha(128)  # Half alpha; alpha argument must be an int
    im.save("zig.png")
    new_file="zig.pdf"

    if not os.path.exists(new_file):
        im.save(new_file, "PDF", resolution=100.0)
    output = PyPDF2.PdfFileWriter()
    #digitalni žig
    ipdf = PyPDF2.PdfFileReader(open(filename, 'rb'))
    wpdf = PyPDF2.PdfFileReader(open(new_file, 'rb'))
    watermark = wpdf.getPage(0)
    for i in range(ipdf.getNumPages()):
        page = ipdf.getPage(i)
        page.mergePage(watermark)
        output.addPage(page)
    with open('izlaz.pdf', 'wb') as f:
        output.write(f)
    
prozor=Tk()
oznaka_ucitavanje=Label(prozor,text="...",width=20)
oznaka_ucitavanje.grid(row=1,column=0,padx=10,pady=10, columnspan=2)

privitak_ucitaj=ttk.Button(prozor,text="učitaj dokument", command=ucitaj_privitak)
privitak_ucitaj.grid(row=1,column=2, padx=10,pady=10)


#broj stranica
br_str=Label(prozor,text="")
br_str.grid(row=2, column=0, padx=10, pady=10, columnspan=3)


oznaka_sifra=Label(prozor,text="Lozinka: ")
oznaka_sifra.grid(row=3,column=0, padx=10,pady=10)

unesi_sifru=Entry(prozor, show="*")
#provjeri popunjenost polja
unesi_sifru.var = StringVar()
unesi_sifru['textvariable'] = unesi_sifru.var
unesi_sifru.var.trace_add('write', toggle_state)

unesi_sifru.grid(row=3,column=1, padx=10,pady=10)

postavi_sifru=ttk.Button(prozor,text="postavi šifru", state=DISABLED, command=sifriraj)
postavi_sifru.grid(row=3,column=2, padx=10,pady=10)

postavi_digitalni=ttk.Button(prozor,text="postavi digitalni žig", state=DISABLED, command=digitalni, width=30)
postavi_digitalni.grid(row=4,column=0, columnspan=2, padx=10,pady=10)


prouci_metapodatke=ttk.Button(prozor,text="prouči metapodatke", command=metapodatke, state=DISABLED)
prouci_metapodatke.grid(row=4,column=2, padx=10,pady=10)

prozor.title("Upravitelj PDF dokumenata.")
prozor.iconbitmap(r"favicon.ico")
center(prozor)

prozor.protocol('WM_DELETE_WINDOW', doSomething)  # root is your root window
prozor.mainloop()