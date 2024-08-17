import tkinter as tk
from tkinter import messagebox
from zerobit_product import Product
from zerobit_report_generator import ReportGenerator
from zerobit_admin import Admin
from transformers import pipeline
import csv


class Analyzer:
    def __init__(self, win):
        self.win = win
        self.classifier = pipeline("sentiment-analysis")
        self.ADMIN_USERNAME = "admin"
        self.ADMIN_PASSWORD = "115158179"
        self.product = Product("zerobit_products.csv")
        self.admin = Admin(self.ADMIN_USERNAME, self.ADMIN_PASSWORD)
        self.product_sentiment_records = {product_name: [] for product_name in self.product.get_product_names()}
        self.graph_buttons = []
        self.report_buttons = [] 
        self.setup_gui()
        self.load_feedbacks()
    def setup_gui(self):
        self.win.title("Feedback Analyzer")
        self.win.configure(bg="lightblue")
        self.frame = tk.Frame(self.win, bg="lightblue")
        self.frame.pack()

        self.product_label = tk.Label(self.win, text="Select a product:", font=("Arial", 12), bg="lightblue")
        self.product_label.pack()
        self.product_listbox = tk.Listbox(self.win, bg="white", fg="black")
        for product_name in self.product.get_product_names():
            self.product_listbox.insert(tk.END, product_name)
        self.product_listbox.pack()

        self.feedback_label = tk.Label(self.win, text="Enter your feedback:", font=("Arial", 12), bg="lightblue")
        self.feedback_label.pack()
        self.feedback_entry = tk.Entry(self.win, width=50, bg="white", fg="black")
        self.feedback_entry.pack()

        self.submit_button = tk.Button(self.win, text="Submit Feedback", command=self.submit_feedback, bg="#28a745", fg="white", padx=10, pady=5)
        self.submit_button.pack(pady=5)

        self.result_label = tk.Label(self.win, text="", font=("Arial", 12), bg="lightblue")
        self.result_label.pack()

        self.admin_login_button = tk.Button(self.win, text="Admin Login", command=self.admin_login, bg="#0056b3", fg="white", padx=10, pady=5)
        self.admin_login_button.pack(pady=20)

        self.graphs_label = tk.Label(self.win, text="GRAPHS GENERATION", font=("Arial", 12), bg="lightblue")
        self.reports_label = tk.Label(self.win, text="REPORTS GENERATION", font=("Arial", 12), bg="lightblue")
        self.login_label = tk.Label(self.win, text="Admin Login", font=("Arial", 12), bg="lightblue")
        self.username_label = tk.Label(self.win, text="Username:", font=("Arial", 12), bg="lightblue")
        self.username_entry = tk.Entry(self.win)
        self.password_label = tk.Label(self.win, text="Password:", font=("Arial", 12), bg="lightblue")
        self.password_entry = tk.Entry(self.win, show="*")
        self.login_button = tk.Button(self.win, text="Login", command=self.login, bg="#0056b3", fg="white", padx=10, pady=5)
        self.logout_button = tk.Button(self.win, text="Logout", command=self.logout, bg="#dc3545", fg="white", padx=10, pady=5)
        self.back_button = tk.Button(self.win, text="Back to Feedback", command=self.backtofeedback, bg="#fd7e14", fg="white", padx=10, pady=5)
    def submit_feedback(self):
        selected_product = self.product_listbox.get(tk.ACTIVE)
        feedback = self.feedback_entry.get()

        analysis = self.classifier(feedback)

        if analysis:
            sentiment_label = analysis[0].get('label', 'N/A')
            confidence_score = float(analysis[0].get('score', 0))
            self.product_sentiment_records.setdefault(selected_product, [])

            self.product_sentiment_records[selected_product].append((sentiment_label, confidence_score))
            self.save_feedbacks()

            self.result_label.config(
                text=f"Sentiment Analysis Result for {selected_product}: {sentiment_label} (Confidence: {confidence_score:.2f})",
                fg="green")
        else:
            self.result_label.config(text="Error: Unable to perform sentiment analysis", fg="red")

        self.feedback_entry.delete(0, tk.END)

    def admin_login(self):
        self.admin_login_button.pack_forget()
        self.product_label.pack_forget()
        self.product_listbox.pack_forget()
        self.feedback_label.pack_forget()
        self.feedback_entry.pack_forget()
        self.submit_button.pack_forget()
        self.result_label.pack_forget()

        self.login_label.pack()
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack(pady=5)
        self.back_button.pack(pady=5)

    def save_feedbacks(self):
        with open('zerobit_feedbacks.csv', 'w', newline='') as csvfile:
            fieldnames = ['Product', 'Feedback', 'Sentiment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for product, feedbacks in self.product_sentiment_records.items():
                for feedback in feedbacks:
                    writer.writerow({'Product': product, 'Feedback': feedback[0], 'Sentiment': feedback[1]})

    def load_feedbacks(self):
        self.product_sentiment_records.clear()
        with open('zerobit_feedbacks.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product = row['Product']
                feedback = row['Feedback']
                sentiment = row['Sentiment']
                self.product_sentiment_records.setdefault(product, []).append((feedback, sentiment))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.admin.authenticate(username, password):
            messagebox.showinfo("Login Successful", "Welcome, Admin!")

            self.reports_label.pack(side=tk.TOP)
            self.generate_report_buttons()
            self.graphs_label.pack()
            self.generate_graph_buttons()
            self.logout_button.pack()

            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.login_label.pack_forget()
            self.back_button.pack_forget()
            self.username_label.pack_forget()
            self.username_entry.pack_forget()
            self.password_label.pack_forget()
            self.password_entry.pack_forget()
            self.login_button.pack_forget()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def generate_report_buttons(self):
        for product_name in self.product.get_product_names():
            report_button = tk.Button(self.win, text=f"Generate Report for {product_name}",
                                      command=lambda prod=product_name: self.generate_report(prod), bg="#0056b3",
                                      fg="white", padx=10, pady=5)
            report_button.pack(pady=5)
            self.report_buttons.append(report_button)

    def generate_report(self, product_name):
        if product_name in self.product_sentiment_records:
            sentiment_records = self.product_sentiment_records[product_name]
            report_text = ReportGenerator.generate_text_report(product_name, sentiment_records)
            messagebox.showinfo("Sentiment Report", report_text)
        else:
            messagebox.showerror("Error", f"No sentiment records found for product: {product_name}")

    def generate_graph_buttons(self):
        for product_name in self.product.get_product_names():
            graph_button = tk.Button(self.win, text=f"Generate Graph for {product_name}",
                                     command=lambda prod=product_name: self.generate_graph(prod), bg="#28a745", fg="white",
                                     padx=10, pady=5)
            graph_button.pack(pady=5)
            self.graph_buttons.append(graph_button)

    def generate_graph(self, product_name):
        if product_name in self.product_sentiment_records:
            sentiment_records = self.product_sentiment_records[product_name]
            ReportGenerator.generate_graph(product_name, sentiment_records)
        else:
            messagebox.showerror("Error", f"No sentiment records found for product: {product_name}")

    def logout(self):
        self.logout_button.pack_forget()
        for button in self.graph_buttons:
            button.pack_forget()
        for button in self.report_buttons:
            button.pack_forget()

        self.reports_label.pack_forget()
        self.graphs_label.pack_forget()

        self.product_label.pack()
        self.product_listbox.pack()
        self.feedback_label.pack()
        self.feedback_entry.pack()
        self.submit_button.pack()
        self.result_label.pack()
        self.admin_login_button.pack(pady=20)

    def backtofeedback(self):
        self.login_label.pack_forget()
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.password_label.pack_forget()
        self.password_entry.pack_forget()
        self.login_button.pack_forget()
        self.back_button.pack_forget()

        self.product_label.pack()
        self.product_listbox.pack()
        self.feedback_label.pack()
        self.feedback_entry.pack()
        self.submit_button.pack(pady=5)
        self.result_label.pack()
        self.admin_login_button.pack(pady=20)

