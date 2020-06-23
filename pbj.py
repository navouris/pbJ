#NMA June 2020 pbJ python-based journal 
# application to keep track of events in time
import datetime
import os
class Event:
    def __init__(self, d, e):
        self.date = d
        self.event = e.strip()
        # print('....>>>', self.date, self.event)
        # print(self)

    def __repr__(self):
        return self.date + "\t" + self.event

class Calendar:
    mycal = None
    @staticmethod
    def readEvents():
        if not os.path.isfile("myjournal.csv"): return False
        for line in open("myjournal.csv", "r", encoding="utf-8"):
            if line and len(line.split("-")) > 2 and line.split("-")[0].isdigit():
                year = int(line.split("-")[0])
                Calendar.insertEvent(*line.split(";"))
    
    @staticmethod
    def saveEvents():
        if not Calendar.mycal: return
        with open("myjournal.csv", "w", encoding="utf-8") as fout:
            for y, Y in sorted(Calendar.mycal.year.items()):
                for e in Y:
                    fout.write(";".join([e.date, e.event])+"\n")

    @staticmethod
    def insertEvent(d,e):
        # print('to insert...', d, e, type(d), type(e))
        newEvent = Event(d,e)
        # print('inserted event....', newEvent)
        year = int(newEvent.date.split("-")[0])
        Calendar.mycal.year[year] = [newEvent] if year not in Calendar.mycal.year else Calendar.mycal.year[year]+[newEvent]
        # print(Calendar.mycal)
        Calendar.mycal.sorting(year)

    @staticmethod
    def delEvent():
        found = False
        mydate = Calendar.enterValidDate()
        if not mydate: return
        date = str(mydate).split()[0]
        year = int(date.split("-")[0])
        if year in Calendar.mycal.year:
            events = []
            for e in Calendar.mycal.year[year]:
                if date == e.date: 
                    events.append(e)
            if len(events)>0:
                found = True
                print("Τα παρακάτω γεγονότα έχουν συμβεί στις {}:".format(date))
                for i in range(len(events)):
                    print("\t", i+1, e)
                while True:
                    reply = input("επιλέξτε από 1 έως {} για να επιβεβαιώστε τη διαγραφή, x για έξοδο:".format(len(events)))
                    if reply.lower() in "χx":break
                    if reply.isdigit() and 0<int(reply)<=len(events): 
                        toDelete = events[int(reply)-1]
                        Calendar.mycal.year[year].remove(toDelete)
                        del toDelete
                        if len(Calendar.mycal.year[year]) == 0: Calendar.mycal.year.pop(year)
                        print("το γεγονός διαγράφτηκε...")
                        break
        if not found: print('δεν βρέθηκαν γεγονότα ... ')



    @staticmethod
    def enterValidDate():
        while True:
            newDate = input("Εισάγετε ημερομηνία (dd/mm/yyyy):")
            if not newDate: break
            if len(newDate.split("/")) == 3 and len([x for x in newDate.split('/') if x.isdigit()]):
                d = [int(x) for x in newDate.split('/')]

                try: 
                    myDate = datetime.datetime(year= d[2], month=d[1], day=d[0])
                    return myDate
                except: 
                    print("Παρακαλώ εισάγετε έγκυρη ημερομηνία...")
                    continue

    @staticmethod
    def newEvent():
        mydate = Calendar.enterValidDate()
        if not mydate: return False
        date = str(mydate).split()[0]
        while True:
            event = input('Γεγονός της {}:'.format(date))
            if event.strip().lower() in "χx": return False
            if not event:
                print("Παρακαλώ δώστε περιγραφή του γεγονότος,  ή x για ακύρωση...")
            Calendar.insertEvent(date, event)
            break
            
    def __init__(self):
        self.year = {}
        self.months = {"01": "Ιανουάριος", "02": "Φεβρουάριος", "03": "Μάρτιος", "04": "Απρίλιος", \
                "05": "Μάιος", "06": "Ιούνιος", "07": "Ιούλιος", "08": "Αύγουστος", \
                "09": "Σεπτέμβριος", "10": "Οκτώβριος", "11": "Νοέμβριος", "12": "Δεκέμβριος"}

    def overview(self):
        if len(self.year)== 0: print("Δεν βρέθηκε ημερολόγιο")
        elif len(self.year) == 1:
            numberEvents = sum(len(x) for x in self.year.values())
            gegonos = "ός" if numberEvents == 1 else "ότα"
            print('Το ημερολόγιό σας περιέχει {} γεγον{} του {}'.format(numberEvents, gegonos, max(self.year) ))
        else:
            print('Το ημερολόγιό σας εκτείνεται σε {} χρόνια (από το {} μέχρι το {}) και περιέχει {} γεγονότα'.format(len(self.year), \
            min(self.year), max(self.year), sum(len(x) for x in self.year.values())))

    def sorting(self, year = None):
        # print("...calendar object 01...", self)
        for y in self.year:
            if year and y != year: continue
            self.year[y] = sorted([e for e in self.year[y]], key= lambda e: e.date)
        # print("...calendar object 02...", self)
    
    def showYear(self, y):
        if y in self.year:
            out =  "\n......................................\nΈτος {}\n".format(y)
            month = ""
            for event in self.year[y]:
                m = event.date.split("-")[1] 
                if m != month:
                    out += "\n\t"+m+" "+self.months[m] +"\n"
                    month = m
                out += "\t{}:\t{}\n".format(event.date[5:], event.event)
            return out
        else: return ""
    
    def __repr__(self):
        out = ""
        for y in sorted(self.year):
            out += self.showYear(y)
        out += "\n......................................"
        return out

class Menu:
    def __init__(self):
        self.cal = Calendar()
        Calendar.mycal = self.cal
        self.cal.readEvents() # load existing calendar of events
        self.cal.overview()
        while True:
            reply = input("......................................\n\n1.Εισαγωγή γεγονότος...\n2.Διαγραφή γεγονότος...\n3.Ημερολόγιο...\n4.Έξοδος\nΕπιλογη:")
            if reply == "4": break
            if reply == "1": 
                self.cal.newEvent()
            if reply == "2": 
                self.cal.delEvent()
            if reply == "3":
                year = input("Δώστε έτος (enter για όλο το ημερολόγιο):")
                if not year: print(self.cal)
                elif year.isdigit(): 
                    print(self.cal.showYear(int(year)))
            self.cal.overview()
        # exiting
        self.cal.saveEvents()
        print("...bye...")

if __name__ == "__main__":
    Menu()