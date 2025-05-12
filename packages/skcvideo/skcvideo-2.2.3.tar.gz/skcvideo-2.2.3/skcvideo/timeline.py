import cv2
import numpy as np

from skcvideo.colors import BLACK, RED, WHITE
from skcvideo.core import Button
from skcvideo.utils import put_text


class Timeline:
    """
    A widget representing a timeline which can be used to display some information in color.
    Arguments:
        box (list): coordinates of the delimitation of the widget
        timeline_width (int): width of the timeline in pixels
        margin (int): gap between two lines in pixels
        minute_per_line (int): time represented on one line of the timeline
        ticks (int): intervals used to draw white bars on the timeline
        fps (int): framerate of the information to be displayed
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, box=None, timeline_width=20, margin=5, minute_per_line=3, ticks=10, fps=10, *args, **kwargs):
        if box is None:
            box = [955, 110, 1035, 1910]
        self.name = "Timeline"
        self.box = box
        self.fps = fps
        self.ticks = ticks

        self.timeline_length = self.box[3] - self.box[1]

        self.pixel_per_frame = self.timeline_length / (minute_per_line * 60 * self.fps)

        self.frame_banner_flag = "with_frame_banner" in kwargs
        self.fontsize = kwargs.get("fontsize", 1.5)

        self.timeline_width = timeline_width
        self.margin = margin
        self.gap = self.timeline_width + 2 * self.margin

        self.hitbox = (self.box[1], self.box[0], self.box[3], self.box[2])
        self.buttons = [Button(self.hitbox, self.jump_event)]
        if self.frame_banner_flag:
            self.mouse_position_x = None
            self.mouse_position_y = None
            self.move_mouse_events = [Button(self.hitbox, self.set_mouse_coordinates)]

    @property
    def min_frame(self):
        return getattr(self.parent, "min_frame", 0)

    @property
    def max_frame(self):
        return getattr(self.parent, "max_frame", 9000)

    @property
    def n_timelines(self):
        _, y = self.frame_to_position(self.max_frame)
        return y + 1

    def frames(self):
        """Generator that yields each frame in the timeline."""
        end_x, max_y = self.frame_to_position(self.max_frame)
        end_x = int(np.ceil(end_x))
        for y in range(max_y + 1):
            if y == max_y:
                max_x = end_x
            else:
                max_x = self.timeline_length

            for x in range(max_x + 1):
                frame = self.position_to_frame(x, y)
                if frame >= self.max_frame:
                    return
                yield frame

    def jump_event(self, x, y, *args, **kwargs):
        frame = self.get_frame(x, y)
        self.parent.jump(frame)

    def set_mouse_coordinates(self, x, y, *args, **kwargs):
        self.mouse_position_x, self.mouse_position_y = x, y

    def timeline_color(self, frame):
        """
        Here you define the color of the timeline with repect to the frame.
        """
        return None

    def build(self, image):
        """
        Draws the timeline's background composed of several timeline lines
        with box and graduations.
        """
        # Puts time labels label
        put_text(
            img=image,
            text="min",
            org=(self.box[1] - 90, self.box[0] - self.margin - self.timeline_width // 2),
            fontScale=0.6,
            align_x="left",
        )

        # Draws graduations labels
        for x in range(0, self.timeline_length):
            frame = self.position_to_frame(x, 0)
            second = frame / self.fps

            if second % 60 == 0:
                second = int(second)
                put_text(
                    img=image,
                    text=f"{second // 60}min",
                    org=(self.box[1] + x, self.box[0] - self.margin - self.timeline_width // 2 - 2),
                    fontScale=0.6,
                    align_x="center",
                )
            elif second % self.ticks == 0:
                second = int(second)
                put_text(
                    img=image,
                    text=f"{second % 60}s",
                    org=(self.box[1] + x, self.box[0] - self.margin - self.timeline_width // 2 + 4),
                    fontScale=0.4,
                    align_x="center",
                )

        # Draws each timeline's line
        for i in range(self.n_timelines):
            self.draw_timeline_box(image, i)

        # Draws graduations
        for frame in range(self.min_frame, self.max_frame):
            x, y = self.frame_to_position(frame)
            x = int(round(x))
            second = frame / self.fps

            # A small mark every 5 seconds
            if (second % 5) == 0:
                cv2.line(
                    image,
                    (self.box[1] + x, self.box[0] + y * self.gap + self.margin - 1),
                    (self.box[1] + x, self.box[0] + (y + 1) * self.gap - self.margin + 1),
                    color=WHITE,
                    thickness=1,
                )

            # A big mark every minute
            if (second % 60) == 0:
                cv2.line(
                    image,
                    (self.box[1] + x, self.box[0] + y * self.gap + self.margin - 3),
                    (self.box[1] + x, self.box[0] + (y + 1) * self.gap - self.margin + 3),
                    color=WHITE,
                    thickness=2,
                )

        self.draw_timeline_data(image)

    def refresh(self, image, frame):
        self.draw_timer(image, frame)

    def draw_timeline_box(self, image, y):
        """
        Draws one line of the timeline's background, which consists in a
        simple white box.
        """
        # Manage the offset
        y_min = self.box[0] + self.margin + y * self.gap
        y_max = y_min + self.timeline_width

        max_x, max_y = self.frame_to_position(self.max_frame)
        max_x = int(np.ceil(max_x))

        # The last box may not go up to the end.
        if y == max_y:
            timeline_max = self.box[1] + max_x
        else:
            timeline_max = self.box[3]

        # Draws the box
        cv2.rectangle(
            image,
            (self.box[1], y_min),
            (timeline_max, y_max),
            color=WHITE,
            thickness=1,
        )

        # Adds a time label before the line
        min_frame = self.position_to_frame(0, y)
        min_second = min_frame / self.fps
        min_minute = int(np.floor(min_second / 60))
        max_frame = self.position_to_frame(self.timeline_length, y)
        max_second = max_frame / self.fps
        max_minute = int(np.ceil(max_second / 60))
        put_text(
            img=image,
            text=f"{min_minute}-{max_minute}",
            org=(self.box[1] - 90, (y_min + y_max) // 2),
            fontScale=0.6,
            align_x="left",
        )

    def draw_timeline_data(self, im):
        """
        Draws information on the timeline. Useful to have a global view of
        your data or to have a reference for jumping in the video.
        """
        for frame in self.frames():
            color = self.timeline_color(frame)
            self.draw_one_timeline_data(im, frame, color)

    def draw_one_timeline_data(self, im, frame, color):
        """
        Colors the given frame on the timeline according to the timeline_color
        function
        """
        x, y = self.frame_to_position(frame)
        x = int(round(x))
        if color is not None:
            x1 = self.box[1] + x
            x2 = x1 + int(np.ceil(self.pixel_per_frame))
            y1 = y * self.gap + self.box[0] + self.margin + 1
            y2 = y1 + self.timeline_width - 2
            im[y1:y2, x1:x2] = color

    def draw_timer(self, image, frame):
        """
        Draws a timer on the timeline on the given frame. To be used in the
        refresh method of the parent Reader class.
        """
        timer_x, timer_y = self.frame_to_position(frame)
        timer_x = int(round(timer_x))
        cv2.line(
            image,
            (self.box[1] + timer_x, timer_y * self.gap + self.box[0]),
            (self.box[1] + timer_x, (timer_y + 1) * self.gap + self.box[0]),
            color=WHITE,
            thickness=3,
        )
        cv2.line(
            image,
            (self.box[1] + timer_x, timer_y * self.gap + self.box[0]),
            (self.box[1] + timer_x, (timer_y + 1) * self.gap + self.box[0]),
            color=RED,
            thickness=2,
        )
        if self.frame_banner_flag and self.mouse_position_x is not None:
            frame_on_mouse = self.get_frame(self.mouse_position_x, self.mouse_position_y)
            if frame_on_mouse > 0:
                self.draw_frame_banner_on_image(image, frame_on_mouse, self.mouse_position_x, self.mouse_position_y)

    def draw_frame_banner_on_image(self, image, number, x, y):
        """
        Draws a banner with the given frame on the timeline.
        """
        number_str = str(number)

        alpha = 0.7
        overlay = image.copy()

        (text_height, text_width), _ = cv2.getTextSize(
            text=number_str, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=self.fontsize, thickness=2
        )

        banner_width = text_width + 10
        banner_height = text_height + 5

        if x + banner_height > self.box[3]:
            rect_start, rect_end = (x - banner_height, y), (x, y - banner_width)
            text_x = x - banner_height // 2
        else:
            rect_start, rect_end = (x, y), (x + banner_height, y - banner_width)
            text_x = x + banner_height // 2

        text_y = y - banner_width // 2

        cv2.rectangle(overlay, rect_start, rect_end, WHITE, -1)
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

        put_text(
            image,
            number_str,
            (text_x, text_y),
            color=BLACK,
            thickness=2,
            fontScale=self.fontsize,
            align_x="center",
            align_y="center",
        )

    def get_frame(self, x, y):
        """
        Returns the frame corresponding to a given pixel of the timeline.
        It is used to be able to click one the timeline to jump to a
        particular frame.
        """
        x = x - self.box[1]
        y = (y - self.box[0]) // self.gap
        frame = self.position_to_frame(x, y)
        return frame

    def position_to_frame(self, x, y):
        """
        Returns the frame corresponding to a given pixel of the timeline.
        x: position on one line of the timeline
        y: line number
        """
        frame = (x + y * self.timeline_length) / self.pixel_per_frame + self.min_frame
        frame = int(round(frame))
        return frame

    def frame_to_position(self, frame):
        """
        Returns the position of a given frame on the timeline.
        x: position on one line of the timeline
        y: line number
        """
        timer = (frame - self.min_frame) * self.pixel_per_frame
        x = timer % self.timeline_length
        y = timer // self.timeline_length
        y = int(y)
        return x, y


GRAY_BAR = np.array(
    [
        [189, 189, 190],
        [193, 193, 194],
        [196, 197, 198],
        [200, 201, 202],
        [204, 205, 206],
        [208, 208, 209],
        [212, 212, 213],
        [215, 216, 217],
        [219, 220, 221],
        [235, 235, 236],
    ],
)

BLUE_BAR = np.array(
    [
        [224, 137, 44],
        [218, 134, 43],
        [213, 130, 42],
        [207, 127, 41],
        [204, 125, 40],
        [204, 125, 40],
        [204, 125, 40],
        [204, 125, 40],
    ],
)


class VlcTimeline:
    def __init__(self, box=None):
        """
        Args:
            box: list [x1, y1, x2, y2]
        """
        if box is None:
            box = [79, 966, 1771, 976]
        self.box = box
        self.buttons = [Button(self.box, self.jump_event)]
        self.timeline_length = float(self.box[2] - self.box[0])

    @property
    def min_frame(self):
        return getattr(self.parent, "min_frame", 0)

    @property
    def max_frame(self):
        return getattr(self.parent, "max_frame", 9000)

    @property
    def frames_length(self):
        return float(self.max_frame - self.min_frame)

    def jump_event(self, x, y, *kwargs):
        frame = self.get_frame(x, y)
        self.parent.jump(frame)

    def build(self, image):
        image[self.box[1] : self.box[1] + 18] = np.array([240, 241, 242])[np.newaxis, np.newaxis, :]
        image[self.box[1] + 4 : self.box[1] + 14, self.box[0] : self.box[2]] = GRAY_BAR[:, np.newaxis, :]

    def refresh(self, image, frame):
        self.draw_timer(image, frame)

    def draw_timer(self, image, frame):
        frame = float(frame - self.min_frame)
        i = int(np.round(frame / self.frames_length * self.timeline_length))
        image[self.box[1] + 5 : self.box[1] + 13, self.box[0] : self.box[0] + i] = BLUE_BAR[:, np.newaxis, :]

    def get_frame(self, x, y):
        x = float(x - self.box[0])
        frame = int(np.round(x / self.timeline_length * self.frames_length)) + self.min_frame
        return frame
