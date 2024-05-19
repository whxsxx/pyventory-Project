# Intstall sa ka sa python.org
    https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe

# Install command para sa mga imports
pip install ttkbootstrap

pip install mysql-connector-python

python --version 


## Search for product functions
    Start Product Functions
        fetch_product_data()
            eFetch niya ang data pag open palng nimo sa Frame
        populate_treeview(prodtree)
            apil ni sa fetch_product_data()
        prod_on_tree_select(event) 
            pag mag click ka og data sa treeview ma adto sa sya mga Entrys
        readprodData()
            Refresh button ni ya (kung naa kay eUpdate sa Supplier or Category dapat eClick sa nimo ang Refresh button)
        CRUD Operations / Create, Retrieve, Update, Delete
            insert_product()
                Mag add/insert kag product data sa database
            update_product()
                Update  product data
            delete_product()
                delete product data
                messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?") ari kay confirmation ni sya kung mag delete kag data
        stock_in()
            Mag add kag stocks sa product
        stock_out()
            Mag decrease kag stocks
        fetch_suppliers_and_categories()
            Ari mag display syag data sa combobox
        populate_comboboxes(supplier_combobox, category_combobox)
            sabay ni sya sa fetch_suppliers_and_categories()
    EndProduct Functions

## Start Supplier Functions
    Start Product Functions
        CRUD Operations / Create, Retrieve, Update, Delete
            insertsuppData()
            updatesuppData()
            deletesuppData()
        readsuppData()
            Refresh Button
        Supp_on_tree_select(event)
            pag mag click ka og data sa treeview ma adto sa sya mga Entrys
        clearsuppData()
            Clear entrys
        fetch_supplier_data()
            eFetch niya ang data pag open palng nimo sa Frame
        populate_supplier_treeview()
            apil ni sa fetch_product_data()
    End Product Functions

## Start Supplier Functions
    Start Product Functions
        Halos same lang sa supplier na functions
    End Product Functions


# Log in Function
    login(self)

# def show_main_frame(self)
    self.dashboard.pack_forget()
        Para dili makita ang frame sa dashboard
    self.product_list.pack_forget()
        Para dili makita ang frame sa product
    self.supplier_frame.pack_forget()
        same lang
    self.category_frame.pack_forget()
        same lang
    self.usr_entry.delete(0, tk.END)
    self.pswr_entry.delete(0, tk.END)
        Para kung mag log out mang ka walay unod ang entrys
    messagebox.showinfo("", "Logout Successful")
        pag log out nimo amo ni ang Message mag pop up
    self.geometry("1000x600")
        size sa frame sa Log in
    self.title("Login frame")
        title sa frame
    self.main_frame.pack(expand=True, fill=tk.BOTH)
        frame sa log in

# def show_dashboard(self):
# def show_product_list(self):
# def show_supplier_frame(self):
# def show_category_frame(self):
    Same lang sa babaw