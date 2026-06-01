from tkinter import Tk, Canvas
import random
import time

WIDTH = 400
HEIGHT = 400
BASKET_W = 80
BASKET_H = 18
STAR_SIZE = 18

mouse_x = WIDTH / 2
def update_mouse(event):
    global mouse_x
    mouse_x = event.x
def write(canvas, x, y, message, size=14):
    canvas.create_text(x, y, anchor="w", font=("Arial", size), text=message, fill="white")
def draw_stars(canvas, stars):
    for star in stars:
        canvas.create_oval(star["x"], star["y"],
                           star["x"] + STAR_SIZE, star["y"] + STAR_SIZE,
                           fill="gold", outline="gold")
def draw_screen(canvas, basket_x, stars, score, lives, level):
    canvas.delete("all")
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="midnightblue", outline="midnightblue")
    canvas.create_rectangle(basket_x, HEIGHT - 40,
                            basket_x + BASKET_W, HEIGHT - 40 + BASKET_H,
                            fill="tomato", outline="tomato")
    draw_stars(canvas, stars)
    write(canvas, 10, 20, f"Puntos: {score}")
    write(canvas, 10, 45, f"Vidas: {lives}")
    write(canvas, 300, 20, f"Nivel: {level}")
def add_star(stars):
    stars.append({"x": random.randint(0, WIDTH - STAR_SIZE), "y": 0})
def choose_speed(score):
    if score < 5:
        return 1, 4
    elif score < 10:
        return 2, 6
    else:
        return 3, 8
def main():
    root = Tk()
    root.title("Atrapa Estrellas")
    canvas = Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    canvas.bind("<Motion>", update_mouse)

    stars = []
    score = 0
    lives = 3
    frames = 0
    while lives > 0:
        root.update()
        if mouse_x < 0:
            basket_x = 0
        elif mouse_x > WIDTH - BASKET_W:
            basket_x = WIDTH - BASKET_W
        else:
            basket_x = mouse_x

        level, speed = choose_speed(score)
        if frames % 25 == 0:
            add_star(stars)

        for star in stars:
            star["y"] += speed
        for star in stars[:]:
            bottom = star["y"] + STAR_SIZE
            center = star["x"] + STAR_SIZE / 2
            basket_top = HEIGHT - 40
            if bottom >= basket_top and basket_x <= center <= basket_x + BASKET_W:
                stars.remove(star)
                score += 1
            elif star["y"] > HEIGHT:
                stars.remove(star)
                lives -= 1
            else:
                star["falling"] = True

        draw_screen(canvas, basket_x, stars, score, lives, level)
        frames += 1
        time.sleep(0.03)

    canvas.delete("all")
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black")
    write(canvas, 120, 180, "Fin del juego", 20)
    write(canvas, 115, 220, f"Puntos finales: {score}", 16)
    root.mainloop()

if __name__ == "__main__":
    main()
