import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import mysql.connector

##Install command para sa mga imports
## pip install ttkbootstrap
## pip install mysql-connector-python
## python --version 

# Database connection
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pydb2"
    )
    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error connecting to database: {err}")
    exit(1)

##Start Product Functions

def fetch_product_data():
    try:
        # Database connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pydb2"
        )
        mycursor = mydb.cursor()

        # SQL query to join product, suppliers, and product_category tables
        query = """
        SELECT p.product_id, p.product_name, p.product_price, p.product_desc, p.quantity, s.name AS supplier_name, c.category_name
        FROM product p
        JOIN suppliers s ON p.supplier_id = s.supplier_id
        JOIN product_category c ON p.category_id = c.category_id
        """
        mycursor.execute(query)
        product_data = mycursor.fetchall()

        return product_data

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching product data: {err}")
        return []

# Function to populate the Treeview
def populate_treeview(prodtree):
    product_data = fetch_product_data()
    for row in prodtree.get_children():
        prodtree.delete(row)
    for row in product_data:
        prodtree.insert("", "end", values=row)
    pass

def prod_on_tree_select(event):
    selected_item = prodtree.selection()
    if selected_item:
        values = prodtree.item(selected_item)['values']
        productID_entry.delete(0, tk.END)
        productname_entry.delete(0, tk.END)
        productPrice_entry.delete(0, tk.END)
        productDesc_entry.delete(0, tk.END)
        productQuant_entry.delete(0, tk.END)
        supplierName_entry.delete(0, tk.END)
        category_cbox.delete(0, tk.END)

        productID_entry.insert(0, values[0])
        productname_entry.insert(0, values[1])
        productPrice_entry.insert(0, values[2])
        productDesc_entry.insert(0, values[3])
        productQuant_entry.insert(0, values[4])
        supplierName_entry.insert(0, values[5])
        category_cbox.insert(0, values[6])

def readprodData():
    try:
        # Clear existing table data
        for row in prodtree.get_children():
            prodtree.delete(row)
        
        # Fetch data from the database
        product_data = fetch_product_data()
        
        # Insert fetched data into the Treeview
        for row in product_data:
            prodtree.insert("", "end", values=row)
        
        # Refresh supplier and category combo boxes
        populate_comboboxes(supplierName_entry, category_cbox)
        clearprodData()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error reading data from database: {err}")

def insert_product():
    product_name = productname_entry.get()
    product_price = productPrice_entry.get()
    product_desc = productDesc_entry.get()
    quantity = productQuant_entry.get()
    supplier_name = supplierName_entry.get()
    category_name = category_cbox.get()

    if not (product_name and product_price and product_desc and quantity and supplier_name and category_name):
        messagebox.showerror("Error", "Please fill all the fields")
        return

    try:
        # Database connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pydb2"
        )
        mycursor = mydb.cursor()

        # Fetch supplier_id
        mycursor.execute("SELECT supplier_id FROM suppliers WHERE name = %s", (supplier_name,))
        supplier_id = mycursor.fetchone()
        if supplier_id:
            supplier_id = supplier_id[0]
        else:
            messagebox.showerror("Error", "Supplier not found")
            return

        # Fetch category_id
        mycursor.execute("SELECT category_id FROM product_category WHERE category_name = %s", (category_name,))
        category_id = mycursor.fetchone()
        
        if category_id:
            category_id = category_id[0]
        else:
            messagebox.showerror("Error", "Category not found")
            return

        # Insert product
        sql = "INSERT INTO product (product_name, product_price, product_desc, quantity, supplier_id, category_id) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (product_name, product_price, product_desc, quantity, supplier_id, category_id)
        mycursor.execute(sql, values)
        mydb.commit()

        messagebox.showinfo("Success", "Product inserted successfully")
        populate_treeview(prodtree)
        clearprodData()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error inserting product: {err}")

def clearprodData():
    productID_entry.delete(0, tk.END)
    productname_entry.delete(0, tk.END)
    productPrice_entry.delete(0, tk.END)
    productDesc_entry.delete(0, tk.END)
    productQuant_entry.delete(0, tk.END)
    supplierName_entry.delete(0, tk.END)
    category_cbox.delete(0, tk.END)

def update_product():
    product_id = productID_entry.get()
    product_name = productname_entry.get()
    product_price = productPrice_entry.get()
    product_desc = productDesc_entry.get()
    quantity = productQuant_entry.get()
    supplier_name = supplierName_entry.get()
    category_name = category_cbox.get()

    if not (product_id and product_name and product_price and product_desc and quantity and supplier_name and category_name):
        messagebox.showerror("Error", "Please fill all the fields")
        return

    try:
        # Database connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pydb2"
        )
        mycursor = mydb.cursor()

        # Fetch supplier_id
        mycursor.execute("SELECT supplier_id FROM suppliers WHERE name = %s", (supplier_name,))
        supplier_id = mycursor.fetchone()
        if supplier_id:
            supplier_id = supplier_id[0]
        else:
            messagebox.showerror("Error", "Supplier not found")
            return

        # Fetch category_id
        mycursor.execute("SELECT category_id FROM product_category WHERE category_name = %s", (category_name,))
        category_id = mycursor.fetchone()
        if category_id:
            category_id = category_id[0]
        else:
            messagebox.showerror("Error", "Category not found")
            return

        # Update product
        sql = "UPDATE product SET product_name = %s, product_price = %s, product_desc = %s, quantity = %s, supplier_id = %s, category_id = %s WHERE product_id = %s"
        values = (product_name, product_price, product_desc, quantity, supplier_id, category_id, product_id)
        mycursor.execute(sql, values)
        mydb.commit()
        clearprodData()
        messagebox.showinfo("Success", "Product updated successfully")
        populate_treeview(prodtree)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error updating product: {err}")

def delete_product():
    product_id = productID_entry.get()
    if not product_id:
        messagebox.showerror("Error", "Please enter a product ID")
        return
    if messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?"):
      try:
          # Database connection
          mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              password="",
              database="pydb2"
          )
          mycursor = mydb.cursor()

          # Delete product
          sql = "DELETE FROM product WHERE product_id = %s"
          mycursor.execute(sql, (product_id,))
          mydb.commit()

          messagebox.showinfo("Success", "Product deleted successfully")
          populate_treeview(prodtree)
          clearprodData()
      except mysql.connector.Error as err:
          messagebox.showerror("Error", f"Error deleting product: {err}")

def stock_in():
    product_id = productID_entry.get()
    stock_change = stock_entry.get()

    if not (product_id and stock_change):
        messagebox.showerror("Error", "Please enter product ID and stock change quantity")
        return

    try:
        stock_change = int(stock_change)
        if stock_change <= 0:
            messagebox.showerror("Error", "Stock change must be a positive integer")
            return

        # Database connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pydb2"
        )
        mycursor = mydb.cursor()

        # Update quantity
        sql = "UPDATE product SET quantity = quantity + %s WHERE product_id = %s"
        mycursor.execute(sql, (stock_change, product_id))
        mydb.commit()

        messagebox.showinfo("Success", "Stock increased successfully")
        populate_treeview(prodtree)

    except ValueError:
        messagebox.showerror("Error", "Stock change must be an integer")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error updating stock: {err}")

# 
def stock_out():
    product_id = productID_entry.get()
    stock_change = stock_entry.get()

    if not (product_id and stock_change):
        messagebox.showerror("Error", "Please enter product ID and stock change quantity")
        return

    try:
        stock_change = int(stock_change)
        if stock_change <= 0:
            messagebox.showerror("Error", "Stock change must be a positive integer")
            return

        # Database connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pydb2"
        )
        mycursor = mydb.cursor()

        # Check current quantity
        mycursor.execute("SELECT quantity FROM product WHERE product_id = %s", (product_id,))
        current_quantity = mycursor.fetchone()

        if current_quantity and current_quantity[0] < stock_change:
            messagebox.showerror("Error", "Insufficient stock. Cannot decrease stock below zero.")
            return

        # Update quantity
        sql = "UPDATE product SET quantity = quantity - %s WHERE product_id = %s"
        mycursor.execute(sql, (stock_change, product_id))
        mydb.commit()

        messagebox.showinfo("Success", "Stock decreased successfully")
        populate_treeview(prodtree)

    except ValueError:
        messagebox.showerror("Error", "Stock change must be an integer")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error updating stock: {err}")


 ## para mag display ang data sang supplier og category sa combobox 
def fetch_suppliers_and_categories():
    try:
        # Database connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pydb2"
        )
        mycursor = mydb.cursor()

        # Fetch suppliers
        mycursor.execute("SELECT name FROM suppliers")
        suppliers = [row[0] for row in mycursor.fetchall()]

        # Fetch categories
        mycursor.execute("SELECT category_name FROM product_category")
        categories = [row[0] for row in mycursor.fetchall()]

        return suppliers, categories

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error connecting to database: {err}")
        return [], []

# Function to populate combo boxes
def populate_comboboxes(supplier_combobox, category_combobox):
    suppliers, categories = fetch_suppliers_and_categories()
    supplier_combobox['values'] = suppliers
    category_combobox['values'] = categories
    pass
## End Product Functions



## Start Supplier Functions
def insertsuppData():
  name = suppName_entry.get()
  contact = suppContact_entry.get()
  address = suppAddress_entry.get()

  try:
    check_sql = "SELECT * FROM suppliers WHERE name = %s"
    check_val = (name,)
    mycursor.execute(check_sql, check_val)
    result = mycursor.fetchone()
    print(f"Query result: {result}")
  except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error querying database: {err}")
    return

  if result:
    messagebox.showerror("Error", "The Supplier Already Exists.")
    return
  
  try:
    sql = "INSERT INTO suppliers (name, contact_info, address) VALUES (%s, %s, %s)"
    val = (name, contact, address)
    print(f"Executing SQL: {sql} with values {val}")
    mycursor.execute(sql, val)
    mydb.commit()
    messagebox.showinfo("Success", "Record inserted successfully.")
    readsuppData()
  except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error inserting data into database: {err}")

def readsuppData():
    try:
        for row in supptree.get_children():
            supptree.delete(row)
        
        mycursor.execute("SELECT * FROM suppliers")
        result = mycursor.fetchall()
        for row in result:
            supptree.insert("", "end", values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error reading data from database: {err}")


def updatesuppData():

  id = supplierID_entry.get()  
  name = suppName_entry.get()
  contact = suppContact_entry.get()
  address = suppAddress_entry.get()

  try:
    sql = "UPDATE suppliers SET name = %s, contact_info = %s, address = %s WHERE supplier_id = %s"
    val = (name, contact, address, id)
    mycursor.execute(sql, val)
    mydb.commit()
    messagebox.showinfo("Success", "Record updated successfully.")
    readsuppData() 
  except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error updating data in database: {err}")

def deletesuppData():
  try:
    selected_item = supptree.selection()
    if not selected_item:
      messagebox.showwarning("Warning", "Please select a record to delete.")
      return

    if messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?"):
      id = supptree.item(selected_item)['values'][0]
      sql = "DELETE FROM suppliers WHERE supplier_id = %s"  
      val = (id,)
      mycursor.execute(sql, val)
      mydb.commit()
      messagebox.showinfo("Success", "Record deleted successfully.")
      readsuppData()
  except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error deleting data from database: {err}")


def Supp_on_tree_select(event):
    selected_item = supptree.selection()
    if selected_item:
        values = supptree.item(selected_item)['values']
        supplierID_entry.delete(0, tk.END)
        suppName_entry.delete(0, tk.END)
        suppContact_entry.delete(0, tk.END)
        suppAddress_entry.delete(0, tk.END)

        supplierID_entry.insert(0, values[0])
        suppName_entry.insert(0, values[1])
        suppContact_entry.insert(0, values[2])
        suppAddress_entry.insert(0, values[3])

def clearsuppData():
    supplierID_entry.delete(0, tk.END)
    suppName_entry.delete(0, tk.END)
    suppContact_entry.delete(0, tk.END)
    suppAddress_entry.delete(0, tk.END)


## Pag Visit nimo sa Frame naa na dayuy unod na data ang Tree view gikan sa Database 
def fetch_supplier_data():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pydb2"
        )
        mycursor = mydb.cursor()

        query = "SELECT supplier_id, name, contact_info, address FROM suppliers"
        mycursor.execute(query)
        supplier_data = mycursor.fetchall()

        return supplier_data

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching supplier data: {err}")
        return []

    finally:
        if mydb.is_connected():
            mydb.close()


# Function to populate the Treeview widget with supplier data
def populate_supplier_treeview():
    supplier_data = fetch_supplier_data()
    for row in supptree.get_children():
        supptree.delete(row)
    for row in supplier_data:
        supptree.insert("", "end", values=row)



    
##End Supplier Functions


#Start Category Functions
def manage_category(action):
    category_id = categoryID_entry.get()
    category_name = categoryName_entry.get()

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pydb2"
        )
        mycursor = mydb.cursor()

        if action == "insert":
            if not category_name:
                messagebox.showerror("Error", "Category name is required")
                return

            sql = "INSERT INTO product_category (category_name) VALUES (%s)"
            values = (category_name,)
            mycursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Success", "Category inserted successfully")

        elif action == "update":
            if not (category_id and category_name):
                messagebox.showerror("Error", "Both Category ID and Category name are required")
                return

            sql = "UPDATE product_category SET category_name = %s WHERE category_id = %s"
            values = (category_name, category_id)
            mycursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Success", "Category updated successfully")

        elif action == "delete":
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?"):
                if not category_id:
                    messagebox.showerror("Error", "Category ID is required")
                    return

                sql = "DELETE FROM product_category WHERE category_id = %s"
                values = (category_id,)
                mycursor.execute(sql, values)
                mydb.commit()
                messagebox.showinfo("Success", "Category deleted successfully")

        populate_category_treeview()
        clear_category_data()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

    finally:
        mydb.close()

# Function to fetch category data
def fetch_category_data():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pydb2"
        )
        mycursor = mydb.cursor()


        query = "SELECT category_id, category_name FROM product_category"
        mycursor.execute(query)
        category_data = mycursor.fetchall()

        return category_data

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching category data: {err}")
        return []

    finally:
        mydb.close()

# Function to populate the Treeview widget with category data
def populate_category_treeview():
    category_data = fetch_category_data()
    for row in cattree.get_children():
        cattree.delete(row)
    for row in category_data:
        cattree.insert("", "end", values=row)

# Mag Clear Category Entry
def clear_category_data():
    categoryID_entry.delete(0, tk.END)
    categoryName_entry.delete(0, tk.END)

##Mag Select kag data sa Treeview ma get sa Entrys
def cat_on_tree_select(event):
    selected_item = cattree.selection()
    if selected_item:
        values = cattree.item(selected_item)['values']
        categoryID_entry.delete(0, tk.END)
        categoryName_entry.delete(0, tk.END)


        categoryID_entry.insert(0, values[0])
        categoryName_entry.insert(0, values[1])






class MainFrame(ttk.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.geometry("1000x600")
        
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self,width=1000,height=500)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.main_frame.pack_propagate(False)


        login_frame = ttk.Frame(self.main_frame)
        login_frame.pack(side="right",expand=True, fill=tk.BOTH)



        Title_label = ttk.Label(login_frame, text="GROCERY INVENTORY SYSTEM", font=("Helvetica", 20, 'bold'), foreground="white")
        Title_label.pack(pady=(80, 50))

        usr_label = ttk.Label(login_frame, text="User name", font=("", 10, 'bold'))
        usr_label.pack(pady=(50,10))

        self.usr_entry = ttk.Entry(login_frame, width=30)
        self.usr_entry.pack()

        pswr_label = ttk.Label(login_frame, text="Password", font=("", 10, 'bold'))
        pswr_label.pack(pady=10)

        self.pswr_entry = ttk.Entry(login_frame, width=30, show='*')
        self.pswr_entry.pack(pady=(10, 50))

        login_btn = ttk.Button(login_frame, text="Log in", width=29, command=self.login)
        login_btn.pack()

        # Dashboard frame
        self.dashboard = ttk.Frame(self, width=1000, height=1000)
        self.dashboard.pack_propagate(False)

        style = ttk.Style()
        style.configure("db.TButton",
                        font=("Helvetica", 10, 'bold'),
                        foreground="white",
                        background="#57A6A1",
                        padding=20)
        
        product_list = ttk.Button(self.dashboard, text="MANAGE PRODUCT", style="db.TButton", width=40, command=self.show_product_list)
        product_list.pack(pady=(150, 10))

        inventory_stock = ttk.Button(self.dashboard, text="MANAGE SUPPLIER", style="db.TButton", width=40,command=self.show_supplier_frame)
        inventory_stock.pack(pady=10)

        manage_Product = ttk.Button(self.dashboard, text="MANAGE PRODUCT CATEGORY", style="db.TButton", width=40,command=self.show_category_frame)
        manage_Product.pack(pady=(10, 150))

        logout_btn = ttk.Button(self.dashboard, text="Log out", style="db.TButton", command=self.show_main_frame)
        logout_btn.pack()

        # Product list frame



        self.product_list = ttk.Frame(self)
        self.product_list.pack_propagate(False)

        frame1 = ttk.Frame(self.product_list)
        frame1.pack(side="left", fill="both", expand=True)

        frame2 = ttk.Frame(self.product_list, width=1000, height=800)
        frame2.pack(side="right",fill="both", expand=True) 

        global productID_entry
        productID_label =ttk.Label(frame1,text="Product ID",font=("", 10, 'bold'))
        productID_label.pack(padx=20,pady=(50,10))

        productID_entry =ttk.Entry(frame1,width=30)
        productID_entry.pack(padx=20,pady=10)

        global productname_entry
        productname_label = ttk.Label(frame1, text="Product name", font=("", 10, 'bold'))
        productname_label.pack(pady=10)

        productname_entry = ttk.Entry(frame1, width=30)
        productname_entry.pack(pady=10)

        global productPrice_entry
        productPrice_label = ttk.Label(frame1, text="Price", font=("", 10, 'bold'))
        productPrice_label.pack(pady=10)

        productPrice_entry = ttk.Entry(frame1, width=30)
        productPrice_entry.pack(pady=10)

        global productDesc_entry
        productDesc_label = ttk.Label(frame1, text="Description", font=("", 10, 'bold'))
        productDesc_label.pack(pady=10)

        productDesc_entry = ttk.Entry(frame1, width=30)
        productDesc_entry.pack(pady=10)

        global productQuant_entry
        productQuant_label = ttk.Label(frame1, text="Quantity", font=("", 10, 'bold'))
        productQuant_label.pack(pady=10)

        productQuant_entry = ttk.Entry(frame1, width=30)
        productQuant_entry.pack(pady=10)

        global supplierName_entry
        supplierName_label = ttk.Label(frame1, text="Supplier", font=("", 10, 'bold'))
        supplierName_label.pack(pady=10)

        supplierName_entry = ttk.Combobox(frame1, width=30)
        supplierName_entry.pack(pady=10)

        global category_cbox
        category_label = ttk.Label(frame1, text="Category", font=("", 10, 'bold'))
        category_label.pack(pady=(20, 10))

        category_cbox = ttk.Combobox(frame1, width=30)
        category_cbox.pack(pady=10)

        populate_comboboxes(supplierName_entry, category_cbox)


        btnFrame = ttk.Frame(frame1)
        btnFrame.pack()

        addSupp_btn = ttk.Button(btnFrame,text="Create",command=insert_product)
        addSupp_btn.grid(column=0,row=0,padx=15,pady=15)


        refSupp_btn = ttk.Button(btnFrame,text="Refresh" ,command=readprodData)
        refSupp_btn.grid(column=1,row=0,padx=15,pady=15)

        updSupp_btn = ttk.Button(btnFrame,text="Update",command=update_product)
        updSupp_btn.grid(column=0,row=1,padx=15,pady=(15,30))

        delSupp_btn = ttk.Button(btnFrame,text="Delete",command=delete_product)
        delSupp_btn.grid(column=1,row=1,padx=15,pady=(15,30))

        crealData_btn = ttk.Button(frame1,text="Clear",width=18,command=clearprodData)
        crealData_btn.pack(pady=(5,15))

        backFrame_btn = ttk.Button(frame1,text="Back",width=18,command=self.show_dashboard)
        backFrame_btn.pack(pady=(5,10))

        global prodtree
        columns = ("product_id", "product_name", "product_price", "product_desc", "quantity", "supplier_name", "category_name")
        prodtree = ttk.Treeview(frame2, columns=columns, show="headings", height=24)

     
        for col in columns:
            prodtree.column(col, width=150)
            
        
        prodtree.heading("product_id", text="Product ID")
        prodtree.heading("product_name", text="Product Name")
        prodtree.heading("product_price", text="Price")
        prodtree.heading("product_desc", text="Description")

        prodtree.heading("quantity", text="Available Stocks")
        prodtree.heading("supplier_name", text="Supplier")
        prodtree.heading("category_name", text="Category")

        prodtree.grid(row=10, column=0, columnspan=8, padx=(70, 10), pady=(90, 10))


        populate_treeview(prodtree)
        prodtree.bind("<<TreeviewSelect>>", prod_on_tree_select)

        global stock_entry
        stock_entry = ttk.Entry(frame2)
        stock_entry.grid(column=1, row=11, pady=(20, 10), padx=10)

        stockin_btn = ttk.Button(frame2, text="Stock in", command=stock_in)
        stockin_btn.grid(column=2, row=11, pady=(20, 10), padx=10)

        stockout_btn = ttk.Button(frame2, text="Stock out", command=stock_out)
        stockout_btn.grid(column=3, row=11, pady=(20, 10), padx=10)

        



        self.supplier_frame = ttk.Frame(self)
        self.supplier_frame.pack_propagate(False)

        supplierframe1 = ttk.Frame(self.supplier_frame)
        supplierframe1.pack(side="left", fill="both", expand=True)

        supplierframe2 = ttk.Frame(self.supplier_frame, width=1000, height=800)
        supplierframe2.pack(side="right", fill="both", expand=True)

        global supplierID_entry
        supplierID_label =ttk.Label(supplierframe1,text="Supplier ID",font=("", 10, 'bold'))
        supplierID_label.pack(padx=20,pady=(50,10))

        supplierID_entry =ttk.Entry(supplierframe1)
        supplierID_entry.pack(padx=20,pady=10)

        global suppName_entry
        suppName_label =ttk.Label(supplierframe1,text="Name",font=("", 10, 'bold'))
        suppName_label.pack(padx=20,pady=10)

        suppName_entry =ttk.Entry(supplierframe1)
        suppName_entry.pack(padx=20,pady=10)

        global suppContact_entry
        suppContact_label = ttk.Label(supplierframe1,text="Contact Info",font=("", 10, 'bold'))
        suppContact_label.pack(padx=20,pady=10)

        suppContact_entry = ttk.Entry(supplierframe1)
        suppContact_entry.pack(padx=20,pady=10)

        global suppAddress_entry
        suppAddress_label = ttk.Label(supplierframe1,text="Address",font=("", 10, 'bold'))
        suppAddress_label.pack(padx=20,pady=10)

        suppAddress_entry = ttk.Entry(supplierframe1)
        suppAddress_entry.pack(padx=20,pady=10)

        buttonFrame = ttk.Frame(supplierframe1)
        buttonFrame.pack()

        addSupp_btn = ttk.Button(buttonFrame,text="Create",command=insertsuppData)
        addSupp_btn.grid(column=0,row=0,padx=15,pady=15)

        refSupp_btn = ttk.Button(buttonFrame,text="Refresh",command=populate_supplier_treeview)
        refSupp_btn.grid(column=1,row=0,padx=15,pady=15)

        updSupp_btn = ttk.Button(buttonFrame,text="Update",command=updatesuppData)
        updSupp_btn.grid(column=0,row=1,padx=15,pady=(15,30))

        delSupp_btn = ttk.Button(buttonFrame,text="Delete",command=deletesuppData)
        delSupp_btn.grid(column=1,row=1,padx=15,pady=(15,30))

        crealData_btn = ttk.Button(supplierframe1,text="Clear",width=18,command=clearsuppData)
        crealData_btn.pack(pady=(5,15))

        backFrame_btn = ttk.Button(supplierframe1,text="Back",width=18,command=self.show_dashboard)
        backFrame_btn.pack(pady=(5,10))

        global supptree
        supptree = ttk.Treeview(supplierframe2, columns=("supplier_id", "name", "contact_info", "address"), show="headings", height=24)
        supptree.column("#0", width=100)  # Adjust width for "supplier_id" column, pwede sad walaon
        supptree.column("supplier_id", width=100)
        supptree.column("name", width=200)
        supptree.column("contact_info", width=200)
        supptree.column("address", width=200)
        supptree.grid(row=10, column=0, columnspan=8, padx=(70, 10),pady=(90,10))
        supptree.heading("supplier_id", text="Supplier ID")
        supptree.heading("name", text="Name")
        supptree.heading("contact_info", text="Contact Info")
        supptree.heading("address", text="Address")
        
        populate_supplier_treeview()
        supptree.bind("<<TreeviewSelect>>", Supp_on_tree_select)
        

        self.category_frame = ttk.Frame(self)
        self.category_frame.pack_propagate(False)

        catframe1 = ttk.Frame(self.category_frame)
        catframe1.pack(side="left", fill="both", expand=True)

        catframe2 = ttk.Frame(self.category_frame, width=1000, height=800)
        catframe2.pack(side="right", fill="both", expand=True)

        global categoryID_entry
        categoryID_label = ttk.Label(catframe1, text="Category ID", font=("", 10, 'bold'))
        categoryID_label.pack(padx=20, pady=(95, 10))

        categoryID_entry = ttk.Entry(catframe1)
        categoryID_entry.pack(padx=20, pady=10)

        global categoryName_entry
        categoryName_label = ttk.Label(catframe1, text="Category", font=("", 10, 'bold'))
        categoryName_label.pack(padx=20, pady=10)

        categoryName_entry = ttk.Entry(catframe1)
        categoryName_entry.pack(padx=20, pady=10)

        addSupp_btn = ttk.Button(catframe1, text="Create", width=18, command=lambda: manage_category("insert"))
        addSupp_btn.pack(padx=10, pady=(10, 0))

        refSupp_btn = ttk.Button(catframe1, text="Refresh", width=18, command=populate_category_treeview)
        refSupp_btn.pack(padx=10, pady=(10, 0))

        updSupp_btn = ttk.Button(catframe1, text="Update", width=18, command=lambda: manage_category("update"))
        updSupp_btn.pack(padx=10, pady=(10, 0))

        delSupp_btn = ttk.Button(catframe1, text="Delete", width=18, command=lambda: manage_category("delete"))
        delSupp_btn.pack(padx=10, pady=(10, 0))

        crealData_btn = ttk.Button(catframe1, text="Clear", width=18, command=clear_category_data)
        crealData_btn.pack(padx=10, pady=(10, 0))

        backFrame_btn = ttk.Button(catframe1, text="Back", width=18, command=self.show_dashboard)
        backFrame_btn.pack(padx=10, pady=(10, 0))

        global cattree
        columns = ("category_id", "category_name")
        cattree = ttk.Treeview(catframe2, columns=columns, show="headings", height=24)

        # para sa column widths
        for col in columns:
            cattree.column(col, width=350)

        # Para sa headings Treeview
        cattree.heading("category_id", text="Category ID")
        cattree.heading("category_name", text="Category Name")

        cattree.grid(row=10, column=0, columnspan=8, padx=(70, 10), pady=(90, 10))

        populate_category_treeview()
        cattree.bind("<<TreeviewSelect>>", cat_on_tree_select)



    def login(self):
        username = self.usr_entry.get()
        password = self.pswr_entry.get()

        mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = mycursor.fetchone()

        if result:
            messagebox.showinfo("", "Login Successful!")
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_main_frame(self):
        self.dashboard.pack_forget()
        self.product_list.pack_forget()
        self.supplier_frame.pack_forget()
        self.category_frame.pack_forget()
        self.usr_entry.delete(0, tk.END)
        self.pswr_entry.delete(0, tk.END)
        messagebox.showinfo("", "Logout Successful")
        self.geometry("1000x600")
        self.title("Login frame")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

    def show_dashboard(self):
        self.main_frame.pack_forget()
        self.product_list.pack_forget()
        self.supplier_frame.pack_forget()
        self.category_frame.pack_forget()
        self.geometry("1000x700")
        self.title("Dashboard frame")
        self.dashboard.pack(expand=True, fill=tk.BOTH)

    def show_product_list(self):
        self.main_frame.pack_forget()
        self.dashboard.pack_forget()
        self.supplier_frame.pack_forget()
        self.category_frame.pack_forget()
        self.geometry("1500x700")
        self.title("Product frame")
        self.product_list.pack(expand=True, fill=tk.BOTH)

    def show_supplier_frame(self):
        self.dashboard.pack_forget()
        self.product_list.pack_forget()
        self.main_frame.pack_forget()
        self.category_frame.pack_forget()
        self.geometry("1500x700")
        self.title("Supplier frame")
        self.supplier_frame.pack(expand=True, fill=tk.BOTH)


    def show_category_frame(self):
        self.dashboard.pack_forget()
        self.product_list.pack_forget()
        self.main_frame.pack_forget()
        self.supplier_frame.pack_forget()
        self.geometry("1500x700")
        self.title("category frame")
        self.category_frame.pack(expand=True, fill=tk.BOTH)
    

if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()
