from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk , Image


fonts = ('Comic Sans MS' , 12)


def exitapp(event):
    library_app.destroy()


def getlastid(directory):
    try:
        with open(directory) as file:
            last_line = file.readlines()[-1]
            file.close()
            return last_line[ : 3]
    except:
        file = open(directory , 'a')
        file.close()
        return '000'


def gettitleandauthor(directory , lst):
    try:
        with open(directory) as file:
            for line in file:
                id_ , title , author , status = line.split(' - ')
                lst.append([title , author])
    except:
        file = open(directory , 'a')
    file.close()
    return lst


def getbooksinfo(directory , dic):
    with open(directory) as file:
        for line in file:
            id_ , title , author , status = line.split(' - ')
            dic[id_] = [title , author , status[ :-1]]
    file.close()
    return dic


#List
def BookList():

    #Error for when there are no books
    try:
        bookFile = open('src/BookList.txt')
        bookFile.close()

        #Main
        bookListRoot = Toplevel(library_app)
        bookListRoot.title('Library')
        bookListRoot.minsize(width=600 , height=500)
        bookListRoot.maxsize(width=600 , height=500)
        bookListRoot.geometry('600x500')
        bookListRoot.iconbitmap('src/Icon.ico')

        #Canvas
        CanvasBookList = Canvas(bookListRoot) 
        CanvasBookList.config(bg='#3b858c')
        CanvasBookList.pack(expand=True , fill=BOTH)
        
        #Heading    
        bookListFrame = Frame(bookListRoot , bg='#FFBB00' , bd=5)
        bookListFrame.place(relx=0.25 , rely=0.1 , relwidth=0.5 , relheight=0.13)
            
        bookListLabel = Label(bookListFrame , text='Book List' , bg='black' , fg='white' , font=('Comic Sans MS' , 18))
        bookListLabel.place(relx=0 , rely=0 , relwidth=1 , relheight=1)
        
        #Treeview
        treeFrame = Frame(bookListRoot , bg='black')
        treeFrame.place(relx=0.1 , rely=0.3 , relwidth=0.8 , relheight=0.5)

        with open('src/BookList.txt') as bookListFileTreeview:

            bookListTreeview = {}
            i = 1
            for line in bookListFileTreeview:
                bookid , booktitle , bookauthor , bookstatus = line.split(' - ')
                bookListTreeview[i] = (bookid , booktitle , bookauthor , bookstatus)
                i += 1


            tree = ttk.Treeview(treeFrame , columns=('book id' , 'book title' , 'book author' , 'book status') , show='headings' , height=len(bookListTreeview))
            tree.heading('book id' , text='Book ID')
            tree.column('book id' , width=101 , anchor=CENTER)
            tree.heading('book title' , text='Book Title')
            tree.column('book title' , width=131 , anchor=CENTER)
            tree.heading('book author' , text='Book Author')
            tree.column('book author' , width=131 , anchor=CENTER)
            tree.heading('book status' , text='Book Status')
            tree.column('book status' , width=101 , anchor=CENTER)
            for i in bookListTreeview:
                tree.insert('' , END , values=bookListTreeview[i])
            tree.pack(side='left' , anchor=N , fill='x')

            scrollbar = ttk.Scrollbar(treeFrame , orient=VERTICAL , command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side='right', fill='y')

        #Quit Button
        btnQuitBookList = Button(bookListRoot , text='Exit' , bg='#f7f1e3' , fg='black' , font=fonts , command=bookListRoot.destroy)
        btnQuitBookList.place(relx=0.4 , rely=0.9 , relwidth=0.18 , relheight=0.08)
        
        bookListRoot.mainloop()

    except FileNotFoundError:
        messagebox.showerror(title='No book' , message='There is no book registered in this library.')


#Search
def SearchBook():

    global SearchIDEntry

    #Error for when there are no books
    try:
        bookFile = open('src/BookList.txt')
        bookFile.close()

        #Main
        bookSearchRoot = Toplevel(library_app)
        bookSearchRoot.title('Library')
        bookSearchRoot.minsize(width=400 , height=300)
        bookSearchRoot.maxsize(width=900 , height=800)
        bookSearchRoot.geometry('600x500')
        bookSearchRoot.iconbitmap('src/Icon.ico')
        
        #Canvas
        CanvasBookSearch = Canvas(bookSearchRoot)
        CanvasBookSearch.config(bg='#893b8c')
        CanvasBookSearch.pack(expand=True , fill=BOTH)

        #Heading
        bookSearchFrame = Frame(bookSearchRoot , bg='#FFBB00' , bd=5)
        bookSearchFrame.place(relx=0.25 , rely=0.1 , relwidth=0.5 , relheight=0.13)
        
        bookSearchLabel = Label(bookSearchFrame , text='Search Book' , bg='black' , fg='white' , font=('Comic Sans MS' , 18))
        bookSearchLabel.place(relx=0 , rely=0 , relwidth=1 , relheight=1)
        
        #Info
        bookSearchInfoFrame = Frame(bookSearchRoot , bg='black')
        bookSearchInfoFrame.place(relx=0.1 , rely=0.3 , relwidth=0.8 , relheight=0.5)  
            
        SearchIDLabel = Label(bookSearchInfoFrame,text='Book ID : ' , bg='black' , fg='white' , font=fonts)
        SearchIDLabel.place(relx=0.07 , rely=0.43)
            
        SearchIDEntry = Entry(bookSearchInfoFrame)
        SearchIDEntry.place(relx=0.28 , rely=0.46 , relwidth=0.62)
        
        #Submit Button
        btnBookSearch = Button(bookSearchRoot , text='Search' , bg='#f7f1e3' , fg='black' , font=fonts , command=Search)
        btnBookSearch.place(relx=0.28 , rely=0.9 , relwidth=0.18 , relheight=0.08)
        
        #Quit Button
        btnQuitBookSearch = Button(bookSearchRoot , text='Exit' , bg='#f7f1e3' , fg='black' , font=fonts , command=bookSearchRoot.destroy)
        btnQuitBookSearch.place(relx=0.53 , rely=0.9 , relwidth=0.18 , relheight=0.08)
        
        bookSearchRoot.mainloop()

    except FileNotFoundError:
        messagebox.showerror(title='No book' , message='There is no book registered in this library.')

def Search():

    #Get ID
    searchID = SearchIDEntry.get().strip()
    if len(searchID) == 3:
        try:
            dicSearch = {}
            booksInfoSearch = getbooksinfo('src/BookList.txt' , dicSearch)
            bookInfo = booksInfoSearch[searchID]
            messagebox.showinfo(title='Book information' , message=f'Book Title : {bookInfo[0]}\nBook Author : {bookInfo[1]}\nBook Status : {bookInfo[2]}')
        except KeyError:
            messagebox.showerror(title='The book was not found' , message=f'There is no book with ID : {searchID}.')
    else:
        messagebox.showerror(title='Invalid ID' , message='The entered book ID is not correct.')
    SearchIDEntry.delete(0 , END)
    SearchIDEntry.focus_force()


#Borrow
def BorrowBook(): 
    
    global BorrowIDEntry

    #Error for when there are no books
    try:
        bookFile = open('src/BookList.txt')
        bookFile.close()

        #Main
        bookBorrowRoot = Toplevel(library_app)
        bookBorrowRoot.title('Library')
        bookBorrowRoot.minsize(width=400 , height=300)
        bookBorrowRoot.maxsize(width=900 , height=800)
        bookBorrowRoot.geometry('600x500')
        bookBorrowRoot.iconbitmap('src/Icon.ico')
        
        #Canvas
        CanvasBookBorrow = Canvas(bookBorrowRoot)
        CanvasBookBorrow.config(bg='#748c3b')
        CanvasBookBorrow.pack(expand=True , fill=BOTH)

        #Heading
        bookBorrowFrame = Frame(bookBorrowRoot , bg='#FFBB00' , bd=5)
        bookBorrowFrame.place(relx=0.25 , rely=0.1 , relwidth=0.5 , relheight=0.13)
        
        bookBorrowLabel = Label(bookBorrowFrame , text='Borrow Book' , bg='black' , fg='white' , font=('Comic Sans MS' , 18))
        bookBorrowLabel.place(relx=0 , rely=0 , relwidth=1 , relheight=1)
        
        #Info
        bookBorrowInfoFrame = Frame(bookBorrowRoot , bg='black')
        bookBorrowInfoFrame.place(relx=0.1 , rely=0.3 , relwidth=0.8 , relheight=0.5)  
            
        BorrowIDLabel = Label(bookBorrowInfoFrame,text='Book ID : ' , bg='black' , fg='white' , font=fonts)
        BorrowIDLabel.place(relx=0.07 , rely=0.43)
            
        BorrowIDEntry = Entry(bookBorrowInfoFrame)
        BorrowIDEntry.place(relx=0.28 , rely=0.46 , relwidth=0.62)
        
        #Submit Button
        btnBookBorrow = Button(bookBorrowRoot , text='Borrow' , bg='#f7f1e3' , fg='black' , font=fonts , command=Borrow)
        btnBookBorrow.place(relx=0.28 , rely=0.9 , relwidth=0.18 , relheight=0.08)
        
        #Quit Button
        btnQuitBookBorrow = Button(bookBorrowRoot , text='Exit' , bg='#f7f1e3' , fg='black' , font=fonts , command=bookBorrowRoot.destroy)
        btnQuitBookBorrow.place(relx=0.53 , rely=0.9 , relwidth=0.18 , relheight=0.08)
        
        bookBorrowRoot.mainloop()

    except FileNotFoundError:
        messagebox.showerror(title='No book' , message='There is no book registered in this library.')

def Borrow():
    
    #Get ID
    borrowID = BorrowIDEntry.get().strip()
    if len(borrowID) == 3:
        try:
            dicBorrow = {}
            booksInfoBorrow = getbooksinfo('src/BookList.txt' , dicBorrow)
            if booksInfoBorrow[borrowID][-1] == 'not taken':
                new_file = []
                with open('src/BookList.txt' , 'r') as file:
                    for line in file:
                        if line[ : 3] == borrowID:
                            new_file.append(line.replace('not taken' , 'taken'))
                        else:
                            new_file.append(line)
                file.close()
                with open('src/BookList.txt' , 'w') as file:
                    for line in new_file:
                        file.writelines(line)
                file.close()
                messagebox.showinfo(title='Successfully borrowed' , message=f'The book : {booksInfoBorrow[borrowID][0]}\nwritten by : {booksInfoBorrow[borrowID][1]}\nwith ID : {borrowID}\nsuccessfully borrowed.')
            else:
                messagebox.showerror(title='Already borrowed' , message=f'The book : {booksInfoBorrow[borrowID][0]}\nwritten by : {booksInfoBorrow[borrowID][1]}\nwith ID : {borrowID}\nhas already been borrowed.')
        except KeyError:
            messagebox.showerror(title='The book was not found' , message=f'There is no book with ID : {borrowID}.')
    else:
        messagebox.showerror(title='Invalid ID' , message='The entered book ID is not correct.')
    BorrowIDEntry.delete(0 , END)
    BorrowIDEntry.focus_force()


#Return
def ReturnBook(): 
    
    global ReturnIDEntry

    #Error for when there are no books
    try:
        bookFile = open('src/BookList.txt')
        bookFile.close()

        #Main
        bookReturnRoot = Toplevel(library_app)
        bookReturnRoot.title('Library')
        bookReturnRoot.minsize(width=400 , height=300)
        bookReturnRoot.maxsize(width=900 , height=800)
        bookReturnRoot.geometry('600x500')
        bookReturnRoot.iconbitmap('src/Icon.ico')
        
        #Canvas
        CanvasBookReturn = Canvas(bookReturnRoot)
        CanvasBookReturn.config(bg='#8c663b')
        CanvasBookReturn.pack(expand=True , fill=BOTH)
        
        #Heading
        bookReturnFrame = Frame(bookReturnRoot , bg='#FFBB00' , bd=5)
        bookReturnFrame.place(relx=0.25 , rely=0.1 , relwidth=0.5 , relheight=0.13)
            
        bookReturnLabel = Label(bookReturnFrame , text='Return Book' , bg='black' , fg='white' , font=('Comic Sans MS' , 18))
        bookReturnLabel.place(relx=0 , rely=0 , relwidth=1 , relheight=1)
        
        #Info
        bookReturnInfoFrame = Frame(bookReturnRoot , bg='black')
        bookReturnInfoFrame.place(relx=0.1 , rely=0.3 , relwidth=0.8 , relheight=0.5)   
            
        ReturnIDLabel = Label(bookReturnInfoFrame , text='Book ID : ' , bg='black' , fg='white' , font=fonts)
        ReturnIDLabel.place(relx=0.07 , rely=0.43)
            
        ReturnIDEntry = Entry(bookReturnInfoFrame)
        ReturnIDEntry.place(relx=0.28 , rely=0.46 , relwidth=0.62)

        #Submit Button
        btnBookReturn = Button(bookReturnRoot , text='Return' , bg='#f7f1e3' , fg='black' , font=fonts , command=Return)
        btnBookReturn.place(relx=0.28 , rely=0.9 , relwidth=0.18 , relheight=0.08)
        
        #Quit Button
        btnQuitBookReturn = Button(bookReturnRoot , text='Exit' , bg='#f7f1e3' , fg='black' , font=fonts , command=bookReturnRoot.destroy)
        btnQuitBookReturn.place(relx=0.53 , rely=0.9 , relwidth=0.18 , relheight=0.08)
        
        bookReturnRoot.mainloop()

    except FileNotFoundError:
        messagebox.showerror(title='No book' , message='There is no book registered in this library.')

def Return():
    
    #Get ID
    returnID = ReturnIDEntry.get().strip()
    if len(returnID) == 3:
        try:
            dicReturn = {}
            booksInfoReturn = getbooksinfo('src/BookList.txt' , dicReturn)
            if booksInfoReturn[returnID][-1] == 'taken':
                new_file = []
                with open('src/BookList.txt' , 'r') as file:
                    for line in file:
                        if line[ : 3] == returnID:
                            new_file.append(line.replace('taken' , 'not taken'))
                        else:
                            new_file.append(line)
                file.close()
                with open('src/BookList.txt' , 'w') as file:
                    for line in new_file:
                        file.writelines(line)
                file.close()
                messagebox.showinfo(title='Successfully returned' , message=f'The book : {booksInfoReturn[returnID][0]}\nwritten by : {booksInfoReturn[returnID][1]}\nwith ID : {returnID}\nsuccessfully returned.')
            else:
                messagebox.showerror(title='Not borrowed' , message=f'The book : {booksInfoReturn[returnID][0]}\nwritten by : {booksInfoReturn[returnID][1]}\nwith ID : {returnID}\nhas not been borrowed before.')
        except KeyError:
            messagebox.showerror(title='The book was not found' , message=f'There is no book with ID : {returnID}.')
    else:
        messagebox.showerror(title='Invalid ID' , message='The entered book ID is not correct.')
    ReturnIDEntry.delete(0 , END)
    ReturnIDEntry.focus_force()


#Add
def AddBook():
    
    global AddTitleEntry , AddAuthorEntry
    
    #Main
    bookAddRoot = Toplevel(library_app)
    bookAddRoot.title('Library')
    bookAddRoot.minsize(width=400 , height=300)
    bookAddRoot.maxsize(width=900 , height=800)
    bookAddRoot.geometry('600x500')
    bookAddRoot.iconbitmap('src/Icon.ico')

    #Canvas
    CanvasBookAdd = Canvas(bookAddRoot)
    CanvasBookAdd.config(bg='#683b8c')
    CanvasBookAdd.pack(expand=True , fill=BOTH)
        
    #Heading
    bookAddFrame = Frame(bookAddRoot , bg='#FFBB00' , bd=5)
    bookAddFrame.place(relx=0.25 , rely=0.1 , relwidth=0.5 , relheight=0.13)

    bookAddLabel = Label(bookAddFrame , text='Add Book' , bg='black' , fg='white' , font=('Comic Sans MS' , 18))
    bookAddLabel.place(relx=0 , rely=0 , relwidth=1 , relheight=1)

    #Info
    bookAddInfoFrame = Frame(bookAddRoot , bg='black')
    bookAddInfoFrame.place(relx=0.1 , rely=0.3 , relwidth=0.8 , relheight=0.5)
    
    AddTitleLabel = Label(bookAddInfoFrame , text='Book Title : ' , bg='black' , fg='white' , font=fonts)
    AddTitleLabel.place(relx=0.06 , rely=0.33)

    AddTitleEntry = Entry(bookAddInfoFrame)
    AddTitleEntry.place(relx=0.29 , rely=0.36 , relwidth=0.62)
    
    AddAuthorLabel = Label(bookAddInfoFrame,text='Book Author : ' , bg='black' , fg='white' , font=fonts)
    AddAuthorLabel.place(relx=0.06 , rely=0.50)
        
    AddAuthorEntry = Entry(bookAddInfoFrame)
    AddAuthorEntry.place(relx=0.29 , rely=0.53 , relwidth=0.62)
        
    #Submit Button
    SubmitBtn = Button(bookAddRoot,text='Add' , bg='#f7f1e3' , fg='black' , font=fonts , command=Add)
    SubmitBtn.place(relx=0.28 , rely=0.9 , relwidth=0.18 , relheight=0.08)
    
    #Quit Button
    btnQuitBookAdd = Button(bookAddRoot , text='Exit' , bg='#f7f1e3' , fg='black' , font=fonts , command=bookAddRoot.destroy)
    btnQuitBookAdd.place(relx=0.53 , rely=0.9 , relwidth=0.18 , relheight=0.08)
    
    bookAddRoot.mainloop()

def Add():
    
    #Get values
    bookTitle = AddTitleEntry.get().title().strip()
    bookAuthor = AddAuthorEntry.get().title().strip()
    if len(bookTitle) != 0:
        if len(bookAuthor) != 0:
            lst1 = []
            bookInfoList = gettitleandauthor('src/BookList.txt' , lst1)
            bookInfo = [bookTitle , bookAuthor]
            if bookInfo in bookInfoList:
                messagebox.showerror(title='Already added' , message='This book has already been added.')
                AddTitleEntry.delete(0 , END)
                AddAuthorEntry.delete(0 , END)
                AddTitleEntry.focus_force()
            else:
                bookID = getlastid('src/BookList.txt')
                if 99 > int(bookID) >= 9:
                    bookID = f'0{str(int(bookID)+1)}'
                elif int(bookID) >= 99:
                    bookID = f'{str(int(bookID)+1)}'
                else:
                    bookID = f'00{str(int(bookID)+1)}'
                bookList = open('src/BookList.txt' , 'a')
                bookList.write(f'{bookID} - {bookTitle} - {bookAuthor} - not taken\n')
                bookList.close()
                messagebox.showinfo(title='Successfully added' , message=f'The book : {bookTitle}\nwritten by : {bookAuthor}\nwith ID : {bookID}\nhas been successfully added.')
                AddTitleEntry.delete(0 , END)
                AddAuthorEntry.delete(0 , END)
                AddTitleEntry.focus_force()
        else:
                messagebox.showerror(title='Invalid author' , message='The entered book author is not correct.')
                AddAuthorEntry.delete(0 , END)
                AddAuthorEntry.focus_force()
    else:
        messagebox.showerror(title='Invalid title' , message='The entered book title is not correct.')
        AddTitleEntry.delete(0 , END)
        AddTitleEntry.focus_force()


#Delete
def DeleteBook(): 
    
    global DeleteIDEntry

    #Error for when there are no books
    try:
        bookFile = open('src/BookList.txt')
        bookFile.close()

        #Main
        bookDeleteRoot = Toplevel(library_app)
        bookDeleteRoot.title('Library')
        bookDeleteRoot.minsize(width=400 , height=300)
        bookDeleteRoot.maxsize(width=900 , height=800)
        bookDeleteRoot.geometry('600x500')
        bookDeleteRoot.iconbitmap('src/Icon.ico')
        
        #Canvas
        CanvasBookDelete = Canvas(bookDeleteRoot)
        CanvasBookDelete.config(bg='#3b8c5a')
        CanvasBookDelete.pack(expand=True , fill=BOTH)
            
        #Heading
        bookDeleteFrame = Frame(bookDeleteRoot , bg='#FFBB00' , bd=5)
        bookDeleteFrame.place(relx=0.25 , rely=0.1 , relwidth=0.5 , relheight=0.13)
            
        bookDeleteLabel = Label(bookDeleteFrame, text='Delete Book' , bg='black', fg='white', font=('Comic Sans MS' , 18))
        bookDeleteLabel.place(relx=0 , rely=0 , relwidth=1 , relheight=1)
        
        #Info
        bookDeleteInfoFrame = Frame(bookDeleteRoot , bg='black')
        bookDeleteInfoFrame.place(relx=0.1 , rely=0.3 , relwidth=0.8 , relheight=0.5)   

        DeleteIDLabel = Label(bookDeleteInfoFrame,text='Book ID : ' , bg='black' , fg='white' , font=fonts)
        DeleteIDLabel.place(relx=0.07 , rely=0.43)
            
        DeleteIDEntry = Entry(bookDeleteInfoFrame)
        DeleteIDEntry.place(relx=0.28 , rely=0.46 , relwidth=0.62)
        
        #Submit Button
        SubmitBtn = Button(bookDeleteRoot , text='Delete' , bg='#f7f1e3' , fg='black' , font=fonts , command=Delete)
        SubmitBtn.place(relx=0.28 , rely=0.9 , relwidth=0.18 , relheight=0.08)
        
        #Quit Button
        btnQuitBookDelete = Button(bookDeleteRoot,text='Exit' , bg='#f7f1e3' , fg='black' , font=fonts , command=bookDeleteRoot.destroy)
        btnQuitBookDelete.place(relx=0.53 , rely=0.9 , relwidth=0.18 , relheight=0.08)
        
        bookDeleteRoot.mainloop()
    except FileNotFoundError:
        messagebox.showerror(title='No book' , message='There is no book registered in this library.')

def Delete():

    #Get ID
    deleteID = DeleteIDEntry.get().strip()
    if len(deleteID) == 3:
        try:
            dicDelete = {}
            booksInfoDelete = getbooksinfo('src/BookList.txt' , dicDelete)
            if deleteID in booksInfoDelete.keys():
                new_file = []
                with open('src/BookList.txt' , 'r') as file:
                    for line in file:
                        if int(line[ : 3]) < int(deleteID):
                            new_file.append(line)
                        if line[ : 3] == deleteID:
                            pass
                        if int(line[ : 3]) > int(deleteID):
                            if int(line[ : 3]) <= 10 :
                                new_file.append(line.replace(line[ : 3] , f'00{str(int(line[ : 3])-1)}'))
                            elif 10 < int(line[ : 3]) <=100:
                                new_file.append(line.replace(line[ : 3] , f'0{str(int(line[ : 3])-1)}'))
                            else:
                                new_file.append(line.replace(line[ : 3] , f'{str(int(line[ : 3])-1)}'))
                file.close()
                with open('src/BookList.txt' , 'w') as file:
                    for line in new_file:
                        file.writelines(line)
                file.close()
                messagebox.showinfo(title='Successfully deleted' , message=f'The book : {booksInfoDelete[deleteID][0]}\nwritten by : {booksInfoDelete[deleteID][1]}\nwith ID : {deleteID}\nhas been successfully deleted.')
            else:
                messagebox.showerror(title='The book was not found' , message=f'There is no book with ID : {deleteID}.')
        except KeyError:
            messagebox.showerror(title='The book was not found' , message=f'There is no book with ID : {deleteID}.')
    else:
        messagebox.showerror(title='Invalid ID' , message='The entered book ID is not correct.')
    DeleteIDEntry.delete(0 , END)
    DeleteIDEntry.focus_force()


#Main App
library_app = Tk()
library_app.title('Library')
library_app.minsize(width=400 , height=300)
library_app.maxsize(width=900 , height=800)
library_app.geometry('600x500')
library_app.iconbitmap('src/Icon.ico')

#Background Image

backgroundImage =Image.open('src/background.jpg')
[imageSizeWidth , imageSizeHeight] = backgroundImage.size

newImageSizeWidth = int(imageSizeWidth*0.25)
newImageSizeHeight = int(imageSizeHeight*0.25)

backgroundImage = backgroundImage.resize((newImageSizeWidth , newImageSizeHeight))
img = ImageTk.PhotoImage(backgroundImage)

CanvasMain = Canvas(library_app)
CanvasMain.create_image(350 , 540 , image = img)      
CanvasMain.config(bg='white' , width = newImageSizeWidth , height = newImageSizeHeight)
CanvasMain.pack(expand=True , fill=BOTH)

#Heading
welcomeFrame = Frame(library_app , bg='#FFBB00' , bd=5)
welcomeFrame.place(relx=0.2 , rely=0.05 , relwidth=0.6 , relheight=0.16)

welcomeLabel = Label(welcomeFrame, text='Welcome to Library' , bg='black' , fg='white' , font=('Comic Sans MS' , 18))
welcomeLabel.place(relx=0 , rely=0 , relwidth=1 , relheight=1)

#Buttons
btnBookList = Button(library_app , text='Book List' , bg='black' , fg='white' , font=fonts , command=BookList)
btnBookList.place(relx=0.28 , rely=0.25 , relwidth=0.45 , relheight=0.1)

btnBookSearch = Button(library_app , text='Search Book' , bg='black' , fg='white' , font=fonts , command=SearchBook)
btnBookSearch.place(relx=0.28 , rely=0.35 , relwidth=0.45 , relheight=0.1)

btnBookBorrow = Button(library_app , text='Borrow Book' , bg='black' , fg='white' , font=fonts , command=BorrowBook)
btnBookBorrow.place(relx=0.28 , rely=0.45 , relwidth=0.45 , relheight=0.1)
    
btnBookReturn = Button(library_app , text='Return Book' , bg='black' , fg='white' , font=fonts , command=ReturnBook)
btnBookReturn.place(relx=0.28 , rely=0.55 , relwidth=0.45 , relheight=0.1)

btnBookAdd = Button(library_app , text='Add Book' , bg='black' , fg='white' , font=fonts , command=AddBook)
btnBookAdd.place(relx=0.28 , rely=0.65 , relwidth=0.45 , relheight=0.1)

btnBookDelete = Button(library_app , text='Delete Book' , bg='black' , fg='white' , font=fonts , command=DeleteBook)
btnBookDelete.place(relx=0.28 , rely=0.75 , relwidth=0.45 , relheight=0.1)

btnQuit = Button(library_app , text='Exit' , bg='black' , fg='white' , font=fonts , command=library_app.destroy)
btnQuit.place(relx=0.28 , rely=0.85 , relwidth=0.45 , relheight=0.1)
library_app.bind('<Escape>' , exitapp)
mainloop()
