from PyQt5 import QtWidgets, uic, QtCore
import sys
import ebookstore


# ========== Main Window Area ========== #
class MainWindow(QtWidgets.QMainWindow):
    """This is the Main Window of the app."""

    def __init__(self):
        # Here, we load and display the main window.
        super(MainWindow, self).__init__()

        # Setting  the fixed size of window
        width = 650
        height = 550
        self.setFixedSize(width, height)

        uic.loadUi('app_gui.ui', self)
        self.show()

        # Open the second window after the user clicks 'add' button.
        self.second_window = None
        self.add_new_book_button.clicked.connect(self.show_second_window)

        # Open the third window after the user clicks 'delete' button.
        self.third_window = None
        self.delete_book_button.clicked.connect(self.show_third_window)

        # Open the fourth window after the user clicks 'update' button.
        self.fourth_window = None
        self.update_book_button.clicked.connect(self.show_fourth_window)

        # Open the fifth window after user clicks 'search' button.
        self.fifth_window = None
        self.search_book_button.clicked.connect(self.show_fifth_window)

    def show_second_window(self):
        """Function that closes main window and opens second window."""
        self.close()
        self.second_window = SecondWindow()
        self.second_window.show()

    def show_third_window(self):
        """Function that closes main window and opens third window."""
        self.close()
        self.third_window = ThirdWindow()
        self.third_window.show()

    def show_fourth_window(self):
        """Function that closes main window and opens fourth window."""
        self.close()
        self.fourth_window = FourthWindow()
        self.fourth_window.show()

    def show_fifth_window(self):
        """Function that closes main window and opens fifth window."""
        self.close()
        self.fifth_window = FifthWindow()
        self.fifth_window.show()


# ========== Second Window Area ========== #
class SecondWindow(QtWidgets.QMainWindow):
    """This is the Second Window of the app - Add New Book."""

    def __init__(self):
        # Here, we load and display the second window.
        super(SecondWindow, self).__init__()

        # Setting  the fixed size of window
        width = 650
        height = 550
        self.setFixedSize(width, height)

        uic.loadUi('app_gui_2.ui', self)

        # Close the second window and open the main window again after user clicks 'return' button.
        self.main_window = None
        self.return_main_window_button.clicked.connect(self.return_main_window)

        # Add new item into database.
        self.id = None
        self.title = self.book_title_line
        self.author = self.book_author_line
        self.quantity = self.book_quantity_line
        self.add_new_book_button.clicked.connect(self.add_new_book)

        # Clear all data that was typed inside the input fields.
        self.clear_inputs_button.clicked.connect(self.clear_input_field)

    def return_main_window(self):
        """Function that closes second window and opens the main window."""
        self.close()
        self.main_window = MainWindow()
        self.main_window.show()

    def add_new_book(self):
        """
        Function that will add a new book to database of bookshop.
        First, get the last id unique primary key that is stored inside the table books:
            . If the table is empty, set-up id number to 1;
            . Otherwise, add one to the last id number and register a new book in a new row.
        Finally, clear input fields.
        """
        self.id = ebookstore.grab_last_id()

        if self.id is None:
            self.id = 1
            ebookstore.add_data(
                self.id,
                self.title.text(),
                self.author.text(),
                self.quantity.text()
            )
        else:
            self.id = ebookstore.grab_last_id()[0] + 1
            ebookstore.add_data(
                self.id,
                self.title.text(),
                self.author.text(),
                self.quantity.text()
            )

        self.clear_input_field()  # Clear Input Fields.

    def clear_input_field(self):
        """Function that will clear all input fields on screen as soon as user clicks 'clear' button."""
        if (
            self.title.text() != "" or
            self.author.text() != "" or
            self.quantity.text() != ""
        ):
            self.title.setText("")
            self.author.setText("")
            self.quantity.setText("")
        else:
            # Pass for now; Later will implement a pop-up window saying:
            # Error: all inputs are empty. Or something similar to this phrase.
            pass


# ========== Third Window Area ========== #
class ThirdWindow(QtWidgets.QMainWindow):
    """This is the Third Window of the app - Delete Book."""

    def __init__(self):
        # Here, we load and display the third window.
        super(ThirdWindow, self).__init__()

        # Setting  the fixed size of window
        width = 650
        height = 550
        self.setFixedSize(width, height)

        uic.loadUi('app_gui_3.ui', self)

        # Set-up size of each column.
        self.books_table.setColumnWidth(0, 100)
        self.books_table.setColumnWidth(1, 400)
        self.books_table.setColumnWidth(2, 600)
        self.books_table.setColumnWidth(3, 100)

        # Close the third window and open the main window again after user clicks 'return' button.
        self.main_window = None
        self.return_main_window_button.clicked.connect(self.return_main_window)

        # Load all datas from bookshop database and display them on screen.
        self.rows = None
        self.display_data_on_screen()

        # Get the unique ID primary key from the row that the user clicked over it.
        self.id_primary_key = None
        self.books_table.cellClicked.connect(self.row_clicked)

        # Delete selected data from database; Re-load screen after it.
        self.id_number_primary_key = None
        self.delete_button.clicked.connect(self.delete_book_from_database)

    def return_main_window(self):
        """Function that closes third window and opens the main window."""
        self.close()
        self.main_window = MainWindow()
        self.main_window.show()

    def display_data_on_screen(self):
        """
        Function that will display all the info of all books stored inside the books
        table of bookshop database into screen.
        First, gets each row of the database and append them into a python list called 'row'.
        Second, setting-up the total number of the rows of the table on screen according to:
            . the total length of the list that received all the data from books table (bookshop database).
        Third, loop through the list and them add each row on screen:
            . Each row has 4 values inside it, so we distributed each value to its respectively column.
            . The first column of the table 'ID' will not be able to edit.
        """
        self.rows = ebookstore.grab_all_data()

        self.books_table.setRowCount(len(self.rows))

        table_row = 0
        for row in self.rows:
            self.books_table.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            # Get each item of the column ID.
            item = self.books_table.item(table_row, 0)
            # Change its flags in order to not be able to modify its contents
            # due to the fact that is a UNIQUE PRIMARY KEY.
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            # Keeps adding the other values of the row.
            self.books_table.setItem(table_row, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.books_table.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.books_table.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            table_row += 1

    def row_clicked(self):
        """
        Function that returns the unique ID primary key number of the clicked row:
            1 - get all items that were selected and store them into an object list:
                1.1 - use selectedItems() of PyQt5 functions.
            2 - Loop through the list:
                2.1 - get only the item with index 0 which is equivalent to the unique ID primary key.
                2.2 - convert from string to integer.
            3 - return its value.
        """
        items = self.books_table.selectedItems()
        for index, item in enumerate(items):
            if index == 0:
                self.id_primary_key = item.text()

        return self.id_primary_key

    def delete_book_from_database(self):
        """
        Function that will delete selected book from the database and after that will
        re-load the window excluding without the book that was deleted.
        In order to do that:
            1 - Get the unique ID primary key NUMBER from the selected row:
                1.1 - Need to convert from string to number.
            2 - Call a function called "delete_book_data(id)":
                2.1 - Pass the ID as parameters to this function.
                2.2 - It will delete it from the database.
            3 - Call the function display_data_on_screen() to re-load the window excluding the fresh deleted row.
        """
        self.id_number_primary_key = int(self.id_primary_key)

        ebookstore.delete_book_data(self.id_number_primary_key)

        self.display_data_on_screen()


# ========== Fourth Window Area ========== #
class FourthWindow(ThirdWindow):
    """This is the Fourth Window of the App - Update a Book Entry."""

    def __init__(self):
        # Here, we load and display the fourth window.
        super(FourthWindow, self).__init__()

        # Setting  the fixed size of window
        width = 650
        height = 550
        self.setFixedSize(width, height)

        uic.loadUi('app_gui_4.ui', self)

        # Set-up size of each column.
        self.books_table.setColumnWidth(0, 100)
        self.books_table.setColumnWidth(1, 400)
        self.books_table.setColumnWidth(2, 600)
        self.books_table.setColumnWidth(3, 100)

        # Close the fourth window and open the main window again after user clicks 'return' button.
        self.main_window = None
        self.return_main_window_button.clicked.connect(self.return_main_window)

        # Load all datas from bookshop database and display them on screen.
        self.display_data_on_screen()

        # Get the item that was selected by the user to be updated.
        self.id_number = None  # Variable that will receive the ID number of the cell that was clicked by the user.
        self.books_table.itemDoubleClicked.connect(self.on_item_double_clicked)

        # Here, we update the text - in the bookshop database - of the cell that the user wants to
        # and then update the window (load once again) in order to display the correct information
        # after user clicks on 'update' button.
        self.current_item = None  # Variable that will receive the new text of the cell that was changed by the user.
        self.current_col = None  # Variable that will receive the number of the column of the cell that will be changed.
        self.update_book_data_button.clicked.connect(self.update_book_data)

    def return_main_window(self):
        """Function that close fourth window and open the main window."""
        self.close()
        self.main_window = MainWindow()
        self.main_window.show()

    def on_item_double_clicked(self, item):
        """Function that captures the ID UNIQUE NUMBER of the cell that the user wants to update."""
        row = self.books_table.row(item)

        rows = 0
        for index in range(self.books_table.rowCount()):
            if row == rows:
                self.id_number = self.books_table.item(row, 0).text()
            rows += 1

        return int(self.id_number)

    def update_book_data(self):
        """Function that change some specific item of any book that the user wants to from bookshop database."""
        # Get the current text that the user already has written.
        self.current_item = self.books_table.currentItem().text()

        # Get the number of the column of the cell that the user wants to change.
        self.current_col = self.books_table.currentColumn()

        # Call the function that will update the database.
        ebookstore.update_book_data(self.current_item, self.id_number, self.current_col)

        # Re-load the window displaying the new value there.
        self.display_data_on_screen()


# ========== Fourth Window Area ========== #
class FifthWindow(QtWidgets.QMainWindow):
    """This is the Fifth Window of the App - Search a Book."""

    def __init__(self):
        # Here we load and display the fifth window.
        super(FifthWindow, self).__init__()

        # Setting  the fixed size of window
        width = 650
        height = 550
        self.setFixedSize(width, height)
        
        uic.loadUi('app_gui_5.ui', self)

        # Close the fifth window and open the main window again after user clicks 'return' button.
        self.main_window = None
        self.return_main_window_button.clicked.connect(self.return_main_window)

        # Set-up size of each column.
        self.books_table.setColumnWidth(0, 100)
        self.books_table.setColumnWidth(1, 400)
        self.books_table.setColumnWidth(2, 600)
        self.books_table.setColumnWidth(3, 100)

        # Here, we search for a book(s) after user clicks 'search' button
        # using the following information:
        # Combo Box value and Line Edit value.
        self.combo_box_value = None
        self.line_edit_value = None
        self.datas = None
        self.search_book_button.clicked.connect(self.search_book)

    def return_main_window(self):
        """Function that closes the fifth window and opens the main window."""
        self.close()
        self.main_window = MainWindow()
        self.main_window.show()

    def search_book(self):
        """
        Function that search for a book(s) by using the following parameters: ID, Author, Title.
        In order to do that:
            1 - capture the value of the combo box Index and add 1 to it in order to be like as follows below:
                1 - ID;
                2 - Title;
                3 - Author.
            2 - capture the value of the line edit field and store in a variable;
                2.1 - If the user type a number (ID search), convert from string to integer.
            3 - display the datas on screen - more specific - inside books_table widget by calling
                the function display_data_on_screen.
        """
        self.combo_box_value = self.combo_box.currentIndex() + 1

        if self.combo_box_value != 1:
            self.line_edit_value = self.line_edit.text()
        else:
            self.line_edit_value = int(self.line_edit.text())

        self.datas = ebookstore.search_book(self.combo_box_value, self.line_edit_value)

        self.display_data_on_screen(self.datas)

    def display_data_on_screen(self, datas):
        """Function that display data on screen - books_table."""
        self.datas = datas

        self.books_table.setRowCount(len(self.datas))

        table_row = 0

        for data in self.datas:
            self.books_table.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(data[0])))
            self.books_table.setItem(table_row, 1, QtWidgets.QTableWidgetItem(str(data[1])))
            self.books_table.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(data[2])))
            self.books_table.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(data[3])))
            table_row += 1


# First thing that the app does it create the database file.
ebookstore.create_database()

# ===== Main Application Execution =====
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()  # Start the application
