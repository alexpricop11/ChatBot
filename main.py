import flet as ft

from chatbot import ChatBot


def main(page: ft.Page):
    page.title = "Chatbot"
    page.scroll = "auto"
    page.theme_mode = 'dark'
    page.window.width = 350
    page.window.height = 700
    bot = ChatBot()
    messages = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=10)

    def add_message(sender, text):
        bg_color = ft.Colors.BLUE_GREY_800 if sender == "Bot" else ft.Colors.BLUE_700
        align = ft.alignment.center_left if sender == "Bot" else ft.alignment.center_right
        text_color = ft.Colors.WHITE

        messages.controls.append(
            ft.Container(
                content=ft.Text(f"{sender}: {text}", color=text_color),
                bgcolor=bg_color,
                padding=10,
                border_radius=10,
                alignment=align,
                margin=5,
                width=300
            )
        )
        page.update()

    def send_message(e=None):
        if not input_field.value.strip():
            return
        user_text = input_field.value.strip()
        input_field.value = ""
        add_message("User", user_text)

        response = bot.process_input(user_text)
        add_message("Bot", response)

    def restart_conversation(e):
        bot.reset()
        messages.controls.clear()
        input_field.disabled = False
        send_button.disabled = False
        first_question = bot.get_next_question()
        if first_question:
            bot.add_to_history("Bot", first_question)
            add_message("Bot", first_question)

    def end_conversation(e):
        end_msg = "Conversatia a fost incheiata. Mulțumesc!"
        bot.add_to_history("Bot", end_msg)
        add_message("Bot", end_msg)
        input_field.disabled = True
        send_button.disabled = True

    input_field = ft.TextField(
        label="Scrie un mesaj...",
        height=50,
        border_radius=10,
        bgcolor=ft.Colors.BLUE_GREY_900,
        color=ft.Colors.WHITE,
        on_submit=send_message,
        expand=True
    )

    send_button = ft.IconButton(icon=ft.Icons.SEND, on_click=send_message, icon_color=ft.Colors.BLUE)
    restart_button = ft.TextButton("Relua conversația", on_click=restart_conversation)
    end_button = ft.TextButton("Încheie conversația", on_click=end_conversation)

    page.add(
        ft.Row(
            [ft.Text("ChatBot", size=20)],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Container(
            content=messages,
            expand=True,
            height=page.window.height - 200
        ),
        ft.Row([restart_button, end_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([input_field, send_button]),
    )

    if bot.current_question == 0:
        first_question = bot.get_next_question()
        if first_question:
            add_message("Bot", first_question)


if __name__ == '__main__':
    ft.app(target=main)
