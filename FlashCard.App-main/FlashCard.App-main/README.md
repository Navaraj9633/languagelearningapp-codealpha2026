# 📚 Python Flashcard Quiz App

**Project Status:** Completed (Code Alpha Virtual Internship - Task 1)

This project is a desktop Flashcard Quiz application designed for studying, built using Python and the modern GUI library, `customtkinter`. It fulfills the requirements for Code Alpha's App Development Internship Task 1.

## ✨ Features

The application provides a comprehensive solution for managing and reviewing flashcards:

* **Quiz Mode:** Navigate between cards using **Next** and **Previous** buttons.
* **Study Mode:** Toggle between the **Question** (front) and the **Answer** (back) using a "Show Answer" button.
* **CRUD Manager:** A dedicated window allows users to **Add, Edit, and Delete** flashcards (full CRUD functionality).
* **Data Persistence:** Flashcard data is stored and loaded from a **JSON file** (`flashcards.json`) using a custom `json_handler.py` module.
* **Modern UI:** Features a simple, clean, and customizable interface with an **Appearance Mode Switch** (Light/Dark/System Theme).

## 💻 Tech Stack

* **Language:** Python 3.x
* **GUI Library:** `customtkinter` (for modern look and themes)
* **Data Handling:** `json`
* **Utility:** `tkinter` (used specifically for the Listbox in the manager window)

## 🚀 Installation and Setup

### Prerequisites

You need Python 3.x installed on your system.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourUsername/RepoName.git](https://github.com/YourUsername/RepoName.git)
    cd RepoName
    ```

2.  **Install Dependencies:**
    ```bash
    pip install customtkinter
    ```
    *(Note: This project does not require the `pandas` or `numpy` libraries seen in some terminal outputs).*

3.  **Run the Application:**
    ```bash
    python main_app.py
    ```

---
**Completed as part of the Code Alpha Virtual Internship Program.**
