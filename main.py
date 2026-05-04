import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class MovieLibrary:
    """Класс для управления библиотекой фильмов"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Library")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.movies = []
        self.filename = "movies.json"

        self.create_widgets()
        self.load_movies()

    def create_widgets(self):
        """Создание элементов интерфейса"""

        # Заголовок
        title_label = tk.Label(
            self.root,
            text="🎬 Movie Library",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#1a1a2e"
        )
        title_label.pack(pady=15)

        # Фрейм для ввода данных
        input_frame = tk.LabelFrame(
            self.root,
            text="Добавить новый фильм",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        input_frame.pack(fill="x", padx=20, pady=10)

        # Название
        tk.Label(input_frame, text="Название:", bg="#ffffff",
                 font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5)
        self.entry_title = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.entry_title.grid(row=0, column=1, padx=10, pady=5)

        # Жанр
        tk.Label(input_frame, text="Жанр:", bg="#ffffff",
                 font=("Arial", 10)).grid(row=0, column=2, sticky="e", pady=5)
        self.entry_genre = tk.Entry(input_frame, width=20, font=("Arial", 10))
        self.entry_genre.grid(row=0, column=3, padx=10, pady=5)

        # Год
        tk.Label(input_frame, text="Год:", bg="#ffffff",
                 font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5)
        self.entry_year = tk.Entry(input_frame, width=10, font=("Arial", 10))
        self.entry_year.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Рейтинг
        tk.Label(input_frame, text="Рейтинг (0-10):", bg="#ffffff",
                 font=("Arial", 10)).grid(row=1, column=2, sticky="e", pady=5)
        self.entry_rating = tk.Entry(input_frame, width=10, font=("Arial", 10))
        self.entry_rating.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        # Кнопка добавления
        btn_add = tk.Button(
            input_frame,
            text="➕ Добавить фильм",
            command=self.add_movie,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2
        )
        btn_add.grid(row=2, column=0, columnspan=4, pady=10)

        # Фрейм для фильтрации
        filter_frame = tk.LabelFrame(
            self.root,
            text="Фильтрация",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=10
        )
        filter_frame.pack(fill="x", padx=20, pady=10)

        # Фильтр по жанру
        tk.Label(filter_frame, text="Жанр:", bg="#ffffff",
                 font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.filter_genre = tk.Entry(filter_frame, width=15, font=("Arial", 10))
        self.filter_genre.grid(row=0, column=1, padx=5)
        self.filter_genre.insert(0, "Все")

        # Фильтр по году
        tk.Label(filter_frame, text="Год:", bg="#ffffff",
                 font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.filter_year = tk.Entry(filter_frame, width=10, font=("Arial", 10))
        self.filter_year.grid(row=0, column=3, padx=5)
        self.filter_year.insert(0, "Все")

        # Кнопки фильтрации
        btn_filter = tk.Button(
            filter_frame,
            text="🔍 Применить",
            command=self.apply_filter,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_filter.grid(row=0, column=4, padx=10)

        btn_reset = tk.Button(
            filter_frame,
            text="🔄 Сбросить",
            command=self.reset_filter,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_reset.grid(row=0, column=5, padx=10)

        # Таблица фильмов (Treeview)
        table_frame = tk.Frame(self.root, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        # Настройка заголовков
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")

        # Настройка ширины колонок
        self.tree.column("title", width=300)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=80)
        self.tree.column("rating", width=80)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        btn_delete = tk.Button(
            btn_frame,
            text="🗑️ Удалить выбранный",
            command=self.delete_movie,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_delete.pack(side="left", padx=5)

        btn_save = tk.Button(
            btn_frame,
            text="💾 Сохранить",
            command=self.save_movies,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_save.pack(side="left", padx=5)

        # Статус бар
        self.status_label = tk.Label(
            self.root,
            text=f"Всего фильмов: 0",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="white",
            pady=5
        )
        self.status_label.pack(fill="x", side="bottom")

    def validate_input(self, title, genre, year, rating):
        """Проверка корректности ввода"""

        # Проверка названия
        if not title.strip():
            messagebox.showerror("Ошибка", "Введите название фильма!")
            return False

        # Проверка жанра
        if not genre.strip():
            messagebox.showerror("Ошибка", "Введите жанр!")
            return False

        # Проверка года (должен быть числом)
        try:
            year_int = int(year)
            if year_int < 1888 or year_int > 2026:
                messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2026!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return False

        # Проверка рейтинга (от 0 до 10)
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return False

        return True

    def add_movie(self):
        """Добавление нового фильма"""

        title = self.entry_title.get()
        genre = self.entry_genre.get()
        year = self.entry_year.get()
        rating = self.entry_rating.get()

        # Валидация ввода
        if not self.validate_input(title, genre, year, rating):
            return

        # Создание словаря фильма
        movie = {
            "title": title.strip(),
            "genre": genre.strip(),
            "year": int(year),
            "rating": float(rating)
        }

        # Добавление в список
        self.movies.append(movie)

        # Обновление таблицы
        self.update_table()

        # Сохранение в файл
        self.save_movies()

        # Очистка полей
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")

    def delete_movie(self):
        """Удаление выбранного фильма"""

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите фильм для удаления!")
            return

        # Получение индекса
        index = self.tree.index(selected[0])

        # Подтверждение удаления
        movie = self.movies[index]
        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Удалить фильм '{movie['title']}'?"
        )

        if confirm:
            self.movies.pop(index)
            self.update_table()
            self.save_movies()
            messagebox.showinfo("Успех", "Фильм удалён!")

    def apply_filter(self):
        """Применение фильтрации"""

        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()

        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Фильтрация
        filtered = []
        for movie in self.movies:
            # Фильтр по жанру
            if genre_filter and genre_filter != "все":
                if genre_filter not in movie["genre"].lower():
                    continue

            # Фильтр по году
            if year_filter and year_filter != "все":
                try:
                    if int(year_filter) != movie["year"]:
                        continue
                except ValueError:
                    pass

            filtered.append(movie)

        # Вывод отфильтрованных
        for movie in filtered:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

        self.status_label.config(text=f"Показано: {len(filtered)} из {len(self.movies)}")

    def reset_filter(self):
        """Сброс фильтров"""

        self.filter_genre.delete(0, tk.END)
        self.filter_genre.insert(0, "Все")
        self.filter_year.delete(0, tk.END)
        self.filter_year.insert(0, "Все")

        self.update_table()

    def update_table(self):
        """Обновление таблицы фильмов"""

        # Очистка
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение
        for movie in self.movies:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

        self.status_label.config(text=f"Всего фильмов: {len(self.movies)}")

    def save_movies(self):
        """Сохранение фильмов в JSON"""

        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.movies, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def load_movies(self):
        """Загрузка фильмов из JSON"""

        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.movies = json.load(file)
                self.update_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
                self.movies = []


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()