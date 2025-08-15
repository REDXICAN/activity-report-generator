import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import threading
import os
from dotenv import load_dotenv, set_key
from main import ActivityReportGenerator

class ActivityReportGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Report Generator - TurboAir")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Load environment variables
        load_dotenv()
        self.env_file = '.env'
        
        # Initialize generator
        self.generator = ActivityReportGenerator()
        
        # Create GUI
        self.create_widgets()
        
        # Load saved settings
        self.load_settings()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Activity Report Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Date Range Section
        date_frame = ttk.LabelFrame(main_frame, text="Report Period", padding="10")
        date_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(date_frame, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
        self.start_date = DateEntry(date_frame, width=12, background='darkblue',
                                   foreground='white', borderwidth=2)
        self.start_date.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(date_frame, text="End Date:").grid(row=0, column=2, padx=5, pady=5)
        self.end_date = DateEntry(date_frame, width=12, background='darkblue',
                                 foreground='white', borderwidth=2)
        self.end_date.grid(row=0, column=3, padx=5, pady=5)
        
        # Quick date buttons
        ttk.Button(date_frame, text="Last 15 Days", 
                  command=self.set_last_15_days).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(date_frame, text="Current Month", 
                  command=self.set_current_month).grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
        # Data Sources Section
        sources_frame = ttk.LabelFrame(main_frame, text="Data Sources", padding="10")
        sources_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Email settings
        self.email_enabled = tk.BooleanVar(value=True)
        email_check = ttk.Checkbutton(sources_frame, text="Email (Gmail)", 
                                      variable=self.email_enabled,
                                      command=self.toggle_email_settings)
        email_check.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.email_frame = ttk.Frame(sources_frame)
        self.email_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=(20, 0))
        
        ttk.Label(self.email_frame, text="Gmail Credentials:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.gmail_creds_path = tk.StringVar()
        ttk.Entry(self.email_frame, textvariable=self.gmail_creds_path, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(self.email_frame, text="Browse", 
                  command=lambda: self.browse_file(self.gmail_creds_path)).grid(row=0, column=2)
        
        ttk.Label(self.email_frame, text="Email Accounts:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.email_accounts = tk.StringVar()
        ttk.Entry(self.email_frame, textvariable=self.email_accounts, width=40).grid(row=1, column=1, padx=5)
        ttk.Label(self.email_frame, text="(comma separated)", 
                 font=('Arial', 8)).grid(row=1, column=2, sticky=tk.W)
        
        # GitHub settings
        self.github_enabled = tk.BooleanVar(value=True)
        github_check = ttk.Checkbutton(sources_frame, text="GitHub", 
                                       variable=self.github_enabled,
                                       command=self.toggle_github_settings)
        github_check.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.github_frame = ttk.Frame(sources_frame)
        self.github_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=(20, 0))
        
        ttk.Label(self.github_frame, text="GitHub Token:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.github_token = tk.StringVar()
        ttk.Entry(self.github_frame, textvariable=self.github_token, width=40, show="*").grid(row=0, column=1, padx=5)
        
        ttk.Label(self.github_frame, text="GitHub Username:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.github_username = tk.StringVar()
        ttk.Entry(self.github_frame, textvariable=self.github_username, width=40).grid(row=1, column=1, padx=5)
        
        # WhatsApp settings
        self.whatsapp_enabled = tk.BooleanVar(value=True)
        whatsapp_check = ttk.Checkbutton(sources_frame, text="WhatsApp Business", 
                                         variable=self.whatsapp_enabled,
                                         command=self.toggle_whatsapp_settings)
        whatsapp_check.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.whatsapp_frame = ttk.Frame(sources_frame)
        self.whatsapp_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=(20, 0))
        
        ttk.Label(self.whatsapp_frame, text="WhatsApp Export:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.whatsapp_path = tk.StringVar()
        ttk.Entry(self.whatsapp_frame, textvariable=self.whatsapp_path, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(self.whatsapp_frame, text="Browse", 
                  command=lambda: self.browse_folder(self.whatsapp_path)).grid(row=0, column=2)
        
        # Output Settings
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(output_frame, text="Output Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar(value=r"O:\OneDrive\Documentos\-- TurboAir\-- Reportes de Actividad")
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(output_frame, text="Browse", 
                  command=lambda: self.browse_folder(self.output_path)).grid(row=0, column=2)
        
        ttk.Label(output_frame, text="Format:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_format = tk.StringVar(value="both")
        format_frame = ttk.Frame(output_frame)
        format_frame.grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(format_frame, text="Excel Only", variable=self.output_format, 
                       value="excel").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="Word Only", variable=self.output_format, 
                       value="word").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="Both", variable=self.output_format, 
                       value="both").pack(side=tk.LEFT, padx=5)
        
        # Progress Section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.progress = ttk.Progressbar(progress_frame, length=400, mode='indeterminate')
        self.progress.grid(row=0, column=0, columnspan=2, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready to generate report")
        self.status_label.grid(row=1, column=0, columnspan=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Save Settings", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate Report", 
                  command=self.generate_report,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Set initial state
        self.toggle_email_settings()
        self.toggle_github_settings()
        self.toggle_whatsapp_settings()
    
    def toggle_email_settings(self):
        if self.email_enabled.get():
            for widget in self.email_frame.winfo_children():
                widget.configure(state='normal')
        else:
            for widget in self.email_frame.winfo_children():
                if isinstance(widget, (ttk.Entry, ttk.Button)):
                    widget.configure(state='disabled')
    
    def toggle_github_settings(self):
        if self.github_enabled.get():
            for widget in self.github_frame.winfo_children():
                widget.configure(state='normal')
        else:
            for widget in self.github_frame.winfo_children():
                if isinstance(widget, ttk.Entry):
                    widget.configure(state='disabled')
    
    def toggle_whatsapp_settings(self):
        if self.whatsapp_enabled.get():
            for widget in self.whatsapp_frame.winfo_children():
                widget.configure(state='normal')
        else:
            for widget in self.whatsapp_frame.winfo_children():
                if isinstance(widget, (ttk.Entry, ttk.Button)):
                    widget.configure(state='disabled')
    
    def browse_file(self, var):
        filename = filedialog.askopenfilename()
        if filename:
            var.set(filename)
    
    def browse_folder(self, var):
        folder = filedialog.askdirectory()
        if folder:
            var.set(folder)
    
    def set_last_15_days(self):
        end = datetime.now()
        start = end - timedelta(days=15)
        self.start_date.set_date(start)
        self.end_date.set_date(end)
    
    def set_current_month(self):
        now = datetime.now()
        start = now.replace(day=1)
        self.start_date.set_date(start)
        self.end_date.set_date(now)
    
    def save_settings(self):
        """Save settings to .env file"""
        try:
            if not os.path.exists(self.env_file):
                open(self.env_file, 'a').close()
            
            if self.gmail_creds_path.get():
                set_key(self.env_file, 'GMAIL_CREDENTIALS_FILE', self.gmail_creds_path.get())
            if self.email_accounts.get():
                set_key(self.env_file, 'EMAIL_ACCOUNTS', self.email_accounts.get())
            if self.github_token.get():
                set_key(self.env_file, 'GITHUB_TOKEN', self.github_token.get())
            if self.github_username.get():
                set_key(self.env_file, 'GITHUB_USERNAME', self.github_username.get())
            if self.whatsapp_path.get():
                set_key(self.env_file, 'WHATSAPP_DATA_PATH', self.whatsapp_path.get())
            if self.output_path.get():
                set_key(self.env_file, 'REPORT_OUTPUT_PATH', self.output_path.get())
            
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def load_settings(self):
        """Load settings from .env file"""
        self.gmail_creds_path.set(os.getenv('GMAIL_CREDENTIALS_FILE', ''))
        self.email_accounts.set(os.getenv('EMAIL_ACCOUNTS', ''))
        self.github_token.set(os.getenv('GITHUB_TOKEN', ''))
        self.github_username.set(os.getenv('GITHUB_USERNAME', ''))
        self.whatsapp_path.set(os.getenv('WHATSAPP_DATA_PATH', ''))
        self.output_path.set(os.getenv('REPORT_OUTPUT_PATH', 
                            r'O:\OneDrive\Documentos\-- TurboAir\-- Reportes de Actividad'))
    
    def generate_report(self):
        """Generate the activity report"""
        # Validate inputs
        if not any([self.email_enabled.get(), self.github_enabled.get(), self.whatsapp_enabled.get()]):
            messagebox.showwarning("Warning", "Please select at least one data source")
            return
        
        # Save settings first
        self.save_settings()
        
        # Reload environment variables
        load_dotenv(override=True)
        
        # Start generation in separate thread
        thread = threading.Thread(target=self._generate_report_thread)
        thread.daemon = True
        thread.start()
    
    def _generate_report_thread(self):
        """Generate report in separate thread"""
        try:
            # Update UI
            self.progress.start()
            self.status_label.config(text="Generating report...")
            
            # Get dates
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()
            
            # Initialize collectors
            self.generator.initialize_collectors(
                email_enabled=self.email_enabled.get(),
                github_enabled=self.github_enabled.get(),
                whatsapp_enabled=self.whatsapp_enabled.get()
            )
            
            # Generate report
            excel_path, word_path = self.generator.generate_report(
                start_date, end_date, 
                output_format=self.output_format.get()
            )
            
            # Stop progress
            self.progress.stop()
            
            if excel_path:
                self.status_label.config(text="Report generated successfully!")
                messagebox.showinfo("Success", 
                    f"Report generated successfully!\n\nExcel: {excel_path}\nWord: {word_path if word_path else 'Not generated'}")
            else:
                self.status_label.config(text="Report generation failed")
                messagebox.showerror("Error", "Failed to generate report. Check your settings.")
        
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="Error generating report")
            messagebox.showerror("Error", f"Error generating report: {str(e)}")

def main():
    root = tk.Tk()
    app = ActivityReportGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()