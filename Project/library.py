import sqlite3
from datetime import datetime
import create_db_and_tables as create_db


students_records = {} # dictionary in the format {id:Student_Records object}

class Library:
    def __init__(self):
        self.books_dict = {}
    
    def set_book(self, book):
        self.books_dict[book.title] = [book.id, book.copies]

    def set_dict(self, d):
        self.books_dict = d

    def return_book(self, book):
        return self.books_dict[book.title]
    
    def return_all_books(self):
        return self.books_dict

class Book:
    def __init__(self,id,title,copies):
        self.id = id 
        self.title = title 
        self.copies = copies
        
        # Connect to the database
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            sql = """INSERT INTO books(id, title, copies) VALUES(?,?,?)""" # when a new Book object is created a new record is inserterd in the books table
            cursor.execute(sql, (self.id, self.title, self.copies))
            conn.commit()
            conn.close()
        except:
            print("Book id already exist. Please type a different one\n")
            conn.close()

    def print_table(self):
        """
        Method for printing the books table
        """
        query = "SELECT * FROM books"
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        heading = ['Id', 'Title', 'Copies']
        print(f'{heading[0]: <10}{heading[1]: <10}{heading[2]: <10}')

        for row in result:
            print(f'{row[0]: <10}{row[1]: <10}{row[2]: <10}')
        conn.close()
        print()


class Student_Record:

    def __init__(self, id=0, name=0):
        self.id = id 
        self.name = name
        self.borrowed = []
        
    def print_students_table(self):
        query = "SELECT * FROM students"
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        heading = ['ID', 'Name']
        print(f'{heading[0]: <10}{heading[1]: <10}')

        for row in result:
            print(f'{row[0]: <10}{row[1]: <10}')
        print()
        conn.close()
    
    def print_books_table(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        query = """SELECT * FROM books"""
        cursor.execute(query)
        heading_books = ['id', 'title', 'copies']
        result = cursor.fetchall()
        print(f'{heading_books[0]: <10}{heading_books[1]: <10}{heading_books[2]: <10}')
        for row in result:
            print(f'{row[0]: <10}{row[1]: <10}{row[2]: <10}')
        print()
        conn.close()
    
    def print_borrowed_table(self):
        query = """SELECT * FROM borrowed"""
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute(query)
        heading_borrowed = ['book_id', 'student_id', 'borrow_date']
        result = cursor.fetchall()
        print(f'{heading_borrowed[0]: <10}{heading_borrowed[1]: <12}{heading_borrowed[2]: <10}')
        for row in result:
            print(f'{row[0]: <10}{row[1]: <12}{row[2]: <10}')
        conn.close()

    def borrow(self, id, title, library):
        """
        Method for borrowing a book
        """
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        books_available  = library.return_all_books()
        if title in books_available.keys():
            if (len(self.borrowed) < 3) and (not(title in self.borrowed)) and (books_available[title][1] > 0):
                self.borrowed.append(title)
                query = """INSERT INTO borrowed(book_id, student_id, borrow_date) VALUES(?,?,?)"""
                cursor.execute(query, (books_available[title][0], self.id, datetime.now().date()))
                copies_updated = books_available[title][1] - 1
                books_available[title] = [books_available[title][0], copies_updated] # update the titles attribute
                conn.commit()    
                update_query = f"""UPDATE books SET copies = {copies_updated} WHERE id = {books_available[title][0]}"""
                cursor.execute(update_query)
                conn.commit()

                print(f"{self.name} with id {id} borrowed {title}\n")
                conn.commit()
                conn.close()
            else:
                print(f"You can't borrow {title} Name:{self.name} Id:{id}\n")
                conn.commit()
                conn.close()
        else:
            print("Title you requested doesn't exist\n")
            conn.commit()
            conn.close()

    def return_book(self, id, title, library):
        """
        Method for returning a book
        """
        books_available = library.return_all_books()
        if title in self.borrowed:
            self.borrowed.remove(title) # remove the title from the borrowed list
            return_date = datetime.now().date()
            query = f"""SELECT * FROM borrowed WHERE book_id = {books_available[title][0]} AND student_id = {self.id}"""
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            result = cursor.fetchall()
            borrowed_date = result[0][2] # Get the date book was borrowed
            date_format = r"%Y-%m-%d"
            borrowed_date = datetime.strptime(borrowed_date, date_format).date()

            # add 1 to the number of copies since the book is returned
            books_available[title] = [books_available[title][0], books_available[title][1] + 1]
            library.set_dict(books_available)
            update_query = f"""UPDATE books SET copies = {books_available[title][1]} WHERE id = {books_available[title][0]}"""
            cursor.execute(update_query)
            conn.commit()

            # delete the borrowed record of the student that returned the book
            delete_query = f"""DELETE FROM borrowed WHERE book_id = {books_available[title][0]} AND student_id = {self.id}"""
            cursor.execute(delete_query)
            conn.commit()

            delta = return_date - borrowed_date
            days = delta.days 
            if days > 30:
                print(f"{id} get a penalty. The book was kept {days - 30} days more\n")
            else:
                print(f"{id} returned {title}\n")
        else:
            print(f"{id} haven't borrowed {title}\n")

def insert_books_in_db(library):
    books = []
    while True:
        while True:
            try:
                id = int(input("Type book id: "))
                copies = int(input("Type copies of the book available: "))
                if copies <= 0:
                    print("Type positive number")
                    continue
                break
            except:
                print("Please type only numbers for the id and the copies\n")
        title = input("Type title of book: ")
        library.set_book(Book(id, title, copies))
        ans = input("Enter more books?: Yes/No ")
        if ans.lower() == "yes":
            continue 
        elif ans.lower() == "no":
            return books
        else:
            print("Type answer again")

def insert_records(library):
    """
    Insert students, borrow books, return books, print tables (students, books, borrowed)
    """

    while True:

       
        while True:
            id = input("Type student id to continue | E for exit: ")
            if all(char.isdigit() or char.lower() == 'e' for char in id):
                break
            else:
                print("Invalid input. Please try again.")
        
        if "e" == id.lower():
            break

        if id in students_records.keys():  
            ans = input("Borrow or Return? type B for Borrow | R for Return | E for exit: """)
            if ans.lower() == "b":
                title = input("Enter name of the book for borrow: ")
                students_records[id].borrow(id, title, library)
            elif ans.lower() == "r":
                title = input("Enter name of the book for return: ")
                students_records[id].return_book(id, title, library)
            elif ans.lower() == "e":
                return students_records
            else:
                print("Type answer again\n")
        else:
            # if it is the first time the id appears
            name = input("Type full name of student: ")
            s = Student_Record(id, name)
            students_records[id] = s
            ans = input("\nBorrow or Return? type B for Borrow | R for Return | E for exit: ")
            while True:
                if ans.lower() == "b":
                    title = input("Enter name of the book for borrow: ")
                    students_records[id].borrow(id, title, library)
                    break
                elif ans.lower() == "r":
                    title = input("Enter name of the book for return: ")
                    students_records[id].return_book(id, title, library)
                    break
                elif ans.lower() == "e":
                    return students_records
                else:
                    print("Type answer again\n")

def main():
    create_db.remove_database()
    create_db.create_database()
    manager = Student_Record()
    library = Library()
    while True:
        while True:
            ans = input("1:Add Book | 2:Add Student (for borrowing or returning) | 3:Print table of students | 4:Print table of books | 5:Print table of borrowed books | E for exit: ")
            if not(ans in ["1", "2", "3", "4", "5", "e", "E"]):
                print("Type answer again\n")
            else:
                break
        if ans == "1":
            insert_books_in_db(library)
        elif ans == "2":
            insert_records(library)
        elif ans == "3":
            manager.print_students_table()
        elif ans == "4":
            manager.print_books_table()
        elif ans == "5":
            manager.print_borrowed_table()
        elif ans.lower() == "e":
            print("Bye bye")
            break
        else:
            print("Type answer again")

if __name__ == '__main__':
    main()



