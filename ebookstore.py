import sqlite3


def create_database():
    """Function that creates a database that for a bookshop."""
    # Creates or opens a database file called ebookstore.
    db = sqlite3.connect('ebookstore.db')

    # Get a cursor
    cursor = db.cursor()

    # Create a table.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 
            books(
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                quantity INTEGER
            )
        ''')

    # Commit the changes
    db.commit()

    # Close our connection.
    db.close()


def grab_last_id():
    """Function that returns last ID on the books' table from bookshop database."""
    # Open and connect to bookshop database.
    db = sqlite3.connect('ebookstore.db')

    # Get a cursor.
    cursor = db.cursor()

    # Grab Last ID from database.
    cursor.execute("""
        SELECT
            id
        FROM
            books
        ORDER BY 
            id
        DESC
    """)

    # Return last ID on books table.
    record = cursor.fetchone()

    # Close database
    db.close()

    return record


def add_data(id_primary_key, title=None, author=None, quantity=None):
    """Function that adds any a new book to the bookshop database."""
    # Open bookshop database.
    db = sqlite3.connect('ebookstore.db')

    # Get a cursor
    cursor = db.cursor()

    # Insert the data if not inside it.
    data = [
        id_primary_key,
        title.title(),
        author.title(),
        quantity
    ]

    cursor.execute("""
        INSERT OR IGNORE INTO 
            books(
                id, 
                title, 
                author, 
                quantity
            ) 
        VALUES(?,?,?,?)
    """, data)

    # Commit changes.
    db.commit()

    # Close connection
    db.close()


def grab_all_data():
    """Function that grab all data stored inside books table from ebookstore.db"""
    # Connect to the database.
    db = sqlite3.connect('ebookstore.db')

    # Create a cursor
    cursor = db.cursor()

    # Grab all data and store them into a variable; Return this variable.
    cursor.execute('''
        SELECT
            *
        FROM
            books
    ''')

    records = cursor.fetchall()

    # Close connection
    db.close()

    return records


def delete_book_data(id_primary_key):
    """Function that deletes a specific book data according to its unique ID number."""
    # Connect to the database
    db = sqlite3.connect('ebookstore.db')

    # Create a cursor.
    cursor = db.cursor()

    # Delete the book's data.
    cursor.execute("""
        DELETE FROM
            books
        WHERE
            id = ?
    """, (id_primary_key,))

    # Commit the changes
    db.commit()

    # Close database connection.
    db.close()


def update_book_data(item, id_num, column):
    """Function that update a specific data from that the user wants from the books table of bookshop database."""
    # ===== UPDATE TITLE ITEMS =====
    if column == 1:
        # Open and connect to database.
        db = sqlite3.connect('ebookstore.db')

        # Get a cursor
        cursor = db.cursor()

        # Update the data.
        cursor.execute("""
            UPDATE 
                books 
            SET 
                title = ? 
            WHERE 
                id = ? 
        """, (item.title(), id_num))

        # Commit change.
        db.commit()

        # Disconnect and Close database.
        db.close()

    # ===== UPDATE AUTHOR ITEMS =====
    elif column == 2:
        # Open and connect to database.
        db = sqlite3.connect('ebookstore.db')

        # Get a cursor
        cursor = db.cursor()

        # Update the data.
        cursor.execute("""
            UPDATE 
                books 
            SET 
                author = ? 
            WHERE 
                id = ? 
        """, (item.title(), id_num))

        # Commit change.
        db.commit()

        # Disconnect and Close database.
        db.close()

    # ===== UPDATE QUANTITY ITEMS =====
    else:
        # Open and connect to database.
        db = sqlite3.connect('ebookstore.db')

        # Get a cursor
        cursor = db.cursor()

        # Update the data.
        cursor.execute("""
            UPDATE 
                books 
            SET 
                quantity = ? 
            WHERE 
                id = ? 
        """, (item, id_num))

        # Commit change.
        db.commit()

        # Disconnect and Close database.
        db.close()


def search_book(index, value):
    """
    Function that search for a specific book(s) according to what the user wants to use as search parameters.
    If user wants to search either by ID or Title; returns only one book.
    If user wants to search by Author name; returns all the books from that specific author.
    """
    # ===== SEARCH BOOK BY ID =====
    if index == 1:
        # Open and connect to database.
        db = sqlite3.connect('ebookstore.db')

        # Get a cursor.
        cursor = db.cursor()

        # Search for a book by its UNIQUE ID NUMBER.
        cursor.execute("""
            SELECT
                *
            FROM
                books
            WHERE
                ID = ?
        """, (value,))

        # Fetch the specific data and store into a variable called record.
        record = cursor.fetchall()

        # Close database.
        db.close()

        # Return the data that the user wants to.
        return record

    # ===== SEARCH BOOK BY TITLE =====
    elif index == 2:
        # Open and connect to database.
        db = sqlite3.connect('ebookstore.db')

        # Get a cursor.
        cursor = db.cursor()

        # Search for a book by its TITLE.
        cursor.execute("""
            SELECT
                *
            FROM
                books
            WHERE
                title = ?
        """, (value.title(),))

        # Fetch the specific data and store into a variable called record.
        record = cursor.fetchall()

        # Close database.
        db.close()

        # Return the data that the user wants to.
        return record

    # ===== SEARCH BOOK BY TITLE =====
    else:
        # Open and connect to database.
        db = sqlite3.connect('ebookstore.db')

        # Get a cursor.
        cursor = db.cursor()

        # Search for all books by its AUTHOR.
        cursor.execute("""
            SELECT
                *
            FROM
                books
            WHERE
                author = ?
        """, (value.title(),))

        # Fetch specific datas and store them into a variable called records.
        records = cursor.fetchall()

        # Close database
        db.close()

        # Return the datas that the user wants to.
        return records


def check_database():
    # Open database
    db = sqlite3.connect('ebookstore.db')

    # get cursor
    cursor = db.cursor()

    # fetch all data and save into a variable
    cursor.execute("""
        SELECT
            *
        FROM 
            books 
    """)
    records = cursor.fetchall()

    # Print out database info
    print(records)