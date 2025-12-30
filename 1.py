import tkinter as tk
import random
import time
import threading

# ======================
# TKINTER МЕГА-АРКАДА 4000
# ======================

class MegaArcade(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mega Arcade 4000")
        self.geometry("600x420")
        self.resizable(False, False)
        self.main_menu()

    # --------------------
    # МЕНЮ
    # --------------------
    def main_menu(self):
        self.clear()
        tk.Label(self, text="🔥 MEGA ARCADE 4000 🔥", font=("Arial", 22, "bold"), fg="red").pack(pady=20)
        games = [
            ("Камень / Ножница / Бумага", self.rps_game),
            ("Угадай число", self.guess_number),
            ("Кости", self.dice_game),
            ("Виселица", self.hangman),
            ("Гонки улучшенные", self.race_game),
            ("STAR WARS: Galactic Waves", self.star_wars)
        ]
        for name, cmd in games:
            tk.Button(self, text=name, font=("Arial", 14), command=cmd, width=36).pack(pady=5)

    # --------------------
    # УТИЛИТЫ
    # --------------------
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --------------------
    # ИГРА 1 — RPS
    # --------------------
    def rps_game(self):
        self.clear()
        tk.Label(self, text="Камень/Ножница/Бумага", font=("Arial", 20, "bold"), fg="blue").pack(pady=10)
        result = tk.Label(self, text="", font=("Arial", 16))
        result.pack(pady=10)

        def play(choice):
            bot = random.choice(["камень", "ножница", "бумага"])
            if choice == bot:
                res = "Ничья"
            elif (choice == "камень" and bot == "ножница") or (choice == "ножница" and bot == "бумага") or (choice == "бумага" and bot == "камень"):
                res = "Ты выиграл!"
            else:
                res = "Робот выиграл!"

            # исправлено: использовать явный \n, а не перенос строки внутри литерала
            result.config(text=f"Ты: {choice}  |  Робот: {bot}\\n{res}")

        for ch in ["камень", "ножница", "бумага"]:
            tk.Button(self, text=ch, font=("Arial", 14), command=lambda c=ch: play(c), width=20).pack(pady=5)

        tk.Button(self, text="Назад", font=("Arial", 14), command=self.main_menu).pack(pady=20)

    # --------------------
    # ИГРА 2 — Угадай число
    # --------------------
    def guess_number(self):
        self.clear()
        tk.Label(self, text="Угадай число!", font=("Arial", 20, "bold"), fg="green").pack(pady=10)
        target = random.randint(1, 100)

        entry = tk.Entry(self, font=("Arial", 14))
        entry.pack(pady=5)
        info = tk.Label(self, text="Введите число от 1 до 100", font=("Arial", 14))
        info.pack(pady=10)

        def check():
            try:
                n = int(entry.get())
                if n == target:
                    info.config(text="🎉 Угадал!")
                elif n < target:
                    info.config(text="Больше!")
                else:
                    info.config(text="Меньше!")
            except:
                info.config(text="Ошибка ввода!")

        tk.Button(self, text="Проверить", font=("Arial", 14), command=check).pack(pady=10)
        tk.Button(self, text="Назад", font=("Arial", 14), command=self.main_menu).pack(pady=20)

    # --------------------
    # ИГРА 3 — Кости
    # --------------------
    def dice_game(self):
        self.clear()
        tk.Label(self, text="Кости 🎲", font=("Arial", 20, "bold"), fg="purple").pack(pady=10)
        result = tk.Label(self, text="", font=("Arial", 16))
        result.pack(pady=20)

        def roll():
            p = random.randint(1, 6)
            b = random.randint(1, 6)
            if p > b:
                w = "Ты победил!"
            elif p < b:
                w = "Робот победил!"
            else:
                w = "Ничья!"
            # исправлено: \n вместо реального переноса
            result.config(text=f"Ты: {p} | Робот: {b}\\n{w}")

        tk.Button(self, text="Бросить!", font=("Arial", 16), command=roll).pack(pady=10)
        tk.Button(self, text="Назад", font=("Arial", 14), command=self.main_menu).pack(pady=20)

    # --------------------
    # ИГРА 4 — Виселица
    # --------------------
    def hangman(self):
        self.clear()
        tk.Label(self, text="Виселица", font=("Arial", 20, "bold"), fg="brown").pack(pady=10)

        words = ["компьютер", "машина", "робот", "ананас", "python"]
        word = random.choice(words)
        guessed = set()
        tries = [6]

        display = tk.Label(self, text="_ " * len(word), font=("Arial", 20))
        display.pack(pady=10)

        info = tk.Label(self, text="Осталось попыток: 6", font=("Arial", 14))
        info.pack(pady=5)

        entry = tk.Entry(self, font=("Arial", 14))
        entry.pack(pady=5)

        def attempt():
            letter = entry.get().lower()
            entry.delete(0, tk.END)
            if len(letter) != 1 or not letter.isalpha():
                return

            if letter in word:
                guessed.add(letter)
            else:
                tries[0] -= 1

            disp = " ".join([c if c in guessed else "_" for c in word])
            display.config(text=disp)
            info.config(text=f"Осталось попыток: {tries[0]}")

            if disp.replace(" ", "") == word:
                info.config(text="🎉 Победа!")
            elif tries[0] <= 0:
                info.config(text=f"Проигрыш! Слово: {word}")

        tk.Button(self, text="Пробовать", font=("Arial", 14), command=attempt).pack(pady=10)
        tk.Button(self, text="Назад", font=("Arial", 14), command=self.main_menu).pack(pady=20)

    # --------------------
    # ИГРА 5 — УЛУЧШЕННЫЕ ГОНКИ (2D Canvas Racing)
    # --------------------
    def race_game(self):
        self.clear()
        tk.Label(self, text="ГОНКИ 🏎️", font=("Arial", 22, "bold"), fg="darkblue").pack(pady=10)

        canvas = tk.Canvas(self, width=500, height=300, bg="black")
        canvas.pack()

        car = canvas.create_rectangle(230, 250, 270, 290, fill="yellow")
        obstacles = []
        speed = [5]
        playing = [True]

        def spawn_obstacle():
            x = random.randint(20, 480)
            ob = canvas.create_rectangle(x, 0, x+30, 40, fill="red")
            obstacles.append(ob)

        def game_loop():
            if not playing[0]:
                return

            if random.random() < 0.05:
                spawn_obstacle()

            for ob in list(obstacles):
                canvas.move(ob, 0, speed[0])
                pos = canvas.coords(ob)
                car_pos = canvas.coords(car)

                if pos[3] >= car_pos[1] and pos[1] <= car_pos[3] and pos[0] <= car_pos[2] and pos[2] >= car_pos[0]:
                    playing[0] = False
                    tk.Label(self, text="💥 Авария!", font=("Arial", 20), fg="red").pack(pady=10)
                    return

                if pos[1] > 300:
                    canvas.delete(ob)
                    obstacles.remove(ob)

            canvas.after(50, game_loop)

        def left(event):
            canvas.move(car, -20, 0)
        def right(event):
            canvas.move(car, 20, 0)

        self.bind("<Left>", left)
        self.bind("<Right>", right)

        threading.Thread(target=game_loop, daemon=True).start()

        tk.Button(self, text="Назад", font=("Arial", 14), command=self.main_menu).pack(pady=10)

    # --------------------
    # ИГРА 6 — STAR WARS: GALACTIC WAVES (переписанная)
    # --------------------
    def star_wars(self):
        self.clear()
        tk.Label(self, text="STAR WARS: GALACTIC WAVES 🚀", font=("Arial", 22, "bold"), fg="cyan").pack(pady=6)

        hp_frame = tk.Frame(self)
        hp_frame.pack(pady=2)
        hp_label = tk.Label(hp_frame, text="HP: 5", font=("Arial", 14), fg="red")
        hp_label.pack(side="left", padx=10)
        wave_label = tk.Label(hp_frame, text="Волна: 1", font=("Arial", 14), fg="yellow")
        wave_label.pack(side="left", padx=10)
        score_label = tk.Label(hp_frame, text="Очки: 0", font=("Arial", 14), fg="white")
        score_label.pack(side="left", padx=10)

        canvas = tk.Canvas(self, width=600, height=320, bg="black")
        canvas.pack()

        # КОРАБЛЬ
        ship = canvas.create_polygon(300, 300, 285, 330, 315, 330, fill="white")
        bullets = []
        enemies = []
        asteroids = []

        wave = [1]
        hp = [5]
        playing = [True]
        score = [0]

        # ----------------- SPAWN -----------------
        def spawn_asteroid():
            x = random.randint(20, 560)
            size = random.randint(18, 44)
            a = canvas.create_oval(x, -size, x + size, 0, fill="gray")
            asteroids.append(a)

        def spawn_alien():
            x = random.randint(40, 560)
            e = canvas.create_rectangle(x-18, -30, x+18, 0, fill="green")
            enemies.append(e)

        def spawn_boss():
            b = canvas.create_rectangle(150, -120, 450, -20, fill="purple")
            enemies.append(b)

        # ----------------- LEVELS -----------------
        def start_wave():
            count = wave[0] * 6
            for _ in range(count):
                spawn_asteroid()
            for _ in range(max(0, wave[0] // 2)):
                spawn_alien()
            if wave[0] % 5 == 0:
                spawn_boss()

        start_wave()

        # ----------------- GAME LOOP -----------------
        def game_loop():
            if not playing[0]:
                return

            # bullets movement
            for b in list(bullets):
                canvas.move(b, 0, -18)
                bcoords = canvas.coords(b)
                if not bcoords or bcoords[1] < -10:
                    try:
                        canvas.delete(b)
                    except:
                        pass
                    if b in bullets:
                        bullets.remove(b)

            # asteroids movement & collisions
            for a in list(asteroids):
                canvas.move(a, 0, 6 + wave[0]//2)
                apos = canvas.coords(a)
                ship_pos = canvas.bbox(ship)

                if apos and ship_pos:
                    # collision ship <-> asteroid
                    # use bbox for ship to simplify collision
                    if apos[3] >= ship_pos[1] and apos[1] <= ship_pos[3] and apos[0] <= ship_pos[2] and apos[2] >= ship_pos[0]:
                        hp[0] -= 1
                        hp_label.config(text=f"HP: {hp[0]}")
                        try:
                            canvas.delete(a)
                        except:
                            pass
                        if a in asteroids:
                            asteroids.remove(a)
                        if hp[0] <= 0:
                            playing[0] = False
                            tk.Label(self, text="💥 КОРАБЛЬ УНИЧТОЖЕН!", fg="red", font=("Arial", 18)).pack(pady=10)
                            return

                    # bullet hits asteroid
                    for b in list(bullets):
                        bpos = canvas.coords(b)
                        if bpos and apos:
                            if bpos[0] <= apos[2] and bpos[2] >= apos[0] and bpos[1] <= apos[3] and bpos[3] >= apos[1]:
                                try:
                                    canvas.delete(a)
                                    canvas.delete(b)
                                except:
                                    pass
                                if a in asteroids:
                                    asteroids.remove(a)
                                if b in bullets:
                                    bullets.remove(b)
                                score[0] += 10
                                score_label.config(text=f"Очки: {score[0]}")
                                break

                if apos and apos[1] > 350:
                    try:
                        canvas.delete(a)
                    except:
                        pass
                    if a in asteroids:
                        asteroids.remove(a)

            # enemies movement & collisions (aliens and boss)
            for e in list(enemies):
                # boss moves slower
                e_is_boss = False
                ecoords = canvas.coords(e)
                if not ecoords:
                    continue
                # simple heuristic: wide rectangle -> boss
                if (ecoords[2] - ecoords[0]) > 200:
                    canvas.move(e, 0, 2 + wave[0]//4)
                    e_is_boss = True
                else:
                    canvas.move(e, 0, 4 + wave[0]//3)

                epos = canvas.coords(e)
                ship_pos = canvas.bbox(ship)

                if epos and ship_pos:
                    if epos[3] >= ship_pos[1] and epos[1] <= ship_pos[3] and epos[0] <= ship_pos[2] and epos[2] >= ship_pos[0]:
                        hp[0] -= 1 if not e_is_boss else 2
                        hp_label.config(text=f"HP: {hp[0]}")
                        try:
                            canvas.delete(e)
                        except:
                            pass
                        if e in enemies:
                            enemies.remove(e)
                        if hp[0] <= 0:
                            playing[0] = False
                            tk.Label(self, text="💥 КОРАБЛЬ УНИЧТОЖЕН!", fg="red", font=("Arial", 18)).pack(pady=10)
                            return

                    # bullet hits enemy
                    for b in list(bullets):
                        bpos = canvas.coords(b)
                        if bpos and epos:
                            if bpos[0] <= epos[2] and bpos[2] >= epos[0] and bpos[1] <= epos[3] and bpos[3] >= epos[1]:
                                try:
                                    canvas.delete(e)
                                    canvas.delete(b)
                                except:
                                    pass
                                if e in enemies:
                                    enemies.remove(e)
                                if b in bullets:
                                    bullets.remove(b)
                                # boss gives more points
                                score[0] += 50 if e_is_boss else 20
                                score_label.config(text=f"Очки: {score[0]}")
                                break

                if epos and epos[1] > 400:
                    try:
                        canvas.delete(e)
                    except:
                        pass
                    if e in enemies:
                        enemies.remove(e)

            # check end of wave
            if len(asteroids) == 0 and len(enemies) == 0:
                wave[0] += 1
                wave_label.config(text=f"Волна: {wave[0]}")
                # small heal between waves (but not exceed some cap)
                hp[0] = min(8, hp[0] + 1)
                hp_label.config(text=f"HP: {hp[0]}")
                start_wave()

            canvas.after(40, game_loop)

        # ----------------- УПРАВЛЕНИЕ -----------------
        def left(event):
            canvas.move(ship, -20, 0)
        def right(event):
            canvas.move(ship, 20, 0)
        def shoot(event):
            # быстрые пули (можно держать пробел)
            bbox = canvas.bbox(ship)
            if not bbox:
                return
            x_center = (bbox[0] + bbox[2]) / 2
            b = canvas.create_rectangle(x_center - 3, bbox[1] - 12, x_center + 3, bbox[1], fill="yellow")
            bullets.append(b)

        self.bind("<Left>", left)
        self.bind("<Right>", right)
        # bind both space press and key repeat friendly method
        self.bind("<space>", shoot)

        # start loop in a thread-safe manner (we use after loop inside)
        game_loop()

        tk.Button(self, text="Назад", font=("Arial", 14), command=self.main_menu).pack(pady=6)


# ======================
# ЗАПУСК TKINTER АРКАДЫ
# ======================
if __name__ == "__main__":
    app = MegaArcade()
    app.mainloop()
