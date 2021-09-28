from plugins.screenshot import replace_gui_component

# In this JSON is specified all functions available for each type of GUI component
gui_component_classes = {
    "ImageView": {
        "transformations": {
            replace_gui_component
        }
    },
    "ImageButton": {
        "transformations": {
            replace_gui_component
        }
    },
    "Button": {
        "transformations": {
            replace_gui_component
        }
    },
    "Spinner": {
        "transformations": {
            replace_gui_component
        }
    },
    "RatingBar": {
        "transformations": {
            replace_gui_component
        }
    },
    "NumberPicker": {
        "transformations": {
            replace_gui_component
        }
    },
    "ToggleButton": {
        "transformations": {
            replace_gui_component
        }
    },
    "SeekBar": {
        "transformations": {
            replace_gui_component
        }
    },
    "Switch": {
        "transformations": {
            replace_gui_component
        }
    },
    "ProgressBar": {
        "transformations": {
            replace_gui_component
        }
    },
    "RadioButton": {
        "transformations": {
            replace_gui_component
        }
    },
    "CheckBox": {
        "transformations": {
            replace_gui_component
        }
    },
    "CheckedTextView": {
        "transformations": {
            replace_gui_component
        }
    },
    "EditText": {
        "transformations": {
            replace_gui_component
        }
    }
}
