import tkinter as tk
from tkinter import messagebox
from connection import connection
import psycopg2
import hashlib

class LoginApp:
    def __init__(self,root):
        self.root=root
        self.root.title("POSTGRESQL LOGIN PAGE")
        self.root.geometry("500x500")

        self.root.configure(bg="#f0f0f0")
        font=("Arial",12)

        tk.Label(root,text="USERNAME",bg="#f0f0f0",font=font).pack(pady=(50,5))
        self.entry_username=tk.Entry(root,font=font)
        self.entry_username.pack()

        tk.Label(root,text="PASSORD",bg="#f0f0f0",font=font).pack(pady=(50,5))
        self.entry_password=tk.Entry(root,font=font,show="*")
        self.entry_password.pack()
        self.show_password=tk.BooleanVar()
        tk.Checkbutton(root,text="Show password",variable=self.show_password,command=self.toogle_password,bg="#F0F0F0").pack(pady=(5,0))

        button_frame=tk.Frame(root,bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(button_frame,text="LOGIN", command=self.login,font=font,bg="#4caf50",fg="white").pack(side=tk.LEFT,padx=10)
        tk.Button(button_frame,text="REGISTER", command=self.register,font=font,bg="#2196f3",fg="white").pack(side=tk.LEFT)

        
    def toogle_password(self):
        if self.show_password.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")
    def execute_query(self,query,params):
        conn=connection()
        if conn:
            try:
                cursor=conn.cursor()
                cursor.execute(query,params or ())
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchone()
                conn.commit()
                return True
            except psycopg2.Error as e:
                conn.rollback()
                messagebox.showerror("Database Error")
                return False
            finally:
                if conn:
                    cursor.close()
                    conn.close()

        return False
    
    def login(self):
        username=self.entry_username.get()
        password=self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Both fields required")
            return
        user=self.execute_query(
            "SELECT * FROM users WHERE USERNAME=%s AND password=%s",
            (username,password)
        )

        if user:
            messagebox.showinfo("Success","Logged in successfully")
        else:
            messagebox.showerror("Error","Wrong username or password")

    def register(self):
        username=self.entry_username.get()
        password=self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Both fields must be filled")
            return
        
        if self.execute_query(
            "INSERT INTO users(username,password) VALUES(%s,%s)",
            (username,password)
        ):
            messagebox.showinfo("Success","Registered successfully")

if __name__ == "__main__":
    root=tk.Tk()
    app=LoginApp(root)
    root.mainloop()