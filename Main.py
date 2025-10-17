import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry 
import json

def read_values_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            values = file.read().splitlines()
        return values
    except FileNotFoundError:
        return []

def load_config():
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Return default config if file doesn't exist
        return {
            "tax_settings": {
                "cgst_rate": 2.5,
                "sgst_rate": 2.5,
                "igst_rate": 5.0,
                "tax_type": "intrastate"
            },
            "business_details": {
                "name": "SHRI JAYASAKTHI TRADERS",
                "address_line1": "NO.10, Selva Vinayagar Kovil Street",
                "address_line2": "Kumarananthapuram, Tirupur-641602",
                "phone": "9442341916",
                "email": "shrijayasakthitraders@gmail.com",
                "gstin": "33AYDPS3713R1ZZ",
                "state": "Tamilnadu",
                "state_code": "33",
                "bank_name": "IOB, KNIT CITY BRANCH, TIRUPUR-641602",
                "account_number": "133002000005795",
                "ifsc": "IOBA0001330"
            },
            "product_settings": {
                "default_hsn": "5508"
            }
        }

class BillingSoftware:
    def __init__(self, master):

        self.CUSTOMER_FILE = "customer_data.json"
        self.master = master
        self.master.title("Billing Software")

        # Load configuration
        self.config = load_config()
        
        # Load customer data from the file
        self.customer_data = self.load_customer_data()

        # Tax rates from config
        self.cgst_rate = self.config['tax_settings']['cgst_rate'] / 100  # Convert to decimal
        self.sgst_rate = self.config['tax_settings']['sgst_rate'] / 100  # Convert to decimal

        self.total_value = 0.00
        self.singleGST = 0.00
        self.totalWithGST = 0.00

        # Panel 1: Fields for billing details till GSTIN Number
        self.panel1 = tk.Frame(master)
        self.panel1.grid(row=0, column=0, padx=10, pady=10)

        self.bill_no_label = tk.Label(self.panel1, text="Bill No:")
        self.bill_no_label.grid(row=0, column=0, padx=10, pady=10)
        self.bill_no_entry = tk.Entry(self.panel1)
        self.bill_no_entry.grid(row=0, column=1, padx=10, pady=10)

        # Date Entry using tkcalendar's DateEntry widget
        self.date_label = tk.Label(self.panel1, text="Date:")
        self.date_label.grid(row=1, column=0, padx=10, pady=10)
        self.date_entry = DateEntry(self.panel1, date_pattern='dd/MM/yyyy')
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)


        self.company_name_label = tk.Label(self.panel1, text="Company Name:")
        self.company_name_label.grid(row=2, column=0, padx=10, pady=10)
        self.company_name_var = tk.StringVar()
        # Uncomment this line
        self.company_name_dropdown = ttk.Combobox(self.panel1, textvariable=self.company_name_var, values=["Company A", "Company B"])
        self.company_name_dropdown.grid(row=2, column=1, padx=10, pady=10)
        # Company dropdown selection event
        self.company_name_dropdown.bind("<<ComboboxSelected>>", self.update_company_details)


        self.address1_label = tk.Label(self.panel1, text="Address 1:")
        self.address1_label.grid(row=3, column=0, padx=10, pady=10)
        self.address1_entry = tk.Entry(self.panel1)
        self.address1_entry.grid(row=3, column=1, padx=10, pady=10)

        self.address2_label = tk.Label(self.panel1, text="Address 2:")
        self.address2_label.grid(row=4, column=0, padx=10, pady=10)
        self.address2_entry = tk.Entry(self.panel1)
        self.address2_entry.grid(row=4, column=1, padx=10, pady=10)

        self.cell_no_label = tk.Label(self.panel1, text="Cell No:")
        self.cell_no_label.grid(row=5, column=0, padx=10, pady=10)
        self.cell_no_entry = tk.Entry(self.panel1)
        self.cell_no_entry.grid(row=5, column=1, padx=10, pady=10)

        self.gstin_label = tk.Label(self.panel1, text="GSTIN Number:")
        self.gstin_label.grid(row=6, column=0, padx=10, pady=10)
        self.gstin_entry = tk.Entry(self.panel1)
        self.gstin_entry.grid(row=6, column=1, padx=10, pady=10)

        # Panel 2: Fields for product details till Amount
        self.panel2 = tk.Frame(master)
        self.panel2.grid(row=0, column=1, padx=10, pady=10)

        self.description_label = tk.Label(self.panel2, text="Description of Goods:")
        self.description_label.grid(row=0, column=0, padx=10, pady=10)
        self.description_var = tk.StringVar()
        description_values = read_values_from_file('Cone_names.txt')
        self.description_dropdown = ttk.Combobox(self.panel2, textvariable=self.description_var, values=description_values)
        self.description_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.quantity_label = tk.Label(self.panel2, text="Quantity:")
        self.quantity_label.grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(self.panel2)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)
        self.quantity_entry.bind("<FocusOut>", self.update_amount)

        self.rate_label = tk.Label(self.panel2, text="Rate:")
        self.rate_label.grid(row=2, column=0, padx=10, pady=10)
        self.rate_entry = tk.Entry(self.panel2)
        self.rate_entry.grid(row=2, column=1, padx=10, pady=10)
        self.rate_entry.bind("<FocusOut>", self.update_amount)

        self.amount_label = tk.Label(self.panel2, text="Amount:")
        self.amount_label.grid(row=3, column=0, padx=10, pady=10)
        self.amount_value_label = tk.Label(self.panel2, text="0.00")
        self.amount_value_label.grid(row=3, column=1, padx=10, pady=10)

        # Table with 7 columns (excluding the deletion column)
        self.table = ttk.Treeview(self.master, columns=('Serial Number', 'Description of Goods', 'HSN Value', 'Quantity', 'Rate', 'Amount'))
        self.table.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Set column headings
        self.table.heading('#0', text='')
        self.table.heading('#1', text='Serial Number')
        self.table.heading('#2', text='Description of Goods')
        self.table.heading('#3', text='HSN Value')
        self.table.heading('#4', text='Quantity')
        self.table.heading('#5', text='Rate')
        self.table.heading('#6', text='Amount')

        # Set the first column width to 0 and stretch to NO
        self.table.column('#0', width=0, stretch=tk.NO)
        # Bind the delete_row method to the selection event
        self.table.bind('<ButtonRelease-1>', self.delete_row)

        # Set the anchor to 'w' (west) for left alignment
        for col in self.table['columns']:
            self.table.column(col, anchor='e')        

        # Button to add to bill
        self.add_button = tk.Button(self.panel2, text="Add To Bill", command=self.add_to_bill)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Counter for serial number
        self.serial_number_counter = 1

        # Select the first row if available
        if self.table.get_children():
            self.table.selection_set(self.table.get_children()[0])  # Select the first row by default
            self.table.focus_set()  # Set focus to the treeview

        # Print button
        self.print_button = tk.Button(self.master, text="Print", command=self.print_invoice)
        self.print_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Add new customer button
        self.add_new_customer_button = tk.Button(self.master, text="Add New Customer", command=self.add_new_customer)
        self.add_new_customer_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Load customer data from the file and update company_details
        self.customer_data, company_details = self.load_customer_data()

        # Update company_details with loaded data
        self.company_details = company_details

        # Update company dropdown with customer names
        self.update_company_dropdown()

    # Add this method to update the company dropdown with customer names
    def update_company_dropdown(self):
        customer_names = list(self.customer_data.keys())
        self.company_name_dropdown['values'] = customer_names

    def amountToWords(self, amount):
        # Simple number to words converter (replacing inflect to avoid PyInstaller issues)
        ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
        teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
        
        def convert_hundreds(num):
            result = ''
            hundreds = num // 100
            remainder = num % 100
            
            if hundreds > 0:
                result += ones[hundreds] + ' hundred '
            
            if remainder >= 20:
                tens_digit = remainder // 10
                ones_digit = remainder % 10
                result += tens[tens_digit] + ' ' + ones[ones_digit]
            elif remainder >= 10:
                result += teens[remainder - 10]
            elif remainder > 0:
                result += ones[remainder]
                
            return result.strip()
        
        if amount == 0:
            return 'zero'
        
        amount = int(amount)
        
        # Handle up to 9,99,99,999 (Indian numbering system)
        if amount >= 10000000:  # Crores
            crores = amount // 10000000
            remainder = amount % 10000000
            result = convert_hundreds(crores) + ' crore '
            if remainder > 0:
                result += self.amountToWords(remainder)
            return result.strip()
        elif amount >= 100000:  # Lakhs
            lakhs = amount // 100000
            remainder = amount % 100000
            result = convert_hundreds(lakhs) + ' lakh '
            if remainder > 0:
                result += self.amountToWords(remainder)
            return result.strip()
        elif amount >= 1000:  # Thousands
            thousands = amount // 1000
            remainder = amount % 1000
            result = convert_hundreds(thousands) + ' thousand '
            if remainder > 0:
                result += convert_hundreds(remainder)
            return result.strip()
        else:
            return convert_hundreds(amount)
    
    def load_customer_data(self):
        try:
            with open(self.CUSTOMER_FILE, 'r') as file:
                customer_data = json.load(file)
                # Extract the company_details from customer_data
                company_details = {key: value for key, value in customer_data.items()}
                return customer_data, company_details
        except FileNotFoundError:
            return {}, {}

    def save_customer_data(self):
        with open(self.CUSTOMER_FILE, 'w') as file:
            json.dump(self.customer_data, file, indent=2)

    def add_new_customer(self):
        # Create a new Toplevel window for the dialog
        new_customer_dialog = tk.Toplevel(self.master)
        new_customer_dialog.title("Add New Customer")

        # Fields for the new customer details
        tk.Label(new_customer_dialog, text="Company Name:").grid(row=0, column=0, padx=10, pady=10)
        company_name_var = tk.StringVar()
        tk.Entry(new_customer_dialog, textvariable=company_name_var).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(new_customer_dialog, text="Address 1:").grid(row=1, column=0, padx=10, pady=10)
        address1_var = tk.StringVar()
        tk.Entry(new_customer_dialog, textvariable=address1_var).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(new_customer_dialog, text="Address 2:").grid(row=2, column=0, padx=10, pady=10)
        address2_var = tk.StringVar()
        tk.Entry(new_customer_dialog, textvariable=address2_var).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(new_customer_dialog, text="Cell No:").grid(row=3, column=0, padx=10, pady=10)
        cell_no_var = tk.StringVar()
        tk.Entry(new_customer_dialog, textvariable=cell_no_var).grid(row=3, column=1, padx=10, pady=10)

        tk.Label(new_customer_dialog, text="GSTIN No:").grid(row=4, column=0, padx=10, pady=10)
        gstin_var = tk.StringVar()
        tk.Entry(new_customer_dialog, textvariable=gstin_var).grid(row=4, column=1, padx=10, pady=10)

        # Button to save the new customer details
        tk.Button(new_customer_dialog, text="Save", command=lambda: self.save_customer_details(
            company_name_var.get(), address1_var.get(), address2_var.get(), cell_no_var.get(), gstin_var.get(),
            new_customer_dialog)).grid(row=5, column=0, columnspan=2, pady=10)

    def update_company_details(self, event):
        selected_company = self.company_name_var.get()

        # Retrieve details from the loaded customer data
        if selected_company in self.company_details:
            details = self.company_details[selected_company]
            self.address1_entry.delete(0, tk.END)
            self.address1_entry.insert(0, details["Address1"])
            self.address2_entry.delete(0, tk.END)
            self.address2_entry.insert(0, details["Address2"])
            self.cell_no_entry.delete(0, tk.END)
            self.cell_no_entry.insert(0, details["CellNo"])
            self.gstin_entry.delete(0, tk.END)
            self.gstin_entry.insert(0, details["GSTIN"])

    def save_customer_details(self, company_name, address1, address2, cell_no, gstin, dialog):
        # Update the company dropdown with the new customer
        self.company_name_dropdown['values'] = [*self.company_name_dropdown['values'], company_name]
        self.company_name_var.set(company_name)

        # Update other fields
        self.address1_entry.delete(0, tk.END)
        self.address1_entry.insert(0, address1)

        self.address2_entry.delete(0, tk.END)
        self.address2_entry.insert(0, address2)

        self.cell_no_entry.delete(0, tk.END)
        self.cell_no_entry.insert(0, cell_no)

        self.gstin_entry.delete(0, tk.END)
        self.gstin_entry.insert(0, gstin)

        # Save the new customer details to the file
        self.customer_data[company_name] = {
            "Address1": address1,
            "Address2": address2,
            "CellNo": cell_no,
            "GSTIN": gstin
        }
        self.save_customer_data()
        self.update_company_dropdown()
        # Close the dialog
        dialog.destroy()

    def print_invoice(self):
        try:
            # Gather information from input fields
            bill_no = self.bill_no_entry.get()
            date = self.date_entry.get()
            company_name = self.company_name_var.get()
            address1 = self.address1_entry.get()
            address2 = self.address2_entry.get()
            cell_no = self.cell_no_entry.get()
            gstin = self.gstin_entry.get()

            # Get business details from config
            business = self.config['business_details']
            cgst_percent = self.config['tax_settings']['cgst_rate']
            sgst_percent = self.config['tax_settings']['sgst_rate']

            # Gather information from the table
            table_data = []
            for item_id in self.table.get_children():
                values = self.table.item(item_id, 'values')
                if values:
                    table_data.append(values[0:])  # Exclude the serial number
            
            # Check if there's data to print
            if not table_data:
                messagebox.showwarning("No Data", "Please add items to the bill before printing.")
                return

            # Create the HTML invoice
            html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Invoice</title>
            <style>
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 2px;
                    text-align: left;
                    max-height: 15px;
                    height: 15px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                tr{{
                    height: 15px !important;
                    max-height: 15px !important;
                }}
            </style>
            <script>
                window.onload = function() {{
                    window.print();
                }};
            </script>
        </head>
        <body>  
            <table>
                <tr >
                    <th colspan="5"style="text-align: center; border-bottom: none;">{business['name']}</th>
                    <th colspan="2" style="text-align: center">INVOICE</th>
                </tr>
                <tr style="height: 15px;">
                    <th colspan="5" style="text-align: center; border-top: none; border-bottom: none;">{business['address_line1']}</th>
                    <th style="text-align: center" rowspan='2'>No:</th>
                    <th style="text-align: center" rowspan='2'> {bill_no}</th>
                </tr>
                <tr style="height: 15px;">
                    <th colspan="5" style="text-align: center; border-top: none; border-bottom: none;">{business['address_line2']}</th>
                </tr>
                <tr>
                    <th colspan="5" style="text-align: center; border-bottom: none; border-top: none;">CELL: {business['phone']}</th>
                    <th style="text-align: center" rowspan='2'>Date:</th>
                    <th style="text-align: center" rowspan='2'> {date}</th>
                </tr>
                <tr>
                    <th colspan="5" style="text-align: center; border-top: none;">EMAIL ID: {business['email']}</th>
                </tr>
                <tr>
                    <th colspan="2" style="text-align: center;">STATE: {business['state']}</th>
                    <th colspan="2" style="text-align: center;">STATE CODE: {business['state_code']}</th>
                    <th colspan="3" style="text-align: center;">GSTIN: {business['gstin']}</th>
                </tr>
                <tr>
                    <th colspan="4">To:</th>
                    <th colspan="3">Consignee:</th>
                </tr>
                <tr>
                    <th colspan="4" style="text-align: center">{company_name}</th>
                    <th colspan="3"></th>
                </tr>
                <tr>
                    <th colspan="4" style="text-align: center">{address1}</th>
                    <th colspan="3"></th>
                </tr>
                <tr>
                    <th colspan="4" style="text-align: center">{address2}</th>
                    <th colspan="3">GSTIN: </th>
                </tr>
                <tr>
                    <th colspan="4" style="text-align: center">Cell No: {cell_no}</th>
                    <th colspan="3">State:</th>
                </tr>
                <tr>
                    <th colspan="4" rowspan="2" style="text-align: center">GSTIN: {gstin}</th>
                    <th colspan="3" style="font-size: 12px;">MODE OF TRANSPORT: By Road</th> 
                </tr>
                <tr>
                    <th colspan="3">Place of Supply: </th>
                </tr>
                <tr>
                    <th colspan="2" style="border-right: none">STATE: TAMILNADU</th>
                    <th colspan="2" style="border-left: none">STATE CODE: 33</th>
                    <th colspan="3">No of Bundles: </th>
                </tr>
                <tr>
                    <th style="text-align: center; width: 60px;" colspan="1">S. No.</th>
                    <th style="text-align: center" colspan='2'>Description of Goods</th>
                    <th style="text-align: center; width: 60px;">HSN Value</th>
                    <th style="text-align: center">Quantity</th>
                    <th style="text-align: center">Rate</th>
                    <th style="text-align: center">Amount</th>
                </tr>
        """

            for row in table_data:
                html_content += f"""
                <tr>
                    <td style="text-align: center; width: 60px;" colspan="1">{row[0]}.</td>
                    <td colspan='2'>{row[1]}</td>
                    <td style="text-align: center">{row[2]}</td>
                    <td style="text-align: right; width: 60px;">{f"{round(float(row[3]),3): .3f}"}</td>
                    <td style="text-align: right">{f"{round(float(row[4]),2): .2f}"}</td>
                    <td style="text-align: right">{f"{round(float(row[5]),2): .2f}"}</td>
                </tr>
                """
            remaining = 12-len(table_data)
            for i in range(remaining):
                html_content += f"""
                <tr>
                    <td style="text-align: center"></td>
                    <td colspan='2'></td>
                    <td style="text-align: center"></td>
                    <td style="text-align: right"></td>
                    <td style="text-align: right"></td>
                    <td style="text-align: right"></td>
                </tr>
                """
            html_content += f"""
            <tr>
                <td colspan="4" style="text-align: center">TOTAL INVOICE AMOUNT IN WORDS</td>
                <td colspan="2" style="font-size: 14px;">GROSS VALUE:</td>
                <td>{round(self.total_value,2)}</td>
            </tr>
            <tr>
                <td colspan="4" rowspan="3" style="text-align: center; font-size: 14px;">{(self.amountToWords(round(self.totalWithGST))).upper()} RUPEES ONLY</td>
                <td colspan="2" style="font-size: 14px;">CGST {cgst_percent}%: </td>
                <td colspan="1">{f"{round(self.singleGST,2): .2f}"}</td>
            </tr>
            <tr>
                <td colspan="2" style="font-size: 14px;">SGST {sgst_percent}%: </td>
                <td colspan="1">{f"{round(self.singleGST,2): .2f}"}</td>
            </tr>
            <tr>
                <td colspan="2" style="font-size: 14px;">ROUND OFF VALUE: </td>
                <td colspan="1">{f"{round(round(self.totalWithGST) - self.totalWithGST ,2): .2f}"}</td>
            </tr>
            <tr>
                <td colspan="4" style="font-size: 14px">Bank Name: {business['bank_name']}</td>
                <td colspan="2" style="font-size: 14px;">TOTAL: </td>
                <td colspan="1">{f"{round(self.totalWithGST): .2f}"}</td>
            </tr>
            <tr>
               <td colspan="4">Bank Account Number: {business['account_number']}</td>
               <td colspan="3" style="border-bottom: none;font-size: 10px; text-align: center;">Certified that the particulars given above are true.</td> 
            </tr>
            <tr>
                <td colspan="4">Bank Branch IFSC: {business['ifsc']}</td>
                <td colspan="3" style="text-align: center; border-top: none">For {business['name']}</td>
            </tr>
            <tr>
                <td colspan="4" style="text-align: center">CUSTOMER SIGNATURE</td>
                <td colspan="3" style="border-bottom: none"></td>
            </tr>
            <tr>
                <td  colspan="4" style="border-bottom: none"></td>
                <td  colspan="3" style="border-top: none; border-bottom: none;"></td>
            </tr>
            <tr>
                <td  colspan="4" style="border-top: none; border-bottom: none;"></td>
                <td  colspan="3" style="border-top: none; border-bottom: none;"></td>
            </tr>
            <tr>
                <td  colspan="4" style="border-top: none; "></td>
                <td  colspan="3" style="border-top: none; "></td>
            </tr>
            </table>
        </body>
        </html>
        """
            
            # Save HTML content to a file
            with open("invoice.html", "w") as html_file:
                html_file.write(html_content)

            # Open the HTML file for printing with absolute path
            import webbrowser
            import os
            abs_path = os.path.abspath("invoice.html")
            file_url = f"file://{abs_path}"
            result = webbrowser.open(file_url, new=2)
            
            if not result:
                messagebox.showerror("Error", "Failed to open invoice in browser")
                
        except Exception as e:
            messagebox.showerror("Print Error", f"An error occurred while printing:\n{str(e)}")
            print(f"Print error: {e}")
            import traceback
            traceback.print_exc()
    

    # def update_company_details(self, event):
    #     selected_company = self.company_name_var.get()

    #     # Example data - Replace with your actual data or fetching mechanism
    #     company_details = {
    #         "Company A": {"Address1": "Address A1", "Address2": "Address A2", "CellNo": "1234567890", "GSTIN": "GSTIN123"},
    #         "Company B": {"Address1": "Address B1", "Address2": "Address B2", "CellNo": "9876543210", "GSTIN": "GSTIN456"}
    #     }

    #     if selected_company in company_details:
    #         details = company_details[selected_company]
    #         self.address1_entry.delete(0, tk.END)
    #         self.address1_entry.insert(0, details["Address1"])
    #         self.address2_entry.delete(0, tk.END)
    #         self.address2_entry.insert(0, details["Address2"])
    #         self.cell_no_entry.delete(0, tk.END)
    #         self.cell_no_entry.insert(0, details["CellNo"])
    #         self.gstin_entry.delete(0, tk.END)
    #         self.gstin_entry.insert(0, details["GSTIN"])

    def update_amount(self, event):
        try:
            quantity = float(self.quantity_entry.get())
            rate = float(self.rate_entry.get())
            amount = quantity * rate
            self.amount_value_label.config(text=f"{amount:.2f}")
        except ValueError:
            self.amount_value_label.config(text="0.00")

    def add_to_bill(self):
        # Get values from entries
        description = self.description_var.get()
        hsn_value = self.config['product_settings']['default_hsn']  # From config
        quantity = self.quantity_entry.get()
        rate = self.rate_entry.get()

        if description and quantity and rate:
            # Calculate amount
            amount = float(quantity) * float(rate)

            # Insert into the table with dynamically generated serial number
            self.table.insert('', 'end',values=(self.serial_number_counter, description, hsn_value, quantity, rate, amount))

            # Increment serial number counter
            self.serial_number_counter += 1

            # Reset entry values
            self.description_var.set('')
            self.quantity_entry.delete(0, tk.END)
            self.rate_entry.delete(0, tk.END)
            self.amount_value_label.config(text="0.00")  # Reset amount display

            # Update total
            self.total_value += amount
            # Use configurable tax rates
            self.singleGST = self.total_value * self.cgst_rate  # Using rate from config
            total_tax_rate = self.cgst_rate + self.sgst_rate
            self.totalWithGST = self.total_value * total_tax_rate + self.total_value

        else:
            messagebox.showerror("Error", "Please enter all required details.")


    def delete_row(self, event):
        # Get the selected item
        item_id = self.table.selection()

        if item_id:
            # Extract values from the selected row
            values = self.table.item(item_id, 'values')

            if values:
                serial_number, _, _, quantity, rate, amount = values

                # Update total by subtracting the deleted amount
                self.total_value -= float(amount)
                
                # Recalculate GST with the new total
                self.singleGST = self.total_value * self.cgst_rate
                total_tax_rate = self.cgst_rate + self.sgst_rate
                self.totalWithGST = self.total_value * total_tax_rate + self.total_value
                
                self.amount_value_label.config(text=f"{self.total_value:.2f}")

                # Delete the selected row
                self.table.delete(item_id)

                # Update serial numbers
                self.update_serial_numbers()

    def update_serial_numbers(self):
        # Get all the items in the table
        items = self.table.get_children()
        
        # Update the serial numbers
        for i, item in enumerate(items, start=1):
            self.table.item(item, values=(i, *self.table.item(item, 'values')[1:]))

    

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingSoftware(root)
    root.mainloop()
