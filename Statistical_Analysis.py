# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:51:00 2023

@author: m_ant
"""

import heartpy as hp
from tkinter import filedialog
import mne
import numpy as np
import sys
import tkinter as tk
from tkinter import ttk
import os
from scipy import stats


class Button_Chooser(tk.Toplevel):
    def __init__(self,master,list_of_words):
        super().__init__(master)
        self.list_of_words=list_of_words
        self.selected_words = []

        # Create a frame to contain the buttons
        frame = tk.Frame(self)
        frame.pack()

        # Create a button for each word
        
        for item in self.list_of_words:
            button = tk.Button(self, text=item, command=lambda x=item: self.word_selected(x))
            button.pack()

        # Create an OK button to save the selected words
        ok_button = tk.Button(self, text="OK", command=self.save_words)
        ok_button.pack()

    def word_selected(self, word):
        self.selected_words.append(word)
        print("called")

    def save_words(self):
        self.return_value = self.selected_words
        self.destroy()
    


class window_independent_samples_t_test(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.original_stdout = sys.stdout
        self.title('Independent Samples T-test')
        self.dire=None
        self.biomarkers=["bpm"]
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.button1 = ttk.Button(self,text="Choose Save", command=self.save_clicked)
        self.button1.pack()
        
        self.button2 = ttk.Button(self,text="Choose biomarkers", command=self.choose_biomarkers)
        self.button2.pack()
        
        self.button3 = ttk.Button(self, text="Run T-TEST", command=self.run_test_clicked)
        self.button3.pack()
        
        self.button4 = ttk.Button(self, text="print biomarkers", command=self.print_biomarkers)
        self.button4.pack()
        
        self.console = tk.Text(self)
        self.console.pack(fill=tk.BOTH,expand=True)
        self.console.insert("end","1) Press the <Choose Save> button and pick a txt file to save the results.\n You should keep this txt file closed throughout the execution")
        self.console.insert("end","\n2) Press the <Run T-Test> button and choose exactly 2 .set files (one calm and one stressed) of the same subject")
    
    def on_closing(self):
        self.destroy()
    
    def save_clicked(self):
        dire = filedialog.askopenfilename(filetypes=[(".txt file","*.txt")],title="where to save the results")
        self.dire=dire
        
    def print_biomarkers(self):
        print(self.biomarkers)
    
    def choose_biomarkers(self):
        list_of_words=['bpm',
                       'ibi',
                       'sdnn',
                       'sdsd',
                       'rmssd',
                       'pnn20',
                       'pnn50',
                       'hr_mad',
                       'sd1',
                       'sd2',
                       's',
                       'sd1/sd2',
                       'breathingrate',
                       'segment_indices']
        
        self.child_window = Button_Chooser(self,list_of_words)
        self.wait_window(self.child_window)
        biomarkers=self.child_window.return_value
        print("broo")
        self.biomarkers=biomarkers

    def run_test_clicked(self):
        print("run_test_clicked")
        self.perform_t_tests(self.dire)
        
    def independent_t_test(self,arr1,arr2):
        '''
        Parameters
        ----------
        arr1 : numpy array
        arr2 : numpy array

        Returns
        -------
        t : t-statistic (usually not usefull)
        p : p-value
        x : True if the samples ARE significantly different, False if they are not

        '''
        t,p = stats.ttest_ind(arr1,arr2)
        x = True if p<0.05 else False
        return t,p,x
    

    def t_test_two_files(self,filepath1,filepath2):
        '''
        Parameters
        ----------
        filepath1 : filepath of one .set file (for example stress.set)
        filepath2 : filepath of one .set file (for example calm.set)

        Returns
        -------
        t : t-statistic (usually not usefull)
        p : p-value
        x : True if the samples ARE significantly different, False if they are not
        ''' 
        data1=mne.io.read_raw_eeglab(filepath1,preload=True)
        ecg1=np.transpose(data1.pick_channels(["ECG"]).get_data()).flatten()
        
        data2=mne.io.read_raw_eeglab(filepath2,preload=True)
        ecg2=np.transpose(data2.pick_channels(["ECG"]).get_data()).flatten()

        _, m1 = hp.process_segmentwise(ecg1, sample_rate=300, segment_width=10, segment_overlap=0.5)
        _, m2 = hp.process_segmentwise(ecg2, sample_rate=300, segment_width=10, segment_overlap=0.5)
        tl=[]
        pl=[]
        xl=[]
        for biom in self.biomarkers:
            t,p,x=self.independent_t_test(m1[biom],m2[biom])
            tl.append(t)
            pl.append(p)
            xl.append(x)
        return tl,pl,xl

    def perform_t_tests(self,file=None):
        print("perform_t_tests")
        filepaths = filedialog.askopenfilenames(filetypes=[("set file","*.set")], title="Select 2 .set files (stress, calm) of same person")
        while len(filepaths)== 2:
            tl,pl,xl= self.t_test_two_files(filepaths[0], filepaths[1])
            filename1 = os.path.basename(filepaths[0])
            filename2 = os.path.basename(filepaths[1])
            if file != None:
                with open(file, 'a') as f:
                    sys.stdout = f # Change the standard output to the file we created.
                    print("Independent samples t-test in files:",filename1, "and", filename2)
                    for i,biom in enumerate(self.biomarkers):
                        print("Biomarker: ", biom, "Is the difference significant? ", str(xl[i]),"P-value", pl[i])
                    print(" _____________________________________")
                    sys.stdout = self.original_stdout # Reset the standard output to its original value
            self.console.insert("end", "\nIndependent samples t-test in files:" + filename1 + "and" + filename2)
            for i,biom in enumerate(self.biomarkers):
                self.console.insert("end","\nBiomarker: "+ biom + " Is the difference significant? "+ str(xl[i]) +" P-value"+ str(pl[i]))
            filepaths = filedialog.askopenfilenames(filetypes=[("set file","*.set")])
        


if __name__ == "__main__":   
    app=window_independent_samples_t_test()
    app.mainloop()