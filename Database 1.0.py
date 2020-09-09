import os, sys
import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta
import random

connection = None
try:
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    print("Connection to SQLite DB successful")
except Error as e:
    print(f"The error '{e}' occurred")

movieInfoDict = {0: {'name': 'Terminator 2: Judgement Day', 'director': 'James Cameron', 'music': 'Brad Fiedel', 
                    'actors': 'Arnold Schwarzenegger, Linda Hamilton, Edward Furlong, Robert Patrick', 'poster': 'Terminator', 'csfd': 'https://www.csfd.cz/film/1248-terminator-2-den-zuctovani/prehled/',
                    'description': 'Deset let po neúspěšném pokusu zabít Sarah Connorovou, matku budoucího vůdce lidstva ve válce proti strojům, se do Los Angeles vrací z budoucnosti nový Terminátor, typ T-1000, aby zlikvidoval už narozeného Johna Connora. Dospělý Connor v roce 2029 na svoji ochranu posílá do minulosti druhého terminátora T-800. Oba stroje nezávisle na sobě pátrají po malém Johnovi. Chlapec zjišťuje, že T-800 je naprogramován na jeho ochranu a s jeho pomocí osvobodí svou matku z psychiatrického ústavu, kde je léčena z údajné schizofrenie. T-800 oběma vysvětluje, co přinese budoucnost. Tu je však možné změnit...a při tom všem hrdiny stíhá nemilosrdný a zřejmě nezničitelný T-1000.'                    
                    },
                1: {'name': 'Die Hard', 'director': 'John McTiernan', 'music': 'Michael Kamen', 
                    'actors': 'Bruce Willis, Bonnie Bedelia, Alan Rickman, Paul Gleason', 'poster': 'Die Hard', 'csfd': 'https://www.csfd.cz/film/6642-smrtonosna-past/prehled/',
                    'description': 'Newyorský policista John McClane (Bruce Willis) přijel do Los Angles navštívit svou ženu, která je zrovna na vánočním večírku v nedostavěné budově firmy Nakatomi. Do budovy však vtrhne německý terorista Hans Gruber (Alan Rickman) se svou jednotkou a zajme všechny hosty (včetně McClaneovy ženy). Jen McClane unikne požárním schodištěm. Teroristé nechtějí propuštění několika svých členů, jak říkají, ale jejich hacker se pokouší dostat do sejfu firmy Nakatomi, ve kterém se nachází 640 milionů dolarů. McClane musí zasáhnout. Film byl nominován na několik technických Oscarů a odstartoval hvězdnou kariéru Bruce Willise.'
                    },
                2: {'name': 'Matrix', 'director': 'Lilly Wachowski, Lana Wachowski', 'music': 'Don Davis', 
                    'actors': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving', 'poster': 'Matrix', 'csfd': 'https://www.csfd.cz/film/9499-matrix/prehled/',
                    'description': 'Představte si, že vaše realita je jen iluzí a vaše noční můry jsou ve skutečnosti pravdivé. Představte si, že vaše současnost je vlastně minulostí a to budoucí se děje právě teď. Pokud to dokážete, budete se cítit jako Thomas Anderson (Keanu Reeves) a nebude to příjemný pocit. Anderson je normální mladý muž, který se jen snaží přežít v každodenním shonu velkoměsta. A má všechno aby se mu to povedlo: přátele, rodinu a práci v IT společnosti Meta Cortech. Jednoho dne se však do jeho mozku zakousne noční můra. Zdá se mu, že byl proti své vůli vložen v podobě dat do počítače a všechno to, co až dosud považoval za svůj osud, je jen vírem dat okolo několika tištěných spojů. Má pocit, že mu byla jeho mysl uvězněna v obřím Matrix počítače budoucnosti. Začíná pochybovat o své každodenní skutečnosti.'
                    },
                3: {'name': 'Braveheart', 'director': 'Mel Gibson', 'music': 'James Horner', 
                    'actors': 'Mel Gibson, Sophie Marceau, Patrick McGoohan, Angus Macfadyen', 'poster': 'Braveheart', 'csfd': 'https://www.csfd.cz/film/3297-statecne-srdce/prehled/',
                    'description':'Film je inspirovaný skutečnou historickou postavou Williama Wallace, který se v 13.století postavil do čela odporu proti anglickému králi Eduardovi I. William se tajně oženil, aby se jeho žena Murron [Marn] vyhnula králem nařízenému právu první noci. Jednoho dne se ji však pokusí znásilnit angličtí vojáci, a když ji William brání, je prohlášen za psance a Murron popravena. Wallace se postaví do čela odporu proti anglické vrchnosti a získává spojence v princezně Isabelle, díky které se vyhne většině králových nástrah. Nakonec je však Wallace kvůli zradě vlastního vojska zajat'
                    },
                4: {'name': 'The Rock', 'director': 'Michael Bay', 'music': 'Hans Zimmer', 
                    'actors': 'Sean Connery, Nicolas Cage, Ed Harris, John Spencer', 'poster': 'The Rock', 'csfd': 'https://www.csfd.cz/film/546-skala/prehled/',
                    'description': 'Generál amerického námořnictva Francis Hummel (Ed Harris) je hrdina a veterán několika tajných vojenských operací, který s hrstkou svých vyzbrojených mužů ukradne ze střeženého armádního skladu patnáct raket s nebezpečným nervovým plynem zabarikáduje v bývalém vězení Alcatraz (Skála) v sanfranciské zátoce a namíří je na město. Generál totiž žádá spravedlnost - chce od Pentagonu získat sto milionů dolarů pro odškodnění rodin padlých vojáků. Přesto je však terorista a muži z FBI pracují na plánech na jeho likvidaci. Ale jak proniknout do Alcatrazu a zneškodnit rakety? Mohou to dokázat jen špičkový chemický specialista FBI Stanley Goodspeed. Druhý je jediný člověk, který kdy uprchl z Alcatrazu a který proslulé vězení dokonale zná: kdysi polapený britský agent Mason (Sean Connery).'
                    },
                5: {'name': 'Aliens', 'director': 'James Cameron', 'music': 'James Horner', 
                    'actors': 'Sigourney Weaver, Carrie Henn, Michael Biehn, Lance Henriksen', 'poster': 'Aliens', 'csfd': 'https://www.csfd.cz/film/1245-vetrelci/prehled/',
                    'description':'Důstojnice Ripleyová, která jako jediná přežila boj na život a na smrt v nákladní lodi Nostromo s vesmírným vetřelcem, je po několika letech nalezena záchrannou lodí a vrací se zpět na Zemi. Když už se zdá, že je po všem, začíná horror znova, tentokrát na vzdálené nedávno kolonizované planetě. Tentokrát nevšichni proti jednomu, ale Ripleyová se skupinou speciálně vycvičených vojáků proti tisícihlavé smrtící síle vetřelců.'
                    },
                6: {'name': 'Rocky', 'director': 'John G. Avildsen', 'music': 'Bill Conti', 
                    'actors': 'Sylvester Stallone, Talia Shire, Burt Young, Carl Weathers', 'poster': 'Rocky', 'csfd': 'https://www.csfd.cz/film/16103-rocky/prehled/',
                    'description':'Slavné boxerské drama outsidera, který dostal šanci a zvítězil sám nad sebou. Titulní hrdina, neúspěšný třicetiletý boxer Rocky Balboa, pracuje jako výběrčí dluhů pro místního lichváře, boxuje v pokoutních zápasech a neúspěšně se dvoří Adrian, plaché prodavačce v obchodě s drobným zvířectvem. V době, kdy bývalý trenér vyhodí Rockyho z tělocvičny, protože se mu zdá, že jako boxer promrhal svůj talent a je vyřízená existence, chystá se ve Filadelfii boj o titul mistra světa v těžké váze. Protože se však vyzyvatel nemůže k zápasu nastoupit, vyhlásí obhájce titulu Apollo Creed, že bude boxovat s kterýmkoli místním boxerem, protože chce dokázat, že Amerika je zemí, v níž má každý šanci uspět. Vybere si Rockyho.'
                    },
                7: {'name': 'Heat', 'director': 'Michael Mann', 'music': 'Elliot Goldenthal', 
                    'actors': ' Al Pacino, Robert De Niro, Val Kilmer, Jon Voight', 'poster': 'Heat', 'csfd': 'https://www.csfd.cz/film/6444-nelitostny-souboj/prehled/',
                    'description':'Lupič Neil McCauley se specializuje na akce, při kterých jde o velké peníze. Ať už připravuje přepadení pancéřového vozu nebo vyloupení banky, vždy se může opřít o spolehlivé spolupracovníky. Každý jeho zločin je pečlivě naplánovaný a provedený s dokonalou profesionalitou. Když McCauley připravuje svou poslední velkou loupež je mu už v patách policejní detektiv Vincent Hanna. Potíž je, že Hanna je stejně schopný a posedlý svou prací jako McCauley. Oba muži toho mají společného víc, než se zdá: ani jednomu z nich to například v soukromí neklape. Vincentu Hannovi se hroutí už třetí manželství, McCauley pro jistotu nikdy s nikým nenavázal trvalý vztah. Oba by si vlastně mohli skvěle rozumět. Jenže stojí na opačných stranách zákona a jejich setkání nemůže skončit jinak, než soubojem na život a na smrt.'
                    },
                    }

# Create Movieinfo table
cursor.execute("""CREATE TABLE IF NOT EXISTS Movieinfo ( 
    movieNumber INT,
    movieName VARCHAR(30),
    movieDirector VARCHAR(30),
    movieMusic VARCHAR(30),
    movieActors VARCHAR(255),
    moviePoster VARCHAR(30),
    movieDescription VARCHAR(2000),
    linkToCSFD VARCHAR(255))"""
)
# Insert into Movieinfo table
for i in range(8):
    connection.execute("INSERT INTO Movieinfo (movieNumber, movieName, movieDirector, movieMusic, movieActors, moviePoster, movieDescription, linkToCSFD) values(?,?,?,?,?,?,?,?)",
                                        (i, movieInfoDict[i]['name'], movieInfoDict[i]['director'], movieInfoDict[i]['music'], movieInfoDict[i]['actors'], 
                                        movieInfoDict[i]['poster'], movieInfoDict[i]['description'], movieInfoDict[i]['csfd']))


# Create MovieScreening table
cursor.execute("""CREATE TABLE IF NOT EXISTS MovieScreening ( 
    indexNumber INT,
    movieNumber INT,
    screeningDate VARCHAR(30),
    movieName VARCHAR(30),
    screeningHall VARCHAR(30),
    screeningTime VARCHAR(30))"""
)

movieLength = { 0: {'movieId':0, 'name': 'Terminator 2: Judgement Day', 'hours': 2, 'minutes': 17},
            1: {'movieId':1, 'name': 'Die Hard',  'hours': 2, 'minutes': 11},
            2: {'movieId':2, 'name': 'Matrix',  'hours': 2, 'minutes': 16},
            3: {'movieId':3, 'name': 'Braveheart',  'hours': 2, 'minutes': 50},
            4: {'movieId':4, 'name': 'The Rock',  'hours': 2, 'minutes': 16},
            5: {'movieId':5, 'name': 'Aliens',  'hours': 2, 'minutes': 17},
            6: {'movieId':6, 'name': 'Rocky',  'hours': 1, 'minutes': 55},
            7: {'movieId':7, 'name': 'Heat',  'hours': 2, 'minutes': 50},
             }


days = [1,2,3,4,5,6]
halls = ['Sál 1', 'Sál 2', 'Sál 3', 'Sál 4']
screeningTime = []

# Create dates and time data
def daterange(i, startDate, endDate):
    delta = timedelta(hours=movieLength[i]['hours'], minutes=round((movieLength[i]['minutes']+15),-1))
    for loop in range(5):
        yield startDate
        startDate += delta

index=0

for day in days:
    for i in range(len(movieLength)):
        if (i < 4) and (day % 2 == 1):
            name = movieLength[i]['name']
            hall = halls[i]
            startDate = datetime(2020, 1, day, random.choice([9,10]), random.choice([5,10,15,20,25,30]))
            endDate = datetime(2020, 1, day, 23, 45)
            for singleDate in daterange(i, startDate, endDate):
                screeningTime.append(singleDate.strftime("%H:%M"))
                connection.execute("INSERT INTO MovieScreening (indexNumber, movieNumber, screeningDate, movieName, screeningHall, screeningTime) values(?,?,?,?,?,?)",(index, i, singleDate.strftime("%Y-%m-%d"), name, hall, screeningTime[index]))
                index += 1
        elif (i >= 4) and (day % 2 == 0):
            name = movieLength[i]['name']
            hall = halls[i-4]
            startDate = datetime(2020, 1, day, random.choice([9,10]), random.choice([5,10,15,20,25,30]))
            endDate = datetime(2020, 1, day, 23, 45)
            for singleDate in daterange(i, startDate, endDate):
                screeningTime.append(singleDate.strftime("%H:%M"))
                connection.execute("INSERT INTO MovieScreening (indexNumber, movieNumber, screeningDate, movieName, screeningHall, screeningTime) values(?,?,?,?,?,?)",(index, i, singleDate.strftime("%Y-%m-%d"), name, hall, screeningTime[index]))
                index += 1

# Create ScreeningHallSetup table
cursor.execute("""CREATE TABLE IF NOT EXISTS ScreeningHallSetup ( 
    screeningHall VARCHAR(30),
    hallRow INT,
    hallColumn_0  INT,
    hallColumn_1  INT,
    hallColumn_2  INT,
    hallColumn_3  INT,
    hallColumn_4  INT)"""
)
# 255 = no seat
hallDict = { 0: {'hall': 'Sál 1', 'row': 0, 'col_0': 0, 'col_1': 1, 'col_2': 255, 'col_3': 3, 'col_4': 4}, 1: {'hall': 'Sál 1', 'row': 1, 'col_0': 0, 'col_1': 1, 'col_2': 255, 'col_3': 3, 'col_4': 4},
            2: {'hall': 'Sál 1', 'row': 2, 'col_0': 0, 'col_1': 1, 'col_2': 255, 'col_3': 3, 'col_4': 4}, 3: {'hall': 'Sál 1', 'row': 3, 'col_0': 0, 'col_1': 1, 'col_2': 255, 'col_3': 3, 'col_4': 4},
            4: {'hall': 'Sál 1', 'row': 4, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4},

            5: {'hall': 'Sál 2', 'row': 0, 'col_0': 255, 'col_1': 255, 'col_2': 2, 'col_3': 255, 'col_4': 255}, 6: {'hall': 'Sál 2', 'row': 1, 'col_0': 255, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 255},
            7: {'hall': 'Sál 2', 'row': 2, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4}, 8: {'hall': 'Sál 2', 'row': 3, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4},
            9: {'hall': 'Sál 2', 'row': 4, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4},

            10: {'hall': 'Sál 3', 'row': 0, 'col_0': 255, 'col_1':1, 'col_2': 2, 'col_3': 3, 'col_4': 255}, 11: {'hall': 'Sál 3', 'row': 1, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4},
            12: {'hall': 'Sál 3', 'row': 2, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4}, 13: {'hall': 'Sál 3', 'row': 3, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4},
            14: {'hall': 'Sál 3', 'row': 4, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4},

            15: {'hall': 'Sál 4', 'row': 0, 'col_0': 0, 'col_1':1, 'col_2': 2, 'col_3': 3, 'col_4': 4}, 16: {'hall': 'Sál 4', 'row': 1, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4},
            17: {'hall': 'Sál 4', 'row': 2, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4}, 18: {'hall': 'Sál 4', 'row': 3, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4},
            19: {'hall': 'Sál 4', 'row': 4, 'col_0': 0, 'col_1': 1, 'col_2': 2, 'col_3': 3, 'col_4': 4},
             }

for i in range(0, 20):
    connection.execute("INSERT INTO ScreeningHallSetup (screeningHall, hallRow, hallColumn_0, hallColumn_1, hallColumn_2, hallColumn_3, hallColumn_4) values(?,?,?,?,?,?,?)",
                                        (hallDict[i]['hall'], hallDict[i]['row'],  hallDict[i]['col_0'], hallDict[i]['col_1'], hallDict[i]['col_2'], 
                                        hallDict[i]['col_3'], hallDict[i]['col_4']))

# Create ScreeningHallOccupancy table
cursor.execute("""CREATE TABLE IF NOT EXISTS ScreeningHallOccupancy( 
     indexNumber INT,
     hallRow INT,
     hallColumn_0 VARCHAR(20),
     hallColumn_1 VARCHAR(20),
     hallColumn_2 VARCHAR(20),
     hallColumn_3 VARCHAR(20),
     hallColumn_4 VARCHAR(20))"""
)

occupyLst = []
# Create random 'yes/no' occupation for seats in screening hall
for indexNumber in range(0, 120):
    selectMovieNumber = "select * from MovieScreening WHERE indexNumber = ?"
    cursor = connection.cursor()
    cursor.execute(selectMovieNumber, (indexNumber, ))
    records = cursor.fetchall()
    for record in records:
        if record[4] == 'Sál 1':
            for nest in range(5):
                for col in range(5):
                    if hallDict[nest]["col_{}".format(col)] != 255:
                        occupyLst.append(random.choice(['yes', 'no', 'no']))
                    elif hallDict[nest]["col_{}".format(col)] == 255:
                        occupyLst.append(255)
                connection.execute("INSERT INTO ScreeningHallOccupancy (indexNumber, hallRow, hallColumn_0, hallColumn_1, hallColumn_2, hallColumn_3, hallColumn_4) values(?,?,?,?,?,?,?)",
                                        (record[0], hallDict[nest]['row'],  occupyLst[0], occupyLst[1], occupyLst[2], occupyLst[3], occupyLst[4]))
                occupyLst=[]                   
        elif record[4] == 'Sál 2':
            for nest in range(5, 10):
                for col in range(5):
                    if hallDict[nest]["col_{}".format(col)] != 255:
                        occupyLst.append(random.choice(['yes', 'no', 'no']))
                    elif hallDict[nest]["col_{}".format(col)] == 255:
                        occupyLst.append(255)
                connection.execute("INSERT INTO ScreeningHallOccupancy (indexNumber, hallRow, hallColumn_0, hallColumn_1, hallColumn_2, hallColumn_3, hallColumn_4) values(?,?,?,?,?,?,?)",
                                        (record[0], hallDict[nest]['row'],  occupyLst[0], occupyLst[1], occupyLst[2], occupyLst[3], occupyLst[4]))
                occupyLst=[]
        elif record[4] == 'Sál 3':
            for nest in range(10, 15):
                for col in range(5):
                    if hallDict[nest]["col_{}".format(col)] != 255:
                        occupyLst.append(random.choice(['yes', 'no', 'no']))
                    elif hallDict[nest]["col_{}".format(col)] == 255:
                        occupyLst.append(255)
                connection.execute("INSERT INTO ScreeningHallOccupancy (indexNumber, hallRow, hallColumn_0, hallColumn_1, hallColumn_2, hallColumn_3, hallColumn_4) values(?,?,?,?,?,?,?)",
                                        (record[0], hallDict[nest]['row'],  occupyLst[0], occupyLst[1], occupyLst[2], occupyLst[3], occupyLst[4]))
                occupyLst=[]
        elif record[4] == 'Sál 4':
            for nest in range(15, 20):
                for col in range(5):
                    if hallDict[nest]["col_{}".format(col)] != 255:
                        occupyLst.append(random.choice(['yes', 'no', 'no']))
                    elif hallDict[nest]["col_{}".format(col)] == 255:
                        occupyLst.append(255)
                connection.execute("INSERT INTO ScreeningHallOccupancy (indexNumber, hallRow, hallColumn_0, hallColumn_1, hallColumn_2, hallColumn_3, hallColumn_4) values(?,?,?,?,?,?,?)",
                                        (record[0], hallDict[nest]['row'],  occupyLst[0], occupyLst[1], occupyLst[2], occupyLst[3], occupyLst[4]))
                occupyLst=[]

cursor.execute("""CREATE TABLE IF NOT EXISTS Tickets ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indexNumber INT,
    movieNumber INT,
    screeningHall VARCHAR(30),
    movieName VARCHAR(30),
    screeningDate VARCHAR(30),
    screeningTime VARCHAR(30),
    ticketRow INT,
    ticketCol INT,
    ticketType VARCHAR(30),
    ticketPrice VARCHAR(30))"""
)

connection.commit()

connection.close()



