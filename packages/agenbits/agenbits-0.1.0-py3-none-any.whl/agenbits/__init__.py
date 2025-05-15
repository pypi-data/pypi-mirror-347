from agenbits.interfaces import Excel, ImageFile, Audio, Text, Video, Binary

input_data = type("input_data", (), {
    "Excel": Excel,
    "Image": ImageFile,
    "Audio": Audio,
    "Text": Text,
    "Video": Video,
    "Binary": Binary
})()
