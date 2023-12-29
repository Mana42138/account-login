import keyboard
import pyperclip


word_list = [
"UPD4",
"SORRYDELAYS3",
"100MVISITSTHANKS",
"SEASONONE",
"SORRYDELAYS2",
"BETA",
"XMAS",
"FOLLOWER",
]

index = 0

def copy_next_word(event):
    global index
    if event.name == 'f':  # you can change 'f' to any key
        if index < len(word_list):
            word_to_copy = word_list[index]
            index += 1
            pyperclip.copy(word_to_copy)
            # print(f"Copied: {word_to_copy}")
        else:
            index = 0
            # print("End of the list. Restarting...")

def main_copy():
    keyboard.on_press(copy_next_word)

    keyboard.wait('f5')
