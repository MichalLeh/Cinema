import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from functools import partial
import sqlite3
from sqlite3 import Error
import webbrowser
import re 

class Cinema(tk.Frame):
    def __init__(self, root):
        self.root = root
        # Title of the window
        self.root.title("Cinema")
        # Window Geometry
        self.screenWidth = 1250 
        self.screenHeight = 900 
        self.root.geometry("{}x{}+0+50".format(self.screenWidth, self.screenHeight))
        # Define colors
        self.backgroundColor = '#1f1f1f'
        self.headingColor = '#e8b321'
        self.contentColor = '#cccccc'
        self.btnColor = '#5c7e39'

        self.root.configure(background=self.backgroundColor)
               
        self.imgList = ['Terminator', 'Die Hard', 'Matrix', 'Braveheart', 'The Rock', 'Aliens', 'Rocky', 'Heat']
        # Call initial screen
        self.screeningMovies()
        
    def clearScreen(self, *args):
        '''Deletes widgets in current screen and calls desired function'''
        # Clear placeOrder (shopping basket) screen
        if args[0] == 'placeOrder':
            buttons = self.formFrame.grid_slaves()
            for button in buttons:
                button.destroy()
            slaves = [self.headingFrame, self.ticketFrame, self.formFrame]
            for slave in slaves:
                slave.destroy()
            # Move back to Screening Hall
            if args[2] == 'back':
                self.screeningHallSeats(args[1])
            # Move to End screen
            elif args[2] == 'continue':
                self.theEnd()
        # Clear Movie detail screen and move back to Screening movies (initial screen)
        elif args[0] == 'movieDetail':
            slaves = [self.posterFrame, self.contentFrame, self.screeningFrame]
            for slave in slaves:
                slave.destroy()
            self.screeningMovies()
        # Clear Screening hall screen
        elif args[0] == 'screeningHallSeats':
            buttons = self.Frame.grid_slaves()
            for button in buttons:
                button.destroy()
            slaves = [self.seatsFrame, self.titleFrame, self.Frame]
            for slave in slaves:
                slave.destroy()
            # Move back to Movie detail screen
            if args[2] == 'back':
                self.movieDetail(args[1]['movieNumber'])
            # Move to Place order screen (shopping basket)
            elif args[2] == 'continue':
                self.placeOrder(args[1])
        # Clear Screening movies screen and move to Movie detail screen
        elif args[0] == 'screeningMovies':
            slaves = [self.cinemaTitleFrame, self.posterFrame]
            buttons = self.posterFrame.grid_slaves()
            for button in buttons:
                button.destroy()
            for slave in slaves:
                slave.destroy()
            self.movieDetail(args[1])
        # Clear Movie detail screen and move to Screening Hall
        elif args[0] == 'screeningTime':
            slaves = [self.posterFrame, self.contentFrame, self.screeningFrame]
            for slave in slaves:
                slave.destroy()
            self.screeningHallSeats(args[1])

    def theEnd(self):
        '''Final sscreen - display label message'''

        # Display label message
        text = 'Děkujeme. Přejeme příjemný zážitek!'
        titleLbl = Label(self.root, text=text, justify=LEFT, bg=self.backgroundColor, fg=self.headingColor, font=("Helvetica", 24))
        titleLbl.place(x=self.screenWidth/4, y=self.screenHeight/2)

    def hyperlink(self, link):
        '''Open webbrowser and link to CSFD site'''
        webbrowser.open_new(link)

    def priceChange(self, index, row, value):
        '''Change the price based on chosen ticket category'''
        
        # DB connect
        connection = sqlite3.connect('database.db')
        updateCursor = connection.cursor()

        # Load the price label into wdg
        wdg = self.ticketWdgLst[row-1][-2]
        # Update price label and table Tickets
        if value !='Základní':
            update = """UPDATE Tickets SET ticketType = ?, ticketPrice = ? WHERE id = ?"""
            price = '139 Kč'
            wdg.configure(text=price)
        else:
            update = """UPDATE Tickets SET ticketType = ?, ticketPrice = ? WHERE id = ?"""
            price = '179 Kč'
            wdg.configure(text=price)
            
        updateCursor.execute(update, (value, price, index, ))
        connection.commit()
        # DB close
        updateCursor.close()
        connection.close()

    def delTicket(self, index, indexNumber, row):
        '''Erase ticket widgets after clicking on delete button'''

        # DB connect
        connection = sqlite3.connect('database.db')
        deleteCursor = connection.cursor()
        updateCursor = connection.cursor()

        # Get seat (Sedadlo) and row (Řada) label from list
        wdgCol = self.ticketWdgLst[row-1][-4]
        wdgRow = self.ticketWdgLst[row-1][-5]
        # Delete from tickets based on id
        delete = """DELETE FROM Tickets WHERE id = ?"""
        # Update ScreeningHallOccupancy's table from 'yes' to 'no' as not occupied anymore fro correct hallRow and hallColumn
        if wdgCol.cget('text') == 0:
            update = """UPDATE ScreeningHallOccupancy SET hallColumn_0 = ? WHERE indexNumber = ? and hallRow = ?"""
        elif wdgCol.cget('text') == 1:
            update = """UPDATE ScreeningHallOccupancy SET hallColumn_1 = ? WHERE indexNumber = ? and hallRow = ?"""
        elif wdgCol.cget('text') == 2:
            update = """UPDATE ScreeningHallOccupancy SET hallColumn_2 = ? WHERE indexNumber = ? and hallRow = ?"""
        elif wdgCol.cget('text') == 3:
            update = """UPDATE ScreeningHallOccupancy SET hallColumn_3 = ? WHERE indexNumber = ? and hallRow = ?"""
        elif wdgCol.cget('text') == 4:
            update = """UPDATE ScreeningHallOccupancy SET hallColumn_4 = ? WHERE indexNumber = ? and hallRow = ?"""

        updateCursor.execute(update, ('no', indexNumber, wdgRow.cget('text'),  ))
        deleteCursor.execute(delete, (index, ))
        
        connection.commit()
        # DB close
        updateCursor.close()
        deleteCursor.close()
        connection.close()

        # Erase it from tkinter grid
        slaves = self.ticketWdgLst[row-1]
        for slave in slaves:
            slave.destroy()

    def checkAllValue(self, tempInfoDict):
        '''Test correctness of entry value after clicking on continue button '''

        # Test entry field
        textValid = 0
        for nest, regex, title in zip(['name', 'surname', 'email', 'phone'], ['^[a-z]+$', '^[a-z]+$', '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', '^[0-9]{9,9}$'], ['Jméno', 'Příjmení', 'Email', 'Telefon']):
            lbl = self.entryLabelDict[nest]['label']
            ent = self.entryLabelDict[nest]['entry']
            if ent.get() == 0 and 'chybný' not in lbl.cget('text'):
                lbl.configure(text='{} má chybný formát'.format(title), bg=self.backgroundColor, fg='red')
            elif ent.get() != 0 and 'chybný' not in lbl.cget('text'):
                if(re.search(regex, ent.get())):
                    textValid += 1
                else:
                    lbl.configure(text='{} má chybný formát'.format(title), bg=self.backgroundColor, fg='red')
            elif ent.get() != 0 and 'chybný' in lbl.cget('text'):
                if(re.search(regex, ent.get())):
                    textValid += 1
                    lbl.configure(text=title, bg=self.backgroundColor, fg=self.contentColor)    
        
        # Call self.clearScreen func
        if textValid == 4:
            self.clearScreen('placeOrder', tempInfoDict, 'continue')

    def placeOrder(self, tempInfoDict):
        '''Display movie tickets (shopping basket) and form to fill out'''

        # Load image
        delImg = PhotoImage(file="J:\CinemaTown\Images\delete.png")
        delImg = delImg.zoom(10).subsample(256)
        # Label frames
        self.headingFrame = LabelFrame(self.root, bg=self.backgroundColor, bd=0)
        self.headingFrame.place(x=150, y=50, width=900, height=200)
        self.ticketFrame = LabelFrame(self.root, bg=self.backgroundColor, bd=0)
        self.ticketFrame.place(x=150, y=100, width=900, height=700)
        self.formFrame = LabelFrame(self.root, bg=self.backgroundColor, bd=0)
        self.formFrame.place(x=150, y=700, width=900, height=200)
     
        ticketTypeOption = ['Základní', 'Dítě', 'Senior', 'Student', 'ZTP']
        titleList = ['Sál', 'Film', 'Datum', 'Čas', 'Řada', 'Sedadlo', 'Kategorie', 'Cena']
        
        # Main heading label
        headingLbl = Label(self.headingFrame, text='Přehled objednávky', bg=self.backgroundColor, fg=self.headingColor, font=("Helvetica", 16, "bold"))
        headingLbl.grid(row=0, column=0)
        # Headings for for ticket's information
        for col in range(len(titleList)):
            titleLbl = Label(self.ticketFrame, text=[titleList[col]], padx=10, pady=10, bg=self.backgroundColor, fg=self.headingColor, font=("Helvetica", 14))
            titleLbl.grid(row=0, column=col)

        # DB connect
        connection = sqlite3.connect('database.db')
        selectCursor = connection.cursor()
        # Load Ticket's table records into ticketRecords
        selectTicket = "select * from Tickets"
        selectCursor.execute(selectTicket) 
        ticketRecords = selectCursor.fetchall()
        
        # Nested list
        self.ticketWdgLst = [[] for _ in range(len(ticketRecords))]

        # Labels, option menu and assign them data from ticketRecords
        row = 1
        for record in ticketRecords: 
            for col in range(len(titleList)-2):     
                valueLbl = Label(self.ticketFrame, text=record[col+3], padx=10, pady=10, bg=self.backgroundColor, fg=self.contentColor, font=("Helvetica", 12)) 
                valueLbl.grid(row=row, column=col)
                self.ticketWdgLst[row-1].append(valueLbl) 
            
            # Option menu and pass in the ticketTypeVal and the ticketTypeOption list
            ticketTypeVal = StringVar(self.ticketFrame)
            ticketTypeVal.set(record[9])
            ticketCategoryMn = OptionMenu(self.ticketFrame, ticketTypeVal, *ticketTypeOption, command=partial(self.priceChange, record[0], row))
            ticketCategoryMn.grid(row=row, column=col+1)
            # Price label
            priceLbl = Label(self.ticketFrame, text=record[10], padx=10, pady=10, bg=self.backgroundColor, fg=self.contentColor, font=("Helvetica", 12))
            priceLbl.grid(row=row, column=col+2)
            # Button to delete ticket from shopping basket and database
            delBtn = Button(self.ticketFrame, image=delImg, bg=self.backgroundColor, command=partial(self.delTicket, record[0], record[1], row))
            delBtn.image = delImg
            delBtn.grid(row=row, column=col+3)
            # Append widgets into list to identify them later in self.priceChange func
            self.ticketWdgLst[row-1].extend((ticketCategoryMn, priceLbl, delBtn))
            row += 1

        # DB close
        connection.close()

        # Form labels and entries
        self.entryLabelDict = {'name' : {'label': None, 'entry': None}, 'surname' : {'label': None, 'entry': None}, 'email': {'label': None, 'entry': None}, 'phone': {'label': None, 'entry': None}}

        nameLbl = Label(self.formFrame, text='Jméno', padx=10, pady=15, bg=self.backgroundColor, fg=self.contentColor, font=("Helvetica", 12))
        nameLbl.grid(row=0, column=0)
        nameEnt = Entry(self.formFrame)
        nameEnt.grid(row=0, column=1)

        surnameLbl = Label(self.formFrame, text='Příjmení', padx=10, pady=15, bg=self.backgroundColor, fg=self.contentColor, font=("Helvetica", 12))
        surnameLbl.grid(row=0, column=2)
        surnameEnt = Entry(self.formFrame)
        surnameEnt.grid(row=0, column=3)

        emailLbl = Label(self.formFrame, text='Email', padx=10, pady=15, bg=self.backgroundColor, fg=self.contentColor, font=("Helvetica", 12))
        emailLbl.grid(row=1, column=0)
        emailEnt = Entry(self.formFrame)
        emailEnt.grid(row=1, column=1)  

        phoneLbl = Label(self.formFrame, text='Telefon', padx=10, pady=15, bg=self.backgroundColor, fg=self.contentColor, font=("Helvetica", 12))
        phoneLbl.grid(row=1, column=2)
        phoneEnt = Entry(self.formFrame)
        phoneEnt.grid(row=1, column=3)

        # Append labels and entries into dict to identify them later in self.checkAllValue func
        for lbl, ent, nest in zip([nameLbl, surnameLbl, emailLbl, phoneLbl], [nameEnt, surnameEnt, emailEnt, phoneEnt], ['name', 'surname', 'email', 'phone']):
            self.entryLabelDict[nest]['label'] = lbl
            self.entryLabelDict[nest]['entry'] = ent

        # Back/Continue buttons
        backBtn = Button(self.formFrame, text='Zpět', bg=self.btnColor, fg=self.backgroundColor, bd=1, font=("Helvetica", 12, "bold"), command = lambda: self.clearScreen('placeOrder', tempInfoDict, 'back'))
        backBtn.grid(row=2, column=0, pady=15)
        continueBtn = Button(self.formFrame, text='Pokračovat', bg=self.btnColor, fg=self.backgroundColor, bd=1, font=("Helvetica", 12, "bold"), command = lambda: self.checkAllValue(tempInfoDict))
        continueBtn.grid(row=2, column=3, pady=15)
        self.conWdg = continueBtn

    def fillSeat(self, tempInfoDict, btnNumber):
        '''Function enables user (customer) to choose seats'''
        
        # DB connect
        connection = sqlite3.connect('database.db')
        updateCursor = connection.cursor()
        insdelCursor = connection.cursor()

        # Check button's (seat's) current image, then change its image, hallRow's, hallColumn's data and create/delete record in Ticket table
        bname = self.chairBtnNumber[btnNumber]
        if bname.cget('image')==str(self.chairImg):
            bname.configure(image=self.checkImg)
            if bname.grid_info()['column'] == 0:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_0 = ? WHERE indexNumber = ? and hallRow = ?"""
            elif bname.grid_info()['column'] == 1:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_1 = ? WHERE indexNumber = ? and hallRow = ?"""
            elif bname.grid_info()['column'] == 2:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_2 = ? WHERE indexNumber = ? and hallRow = ?"""
            elif bname.grid_info()['column'] == 3:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_3 = ? WHERE indexNumber = ? and hallRow = ?"""
            elif bname.grid_info()['column'] == 4:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_4 = ? WHERE indexNumber = ? and hallRow = ?"""
            occupied = "yes"
            insdelCursor.execute("INSERT INTO Tickets (indexNumber, movieNumber, screeningHall, movieName, screeningDate, screeningTime, ticketRow, ticketCol, ticketType, ticketPrice) values(?,?,?,?,?,?,?,?,?,?)",
                                            (tempInfoDict['indexNumber'], tempInfoDict['movieNumber'], tempInfoDict['hall'], tempInfoDict['name'],
                                            tempInfoDict['date'], tempInfoDict['time'], bname.grid_info()['row'], bname.grid_info()['column'], 'Základní', '179 Kč'))
            

        else:
            bname.configure(image=self.chairImg)
            if bname.grid_info()['column'] == 0:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_0 = ? WHERE indexNumber = ? and hallRow = ?"""
            elif bname.grid_info()['column'] == 1:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_1 = ? WHERE indexNumber = ? and hallRow = ?"""
            elif bname.grid_info()['column'] == 2:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_2 = ? WHERE indexNumber = ? and hallRow = ?"""
            elif bname.grid_info()['column'] == 3:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_3 = ? WHERE indexNumber = ? and hallRow = ?"""
            elif bname.grid_info()['column'] == 4:
                occupiedSeatInsert = """UPDATE ScreeningHallOccupancy SET hallColumn_4 = ? WHERE indexNumber = ? and hallRow = ?"""
                
            deleteQuery = ("DELETE from Tickets WHERE ticketRow = ? and ticketCol = ?")
            insdelCursor.execute(deleteQuery, (bname.grid_info()['row'], bname.grid_info()['column'] ))
            occupied = "no"
            
        updateCursor.execute(occupiedSeatInsert, (occupied, tempInfoDict['indexNumber'], bname.grid_info()['row'],  ))

        connection.commit()
        # DB close
        insdelCursor.close()
        updateCursor.close()
        connection.close()

    def screeningHallSeats(self, tempInfoDict): 
        '''Display movie name, screening date and time, hall seats setup and occupation of each seat'''
        
        # Load images
        self.chairImg = PhotoImage(file="J:\CinemaTown\Images\chair.png")
        self.chairImg = self.chairImg.zoom(40).subsample(256)
        self.checkImg = PhotoImage(file="J:\CinemaTown\Images\check.png")
        self.checkImg = self.checkImg.zoom(40).subsample(256)
        # Label frames
        self.Frame = LabelFrame(self.root, bg=self.backgroundColor, bd=0)
        self.Frame.place(x=0, y=0, width=1250, height=900)
        self.titleFrame = LabelFrame(self.Frame, bg=self.backgroundColor, bd=0)
        self.titleFrame.place(x=455.5, y=50, width=365, height=75)
        self.seatsFrame = LabelFrame(self.Frame, bg=self.backgroundColor, bd=0)
        self.seatsFrame.place(x=422.5, y=247.5, width=405, height=405)

        # List stores unique button's numbers
        self.chairBtnNumber = []

        indexNumber = tempInfoDict['indexNumber']
        hallNumber = tempInfoDict['hall']
        
        # Labels for displaying movie name, hall, screening date and time 
        nameLbl = Label(self.titleFrame, text=("{}".format(tempInfoDict['name'])),
        justify=CENTER, bg=self.backgroundColor, fg=self.headingColor, font=("Helvetica", 18, 'bold'))
        nameLbl.grid(row=0, column=0)
        screeningLbl = Label(self.titleFrame, text=("{}, {}, {}".format(tempInfoDict['hall'], tempInfoDict['date'], tempInfoDict['time'])),
        justify=CENTER,  bg=self.backgroundColor, fg=self.headingColor, font=("Helvetica", 18, 'bold'))
        screeningLbl.grid(row=1, column=0)

        # DB connect
        connection = sqlite3.connect('database.db')
        # Select chosen hall's setup from ScreeningHallSetup table 
        selectHall = "select * from ScreeningHallSetup WHERE screeningHall = ?"
        # Select hall's seat occupancy from ScreeningHallOccupancy table
        occupiedSeat = "select * from ScreeningHallOccupancy WHERE indexNumber = ?" 
        # Load ScreeningHallSetup's table records
        selectCursor = connection.cursor()
        selectCursor.execute(selectHall, (hallNumber, ))
        hallRecords = selectCursor.fetchall()
        # Load ScreeningHallOccupancy's table records
        selectCursor = connection.cursor()
        selectCursor.execute(occupiedSeat, (indexNumber, ))
        seatRecords = selectCursor.fetchall()

        btnNumber = 0
        # Buttons, assign a unique argument (btnNumber) to run the function (self.fillSeat)
        for hallRecord, seatRecord in zip(hallRecords, seatRecords):
            # Range(2,7) represents hallColumn_0 upto hallColumn_4 data in both hallRecords and seatRecords
            for col in range(2,7):
                # Number 255 means seat doesnt exist
                if hallRecord[col] != 255:
                    if seatRecord[col] == 'no':
                        # Create Non-occupied buttons (seats)
                        chairBtn = Button(self.seatsFrame, image=self.chairImg, bg=self.backgroundColor, bd=0, command=partial(self.fillSeat, tempInfoDict, btnNumber))
                        chairBtn.image = self.chairImg
                        chairBtn.grid(row=hallRecord[1], column=hallRecord[col], sticky=NSEW)
                        self.chairBtnNumber.append(chairBtn)
                        btnNumber += 1
                    elif seatRecord[col] == 'yes':
                        # Create Occupied (disabled) buttons (seats)
                        chairBtn = Button(self.seatsFrame, image=self.checkImg, bg=self.backgroundColor, bd=0, command=partial(self.fillSeat, btnNumber), state='disabled')
                        chairBtn.image = self.checkImg
                        chairBtn.grid(row=hallRecord[1], column=hallRecord[col], sticky=NSEW)
                        self.chairBtnNumber.append(chairBtn)      
                        btnNumber += 1
                else:
                    pass
        
        # DB close
        selectCursor.close()
        connection.close()

        # Back/Continue buttons
        backBtn = Button(self.Frame, text='Zpět', bg=self.btnColor, fg=self.backgroundColor, bd=1, font=("Helvetica", 12, "bold"), command = lambda: self.clearScreen('screeningHallSeats', tempInfoDict, 'back'))
        backBtn.place(x=422.5, y=652.5)
        continueBtn = Button(self.Frame, text='Pokračovat', bg=self.btnColor, fg=self.backgroundColor, bd=1, font=("Helvetica", 12, "bold"), command = lambda: self.clearScreen('screeningHallSeats', tempInfoDict, 'continue'))
        continueBtn.place(x=710, y=652.5)

    def movieDetail(self, movieNumber):
        '''Display basic infromation about movie and its screening hall, dates and time'''
        
        # Label frames
        self.posterFrame = LabelFrame(self.root, bg=self.backgroundColor, bd=0)
        self.posterFrame.place(x=0, y=0, width=315, height=450)
        self.contentFrame = LabelFrame(self.root, relief=GROOVE, bg=self.backgroundColor, bd=0)
        self.contentFrame.place(x=315, y=0, width=935, height=450)
        self.screeningFrame = LabelFrame(self.root, relief=GROOVE, bg=self.backgroundColor, bd=0)
        self.screeningFrame.place(x=0, y=450, width=1250, height=450)
        
        # Dictionary is used for sharing info between screens
        tempInfoDict = {}

        # DB connect
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        # Select requested movie info (name, director, music composer, actors, description, hyperlink) from Movieinfo table
        selectMovieNumber = "select * from Movieinfo WHERE movieNumber = ?"
        selectCursor = connection.cursor()
        selectCursor.execute(selectMovieNumber, (movieNumber, ))
        records = selectCursor.fetchone()

        # Load images
        posterImg = PhotoImage(file="J:\CinemaTown\Images\{}.png".format(self.imgList[movieNumber]))
        posterImg = posterImg.zoom(4).subsample(8)
        csfdImg = PhotoImage(file="J:\CinemaTown\Images\csfd.png")
        csfdImg = csfdImg.zoom(4).subsample(12)
            
        # Movie poster label
        posterBtn = Label(self.posterFrame, image=posterImg)
        posterBtn.image = posterImg
        posterBtn.grid(row=0, column=0, padx=15, pady=15)   

        # Labels to display description, director, composer, actors
        contentList = [records[6], "Režisér: {}".format(records[2]), "Hudba: {}".format(records[3]), "Herci: {}".format(records[4])]
        row = 0
        for content in contentList:
            textLabel = Label(self.contentFrame, text=content, justify=LEFT, wraplength=900, bg=self.backgroundColor, fg=self.contentColor, font=("Helvetica Neue", 16))
            textLabel.grid(row=row, column=0, padx=5, pady=5, sticky=W)
            row+=1           

        # Link to the movie information on the CSFD website
        csfdBtn = Button(self.contentFrame, image=csfdImg, command=partial(self.hyperlink, records[7]))       
        csfdBtn.image = csfdImg
        csfdBtn.grid(row=4, column=0, padx=15, pady=15, sticky=W)

        # Select requested screening info (date, hall, time ...) from MovieScreening table
        selectMovieNumber = "select * from MovieScreening WHERE movieNumber = ?"
        selectCursor = connection.cursor()
        selectCursor.execute(selectMovieNumber, (movieNumber, ))
        records = selectCursor.fetchall()

        # Hall, date labels and screening time buttons which sends you to the another screen 
        row, col = 0, 1
        for record in records:
            dateLbl = Label(self.screeningFrame, text=record[2], bg=self.backgroundColor, fg=self.contentColor, font=("Helvetica", 14))
            dateLbl.grid(row=row, column=0,  padx=15, pady=25, sticky=W)
            hallLabel = Label(self.screeningFrame, text=record[4], wraplength=800, bg=self.backgroundColor, fg=self.contentColor, font=("Helvetica", 14))
            hallLabel.grid(row=row, column=1,  padx=15, pady=25, sticky=W)

            tempInfoDict = {'indexNumber': record[0], 'movieNumber': record[1], 'hall': record[4], 'date': record[2], 'time': record[5], 'name': record[3]}
            screeningTimeBtn = Button(self.screeningFrame, text=record[5], borderwidth=0, bg=self.backgroundColor, fg=self.contentColor, bd=1, font=("Helvetica", 14), command = lambda: self.clearScreen('screeningTime', tempInfoDict)) 
            screeningTimeBtn.grid(row=row, column=col+1, padx=35, pady=25, sticky=E)
            col += 1
            # There are 6 screening times for one day therefore reset col counter and create new row
            if col == 6:
                row += 1
                col = 1

        # Back button which redirects you back to Initial screen
        backBtn = Button(self.screeningFrame, text='Zpět', bg=self.btnColor, fg=self.backgroundColor, bd=1, font=("Helvetica", 12, "bold"), command = lambda: self.clearScreen('movieDetail')) 
        backBtn.grid(row=row, column=0)

        # DB close
        selectCursor.close()
        connection.close()

    def screeningMovies(self):
        '''Initial screen displaying several movies to choose from'''

        movieNumber=0
        # Coordinates for poster buttons
        posterCoord = {0: {"row": 0, "col": 0 }, 1: {"row": 0, "col": 1 }, 2: {"row": 0, "col": 2 }, 3: {"row": 0, "col": 3 },
                    4: {"row": 1, "col": 0 }, 5: {"row": 1, "col": 1 }, 6: {"row": 1, "col": 2 }, 7: {"row": 1, "col": 3 }}

        # Define LabelFrames for heading label and poster buttons
        self.cinemaTitleFrame = LabelFrame(self.root, bg=self.backgroundColor, bd=0)
        self.cinemaTitleFrame.place(x=0, y=0, width=1250, height=100)
        self.posterFrame = LabelFrame(self.root, bg=self.backgroundColor, bd=0)
        self.posterFrame.place(x=0, y=60, width=1250, height=840)
        
        # Label title
        cinemaTitleLbl = Label(self.cinemaTitleFrame, text='Vítejte v Cinema Town', justify=CENTER, bg=self.backgroundColor, fg=self.headingColor, font=("Helvetica", 30, "bold"))
        cinemaTitleLbl.place(x=self.screenWidth/3, y=0)

        # Create poster buttons
        for img in self.imgList:
            # Load images
            posterImg = PhotoImage(file="J:\CinemaTown\Images\{}.png".format(img))
            posterImg = posterImg.zoom(4).subsample(8)
            # Create buttons
            # posterBtn = Button(self.root, image=posterImg, command= lambda: self.clearScreen(screenToClear, movieNumber)) # doesn't work
            posterBtn = Button(self.posterFrame, image=posterImg, command = partial(self.clearScreen, 'screeningMovies', movieNumber))
            # Keep reference to the image
            posterBtn.image = posterImg
            # Add button widgets to the grid
            posterBtn.grid(row=posterCoord[movieNumber]['row'], column=posterCoord[movieNumber]['col'], padx=33, pady=15)
            movieNumber += 1
          
root=tk.Tk()
cinema = Cinema(root)
root.mainloop()

