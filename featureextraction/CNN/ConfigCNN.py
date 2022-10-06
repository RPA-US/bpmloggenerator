from os.path import join as pjoin
import os


class Config:

    def __init__(self, model_path, cnn_type="custom-v2"):
        # setting CNN (graphic elements) model
        self.image_shape = (64, 64, 3)

        self.project_root = os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).find("detección")+13]
        
        if cnn_type == "custom-v2":
            self.CNN_PATH = model_path
            self.element_class = ['button',
                                'checkbox_checked',
                                'checkbox_unchecked',
                                'image',
                                'radio',
                                'scroll',
                                'seekbar',
                                'text',
                                'text_input',
                                'toggle_switch']
            self.class_number = len(self.element_class)

            self.COLOR = {'button': (0, 255, 0), 'checkbox_checked': (0, 0, 255), 'checkbox_unchecked': (255, 166, 166),
                        'image': (255, 166, 0),
                        'radio': (77, 77, 255), 'scroll': (166, 0, 255),
                        'seekbar': (166, 166, 166),
                        'text': (0, 166, 255), 'text_input': (50, 21, 255),
                        'toggle_switch': (80, 166, 66),
                        'Compo':(0, 0, 255), 'Text':(169, 255, 0), 'Block':(80, 166, 66)}
