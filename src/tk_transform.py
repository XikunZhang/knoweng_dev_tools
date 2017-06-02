from tkinter import Button, Tk, Frame, filedialog
import os
import pandas

def file_upload(root):

    file = filedialog.askopenfilename(filetypes = (("TSV files","*.tsv"),("CSV files","*.csv"),("TXT files", "*.txt")))
    input_full_file_name = os.path.abspath(file)
    try:
        spreadsheet_df = pandas.read_csv(input_full_file_name, sep='\t', index_col=0, header=0)
        spreadsheet_df = spreadsheet_df.transpose()
        output_full_file_name = filedialog.asksaveasfile(mode='w', defaultextension=".tsv")
        spreadsheet_df.to_csv(output_full_file_name, sep='\t', index=True, header=True)
    except:
        pass

    root.destroy()

def init_frame(root):
    frame = Frame(root)
    frame.pack()
    Button(text="Select File", command = lambda: file_upload(root), font=("Helvetica", 21)).pack()
    Button(text="Cancel", command=root.destroy).pack()

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
