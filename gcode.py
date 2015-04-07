#Tool Information you can and should change this...
#       Tool Name |    Tool size
tool = [["Specialty Bit",       0.498],     #1
        ["V-Groove Bit",        0.0],       #2
        ["Slot Cutter",         1.942],     #3
        ["4mm Toe Kick Slot",   0.0],       #4
        ["1/2 Compression",     0.498],     #5
        ["1/4 Bit",             0.225],     #6
        ["3/8 Bit",             0.370],     #7
        ["Surfacing Bit",       3.75]]      #8

fileOutHeader = ["(BRAD RULES)",
    "(SIMPLE CUTOUT)",
    "G20", # Set's input to inch.
    "G91 G28 Z0 M15",
    "G90 G40 G49 M22",
    "M25",
    "M06",
    "G08 P1"]

fileOutFooter =  ["G0 Z1.2500 M59",
    "G40",
    "G91 G28 Z0 M15",
    "G90 G49 H0 M22",
    "M25",
    "M88 B0",
    "M89 B0",
    "G08 P0",
    "G0 X60.0 Y120.0"]
