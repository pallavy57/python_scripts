import os
import time
import moviepy.editor as mp
from tkinter.filedialog import *
from tkinter import *
from PIL import Image, ImageTk

# ==== creating main class


class VideoAudioConverter:
    # ==== creating gui window
    def __init__(self, root):
        self.root = root
        self.root.title("VIDEO-AUDIO CONVERTER by DataFlair")
        self.root.geometry('1280x720')
        image = Image.open("test_image.jpg")
        width = 1280
        height = 720
        resize_image = image.resize((width, height))
        img = ImageTk.PhotoImage(resize_image)

        # create label and add resize image
        label1 = Label(image=img)
        label1.image = img
        label1.pack()
        Button(self.root, text="Browse Files", font=(
            "times new roman", 15), command=self.browse).place(x=40, y=630)

    def browse(self):
        file_name = askopenfilename(
            title="Select a File", filetypes=(("Video files", "*.mp4*"),))
        Label(self.root, text=os.path.basename(file_name), font=(
            "times new roman", 20), bg="blue").place(x=200, y=630)
        res = self.convert(file_name)
        
        label= Label(self.root, text='Processing...', font=(
            "times new roman", 30))
        label.grid(column = 1, row = 1)
        
        label.pack()

    

        
        if(res == "mp3"):
            label.destroy()
            
            Label(self.root, text='Completed!!', font=(
                    "times new roman", 30)).place(x=1000, y=630)
        else:
             Label(self.root, text='There is some issue in processing..', font=(
            "times new roman", 30)).place(x=600, y=630)
      
                 
# ==== convert video to audio


    def convert(self, path):
        try:
            clip = mp.VideoFileClip(r'{}'.format(path))
            clip.audio.write_audiofile(r'{}mp3'.format(path[:-3]))
            output_extension = os.path.splitext(r'{}mp3'.format(path[:-3]))[1][1:]
            print(output_extension)
            if(output_extension != "mp3"):
                 raise Exception("There is some error converting this file")
            return output_extension
        except Exception as inst:
                    print(type(inst))   
                    print(inst.args) 
                    print(inst)
       

# ==== creating main function of python Video to Audio Converter


def main():
    # ==== create tkinter window
    root = Tk()
    # === creating object for class VideoAudioConverter
    obj = VideoAudioConverter(root)
    # ==== start the gui
    root.mainloop()


if __name__ == "__main__":
    # ==== calling main function
    main()
