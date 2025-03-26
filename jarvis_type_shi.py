import PySimpleGUI as sg
from ollama import chat
import threading

def run_ollama_chat(user_input, output_element):
    try:
        stream = chat(
            model='llama3.1',
            messages=[{'role': 'user', 'content': user_input}],
            stream=True,
        )

        full_response = ""
        for chunk in stream:
            content = chunk['message']['content']
            full_response += content
            output_element.update(full_response)

    except Exception as e:
        output_element.update(f"Error: {e}")

layout = [
    [sg.Text("Enter your prompt:")],
    [sg.InputText(key="-INPUT-")],
    [sg.Button("Send"), sg.Button("Exit")],
    [sg.Multiline(size=(80, 20), key="-OUTPUT-", autoscroll=True)],
]

window = sg.Window("O.C.GUI", layout)

while True:
    event, values = window.read()
    if event == "Send":
        user_input = values["-INPUT-"]
        output_element = window["-OUTPUT-"]
        output_element.update("")
        threading.Thread(target=run_ollama_chat, args=(user_input, output_element)).start()

    elif event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()