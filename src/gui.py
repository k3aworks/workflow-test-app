import tkinter as tk
from tkinter import ttk

import wiki_backend


def create_app() -> tk.Tk:
    """Create the main Tkinter window for occupation search.

    Layout requirements for Sub 1.2:
    - Basic window
    - Input field for occupation
    - "Search" button
    - Empty list box for results (with vertical scrollbar)
    """

    root = tk.Tk()
    root.title("Occupation search")

    # Allow the main frame to resize with the window
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=0, sticky="nsew")

    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)

    # Row 0: label, entry, search button
    occupation_label = ttk.Label(main_frame, text="Occupation:")
    occupation_label.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky="w")

    occupation_var = tk.StringVar()
    occupation_entry = ttk.Entry(main_frame, textvariable=occupation_var, width=40)
    occupation_entry.grid(row=0, column=1, padx=(0, 5), pady=(0, 5), sticky="ew")

    def on_search_clicked() -> None:
        """Handle Search button click using the dummy backend from Sub 1.3."""

        occupation = occupation_var.get()
        results = wiki_backend.search_occupation(occupation)

        # Replace list contents with the dummy results from the backend.
        results_listbox.delete(0, tk.END)
        for name in results:
            results_listbox.insert(tk.END, name)

    search_button = ttk.Button(main_frame, text="Search", command=on_search_clicked)
    search_button.grid(row=0, column=2, pady=(0, 5), sticky="ew")

    # Row 1: results listbox with scrollbar
    results_frame = ttk.Frame(main_frame)
    results_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

    results_frame.rowconfigure(0, weight=1)
    results_frame.columnconfigure(0, weight=1)

    results_listbox = tk.Listbox(results_frame, height=10)
    results_listbox.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_listbox.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    results_listbox.configure(yscrollcommand=scrollbar.set)

    return root


def main() -> None:
    """Entry point for running the GUI locally."""

    root = create_app()
    root.mainloop()


if __name__ == "__main__":
    main()
