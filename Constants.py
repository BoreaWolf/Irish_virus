#
# Author: Riccardo Orizio
# Date: Thu 19 Mar 2020
# Description: 
#

DIR_DATA = "./Data"
IMG_IRELAND = DIR_DATA + "/Irish_map.jpg"

EXT_HTML = ".html"

DATE_FORMAT_SHORT = "%Y_%m_%d"
DATE_FORMAT_NICE = "%A %d %B %Y"

COUNTY_SETTINGS = { "Carlow":       { "pos": [ 500, 610 ], "color": "#D82894" },
                    "Cavan":        { "pos": [ 420, 310 ], "color": "#532DA9" },
                    "Clare":        { "pos": [ 210, 550 ], "color": "#D7C56D" },
                    "Cork":         { "pos": [ 250, 780 ], "color": "#DCA912" },
                    "Donegal":      { "pos": [ 350, 150 ], "color": "#8DF59D" },
                    "Dublin":       { "pos": [ 580, 475 ], "color": "#2AB32D" },
                    "Galway":       { "pos": [ 225, 450 ], "color": "#D79571" },
                    "Kerry":        { "pos": [ 130, 750 ], "color": "#FD2C3C" },
                    "Kildare":      { "pos": [ 510, 500 ], "color": "#17D065" },
                    "Kilkenny":     { "pos": [ 450, 650 ], "color": "#E2929B" },
                    "Limerick":     { "pos": [ 250, 630 ], "color": "#172ADE" },
                    "Longford":     { "pos": [ 400, 380 ], "color": "#EED9DF" },
                    "Louth":        { "pos": [ 570, 340 ], "color": "#2344DE" },
                    "Mayo":         { "pos": [ 200, 300 ], "color": "#4461D9" },
                    "Meath":        { "pos": [ 520, 375 ], "color": "#F273E3" },
                    "Offaly":       { "pos": [ 400, 490 ], "color": "#2B86BD" },
                    "Roscommon":    { "pos": [ 330, 380 ], "color": "#97F348" },
                    "Sligo":        { "pos": [ 290, 290 ], "color": "#D7CB30" },
                    "Tipperary":    { "pos": [ 380, 600 ], "color": "#0D05A1" },
                    "Waterford":    { "pos": [ 400, 710 ], "color": "#60D4C5" },
                    "Westmeath":    { "pos": [ 420, 410 ], "color": "#8F8BEB" },
                    "Wexford":      { "pos": [ 525, 650 ], "color": "#C755D4" },
                    "Wicklow":      { "pos": [ 540, 520 ], "color": "#0F20CB" } }

GRAPH_SIZE = ( 800, 600 )
MAP_PATCH_SIZE = ( 5, 150 )

DATA_SOURCE = "https://www.gov.ie/en/news/7e0924-latest-updates-on-covid-19-coronavirus/"
