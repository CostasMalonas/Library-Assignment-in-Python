**Program Execution**

The user should type:

1: For adding a book to the database. When adding a book the user will be prompted to type the id of the book (all numbers), the number of copies (all numbers)  and the title of the book. After adding a book the user will be asked if he wants to add another book.

2: For adding a student record. When typing 2 the user can borrow or return a book. The user will be prompted to add the id of the student and the name of the student (the name only if it is the first time he is borrowing/returning a book) and then he is expected to type B/b or R/r for borrowing or returning a book respectively. In both cases he will be prompted to type the title of the book he wants to return/borrow.

3: For printing the table of the students

4: For printing the table of the books

5: For printing the table of the borrowed books.

The program uses the sqlite3 library for the database



**Library class**:

- **set_book(self, book)** method: This method takes a book object as an input and adds it to the books_dict dictionary using the book.title as the key and the book.id and book.copies as the value.
- **set_dict(self, d)** method: This method takes a dictionary d as an input and sets it as the books_dict dictionary.
- **return_book(self, book)** method: This method takes a book object as an input and returns the value associated with the book.title key in the books_dict dictionary, which is a list containing the book.id and book.copies values.
- **return_all_books(self)** method: This method returns the entire books_dict dictionary, which contains all the books in the library.

**Book class**:

What basically the Book class does is everytime we create a Book object, the info of tha book is added in the books table in the library database.

**Student_Record class**:

- **print_students_table** method: Print the table of the students
- **print_books_table** method: Print the table of the books
- **print_borrowed_table** method: Print the table of the borrowed books
- **borrow** method: For borrowing books 
- **return_book** method: For returning books

**insert_books_in_db** function: Insert books in database and in the dictionary attribute of the Library class

**insert_records** function: For inserting records of students that have borrowed a book in the database. Also for returning books.

**main function**: The main function of the program that takes input from the user

At the **create_db_and_tables.py** I create the database and the tables (books, students, borrowed) with the **create_database** function. Also I implemented the **remove_database** function for deleting the database   

