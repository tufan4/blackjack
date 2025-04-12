import tkinter as tk
from tkinter import messagebox, font as tkfont

class BlackjackMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BLACKJACK MASTER")
        self.root.geometry("400x700")
        self.configure_styles()
        
        # Oyun durumu
        self.running_count = 0
        self.true_count = 0.0
        self.used_cards = 0
        self.total_decks = 6
        self.cards_per_deck = 52
        self.min_cards_for_prediction = 4
        
        # Kart geçmişi
        self.history = []
        self.player_cards = []
        self.dealer_cards = []
        
        # Arayüz oluştur
        self.create_control_panel()
        self.create_display()
        self.create_card_buttons()
        self.create_prediction_panel()
        self.create_deck_settings()
    
    def configure_styles(self):
        self.colors = {
            "primary": "#2C3E50",
            "secondary": "#34495E",
            "accent": "#E74C3C",
            "text": "#ECF0F1",
            "warning": "#F39C12",
            "success": "#2ECC71",
            "background": "#1A1A1A"
        }
        
        self.big_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self.medium_font = tkfont.Font(family="Helvetica", size=14)
        self.small_font = tkfont.Font(family="Helvetica", size=12)
    
    def create_control_panel(self):
        control_frame = tk.Frame(self.root, bg=self.colors["secondary"])
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Geri alma butonu
        self.undo_btn = tk.Button(
            control_frame, text="↩ GERİ AL", 
            command=self.undo_last_card,
            bg=self.colors["warning"],
            fg=self.colors["text"],
            font=self.small_font
        )
        self.undo_btn.pack(side=tk.LEFT, padx=5)
        
        # Sıfırlama butonu
        self.reset_btn = tk.Button(
            control_frame, text="🔄 SIFIRLA", 
            command=self.reset_count,
            bg=self.colors["accent"],
            fg=self.colors["text"],
            font=self.small_font
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Deste modu butonu
        self.deck_mode_btn = tk.Button(
            control_frame, text="🔀 DESTE MODU", 
            command=self.toggle_deck_mode,
            bg="#3498DB",
            fg=self.colors["text"],
            font=self.small_font
        )
        self.deck_mode_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_display(self):
        display_frame = tk.Frame(self.root, bg=self.colors["background"])
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Running Count
        tk.Label(
            display_frame, 
            text="RUNNING COUNT:", 
            bg=self.colors["background"],
            fg=self.colors["text"],
            font=self.small_font
        ).pack(anchor=tk.W)
        
        self.running_count_label = tk.Label(
            display_frame, 
            text="0",
            bg=self.colors["background"],
            fg=self.colors["success"],
            font=self.big_font
        )
        self.running_count_label.pack(anchor=tk.W)
        
        # True Count ve deste bilgisi
        stats_frame = tk.Frame(display_frame, bg=self.colors["background"])
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.true_count_label = tk.Label(
            stats_frame, 
            text="TRUE COUNT: 0.00",
            bg=self.colors["background"],
            fg="#3498DB",
            font=self.medium_font
        )
        self.true_count_label.pack(side=tk.LEFT, padx=5)
        
        self.decks_left_label = tk.Label(
            stats_frame, 
            text="KALAN DESTE: 6.0",
            bg=self.colors["background"],
            fg="#9B59B6",
            font=self.medium_font
        )
        self.decks_left_label.pack(side=tk.RIGHT, padx=5)
    
    def create_card_buttons(self):
        # Yüksek kartlar (10/J/Q/K/A)
        high_frame = tk.Frame(self.root, bg=self.colors["background"])
        high_frame.pack(pady=5)
        
        high_cards = [
            ("10", "#E74C3C"), ("J", "#3498DB"), 
            ("Q", "#9B59B6"), ("K", "#2ECC71"), ("A", "#F39C12")
        ]
        
        for text, color in high_cards:
            btn = tk.Button(
                high_frame, 
                text=text, 
                command=lambda t=text: self.add_card(t, "high"),
                bg=color,
                fg=self.colors["text"],
                font=self.medium_font,
                width=6,
                height=2
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # Orta kartlar (7/8/9)
        mid_frame = tk.Frame(self.root, bg=self.colors["background"])
        mid_frame.pack(pady=5)
        
        for num in ["7", "8", "9"]:
            btn = tk.Button(
                mid_frame, 
                text=num, 
                command=lambda n=num: self.add_card(n, "mid"),
                bg="#7F8C8D",
                fg=self.colors["text"],
                font=self.medium_font,
                width=6,
                height=2
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # Düşük kartlar (2-6)
        low_frame = tk.Frame(self.root, bg=self.colors["background"])
        low_frame.pack(pady=5)
        
        for num in ["2", "3", "4", "5", "6"]:
            btn = tk.Button(
                low_frame, 
                text=num, 
                command=lambda n=num: self.add_card(n, "low"),
                bg="#34495E",
                fg=self.colors["text"],
                font=self.medium_font,
                width=6,
                height=2
            )
            btn.pack(side=tk.LEFT, padx=3)
    
    def create_prediction_panel(self):
        prediction_frame = tk.Frame(
            self.root, 
            bg=self.colors["secondary"],
            padx=10,
            pady=10
        )
        prediction_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            prediction_frame, 
            text="TAHMİN VE STRATEJİ", 
            bg=self.colors["secondary"],
            fg=self.colors["text"],
            font=self.small_font
        ).pack(anchor=tk.W)
        
        self.prediction_label = tk.Label(
            prediction_frame, 
            text="En az 4 kart giriniz",
            bg=self.colors["secondary"],
            fg="#3498DB",
            font=self.medium_font
        )
        self.prediction_label.pack(anchor=tk.W)
        
        self.strategy_label = tk.Label(
            prediction_frame, 
            text="Öneri: -",
            bg=self.colors["secondary"],
            fg="#2ECC71",
            font=self.medium_font
        )
        self.strategy_label.pack(anchor=tk.W)
    
    def create_deck_settings(self):
        settings_frame = tk.Frame(
            self.root, 
            bg=self.colors["primary"],
            padx=10,
            pady=10
        )
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            settings_frame, 
            text="DESTE AYARLARI:", 
            bg=self.colors["primary"],
            fg=self.colors["text"],
            font=self.small_font
        ).pack(anchor=tk.W)
        
        entry_frame = tk.Frame(settings_frame, bg=self.colors["primary"])
        entry_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            entry_frame, 
            text="Kalan Deste:", 
            bg=self.colors["primary"],
            fg=self.colors["text"],
            font=self.small_font
        ).pack(side=tk.LEFT)
        
        self.deck_entry = tk.Entry(entry_frame, width=5)
        self.deck_entry.insert(0, "3.0")
        self.deck_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            entry_frame, 
            text="Uygula", 
            command=self.update_deck_setting,
            bg=self.colors["accent"],
            fg=self.colors["text"],
            font=self.small_font
        ).pack(side=tk.LEFT)
    
    def add_card(self, card, card_type):
        # Hi-Lo değerini belirle
        if card_type == "high":
            value = -1
        elif card_type == "low":
            value = +1
        else:  # mid
            value = 0
        
        # Güncellemeler
        self.running_count += value
        self.used_cards += 1
        self.history.append((card, value))
        
        self.update_display()
        self.update_predictions()
    
    def update_display(self):
        # Kalan deste hesapla
        remaining_decks = max(
            (self.total_decks * self.cards_per_deck - self.used_cards) / self.cards_per_deck, 
            0.1
        )
        
        # True Count hesapla
        self.true_count = self.running_count / remaining_decks
        
        # Arayüzü güncelle
        self.running_count_label.config(text=str(self.running_count))
        self.true_count_label.config(text=f"TRUE COUNT: {self.true_count:.2f}")
        self.decks_left_label.config(text=f"KALAN DESTE: {remaining_decks:.1f}")
        
        # Renk kodlama
        if self.true_count >= 2:
            self.running_count_label.config(fg="#2ECC71")  # Yeşil
        elif self.true_count <= -1:
            self.running_count_label.config(fg="#E74C3C")  # Kırmızı
        else:
            self.running_count_label.config(fg="#F39C12")  # Sarı
    
    def update_predictions(self):
        if self.used_cards < self.min_cards_for_prediction:
            self.prediction_label.config(
                text=f"En az {self.min_cards_for_prediction} kart giriniz",
                fg="#3498DB"
            )
            self.strategy_label.config(text="Öneri: -", fg="#2ECC71")
            return
        
        # Gelişmiş tahmin algoritması
        if self.true_count >= 3:
            prediction = "Yüksek kart olasılığı ÇOK YÜKSEK (10/J/Q/K/A)"
            strategy = "STAND (Kal)" if self.running_count >= 4 else "HIT (Çek)"
        elif self.true_count >= 1.5:
            prediction = "Yüksek kart olasılığı YÜKSEK"
            strategy = "STAND" if self.running_count >= 2 else "HIT"
        elif self.true_count <= -2:
            prediction = "Düşük kart olasılığı YÜKSEK (2-6)"
            strategy = "HIT (Çek)"
        elif self.true_count <= -1:
            prediction = "Düşük kart olasılığı ORTA"
            strategy = "HIT (Çek)"
        else:
            prediction = "Belirsiz (Temel stratejiyi uygula)"
            strategy = "Temel Strateji"
        
        self.prediction_label.config(text=prediction, fg="#3498DB")
        self.strategy_label.config(text=f"Öneri: {strategy}", fg="#2ECC71")
    
    def undo_last_card(self):
        if self.history:
            card, value = self.history.pop()
            self.running_count -= value
            self.used_cards -= 1
            self.update_display()
            self.update_predictions()
        else:
            messagebox.showwarning("Uyarı", "Geri alınacak kart yok!")
    
    def reset_count(self):
        self.running_count = 0
        self.used_cards = 0
        self.history = []
        self.update_display()
        self.update_predictions()
        messagebox.showinfo("Bilgi", "Sayım sıfırlandı!")
    
    def toggle_deck_mode(self):
        current_mode = self.deck_mode_btn.cget("text")
        if "YARIDAN" in current_mode:
            self.deck_mode_btn.config(text="🔀 TAM DESTE")
            self.total_decks = 6
        else:
            self.deck_mode_btn.config(text="🔀 YARIDAN")
            self.total_decks = 3
        
        self.update_display()
        self.update_predictions()
    
    def update_deck_setting(self):
        try:
            remaining = float(self.deck_entry.get())
            if 0.5 <= remaining <= 6:
                self.total_decks = remaining * 2 if "YARIDAN" in self.deck_mode_btn.cget("text") else 6
                messagebox.showinfo("Başarılı", f"Deste ayarı güncellendi: {remaining:.1f}")
            else:
                messagebox.showerror("Hata", "0.5-6 arası değer girin!")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz değer! Örnek: 3.5")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackMasterApp(root)
    root.mainloop()