""" transformers_module.py 
#from tkinter.messagebox import showerror
#from tkinter import Frame

# from ipywidgets import interact, interactive, fixed, interact_manual
jupyter nbextension enable --py --sys-prefix widgetsnbextension
"""
import os
import sys
import time
import pandas as pd

from tkinter import *
from tkinter import Tk, filedialog
from tkinter.filedialog import askopenfilename, asksaveasfile
import ipywidgets as widgets
from IPython.display import display

OUTPUT_FILE_EXT = ['.tsv', '.df', 'txt']

class Transpose_Notebook_GUI():
    def __init__(self):
        self.data = {'start_time':time.strftime("%a_%d_%b_%Y_%H_%M_%S", time.localtime())}
        self.data['input_file_name'] = 'none selected'
        self.data['output_file_name'] = 'untitled.tsv'
        self.populate_GUI()
        
    def populate_GUI(self):
        self.input_file_button = widgets.Button(
            description='Input File',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='input file to transpose',
            data_file_key='input_file_name'
            )
        self.input_file_button.on_click(self.gui_get_file_name)
        
        self.input_file_name_display = widgets.Text(
            value='No File Selected',
            placeholder='select file',
            description='Spreadsheet:',
            disabled=False
            )
        self.input_file_size_display = widgets.Text(
            value='No File Selected',
            placeholder='file shape',
            description='rows x columns:',
            disabled=False
            )
        
        self.output_file_button = widgets.Button(
            description='Transpose',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='file to transpose',
            data_file_key='output_file_name'
            )
        self.output_file_button.on_click(self.gui_set_file_name)
        
        self.output_file_name_display = widgets.Text(
            value='No File Selected',
            placeholder='select file',
            description='Spreadsheet:',
            disabled=False
            )

        self.output_file_size_display = widgets.Text(
            value='No File Selected',
            placeholder='file shape',
            description='rows x columns:',
            disabled=False
            )
        
    def show_spreadsheet_df_ULC(self, call_button):
        file_name = self.data[self.input_file_button.data_file_key]
        try:
            spreadsheet_df = pd.read_csv(file_name, sep='\t', index_col=0, header=0)
            n_rows = spreadsheet_df.shape[0]
            n_cols = spreadsheet_df.shape[1]
        except:
            return
        if n_rows >= 1 and n_cols >= 1:
            self.input_file_size_display.value = '%d x %d'%(n_rows, n_cols)
            self.output_file_size_display.value = '%d x %d'%(n_cols, n_rows)
            spreadsheet_df = spreadsheet_df[list(spreadsheet_df.columns)[0:4]].iloc[0:4]
            display(spreadsheet_df)

        
    def gui_get_file_name(self, call_button):
        """ set the input file name """
        root = Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.focus_force()
        root.lift()
        ret_name = askopenfilename(parent=root, title='Select Input File',
                                   filetypes=(("TSV files", "*.tsv"), ("Text files", "*.txt"),
                                              ("CSV files", "*.csv"), ("Data Frame", "*.df"),
                                              ("All files", "*.*")))
        file_name = os.path.abspath(ret_name)
        
        if not os.path.isfile(file_name): return     #   exit if no file selected
        
        self.data[call_button.data_file_key] = file_name
        self.input_file_name_display.value = os.path.split(file_name)[1]
        
        root.destroy()
        
        self.show_spreadsheet_df_ULC(call_button)
        
    def gui_set_file_name(self, call_button):
        """ set the output file name """
        if not os.path.isfile(self.data['input_file_name']):
            print('No Valid input selected')
            return
        ipt_p, ipt_f = os.path.split(self.data['input_file_name'])
        if len(ipt_p) > 1:
            ifile, ole_ext = os.path.splitext(ipt_f)
            ifile = ifile + '_T.tsv'
        else:
            ipt_p = os.getcwd()
            ifile = 'Untitled_T.tsv'
            
        root = Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.focus_force()
        root.lift()
        file_name = filedialog.asksaveasfilename(parent=root,
                                            initialdir=ipt_p, 
                                            initialfile=ifile,
                                            filetypes=(("TSV files", "*.tsv"), ("Text files", "*.txt"),
                                                       ("CSV files", "*.csv"), ("Data Frame", "*.df"),
                                                       ("All files", "*.*")))
        root.destroy()
        if not file_name:
            return False
            
        self.data[call_button.data_file_key] = os.path.abspath(file_name)
        
        self.output_file_name_display.value = os.path.split(file_name)[1]
        self.read_transpose_write_df(call_button)
        
        return True
    
    def read_transpose_write_df(self, call_button):
        """ using file name in the input file button, read, transpose and write to the output_file_button name """
        if not os.path.isfile(self.data['input_file_name']):
            return
            
        full_file_name = self.data['input_file_name']
        if full_file_name:
            
            spreadsheet_df_0 = pd.read_csv(full_file_name, sep='\t', index_col=0, header=0)
            spreadsheet_df = spreadsheet_df_0.transpose()
            
            output_file_name = self.data['output_file_name']

            otf_name, otf_ext = os.path.splitext(output_file_name)
            if not otf_ext in OUTPUT_FILE_EXT:
                output_file_name = otf_name + '.tsv'
                
            spreadsheet_df.to_csv(output_file_name, sep='\t', index=True, header=True)

            spreadsheet_df = spreadsheet_df[list(spreadsheet_df.columns)[0:4]].iloc[0:4]
            display(spreadsheet_df)

        
        
        
        