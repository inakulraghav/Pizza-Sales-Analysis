import pymongo
import tkinter as tk
from tkinter import messagebox,simpledialog
from tkinter import ttk
from datetime import datetime



def soon():
    messagebox.showinfo("Under maintainance","This feature is available soon🔜")



grand_total=0
def pizzaproducts():
    for widget in f3_f1.winfo_children():
        widget.destroy()
    row=0
    column=0
    for s in client.Pizza_sales.Pizza_type.find({},{"_id":0,"size":1,"pizza_type_id":1,"price":1}):
        tk.Button(f3_f1,text=f"{s["pizza_type_id"]}\n {s["size"]}\n {s["price"]}$",command=lambda item=s: open_quantity_popup(item),font="Arial 16 bold",relief="solid",border=2,height=5,width=12,padx=5,pady=5,bg="#B2EBF2").grid(row=row,column=column)
        column+=1
        if column==2:
            column=0
            row+=1


def on_mousewheel(event):
    widget = event.widget
    if widget == canvas or str(widget).startswith(str(canvas)):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"
    



def add_to_summary(name, size ,qty, total_price):
    global grand_total
    global total_label
    global summary_text
    
    # for widget in f4_f1.winfo_children():
    #     widget.destroy()



    # Summary me item add
    summary_text.insert(tk.END, f"{name}   {size}   {qty} =   ${total_price:.2f}\n")
    total_label = tk.Label(f4, text="Total: $0.00", font=("Arial", 14, "bold"),bg="#1e2b39",fg="white")
    total_label.place(relx=0.6,rely=0.6,relwidth=0.4)
    
    btn=tk.Button(f4,text="Sent To Database",font="arial 12 bold",fg="black",bg="#26A69A",command=sent_to_db)
    btn.place(relx=0.05,rely=0.75,relheight=0.1,relwidth=0.4)

    btn1=tk.Button(f4,text="Cancle Order",font="arial 12 bold",fg="white",bg="red",command=order_clear)
    btn1.place(relx=0.55,rely=0.75,relheight=0.1,relwidth=0.4)

    # Total update
    grand_total += total_price
    total_label.config(text=f"Total: ${grand_total:.2f}")



def open_quantity_popup(item):
    popup = tk.Toplevel(root)
    popup.title("Select Quantity")
    popup.geometry("300x200")
    popup.grab_set()

    tk.Label(popup, text=f"{item['pizza_type_id']}\n {item['size']}", font=("Arial", 14)).pack(pady=10)

    qty_var = tk.IntVar(value=1)
    tk.Entry(popup, textvariable=qty_var, justify="center").pack(pady=5)

    def add_to_order():
        qty = qty_var.get()
        total_price = qty * item['price']

        add_to_summary(item['pizza_type_id'], item['size'],qty, total_price)
        
        summary_text.config(bd=1, highlightthickness=1)
        popup.destroy()


    tk.Button(popup, text="Add", command=add_to_order).pack(pady=15)



def sent_to_db():
    global grand_total
    try:
        mongodbtimestamp=datetime.utcnow().isoformat() + "Z"
        order_id_count=client.Pizza_sales.Order_details.find({},{"order_id":1,"_id":0})
        blank=[]
        for i in order_id_count:
            blank.append(i["order_id"])

        order_id=len(set(blank))+1
        order_details_id=len(blank)+1

        if summary_text.size()==0:
            messagebox.showerror("Empty Cart","Your cart is empty!\n\nPlease add some items before placing order.")
            return
        

        item_inserted=0
        for i in range(summary_text.size()):
            product=summary_text.get(i)
            parts=product.strip().split()


            pizza=parts[0]
            size=parts[1].lower()
            quantity=int(parts[2])
            price   = float(parts[4].replace('$', ''))
            client.Pizza_sales.Order_details.insert_one({"order_details_id":order_details_id+item_inserted,"order_id":order_id,"pizza_id":pizza+"_"+ size,"quantity":quantity})
            item_inserted+=1

        client.Pizza_sales.Orders.insert_one({"order_id":order_id,"order_time":mongodbtimestamp})
        messagebox.showinfo("Upload Successfull",f"Data has been  successfully uploaded to the database, Your order id is {order_id}\nItems: {item_inserted}")
        
        summary_text.delete(0,tk.END)
        grand_total=0
        total_label.config(text=f"Total: ${grand_total:.2f}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
        print(f"Error: {e}")



def order_clear():
    
    global grand_total
    global total_label
    global summary_text
    if grand_total==0:
        messagebox.showinfo("Info","Your cart is already cleared")
    else:
        # summary_text.config(state="normal")
        summary_text.delete(0,tk.END)
        # summary_text.config(state="disabled")
        grand_total=0
        total_label.config(text=f"Total: ${grand_total:.2f}")
        messagebox.showinfo("Cancelled","Your order is cancelled")








try:
    client = pymongo.MongoClient("mongodb+srv://raghavnakul28_db_user:nakulsinghraghav@cluster69.jvc5mxo.mongodb.net/?retryWrites=true&w=majority",serverSelectionTimeoutMS=5000)
    print("Connected succesfully")
except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"Server selection timeout error: Could not connect to MongoDB.")
    print(f"   Possible reasons: Network issue, IP not whitelisted, or incorrect credentials.")
except pymongo.errors.ConnectionFailure as e:
    print(f"Connection failure: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


root = tk.Tk()
root.config(bg="#2C5F8D")
root.title("NR pizza")
root.geometry("600x533")
root.iconbitmap(r"C:\Users\Lenovo\Downloads\3558094-bake-bread-fast-food-pizza_107831.ico")



f1=tk.Frame(root,bg="grey",relief="raised",border=5)
f1.place(relx=0.5,rely=0.5,anchor="center",relheight=0.7,relwidth=0.7)



headframe =tk.Frame(f1,bg="grey")
headframe.place(relx=0.5,rely=0.1,relheight=0.1,relwidth=1,anchor="center")
tk.Label(headframe,text="Insert Order Details",fg="white",font="Arial 20 bold",bg="grey").pack(anchor="center")



f2 =tk.Frame(f1,bg="#263238",relief="ridge",border=5)
f2.place(relx=0,rely=0.15,relheight=0.8,relwidth=0.2)
tk.Label(f2,text="Menu",font="Arial 16 bold",bg="#263238",fg="white").place(relx=0.4,rely=0.05,anchor="e")
f2_f1=tk.Frame(f2,bg="black")
f2_f1.place(relx=0.5,rely=0.5,relheight=0.7,relwidth=0.8,anchor="center")



tk.Button(f2_f1,text="Pizza",command=pizzaproducts,font="Arial 13 bold",bg="#FFA726",relief="solid",border=1).place(relx=0.5,rely=0.1,relheight=0.2,relwidth=1,anchor="center")
tk.Button(f2_f1,text="Burger",command=soon,font="Arial 13 bold",bg="#FFA726",relief="solid",border=1).place(relx=0.5,rely=0.3,relheight=0.2,relwidth=1,anchor="center")
tk.Button(f2_f1,text="Taco",command=soon,font="Arial 13 bold",bg="#FFA726",relief="solid",border=1).place(relx=0.5,rely=0.5,relheight=0.2,relwidth=1,anchor="center")
tk.Button(f2_f1,text="Drinks",command=soon,font="Arial 13 bold",bg="#FFA726",relief="solid",border=1).place(relx=0.5,rely=0.7,relheight=0.2,relwidth=1,anchor="center")
tk.Button(f2_f1,text="Desserts",command=soon,font="Arial 13 bold",bg="#FFA726",relief="solid",border=1).place(relx=0.5,rely=0.9,relheight=0.2,relwidth=1,anchor="center")




f3 =tk.Frame(f1,bg="#263238",relief="ridge",border=5)
f3.place(relx=0.21,rely=0.15,relheight=0.8,relwidth=0.4)
tk.Label(f3,text="Products",font="Arial 16 bold",bg="#263238",fg="white").place(relx=0.3,rely=0.05,anchor="e")


canvas=tk.Canvas(f3,bg="#263238",highlightthickness=0)
canvas.place(relx=0.0,rely=0.1,relheight=0.9,relwidth=1)


f3_f1=tk.Frame(canvas,bg="#263238")
f3_f1.pack(fill="both",expand=True,side="left")

scrollbar=ttk.Scrollbar(canvas,command=canvas.yview,orient="vertical")
scrollbar.pack(fill="y",side="right")
canvas.config(yscrollcommand=scrollbar.set)

# Scroll region auto update
canvas.create_window((0, 0), window=f3_f1, anchor="nw")
def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
f3_f1.bind("<Configure>", update_scrollregion)
canvas.bind_all("<MouseWheel>", on_mousewheel)


l1=tk.Label(f3_f1,text="Plzz select the category from the menu",font="Arial 16 bold", wraplength=350,justify="center",bg="#263238",fg="red")
l1.pack(padx=10,anchor="center",side="bottom",pady=120)


f4 =tk.Frame(f1,bg="#1e2b39",relief="ridge",border=5)
f4.place(relx=0.62,rely=0.15,relheight=0.8,relwidth=0.38)
tk.Label(f4,text="Order Summary",font="Arial 16 bold",bg="#1e2b39",fg="white").place(relx=0.5,rely=0.05,anchor="e")

f4_f1=tk.Frame(f4,bg="#1e2b39")
f4_f1.place(relx=0,rely=0.2,relheight=0.4,relwidth=1)


summary_text=tk.Listbox(f4_f1,bg="#1e2b39" ,fg="white",font="arial 16 bold")
summary_text.pack(fill='both')
summary_text.config(bd=0, highlightthickness=0, bg="#1e2b39")



root.mainloop()


