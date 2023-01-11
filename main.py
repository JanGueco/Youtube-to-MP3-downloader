import sys, os, subprocess

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QFileDialog, QPushButton, QTextEdit, QProgressBar, QComboBox
from PyQt6.QtCore import Qt


from pytube import YouTube

#initialize app
app = QApplication([])

#initialize variables for screen
screen = app.primaryScreen()
width = screen.size().width()
height = screen.size().height()
window_width = 600
window_height = 600


window = QWidget()
window.setWindowTitle("Youtube to Mp3")
window.setGeometry(int(width/2) - int(window_width/2), int(height/2) - int(window_height/2), window_width, window_height)
window.setFixedSize(window_width,window_height)


helloMsg = QLabel("<h1>Youtube to Mp3</h1>", parent=window)
helloMsg.move(15, 15)


label = QLabel(parent=window)
label.setText("Download directory:")
label.move(15,65)


download_directory = QLineEdit(parent=window)
download_directory.resize(300,25)
download_directory.move(135,60)
download_directory.setText("Select directory")
download_directory.setReadOnly(True)

directory_widget = QFileDialog(parent=window)


directory_button = QPushButton(window)
directory_button.setText("change directory")
directory_button.move(450,60)


directory_select = QFileDialog(parent=window)


label1 = QLabel(parent=window)
label1.setText("Youtube videos list:")
label1.move(15,100)


label2 = QLabel(parent=window)
label2.setText("Preferred quality:")
label2.move(350,100)


qualities_list = ["1080p","720p","480p"]
quality_selector = QComboBox(parent=window)
quality_selector.addItems(qualities_list)
quality_selector.move(450,98)


links_list = QTextEdit(window)
links_list.resize(500,300)
links_list.move(15,130)


progress_bar = QProgressBar(parent=window)
progress_bar.setGeometry(15, 450, 500,20)
progress_bar.setValue(0)


download_button = QPushButton(parent=window)
download_button.setText("Convert and Download")
download_button.setGeometry(400,515,150,30)
download_button.setEnabled(False)

credit_label = QLabel(parent=window)
credit_label.setText("by: Jgueco")
credit_label.move(15,580)



window.show()

download_directory.textChanged.connect(lambda: check_directory(download_directory.text()))
directory_button.clicked.connect(lambda: change_directory(directory_widget))
download_button.clicked.connect(lambda: get_youtube_links())


def change_directory(parent):
    #directory = str(QFileDialog.getExistingDirectory(parent, caption="Select Directory"))
    directory = str(directory_select.getExistingDirectory(caption="Select directory"))
    download_directory.setText(directory)

def get_youtube_links():
    links = links_list.toPlainText()
    temp_list = list()
    links_list.setEnabled(False)
    progress_bar.setFormat("Downloading")
    progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
    for line in links.splitlines():
        temp_list.append(line)
    
    download_list(temp_list)

def download_list(list_links):
    progress = 0
    total = len(list_links)
    for link in list_links:
        download_mp3(link)
        progress += 1
        progress_bar.setValue(int((progress/total) * 100))
    
    progress_bar.setFormat("Done")
    links_list.setEnabled(True)
    open_directory()
    

def download_mp3(link):
    #audio = YouTube(link).streams.get_lowest_resolution()
    audio = YouTube(link).streams.get_by_resolution(quality_selector.currentText()) if YouTube(link).streams.get_by_resolution(quality_selector.currentText()) != None else YouTube(link).streams.get_highest_resolution()
    audio_download = audio.download(output_path=download_directory.text())
    base, ext = os.path.splitext(audio_download)
    new_file = base + '.mp3'
    try:
        os.rename(audio_download, new_file)
    except:
        os.replace(audio_download, new_file)

def check_directory(dir):
    if os.path.isdir(dir):
        download_button.setEnabled(True)
    else:
        download_button.setEnabled(False)

def open_directory():
    subprocess.Popen(f'explorer {os.path.realpath(download_directory.text())}')



sys.exit(app.exec())

