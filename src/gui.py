import tkinter as tk
from tkinter import ttk


def run() -> None:
    """Start the basic occupation search GUI.

    Sub 1.2 scope:
    - Window
    - Occupation entry field
    - Search button
    - Empty results list box
    """
    root = tk.Tk()
    root.title("Occupation Search")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill="both", expand=True)

    # Row 0: label, entry, search button
    occupation_label = ttk.Label(main_frame, text="Occupation:")
    occupation_label.grid(row=0, column=0, sticky="w")

    occupation_var = tk.StringVar()
    occupation_entry = ttk.Entry(main_frame, textvariable=occupation_var, width=40)
    occupation_entry.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    search_button = ttk.Button(main_frame, text="Search")
    search_button.grid(row=0, column=2, padx=(5, 0))

    # Row 1: empty results list box
    results_listbox = tk.Listbox(main_frame, height=10)
    results_listbox.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="nsew")

    # Make the layout responsive
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    run()
