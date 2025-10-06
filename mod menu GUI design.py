import tkinter as tk
from tkinter import ttk
import random

class CompactModMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry("300x400")
        self.root.configure(bg='#0a0a0a')
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Always on top
        
        # Position in top-right corner
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"+{screen_width-320}+20")
        
        # Variables for toggles
        self.toggle_vars = {}
        self.is_visible = True  # Start visible
        
        self.setup_gui()
        self.setup_hotkey()
        
    def setup_gui(self):
        # Main container with subtle border
        main_frame = tk.Frame(self.root, bg='#1a1a1a', relief='ridge', bd=1)
        main_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Header - compact
        header_frame = tk.Frame(main_frame, bg='#2a2a2a', height=30)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🔥 PHANTOM", 
                              font=('Consolas', 10, 'bold'), 
                              fg='#00ff00', 
                              bg='#2a2a2a')
        title_label.pack(side='left', padx=8, pady=6)
        
        # Close button
        close_btn = tk.Label(header_frame, text="✕", 
                            font=('Consolas', 10, 'bold'),
                            fg='#ff4444', bg='#2a2a2a',
                            cursor='hand2')
        close_btn.pack(side='right', padx=8, pady=6)
        close_btn.bind('<Button-1>', lambda e: self.toggle_visibility())
        
        # Make header draggable
        header_frame.bind('<Button-1>', self.start_move)
        header_frame.bind('<B1-Motion>', self.on_move)
        title_label.bind('<Button-1>', self.start_move)
        title_label.bind('<B1-Motion>', self.on_move)
        
        # Scrollable content area
        canvas = tk.Canvas(main_frame, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#1a1a1a')
        
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True, padx=(0, 2))
        scrollbar.pack(side='right', fill='y', padx=(0, 2))
        
        # Bind mouse wheel to scroll
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))
        self.scrollable_frame.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))
        
        # Create mod sections
        self.create_mod_sections()
        
    def create_mod_sections(self):
        # Aimbot Section
        self.create_section("AIMBOT", [
            ("Aimbot", "#ff4444"),
            ("Silent Aim", "#ff6666"),
            ("Trigger Bot", "#ff8888"),
            ("FOV: 30°", "#ffaaaa"),
            ("Smooth: 50%", "#ffcccc")
        ])
        
        # Visuals Section
        self.create_section("VISUALS", [
            ("Wallhack", "#44ff44"),
            ("ESP Boxes", "#66ff66"),
            ("Chams", "#88ff88"),
            ("No Fog", "#aaffaa"),
            ("Bright Skies", "#ccffcc")
        ])
        
        # Player Section
        self.create_section("PLAYER", [
            ("Speed Hack", "#4444ff"),
            ("No Recoil", "#6666ff"),
            ("Rapid Fire", "#8888ff"),
            ("God Mode", "#aaaaff"),
            ("Super Jump", "#ccccff")
        ])
        
        # Weapon Section
        self.create_section("WEAPON", [
            ("Magic Bullet", "#ff44ff"),
            ("Infinite Ammo", "#ff66ff"),
            ("No Spread", "#ff88ff"),
            ("Fast Reload", "#ffaaff"),
            ("Damage Multi", "#ffccff")
        ])
        
        # Misc Section
        self.create_section("MISC", [
            ("Unlock All", "#ffff44"),
            ("Radar Hack", "#ffff66"),
            ("XP Boost", "#ffff88"),
            ("Anti-Kick", "#ffffaa"),
            ("Stream Proof", "#ffffcc")
        ])
        
    def create_section(self, title, options):
        """Create a compact section"""
        section_frame = tk.Frame(self.scrollable_frame, bg='#151515', relief='flat')
        section_frame.pack(fill='x', padx=8, pady=4)
        
        # Section title
        title_label = tk.Label(section_frame, text=title, 
                              font=('Consolas', 9, 'bold'),
                              fg='#ffffff', bg='#252525')
        title_label.pack(fill='x', padx=2, pady=(4, 2))
        
        # Options grid (2 columns)
        options_frame = tk.Frame(section_frame, bg='#151515')
        options_frame.pack(fill='x', padx=2, pady=2)
        
        for i, (text, color) in enumerate(options):
            row = i // 2
            col = i % 2
            
            var = tk.BooleanVar()
            self.toggle_vars[text] = var
            
            toggle_frame = tk.Frame(options_frame, bg='#151515')
            toggle_frame.grid(row=row, column=col, sticky='ew', padx=1, pady=1)
            
            options_frame.columnconfigure(col, weight=1)
            
            # Compact toggle switch
            self.create_compact_toggle(toggle_frame, text, var, color)
    
    def create_compact_toggle(self, parent, text, var, color):
        """Create ultra-compact toggle switch"""
        switch_frame = tk.Frame(parent, bg='#151515')
        switch_frame.pack(fill='x', padx=2, pady=1)
        
        # Mini toggle canvas
        canvas = tk.Canvas(switch_frame, width=40, height=18, bg='#151515', 
                          highlightthickness=0, relief='flat')
        canvas.pack(side='left', padx=(0, 6))
        
        # Text label
        label = tk.Label(switch_frame, text=text, 
                        font=('Consolas', 7), 
                        fg='#cccccc', bg='#151515',
                        anchor='w')
        label.pack(side='left', fill='x', expand=True)
        
        # Draw initial toggle state
        self.draw_compact_toggle(canvas, var.get(), color)
        
        # Bind click events
        canvas.bind('<Button-1>', lambda e, v=var, c=color, cv=canvas: self.toggle_switch(v, c, cv))
        label.bind('<Button-1>', lambda e, v=var, c=color, cv=canvas: self.toggle_switch(v, c, cv))
        switch_frame.bind('<Button-1>', lambda e, v=var, c=color, cv=canvas: self.toggle_switch(v, c, cv))
    
    def draw_compact_toggle(self, canvas, state, color):
        """Draw compact toggle switch"""
        canvas.delete("all")
        
        if state:
            # ON state - filled
            canvas.create_rectangle(2, 2, 38, 16, fill=color, outline='#333333', width=1)
            canvas.create_oval(24, 4, 36, 14, fill='#ffffff', outline='#333333', width=1)
            canvas.create_text(12, 9, text="✓", fill='#000000', font=('Consolas', 8, 'bold'))
        else:
            # OFF state - minimal
            canvas.create_rectangle(2, 2, 38, 16, fill='#252525', outline='#444444', width=1)
            canvas.create_oval(4, 4, 16, 14, fill='#666666', outline='#444444', width=1)
            canvas.create_text(28, 9, text="✗", fill='#888888', font=('Consolas', 8))
    
    def toggle_switch(self, var, color, canvas):
        """Toggle switch with smooth animation"""
        var.set(not var.get())
        self.draw_compact_toggle(canvas, var.get(), color)
        
        # Visual feedback
        self.animate_toggle(canvas)
    
    def animate_toggle(self, canvas):
        """Add a quick animation effect"""
        original_bg = canvas.cget('bg')
        canvas.configure(bg='#333333')
        canvas.after(50, lambda: canvas.configure(bg=original_bg))
    
    def start_move(self, event):
        """Start window move"""
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        """Move window"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def setup_hotkey(self):
        """Setup global hotkey detection"""
        # Bind to the root window and all its children
        self.root.bind('<Control-Shift-Alt_L>', self.toggle_visibility)
        self.root.bind('<Control-Shift-Alt_R>', self.toggle_visibility)
        
        # Make sure window can receive focus for hotkeys
        self.root.focus_force()
        
        print("🔥 Phantom Mod Menu - Ctrl+Shift+Alt to toggle visibility")
    
    def toggle_visibility(self, event=None):
        """Toggle menu visibility"""
        if self.is_visible:
            self.hide_menu()
        else:
            self.show_menu()
        
        self.is_visible = not self.is_visible
    
    def hide_menu(self):
        """Hide the menu"""
        self.root.withdraw()
    
    def show_menu(self):
        """Show the menu"""
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.focus_force()

def main():
    root = tk.Tk()
    
    # Set minimal window style
    style = ttk.Style()
    style.theme_use('clam')
    
    app = CompactModMenu(root)
    
    print("🔥 Phantom Mod Menu loaded!")
    print("Menu starts VISIBLE - Press Ctrl+Shift+Alt to hide/show")
    print("Drag the header to move the menu around")
    
    root.mainloop()

if __name__ == "__main__":
    main()
