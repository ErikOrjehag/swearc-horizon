import cv2
import numpy as np
import pygame
import time

class ButtonGridManager:
    def __init__(self, grid_size):
        self._grid_size = grid_size
        self._grids = dict()

    """def new_grid(self, grid_name, grid_size, grid_columns, grid_rows, background_color = (0,0,0)):
        grid_name = ButtonGrid(grid_name, grid_columns, grid_rows, background_color)
        self._grids.append(grid_name)

    def add(self, statename, grid):
        self._grids[statename] = grid

    def update(self):
        self._grids[self.current_state].update();

    def on_click(self):
        .on_click()
    """




class ButtonGrid:

    def __init__(self, size_in, columns_in, rows_in, background_color = (0,0,0), window_name = 'grid'):
        self._columns = columns_in
        self._rows = rows_in
        self._height = size_in[1]
        self._width = size_in[0]
        self.buttons = []
        self._window_name = window_name
        self._mouse_is_pressed = False
        self._background_color = background_color

        #creating a new background image of the apporpriate size to write buttons on
        self.image = np.zeros((self._height, self._width, 3), dtype=np.uint8)
        self.image[:] = background_color
        cv2.startWindowThread()
        cv2.namedWindow(self._window_name)
        pygame.init()

    def add(self, button, col_pos, row_pos):
        """
        Creates a new button object and adds it to 'self.buttons'
        :param btn_event:
        :param text:
        :param fontsize:
        :param thickness:
        :param btn_color:
        :param txt_color:
        :return:
        """
        self.buttons.append((button, col_pos, row_pos))

    def draw(self):
        """
        Draw every button on the image
        """
        for (btn, col_pos, row_pos) in self.buttons:
            btn.draw(self.image, ((self._width/self._columns) * col_pos, (self._height/self._rows) * row_pos), (self._width/self._columns, self._height/self._rows))

        cv2.imshow(self._window_name, self.image)

    def btn_pressed(self, event, x, y, flag, param):
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
            for btn in self.buttons:
                if btn[0].mouse_over((x,y)):
                    self.btn_fill(btn, True)
        elif event == 4:    #cv2.cv.CV_EVENT_LBUTTONUP:
            self._mouse_is_pressed = False
            for btn in self.buttons:
                if btn[0].mouse_over((x,y)):
                    btn[0].run_callback()
        elif event == cv2.cv.CV_EVENT_MOUSEMOVE and self._mouse_is_pressed:
            for btn in self.buttons:
                if btn[0].mouse_over((x,y)):
                    self.btn_fill(btn, True)
                else:
                    self.btn_fill(btn, False)


    def btn_fill(self, btn, fill = True):
        """
        Fills or removes the inner part of a buttonborder with the button color
        :param btn: The button object that is to be filled
        :param fill: True by default, meaning that the button object is to be filled. If False, the button object is to be emptied
        :return: does not return
        """
        if not fill:
            btn[0].btn_filled = False
            btn[0].hide(self.image, self._background_color)
        else:
            btn[0].btn_filled = True



class Button:

    def __init__(self, callback, text, fontsize = 1, thickness = 1, btn_color = (255,0,0), txt_color = (255,255,255)):
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
        self.btn_filled = False
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

        if self.btn_filled:
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
            if mouse_pos[0] > self._position[0] and mouse_pos[0] < self._position[0] + self._size[0] and mouse_pos[1] < self._position[1] + self._size[1] and mouse_pos[1] > self._position[1]:
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
            self._position = None
            self._size = None


def test():
    print('callback is real')


def gui(callback):
    grid_1 = ButtonGrid((800,600), 4, 2)

    grid_1.add(Button(callback, "panda"), 2, 1)

    cv2.setMouseCallback('grid', grid_1.btn_pressed, param=None)


    current_time = time.time()
    start_time = time.time()
    while current_time - start_time < 10:
        current_time = time.time()
        grid_1.draw()
        time.sleep(1)


#size txt_size = cv2.getTextSize(text, fontFace=CV_FONT_HERSHEY_SIMPLEX, fontscale=fontsize, thickness=thick)
#grid = ButtonGrid(800, 600, 4, 2)
# grid.new_button(0,0,"panda", 'pandans_knapp')

gui(test)



cv2.destroyAllWindows()










