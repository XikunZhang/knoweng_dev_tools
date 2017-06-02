from tkinter import Listbox, Scrollbar, Button, Tk, Frame, Label, constants, filedialog, END
import os, sys

def file_save(text):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None: 
        return
    f.write(text)
    f.close()
    return

def transform(text):
    # transform functions HERE
    print("transform")
    output = text
    
    Button(text="Save as", command = lambda: file_save(output), font=("Helvetica", 21)).pack()


def file_upload(root):
    file = filedialog.askopenfilename(filetypes = (("CSV files","*.csv"),("TXT files", "*.txt")))
    
    directory = os.path.abspath(file)

    file_handler = open(directory)
    content = file_handler.read()

    Button(text="Transform", command = lambda: transform(content), font=("Helvetica", 21)).pack()

    return content

def init_frame(root):
    frame = Frame(root)
    frame.pack()
    Button(text="Upload", command = lambda: file_upload(root), font=("Helvetica", 21)).pack()

def main():
    root = Tk()
    root.minsize(width=400, height=247)
    root.lift()
    root.attributes('-topmost', True)
    root.wm_title("Upload")
    
    init_frame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
