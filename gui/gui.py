import cv2
import numpy as np
import time

class GUIManager:

    def __init__(self, size_in, columns_in, rows_in, background_color = (0,0,0), window_name = 'grid'):
        """
        GUIManager handles a set of objects containing the following functions (among others):

        def draw(image, position, size)
        Draws the object at the given position and within the given size.
        image : The image upon wich to draw
        position : The position of the object in columns and rows (columns, rows)
        size : The size that the object has to draw on in pixels (x, y)

        def mouse_event(event, x, y, flag, param)
        Takes parameters regarding the mouse. Every time the mouse is moved, clicked on or otherwise changed
        this function will be called and sent the above parameters. This function may do as it pleases otherwise.
        event : The event that triggered the function. The event is an int but is translated in cv2.cv.CV_eventname
        x = The cursors current x position in pixels
        y = The cursors current y position in pixels

        :param size_in: The size of the window to open in pixels (x, y)
        :param columns_in: How many columns that is supposed to exist
        :param rows_in: How many rows that is supposed to exist
        :param background_color: The color of the background (wich color the default image on wich to write is)
        :param window_name: The name of the window
        :return: None
        """
        self._columns = columns_in
        self._rows = rows_in
        self._height = size_in[1]
        self._width = size_in[0]
        self._gui_objects = []
        self._window_name = window_name
        self._background_color = background_color

        #creating a new background image of the apporpriate size to write on
        self.image = np.zeros((self._height, self._width, 3), dtype=np.uint8)
        self.image[:] = background_color
        cv2.startWindowThread()
        cv2.namedWindow(self._window_name)

    def add(self, gui_object, gui_pos):
        """
        Adds a new gui object
        :param gui_object: the gui object (specified in docstrings of constructor of this class)
        :param gui_pos: the position that the gui is to be drawn in. Following format (column, row)
        :return:
        """

        self._gui_objects.append((gui_object, gui_pos[0], gui_pos[1]))

    def mouse_event(self, event, x, y, flag, param):
        """
        Passes all parameters to each gui object so that it may do what it pleases with them.
        :param event: the mouse event (cv2.cv.CV_...)
        :param x: the x coordinate of the cursor
        :param y: the y coordinate of the cursor
        :param flag:
        :param param:
        """
        for gui_obj in self._gui_objects:
            gui_obj[0].mouse_event(event, x, y, flag, param)


    def draw(self):
        """
        Draws all gui objects in the list
        """
        for (gui_obj, col_pos, row_pos) in self._gui_objects:
            gui_obj.draw(self.image, ((self._width/self._columns) * col_pos, (self._height/self._rows) * row_pos), (self._width/self._columns, self._height/self._rows))

        cv2.imshow(self._window_name, self.image)



class Button:

    def __init__(self, callback, text, fontsize = 1, thickness = 1, btn_color = (255,0,0), txt_color = (255,255,255), background_color = (0,0,0)):
        """
        Contains some basic functions necessary to draw and keep track of a button.
        :param text: Contains the text of the text to be displayed in the button
        :param fontsize: The font size of the text
        :param thickness: The thickness of the button border and text
        :param btn_color: The color of the button
        :param txt_color: The color of the text
        :param callback: The callback function of the button
        :return: None
        """
        self._background_color = background_color
        self._mouse_is_pressed = False
        self._btn_filled = False
        self._to_be_hidden = False
        self._orig_thick = thickness
        self._text = text
        self._btn_color = btn_color
        self._txt_color = txt_color
        self._fontsize = fontsize
        self._txt_thickness = thickness
        self._rec_thickness = thickness
        self._callback = callback
        self._size = None
        self._position = None


    def mouse_event(self, event, x, y, flag, param):
        """
        Checks if the event is either left button is pressed down, released of if the mouse is moved. If the left
        button is pressed down then highlight (fill) the button the mouse hovers over. If the mouse moves between buttons
        the current button is highlighted while the former is returned to normal. If the left mouse button is released
        while over a button, said buttons callback is run.
        :param event: The specific button event (cv2.cv.CV_....)
        :param x: The x position of the cursor
        :param y: The y position of the cursor
        :return:None
        """
        if event == cv2.cv.CV_EVENT_LBUTTONDOWN:
            self._mouse_is_pressed = True
            if self.mouse_over((x,y)):
                self.btn_fill(True)
        elif event == 4:    #cv2.cv.CV_EVENT_LBUTTONUP:
            self._mouse_is_pressed = False
            if self.mouse_over((x,y)):
                self.run_callback()
        elif event == cv2.cv.CV_EVENT_MOUSEMOVE and self._mouse_is_pressed:
            if self.mouse_over((x,y)):
                self.btn_fill(True)
            else:
                self.btn_fill(False)



    def btn_fill(self, fill = True):
        """
        Fills or removes the inner part of a buttonborder with the button color
        :param btn: The button object that is to be filled
        :param fill: True by default, meaning that the button object is to be filled. If False, the button object is to be emptied
        :return: does not return
        """
        if not fill:
            self._btn_filled = False
            self._to_be_hidden = True
        else:
            self._btn_filled = True

    def draw(self, image, btn_pos, btn_size):
        """
        Draws a button of specified position and size. Button is drawn with the color, text and other instance-specific
        parameters. Then returns the image it has drawn on.
        :param image: The image on wich to draw
        :param btn_pos: The position of the button
        :param btn_size: The size of the button
        :return: Returns the new image
        """
        self._position = btn_pos
        self._size = btn_size

        if self._to_be_hidden:
            self.hide(image, self._background_color)
        if self._btn_filled:
            self._rec_thickness = -1
        else:
            self._rec_thickness = self._orig_thick


        pt1 = self._position
        pt2 = (self._position[0] + self._size[0], self._position[1] + self._size[1])
        textpos = (pt1[0] + 5 , pt1[1] + (self._size[1]/3))

        cv2.rectangle(image, pt1, pt2, self._btn_color, thickness=self._rec_thickness)
        cv2.putText(image, self._text, textpos, cv2.FONT_HERSHEY_SIMPLEX, self._fontsize, self._txt_color, thickness=self._txt_thickness)


    def run_callback(self):
        """
        Runs the buttons callback function
        :return:
        """
        self._callback()


    def mouse_over(self, mouse_pos):
        """
        Checks if the mouse is currently hovering over the button. If so, then returns True, otherwise False.
        Also returns false if the button has not been drawn.
        :param mouse_pos: The current position of the mouse
        :return: Returns True if the button occupies the current space of the button, otherwise False
        """
        if self._size and self._position:
            if mouse_pos[0] > self._position[0] and mouse_pos[0] < self._position[0] + self._size[0] and\
                mouse_pos[1] < self._position[1] + self._size[1] and mouse_pos[1] > self._position[1]:
                return True
            else:
                return False
        else:
            return False

    def hide(self, image, background_color):
        """
        Writes over itselfe with the given background color
        :param image: The image the button is drawn on
        :param background_color: The background color of the image
        :return: Returns the new image
        """
        if self._position and self._size:
            cv2.rectangle(image, self._position, (self._position[0] + self._size[0], self._position[1] + self._size[1]), background_color, thickness=-1)


def test():
    print('callback is real')


def gui(callback):
    grid_1 = GUIManager((800,600), 4, 2)

    grid_1.add(Button(callback, "panda"), (2, 1))
    grid_1.add(Button(callback, "pumba"), (0,0))
    grid_1.add(Button(callback, "pumba"), (0,1))
    grid_1.add(Button(callback, "pumba"), (1,0))
    grid_1.add(Button(callback, "pumba"), (1,1))

    #Setting mouse callback
    cv2.setMouseCallback('grid', grid_1.mouse_event, param=None)

    current_time = time.time()
    start_time = time.time()
    while current_time - start_time < 10:
        current_time = time.time()
        grid_1.draw()
        time.sleep(0.01)

gui(test)



cv2.destroyAllWindows()










