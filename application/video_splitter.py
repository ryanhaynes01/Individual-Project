#import PySimpleGUI as sg
from typing import Callable
import file_handler
import threading
import cv2
import wx

fm = file_handler.FileManager()
video_location = fm.create_path_string("application", "bin", "video_source")
frame_output = fm.create_path_string("application", "bin", "frame_output")

def convert_video(selected: str, dialog: wx.ProgressDialog) -> None:
    """
    Take the location of the video the user wanted to convert into frames.
    The frames being placed in the output directory by the name of the video itself.
    Then, after completion, notify the user and exit. If there's an error,
    also inform the user and exit.

    Args:
        selected (str): item that was selected from the user
        dialog (wx.ProgressDialog): progress bar to let the user know how far
                                    into the conversion they are

    Returns:
        None
    """

    # use the file manager to find the location to the item the user selected from
    selected_location = fm.create_path_string(video_location, selected)

    # find the final period in the string as this is the extension of the file, cutting if off
    # before using the file manager to create a string for the path to create a directory
    selected = selected[:selected.rfind(".")]
    output_location = fm.create_path_string(frame_output, selected)

    # if the directory already exists, then the video has been converted before, so return
    if (not fm.make_directory(output_location)):
        wx.CallAfter(dialog.Destroy)
        wx.MessageBox("Video already converted!")
        return
    
    # catch all to prevent the thread from crashing
    try:
        # get the video from the location found earlier, counting the total frames in the video
        video = cv2.VideoCapture(selected_location)
        total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # reset the progress bar max value to the new frame total
        dialog.SetRange(total)

        # for each frame in the video, read the frame, then save it as a new jpg
        # updating the progress bar each iteration
        for i in range(total):
            success, frame = video.read()
            cv2.imwrite(f"{fm.create_path_string(output_location, str(i + 1))}.jpg", frame)
            wx.CallAfter(dialog.Update, i + 1)

        # once finished, destroy the finished progress bar and notify the user that everything went successfully
        wx.CallAfter(dialog.Destroy)
        wx.MessageBox(message="Success!")
    except:

        # if something goes wrong, destroy the progress bar and notify the user
        # deleting the directory made and all items inside if the program got that far
        wx.CallAfter(dialog.Destroy)
        wx.MessageBox(message="Something went wrong! Aborting and clearning.")

        if (fm.exists(output_location)):
            fm.delete_directory(output_location)

def thread_start(function: Callable, *args):
    """
    Create a thread for a function, taking the arguments it'll take

    Args:
        function (Callable): function that will be the target for the new thread
        *args (Any): arguments that the parsed function will need to work
    """
    thread = threading.Thread(target=function, args=args)
    thread.setDaemon(True)
    thread.start()


class FileSelection(wx.Frame):
    """
    A frame to allow users to select a video they'd like to convert into a
    collection of frames.
    """

    def __init__(self, *args, **kw):
        # call the parent init
        super(FileSelection, self).__init__(*args, **kw)

        # get the width and height data from the frame
        width, height = self.Size[0], self.Size[1]

        # variable to keep track of empty directories
        self.is_empty = False

        # create a panel in the frame
        pnl = wx.Panel(self, size=(width, height))

        # create a listbox for holding videos to convert
        selection = wx.ListBox(pnl, pos=(10, 10), size=(int(width - 40), int(height/2)))
        font = selection.GetFont()
        font.PointSize += 2
        font = font.Bold()
        selection.SetFont(font)

        # create a button to trigger the actual conversion process
        convert_button = wx.Button(pnl, label="Convert!", size=(100, 50), pos=(10, int(height/2) + 20))
        convert_button.SetFont(font)
        convert_button.Bind(wx.EVT_BUTTON, self.start_conversion)

        # create a button to refresh the listbox if the directory gets updated
        refresh_button = wx.Button(pnl, label="Refresh List", size=(100, 50), pos=(120, int(height/2) + 20))
        refresh_button.SetFont(font)
        refresh_button.Bind(wx.EVT_BUTTON, self.populateListBox)

        # WIP
        open_file_button = wx.Button(pnl, label="Open Source File", size=(150, 50), pos=(230, int(height/2) + 20))
        open_file_button.SetFont(font)
        open_file_button.Bind(wx.EVT_BUTTON, self.reveal_source_file)

        # create a menu bar
        self.makeMenuBar()

        # make the selection box an attribute for future use and populate it
        self.selection = selection
        self.populateListBox("")


    def populateListBox(self, event):
        """
        Populate the listbox with the names of the files held in the
        directory that's currently being looked at

        Args:
            event (Any): event information passed by the wx event handler
        """

        # clear the selection box to prevent duplication and re-affirm the list isn't empty yet
        self.selection.Clear()
        self.is_empty = False

        # gather all the items that reside in the directory selected
        options = fm.items_in_directory(video_location)

        # if no options were gathered, add that no options were found, assigning is empty
        if (len(options) == 0):
            options.append(f"{video_location} is empty!")
            self.is_empty = True

        # add the items into the listbox, in the order they're in from the directory
        self.selection.InsertItems(items=options, pos=0)


    def start_conversion(self, event):
        """
        Simple funcion to create a progress bar and start the thread creation for the
        actual conversion section of the program

        Args:
            event (Any): event information passed by the wx event handler
        """

        # if the listbox is empty, nothing can be selected to return
        if self.is_empty:
            wx.MessageBox(message="Cannot convert an empty selection!")
            return
        
        # otherwise, get the item that the user selected, creating a progress bar to pass to the new thread
        # so the user can see how much progress has been made on the conversion
        selected_file = self.selection.Items[self.selection.GetSelection()]
        progress = wx.ProgressDialog("Conversion in progress", "Please wait...", maximum=100, parent=self, style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE)

        # call for the creation of a new thread, with the selected file and the progress bar
        thread_start(convert_video, selected_file, progress)

    def reveal_source_file(self, event):
        """
        WIP
        """
        pass

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&WIP...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("WIP")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Basic Video to Frame Converter",
                      "About V2F Converter",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frame = FileSelection(None, title='Video to Frame Converter', size=(1000, 500))
    frame.Show()
    app.MainLoop()