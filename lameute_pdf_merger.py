#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from PyPDF2 import PdfMerger, PdfReader
import threading
from PIL import Image, ImageTk, ImageDraw

class LAMEUTE_PdfMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("LAMEUTE PDF Merger")
        self.root.geometry("920x680")
        self.root.minsize(850, 620)
        self.root.configure(bg="#f5f5f5")
        
        # Initialize variables
        self.file_list = []
        self.logo = None
        
        # Setup styles first
        self.setup_styles()
        
        # Then setup UI
        self.setup_ui()

        # Make sure window stays on top initially
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))

    def setup_styles(self):
        """Configure modern salmon-red theme with rounded buttons"""
        self.style = ttk.Style()
        
        # Base colors
        self.salmon = "#ff6b6b"
        self.salmon_light = "#ff8e8e"
        self.salmon_dark = "#ff5252"
        self.bg_color = "#f5f5f5"
        self.text_color = "#333333"
        
        # Configure theme
        self.style.theme_create("lameute", parent="alt", settings={
            "TFrame": {"configure": {"background": self.bg_color}},
            "TLabel": {
                "configure": {
                    "background": self.bg_color,
                    "foreground": self.text_color,
                    "font": ("Arial", 10)
                }
            },
            "TButton": {
                "configure": {
                    "background": self.salmon,
                    "foreground": "white",
                    "font": ("Arial", 10, "bold"),
                    "borderwidth": 0,
                    "padding": 8,
                    "relief": "flat"
                },
                "map": {
                    "background": [
                        ("pressed", self.salmon_dark),
                        ("active", self.salmon_light)
                    ],
                    "foreground": [("pressed", "white"), ("active", "white")]
                }
            },
            "Treeview": {
                "configure": {
                    "background": "white",
                    "fieldbackground": "white",
                    "foreground": self.text_color,
                    "rowheight": 25,
                    "font": ("Arial", 9)
                },
                "map": {
                    "background": [("selected", self.salmon)],
                    "foreground": [("selected", "white")]
                }
            },
            "Treeview.Heading": {
                "configure": {
                    "background": self.salmon,
                    "foreground": "white",
                    "font": ("Arial", 9, "bold")
                }
            },
            "Horizontal.TProgressbar": {
                "configure": {
                    "background": self.salmon,
                    "troughcolor": "#e0e0e0",
                    "borderwidth": 0,
                    "thickness": 20
                }
            }
        })
        self.style.theme_use("lameute")

    def setup_ui(self):
        """Build the modern UI with proper spacing"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=(20, 15))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with logo
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Try to load logo (optional)
        try:
            logo_img = Image.open("logo.png").resize((48, 48), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.pack(side=tk.LEFT, padx=(0, 15))
        except Exception as e:
            print(f"Note: Logo not loaded - {e}")
        
        ttk.Label(
            header_frame,
            text="LAMEUTE PDF Merger",
            font=("Arial", 18, "bold"),
            foreground=self.salmon
        ).pack(side=tk.LEFT)

        # File list section with more padding
        list_frame = ttk.LabelFrame(
            main_frame, 
            text=" PDF Files to Merge ",
            padding=15
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Treeview with rounded scrollbars
        self.tree = ttk.Treeview(
            list_frame,
            columns=('name', 'path', 'size', 'modified'),
            show='headings',
            selectmode='extended'
        )
        
        # Configure columns
        self.tree.heading('name', text='Filename')
        self.tree.heading('path', text='Path')
        self.tree.heading('size', text='Size')
        self.tree.heading('modified', text='Modified')
        
        self.tree.column('name', width=200, anchor=tk.W)
        self.tree.column('path', width=350, anchor=tk.W)
        self.tree.column('size', width=100, anchor=tk.E)
        self.tree.column('modified', width=150, anchor=tk.W)

        # Scrollbars
        y_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Layout with proper spacing
        self.tree.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        y_scroll.grid(row=0, column=1, sticky='ns', pady=5)
        x_scroll.grid(row=1, column=0, sticky='ew', padx=5)
        
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        # Button panel with rounded buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))

        buttons = [
            ("Add Files", self.add_files),
            ("Add Folder", self.add_folder),
            ("Remove Selected", self.remove_selected),
            ("Clear All", self.clear_all),
            ("Move Up", self.move_up),
            ("Move Down", self.move_down)
        ]

        for text, cmd in buttons:
            btn = ttk.Button(button_frame, text=text, command=cmd)
            btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=3)
            self.make_button_rounded(btn)

        # Output section
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(output_frame, text="Output File:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.output_entry = ttk.Entry(output_frame, width=60, font=("Arial", 10))
        self.output_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output)
        browse_btn.pack(side=tk.LEFT, ipadx=10, ipady=3)
        self.make_button_rounded(browse_btn)

        # Progress bar with salmon color
        self.progress = ttk.Progressbar(
            main_frame, 
            orient=tk.HORIZONTAL, 
            length=100, 
            mode='determinate'
        )
        self.progress.pack(fill=tk.X, pady=(0, 15))

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(
            main_frame, 
            textvariable=self.status_var,
            font=("Arial", 9),
            foreground="#666666"
        )
        status_label.pack(fill=tk.X)

        # Action buttons with more prominent merge button
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X)

        exit_btn = ttk.Button(action_frame, text="Exit", command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT, padx=5, ipadx=20, ipady=5)
        self.make_button_rounded(exit_btn)
        
        merge_btn = ttk.Button(action_frame, text="Merge PDFs", command=self.start_merge)
        merge_btn.pack(side=tk.RIGHT, ipadx=20, ipady=5)
        self.make_button_rounded(merge_btn)

    def make_button_rounded(self, button):
        """Create rounded corners for buttons"""
        button.update()
        w = button.winfo_width() + 1
        h = button.winfo_height() + 1
        
        # Create rounded rectangle image
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((0, 0, w-1, h-1), radius=15, fill=self.salmon)
        
        # Apply as button background
        rounded_img = ImageTk.PhotoImage(img)
        button.config(image=rounded_img, compound="center")
        button.image = rounded_img  # Keep reference

    def add_files(self):
        """Add PDF files via file dialog"""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
        )
        if files:
            self.add_to_list(files)

    def add_folder(self):
        """Add all PDFs from a folder"""
        folder = filedialog.askdirectory(title="Select Folder with PDFs")
        if folder:
            files = []
            for root, _, filenames in os.walk(folder):
                for filename in filenames:
                    if filename.lower().endswith('.pdf'):
                        files.append(os.path.join(root, filename))
            self.add_to_list(files)

    def add_to_list(self, files):
        """Add files to the list with validation"""
        for file_path in files:
            if file_path not in self.file_list:
                try:
                    size_kb = os.path.getsize(file_path) // 1024
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M')
                    self.tree.insert('', tk.END, values=(
                        os.path.basename(file_path),
                        file_path,
                        f"{size_kb:,} KB",
                        mod_time
                    ))
                    self.file_list.append(file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not add {file_path}:\n{str(e)}")

    def remove_selected(self):
        """Remove selected files from the list"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No files selected to remove")
            return
            
        for item in selected_items:
            file_path = self.tree.item(item)['values'][1]
            self.file_list.remove(file_path)
            self.tree.delete(item)

    def clear_all(self):
        """Clear all files from the list"""
        if not self.file_list:
            return
            
        if messagebox.askyesno("Confirm", "Clear all files from the list?"):
            self.tree.delete(*self.tree.get_children())
            self.file_list.clear()

    def move_up(self):
        """Move selected file up in the list"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No file selected")
            return
            
        item = selected[0]
        prev_item = self.tree.prev(item)
        if prev_item:
            self.swap_items(item, prev_item)

    def move_down(self):
        """Move selected file down in the list"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No file selected")
            return
            
        item = selected[0]
        next_item = self.tree.next(item)
        if next_item:
            self.swap_items(item, next_item)

    def swap_items(self, item1, item2):
        """Swap two items in the Treeview"""
        data1 = self.tree.item(item1)['values']
        data2 = self.tree.item(item2)['values']
        self.tree.item(item1, values=data2)
        self.tree.item(item2, values=data1)
        idx1 = self.file_list.index(data1[1])
        idx2 = self.file_list.index(data2[1])
        self.file_list[idx1], self.file_list[idx2] = self.file_list[idx2], self.file_list[idx1]
        self.tree.selection_set(item1)

    def browse_output(self):
        """Select output PDF file location"""
        output_file = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=(("PDF Files", "*.pdf"),)
        )
        if output_file:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_file)

    def validate_pdf(self, file_path):
        """Check if file is a valid PDF"""
        try:
            with open(file_path, 'rb') as f:
                PdfReader(f)
            return True
        except Exception as e:
            print(f"Invalid PDF: {file_path} - {str(e)}")
            return False

    def start_merge(self):
        """Start merging PDFs in a background thread"""
        if not self.file_list:
            messagebox.showerror("Error", "No files selected for merging")
            return
        
        output_path = self.output_entry.get()
        if not output_path:
            messagebox.showerror("Error", "Please specify output file path")
            return

        # Disable UI during merge
        self.set_ui_state(disabled=True)
        self.progress['value'] = 0
        self.status_var.set("Starting merge...")
        
        # Run merge in separate thread
        threading.Thread(
            target=self.merge_pdfs,
            args=(self.file_list, output_path),
            daemon=True
        ).start()

    def merge_pdfs(self, input_paths, output_path):
        """Merge PDFs with progress updates"""
        pdf_merger = PdfMerger()
        processed_files = 0
        total_files = len(input_paths)

        try:
            # Create output directory if needed
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for i, file_path in enumerate(input_paths):
                # Update progress
                progress = int((i / total_files) * 100)
                self.root.after(0, self.update_progress, progress, f"Processing {os.path.basename(file_path)}... ({i+1}/{total_files})")
                
                if self.validate_pdf(file_path):
                    with open(file_path, 'rb') as f:
                        pdf_merger.append(f)
                    processed_files += 1

            if processed_files == 0:
                self.root.after(0, self.merge_complete, False, "No valid PDF files to merge")
                return

            with open(output_path, 'wb') as out:
                pdf_merger.write(out)

            self.root.after(0, self.merge_complete, True, 
                          f"Successfully merged {processed_files} PDFs!\nSaved to: {output_path}")

        except Exception as e:
            self.root.after(0, self.merge_complete, False, f"Error during merging:\n{str(e)}")
        finally:
            pdf_merger.close()

    def update_progress(self, value, status):
        """Update progress bar and status"""
        self.progress['value'] = value
        self.status_var.set(status)

    def merge_complete(self, success, message):
        """Handle merge completion"""
        self.set_ui_state(disabled=False)
        self.progress['value'] = 100 if success else 0
        self.status_var.set("Merge complete!" if success else "Merge failed")
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def set_ui_state(self, disabled):
        """Enable/disable UI elements"""
        state = tk.DISABLED if disabled else tk.NORMAL
        for child in self.root.winfo_children():
            try:
                child.configure(state=state)
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = LAMEUTE_PdfMerger(root)
    
    # Ensure window stays visible
    root.after(100, lambda: root.lift())
    root.after(200, lambda: root.focus_force())
    
    root.mainloop()