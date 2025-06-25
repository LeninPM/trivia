import arcade
import random

# Configuración de la ventana
WIDTH = 1920
HEIGHT = 1080
SCREEN_TITLE = "Trivia Game"

# Colores
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK
GREEN = arcade.color.GREEN
RED = arcade.color.RED
BLUE = arcade.color.BLUE

# Variables de juego
score = 0
current_question = 0

# Preguntas y respuestas
questions = [
    {"question": "¿Qué es una CPU?", "answers": [
        "Unidad Central de Procesamiento", "Unidad Central de Poder", "Unidad Central de Periféricos"], "correct": 0},
    {"question": "¿Qué significa la sigla RAM?", "answers": [
        "Random Access Memory", "Read Access Memory", "Rapid Access Memory"], "correct": 0},
    {"question": "¿Qué es un bus en computadoras?", "answers": [
        "Un canal de comunicación", "Un tipo de memoria", "Un procesador"], "correct": 0},
]


def point_in_button(x, y, button):
    """Devuelve True si el punto (x, y) está dentro del botón."""
    left = button["center_x"] - button["width"] // 2
    right = button["center_x"] + button["width"] // 2
    bottom = button["center_y"] - button["height"] // 2
    top = button["center_y"] + button["height"] // 2
    return left <= x <= right and bottom <= y <= top


class TriviaGame(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, SCREEN_TITLE)
        self.background_image = arcade.load_texture("fondo_inicio.jpg")
        self.question_text = ""
        self.answer_buttons = []
        self.setup()

    def setup(self):
        global current_question
        current_question = 0 if current_question >= len(questions) else current_question
        self.question_text = questions[current_question]["question"]
        self.answer_buttons = []

        # Crea botones de respuestas
        button_height = 100
        button_width = 500
        start_y = HEIGHT // 2 + (button_height + 20)
        for i, answer in enumerate(questions[current_question]["answers"]):
            center_x = WIDTH // 2
            center_y = start_y - i * (button_height + 20)
            self.answer_buttons.append({
                "text": answer,
                "center_x": center_x,
                "center_y": center_y,
                "width": button_width,
                "height": button_height,
                "correct": i == questions[current_question]["correct"]
            })

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(
            WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT, self.background_image)

        arcade.draw_text(self.question_text, WIDTH // 2,
                         HEIGHT // 3 + 100, WHITE, 30, anchor_x="center")

        for button in self.answer_buttons:
            arcade.draw_rectangle_filled(
                button["center_x"], button["center_y"], button["width"], button["height"], BLUE)
            arcade.draw_text(button["text"], button["center_x"],
                             button["center_y"], WHITE, 20, anchor_x="center", anchor_y="center")

        arcade.draw_text(f"Score: {score}", WIDTH - 200, HEIGHT - 50, WHITE, 24)

    def on_update(self, delta_time):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        for button_info in self.answer_buttons:
            if point_in_button(x, y, button_info):
                self.check_answer(button_info["correct"])

    def check_answer(self, correct):
        global score, current_question

        if correct:
            score += 1
            self.show_answer("Correcto", GREEN)
        else:
            self.show_answer("Incorrecto", RED)

        current_question += 1
        if current_question < len(questions):
            self.setup()
        else:
            self.game_over()

    def show_answer(self, message, color):
        arcade.draw_text(message, WIDTH // 2, HEIGHT // 2, color, 40, anchor_x="center")
        arcade.schedule(self.setup, 2)

    def game_over(self):
        arcade.draw_text("Juego terminado", WIDTH // 2, HEIGHT // 2 + 100, WHITE, 50, anchor_x="center")
        arcade.draw_text(f"Tu puntuación final es: {score}", WIDTH // 2, HEIGHT // 2, WHITE, 40, anchor_x="center")
        arcade.finish_render()


def main():
    game = TriviaGame()
    arcade.run()


if __name__ == "__main__":
    main()
