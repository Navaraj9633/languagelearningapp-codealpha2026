import customtkinter as ctk
import tkinter as tk 
from json_handler import load_flashcards, save_flashcards # pyright: ignore[reportMissingImports]
import tkinter.messagebox as messagebox

# ----------------------------------------------------------------------
# 1. CARD MANAGER WINDOW CLASS (CRUD Functionality)
# ----------------------------------------------------------------------

class CardManagerWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Manage Flashcards (CRUD)")
        self.geometry("700x500")
        
        self.main_app = master
        self.cards = self.main_app.flashcards
        self.selected_card_index = -1

        self.create_widgets()
        self.update_card_list_view()

    def create_widgets(self):
        # Main Layout: Two frames (List on Left, Input on Right)
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(side="left", fill="both", padx=10, pady=10, expand=True)
        
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # --- List Frame Content ---
        ctk.CTkLabel(list_frame, text="Current Flashcards", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        # Standard Tkinter Listbox with refined colors for better dark theme integration
        self.card_listbox = tk.Listbox(list_frame, 
                                        width=40, 
                                        height=18, 
                                        bg="#343638",            # Dark background color
                                        fg="white",              # White text
                                        selectbackground="#1f538d", # Blue selection color
                                        selectforeground="white", 
                                        font=("Arial", 12))
        self.card_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        self.card_listbox.bind('<<ListboxSelect>>', self.load_selected_card)
        
        ctk.CTkButton(list_frame, text="Delete Selected Card", fg_color="red", hover_color="#900", command=self.delete_card).pack(pady=10, fill="x", padx=10)

        # --- Input Frame Content ---
        ctk.CTkLabel(input_frame, text="Question:").pack(pady=(10, 0))
        self.question_entry = ctk.CTkEntry(input_frame, width=300)
        self.question_entry.pack(pady=5)

        ctk.CTkLabel(input_frame, text="Answer:").pack(pady=(10, 0))
        self.answer_entry = ctk.CTkEntry(input_frame, width=300)
        self.answer_entry.pack(pady=5)
        
        ctk.CTkButton(input_frame, text="Add New Card", command=self.add_card).pack(pady=(20, 5))
        ctk.CTkButton(input_frame, text="Update Selected Card", command=self.edit_card).pack(pady=5)
        ctk.CTkButton(input_frame, text="Clear Fields", command=self.clear_fields).pack(pady=5)

    def clear_fields(self):
        """Clears the Q and A input fields."""
        self.question_entry.delete(0, ctk.END)
        self.answer_entry.delete(0, ctk.END)
        self.selected_card_index = -1
        self.card_listbox.selection_clear(0, tk.END)


    def update_card_list_view(self):
        """Refreshes the listbox to show the current flashcards."""
        self.card_listbox.delete(0, tk.END)
        for i, card in enumerate(self.cards):
            display_text = card['question'].replace('\n', ' ')
            self.card_listbox.insert(tk.END, f"{i+1}. {display_text[:40]}...")


    def load_selected_card(self, event):
        """Loads the selected card's data into the entry fields for editing."""
        selected_indices = self.card_listbox.curselection()
        if not selected_indices:
            self.selected_card_index = -1
            return

        self.selected_card_index = selected_indices[0]
        card = self.cards[self.selected_card_index]
        
        self.question_entry.delete(0, ctk.END)
        self.answer_entry.delete(0, ctk.END)
        self.question_entry.insert(0, card['question'])
        self.answer_entry.insert(0, card['answer'])
            
    # --- CRUD LOGIC ---

    def add_card(self):
        """Adds a new card to the list and saves."""
        q = self.question_entry.get().strip()
        a = self.answer_entry.get().strip()
        
        if q and a:
            self.cards.append({"question": q, "answer": a})
            save_flashcards(self.cards)
            self.update_card_list_view()
            self.clear_fields()
            self.main_app.update_card_display() 
            messagebox.showinfo("Success", "New card added and saved!")
        else:
            messagebox.showerror("Error", "Question and Answer cannot be empty.")

    def edit_card(self):
        """Updates the selected card with new values and saves."""
        if self.selected_card_index != -1:
            q = self.question_entry.get().strip()
            a = self.answer_entry.get().strip()

            if q and a:
                self.cards[self.selected_card_index] = {"question": q, "answer": a}
                save_flashcards(self.cards)
                self.update_card_list_view()
                
                if self.selected_card_index == self.main_app.current_card_index:
                    self.main_app.update_card_display()
                messagebox.showinfo("Success", f"Card updated and saved!")
            else:
                messagebox.showerror("Error", "Question and Answer cannot be empty.")
        else:
            messagebox.showerror("Error", "Please select a card to edit.")

    def delete_card(self):
        """Deletes the selected card and saves."""
        if self.selected_card_index != -1:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this card?"):
                del self.cards[self.selected_card_index]
                save_flashcards(self.cards)
                
                if self.main_app.current_card_index >= len(self.cards) and len(self.cards) > 0:
                    self.main_app.current_card_index = 0
                elif len(self.cards) == 0:
                     self.main_app.current_card_index = 0

                self.selected_card_index = -1
                self.update_card_list_view()
                self.clear_fields()
                self.main_app.update_card_display()
                messagebox.showinfo("Success", "Card deleted and saved!")
        else:
            messagebox.showerror("Error", "Please select a card to delete.")


# ----------------------------------------------------------------------
# 2. FLASHCARD APP CLASS (Main Window)
# ----------------------------------------------------------------------

class FlashcardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- App Setup ---
        self.title("Flashcard Quiz App")
        self.geometry("600x400")
        
        # --- Data Initialization ---
        self.flashcards = load_flashcards()
        self.current_card_index = 0
        self.showing_question = True
        
        if not self.flashcards:
            self.flashcards.append({"question": "Welcome! Please use the 'Manage Cards' button.", 
                                    "answer": "This is the answer."})

        self.create_widgets()
        self.update_card_display() 

    def create_widgets(self):
        # 1. Main Display Frame
        self.card_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.card_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # 2. Card Display Label
        self.card_text = ctk.CTkLabel(self.card_frame, 
                                      text="", 
                                      font=ctk.CTkFont(size=24, weight="bold"),
                                      wraplength=500,
                                      justify="center")
        self.card_text.pack(fill="both", expand=True)

        # 3. Control Frame for Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10, padx=20)

        # 4. Buttons (Next, Previous, Show Answer)
        ctk.CTkButton(self.button_frame, text="< Previous", command=self.prev_card).pack(side="left", padx=10)
        
        self.answer_button = ctk.CTkButton(self.button_frame, 
                                           text="Show Answer", 
                                           command=self.toggle_answer)
        self.answer_button.pack(side="left", padx=20)
        
        ctk.CTkButton(self.button_frame, text="Next >", command=self.next_card).pack(side="left", padx=10)

        # 5. Manage Cards Button (Opens CRUD window)
        ctk.CTkButton(self, text="Manage Cards (CRUD)", command=self.open_manager_window).pack(pady=10)

        # 6. Appearance Mode Switch (New UI Feature)
        self.appearance_mode_label = ctk.CTkLabel(self.button_frame, text="Appearance:", fg_color="transparent")
        self.appearance_mode_label.pack(side="left", padx=(40, 5))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.button_frame, 
                                                            values=["System", "Dark", "Light"],
                                                            command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.set("System") # Default setting
        self.appearance_mode_optionemenu.pack(side="left")


    def update_card_display(self):
        """Displays the question or answer of the current card."""
        if not self.flashcards:
            self.card_text.configure(text="No cards available. Add new cards via 'Manage Cards'.")
            self.answer_button.configure(text="No Card")
            return
            
        if self.current_card_index >= len(self.flashcards):
            self.current_card_index = 0

        card = self.flashcards[self.current_card_index]
        
        if self.showing_question:
            self.card_text.configure(text=card["question"])
            self.answer_button.configure(text="Show Answer")
        else:
            self.card_text.configure(text=card["answer"])
            self.answer_button.configure(text="Show Question")


    def toggle_answer(self):
        """Switches between showing the question and the answer."""
        self.showing_question = not self.showing_question
        self.update_card_display()


    def next_card(self):
        """Moves to the next card, wrapping around."""
        if not self.flashcards: return
        self.showing_question = True 
        self.current_card_index = (self.current_card_index + 1) % len(self.flashcards)
        self.update_card_display()


    def prev_card(self):
        """Moves to the previous card, wrapping around."""
        if not self.flashcards: return
        self.showing_question = True
        self.current_card_index = (self.current_card_index - 1) % len(self.flashcards)
        self.update_card_display()
        
    def open_manager_window(self):
        """Opens the Card Manager Window."""
        CardManagerWindow(self)

    # --- New UI Feature Method ---
    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Allows user to switch between light, dark, and system themes."""
        ctk.set_appearance_mode(new_appearance_mode)


# ----------------------------------------------------------------------
# 3. EXECUTION BLOCK (Starts the application)
# ----------------------------------------------------------------------

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()