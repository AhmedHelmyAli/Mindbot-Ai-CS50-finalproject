#Used Libraries
import time
import openai
import pyttsx3
import speech_recognition as sr
from translate import Translator
import pytesseract
import requests
from PIL import Image
import qrcode

#Important Variables
mindbot = "MindBot: "

#Code
print("Welcome to MindBot AI\nyour best AI assistant")

commands = ["chatbot", "text-to-speech", "speech-to-text", "ai translator", "text ocr", "remove bg", "generate qr code"]
print("------------------------------------------------------------")
print("These are our features:")
time.sleep(1)
print(commands)

user_command = input(f"{mindbot}Please enter your command:> ").lower()
print(f"You have chosen {user_command}")

if user_command == "chatbot":
    openai.api_key = 'ENTER-YOUR-API-KEY-HERE'

    def chat_with_bot(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

    def main():
        print("Welcome to the Chatbot! Type 'exit' to end the chat.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print(f"{mindbot}Goodbye!")
                break
            response = chat_with_bot(user_input)
            print(f"{mindbot}{response}")

    if __name__ == "__main__":
        main()

elif user_command in ["text-to-speech", "tts", "text", "texttospeech"]:
    print(f"{mindbot}OK!")
    user_tts = input(f"{mindbot}Enter the text to process on it:> ")
    print(f"{mindbot}The text you entered is ({user_tts})")

    try:
        engine = pyttsx3.init()

        save_tts = input(f"{mindbot}Do you want to save and export the generated sound (Y/N):>  ").lower()

        if save_tts in ["y", "yes"]:
            print(f"{mindbot}Ok")
            file_name = input(f"{mindbot}Please enter the filename to save the generated sound (include .wav):> ")
            engine.save_to_file(user_tts, file_name)
            engine.runAndWait()
            print(f"File saved successfully in the project folder by name {file_name}")

        elif save_tts in ["n", "no"]:
            engine.say(user_tts)
            engine.runAndWait()
            print(f"{mindbot}Ok, Thanks For Using (Text-To-Speech) MindBot-Ai")

        else:
            print(f"{mindbot}Please choose (Y/N)")

    except Exception as e:
        print(f"{mindbot}An error occurred: {e}")

elif user_command in ["speech-to-text", "speech", "stt", "speechtotext"]:
    print(f"{mindbot}OK! Please speak after the beep.")
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"{mindbot}You said: {text}")

        save_text = input(f"{mindbot}Do you want to save this text to a file (Y/N)? ").lower()
        if save_text in ["y", "yes"]:
            file_name = input(f"{mindbot}Please enter the filename to save the text (include .txt):> ")
            with open(file_name, 'w') as f:
                f.write(text)
            print(f"{mindbot}Text saved successfully in {file_name}.")
        elif save_text in ["n", "no"]:
            print(f"{mindbot}Ok, text not saved.")
        else:
            print(f"{mindbot}Please choose (Y/N).")

    except sr.UnknownValueError:
        print(f"{mindbot}Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"{mindbot}Could not request results from Google Speech Recognition service; {e}")

elif user_command in ["ai translator", "translator", "translate"]:
    print(f"{mindbot}OK, let's start now!")

    text_to_translate = input(f"{mindbot}Enter the text you want to translate:\nYou: ")
    target_language = input(f"{mindbot}Enter the language you want to translate to (e.g., 'ar' for Arabic):\nYou: ")

    def translate_text(text, target_language='en'):
        translator = Translator(to_lang=target_language)
        translation = translator.translate(text)
        return translation

    translated_text = translate_text(text_to_translate, target_language)
    print(f"{mindbot}Translated text is: ({translated_text})")

elif user_command in ["text ocr", "ocr"]:
    image_path = input(f"{mindbot}Please enter the path of the image for OCR: ")
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        print(f"{mindbot}Extracted text from image: {text}")
    except Exception as e:
        print(f"{mindbot}An error occurred: {e}")

elif user_command in ["remove bg", "remove background"]:
    image_path = input(f"{mindbot}Please enter the path of the image to remove the background: ")
    api_key = "E96Rm16txt12jPpdrZzEo4wC"
    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": image_file},
                data={"size": "auto"},
                headers={"X-Api-Key": api_key},
            )
        if response.status_code == requests.codes.ok:
            output_file = "images/car-removebg-img.png"
            with open(output_file, "wb") as out_file:
                out_file.write(response.content)
            print(f"{mindbot}Background removed successfully! The output image is saved as {output_file}.")
        else:
            print(f"{mindbot}Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"{mindbot}An error occurred: {e}")

elif user_command in ["generate qr code", "qr code", "qr"]:
    data_to_encode = input(f"{mindbot}Enter the text or URL to generate a QR code: ")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    qr_code_filename = "qr_code.png"
    img.save(qr_code_filename)
    print(f"{mindbot}QR Code generated successfully! The QR code is saved as {qr_code_filename}.")

else:
    print(f"{mindbot}Sorry, we don't have this command in our system: {user_command}")
    print(f"{mindbot}Try Again\nPlease choose from this list the command you want: {commands}")
