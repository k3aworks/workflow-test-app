import tkinter as tk
from tkinter import ttk

import webbrowser
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
    main_frame.rowconfigure(2, weight=0)

    # Row 0: label, entry, search button
    occupation_label = ttk.Label(main_frame, text="Occupation:")
    occupation_label.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky="w")

    occupation_var = tk.StringVar()
    occupation_entry = ttk.Entry(main_frame, textvariable=occupation_var, width=40)
    occupation_entry.grid(row=0, column=1, padx=(0, 5), pady=(0, 5), sticky="ew")

    search_results_with_urls = []

    def on_search_clicked() -> None:
        """Handle Search button click using the dummy backend from Sub 1.3."""

        query = occupation_var.get()
        try:
            results = wiki_backend.search_occupation_with_urls(query)
        except Exception:
            results = []

        search_results_with_urls.clear()
        search_results_with_urls.extend(results)

        results_listbox.delete(0, tk.END)
        for item in results:
            title = item.get("title")
            if isinstance(title, str):
                results_listbox.insert(tk.END, title)

    def on_result_double_click(event: tk.Event) -> None:
        """Open the Wikipedia page for the selected result in a browser."""

        if not results_listbox.curselection():
            return

        index = results_listbox.curselection()[0]
        if not (0 <= index < len(search_results_with_urls)):
            return

        url = search_results_with_urls[index].get("url")
        if isinstance(url, str) and url:
            webbrowser.open(url)

    search_button = ttk.Button(main_frame, text="Search", command=on_search_clicked)
    search_button.grid(row=0, column=2, pady=(0, 5), sticky="ew")

    # Row 1: results listbox with scrollbar
    results_frame = ttk.Frame(main_frame)
    results_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

    results_frame.rowconfigure(0, weight=1)
    results_frame.columnconfigure(0, weight=1)

    results_listbox = tk.Listbox(results_frame, height=10)
    results_listbox.grid(row=0, column=0, sticky="nsew")
    results_listbox.bind("<Double-Button-1>", on_result_double_click)

    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_listbox.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    results_listbox.configure(yscrollcommand=scrollbar.set)

    info_frame = ttk.Frame(main_frame, padding=(0, 10, 0, 0))
    info_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

    info_frame.columnconfigure(1, weight=1)

    name_label = ttk.Label(info_frame, text="Name:")
    name_label.grid(row=0, column=0, padx=(0, 5), sticky="w")
    name_value_label = ttk.Label(info_frame, text="")
    name_value_label.grid(row=0, column=1, sticky="w")

    nationality_label = ttk.Label(info_frame, text="Nationality:")
    nationality_label.grid(row=1, column=0, padx=(0, 5), sticky="w")
    nationality_value_label = ttk.Label(info_frame, text="")
    nationality_value_label.grid(row=1, column=1, sticky="w")

    birth_year_label = ttk.Label(info_frame, text="Birth Year:")
    birth_year_label.grid(row=2, column=0, padx=(0, 5), sticky="w")
    birth_year_value_label = ttk.Label(info_frame, text="")
    birth_year_value_label.grid(row=2, column=1, sticky="w")

    def update_info_panel_from_index(index: int) -> None:
        if not (0 <= index < len(search_results_with_urls)):
            name_value_label.config(text="")
            nationality_value_label.config(text="")
            birth_year_value_label.config(text="")
            return

        entry = search_results_with_urls[index]
        title = entry.get("title")
        if isinstance(title, str) and title.strip():
            title_text = title.strip()
            name_value_label.config(text=title_text)
        else:
            name_value_label.config(text="Unknown")
            nationality_value_label.config(text="Unknown")
            birth_year_value_label.config(text="Unknown")
            return

        try:
            nationality = wiki_backend.fetch_nationality(title)
        except Exception:
            nationality = None

        try:
            birth_year = wiki_backend.fetch_birth_year(title)
        except Exception:
            birth_year = None

        nationality_value_label.config(text=nationality if nationality else "Unknown")
        birth_year_value_label.config(
            text=str(birth_year) if isinstance(birth_year, int) else "Unknown"
        )

    def on_result_select(event: tk.Event) -> None:
        if not results_listbox.curselection():
            update_info_panel_from_index(-1)
            return

        index = results_listbox.curselection()[0]
        update_info_panel_from_index(index)

    results_listbox.bind("<<ListboxSelect>>", on_result_select)

    return root


def main() -> None:
    """Entry point for running the GUI locally."""

    root = create_app()
    root.mainloop()


if __name__ == "__main__":
    main()
