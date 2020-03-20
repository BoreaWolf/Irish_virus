#
# Author: Riccardo Orizio
# Date: Thu 19 Mar 2020
# Description: Showing the evolution of the virus in Ireland
# Source: https://www.gov.ie/en/news/7e0924-latest-updates-on-covid-19-coronavirus/
#

import Constants

import argparse
import bs4
from datetime import datetime
import glob
import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import plotly.graph_objects as go
import re
import streamlit as st
from typing import Dict, List

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLASSES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class Information:
    """ Class representing some type of information

    :ivar description: (str) Describing the information carried
    :ivar number: (int) Corresponding number
    :ivar rate: (float) Rate of the current information compared to the population
    :ivar info_type: (str) Type of information, group
    """

    def __init__( self,
                  description: str,
                  number: str,
                  rate: str,
                  info_type: str ):
        self.description = description
        try:
            self.number = int( re.findall( r"([0-9.,]+)", number )[ 0 ] )
        except IndexError:
            self.number = 0
        try:
            self.rate = float( re.findall( r"([0-9.,]+)", rate )[ 0 ] )
        except IndexError:
            self.rate = 0
        self.info_type = info_type

    def __str__( self ):
        return "{} - {}: {} ({:.3f}%)".format( self.info_type,
                                               self.description,
                                               self.number,
                                               self.rate )

    def __repr__( self ):
        return str( self )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def parse_html_table( table: bs4.element.Tag ) -> Dict[ str, List[ str ] ]:
    """ Parsing an html table to a dictionary

    :param table:
    :type table:
    :return:
    :rtype:
    """

    result = { "cols": [ ], "data": [ ] }
    for row in table.find_all( "tr" ):
        # Currently the title of the table is highlighted with a strong tag
        result[ "data" if row.strong is None else "cols" ].append( [ el.text.strip()
                                                                     for el in row.find_all( "td" )
                                                                     if el ] )
    return result


def clean_table_title( title: bs4.element.Tag ) -> str:
    """

    :param title:
    :type title:
    :return:
    :rtype:
    """

    return title.text.strip()


def markdown_table( data: Dict[ str, List[ str ] ],
                    title: str ) -> str:
    """ Creating the markdown syntax to build a table

    :param data: Table data
    :type data: Dict[ str, List[ str ] ]
    :param title: Title of the section before printing the table
    :type title: str
    :return: The formatted string to generate the table
    :rtype: str
    """

    result = "## {}\n".format( title )
    result += "|".join( data.keys() ) + "\n"
    result += "|".join( [ "---" ] * len( data.keys() ) ) + "\n"
    for row in zip( *data.values() ):
        result += "|".join( [ str( el ) for el in row ] ) + "\n"
    return result


def rescale_patch_size( current_value: float ) -> int:
    """ Rescaling the value to the patch limits

    :param current_value:
    :type current_value:
    :return:
    :rtype:
    """

    return int( current_value * Constants.MAP_PATCH_SIZE[ 1 ] + Constants.MAP_PATCH_SIZE[ 0 ] )


def plot_map( data: List[ Information ] ):
    """ Printing the Irish map with information for each county

    :param data: Data to show
    :type data: List[ Information ]
    :return: None
    :rtype: None
    """

    map_figure = plt.figure( num=None, figsize=( 8, 6 ), dpi=100 )
    ax = map_figure.add_subplot( 111 )
    ax.imshow( np.array( Image.open( Constants.IMG_IRELAND ), dtype=np.uint8 ) )
    max_size = max( [ el.number for el in data ] )
    for county in Constants.COUNTY_SETTINGS:
        current_county = [ c for c in data if c.description == county ][ 0 ]
        ax.add_patch( matplotlib.patches.Circle( Constants.COUNTY_SETTINGS[ county ][ "pos" ],
                                                 rescale_patch_size( current_county.number / max_size ),
                                                 label=current_county.number,
                                                 color=Constants.COUNTY_SETTINGS[ county ][ "color" ],
                                                 alpha=0.7 ) )
        plt.text( *Constants.COUNTY_SETTINGS[ county ][ "pos" ], current_county.number )
    ax.axis( "off" )


def plot_bar_chart( data: Dict[ str, float ],
                    title: str = None,
                    legend: bool = False ) -> go.Figure:
    """ Creating a plotly bar chart

    :param data: Data to show
    :type data: Dict[ str, float ]
    :param title: Title of the graph
    :type title: str, optional, default = None
    :param legend: Flag to indicate the use of the legend
    :type legend: bool, optional, default = False
    :return: The plotly figure to print
    :rtype: go.Figure
    """

    fig = go.Figure()
    fig.add_trace( go.Bar( x=list( data.keys() ),
                           y=list( data.values() ),
                           text=list( data.values() ),
                           textposition="auto",
                           name="Sbra" ) )

    layout = { "showlegend": legend,
               "width": Constants.GRAPH_SIZE[ 0 ],
               "height": Constants.GRAPH_SIZE[ 1 ] }
    if title is not None:
        layout[ "title" ] = title
    fig.update_layout( layout )

    return fig


def plot_pie_chart( data: Dict[ str, float ],
                    title: str = None,
                    legend: bool = False ):
    """ Creating a plotly pie chart

    :param data: Data to show
    :type data: Dict[ str, float ]
    :param title: Title of the graph
    :type title: str, optional, default = None
    :param legend: Flag to indicate the use of the legend
    :type legend: bool, optional, default = False
    :return: The plotly figure to print
    :rtype: go.Figure
    """

    fig = go.Figure()
    fig.add_trace( go.Pie( labels=list( data.keys() ),
                           values=list( data.values() ) ) )

    layout = { "showlegend": legend,
               "width": Constants.GRAPH_SIZE[ 0 ],
               "height": Constants.GRAPH_SIZE[ 1 ] }
    if title is not None:
        layout[ "title" ] = title
    fig.update_layout( layout )

    return fig


def plot_line_chart( data: Dict[ str, Dict[ str, float ] ],
                     title: str = None,
                     legend: bool = False ):
    """ Creating a plotly line chart

    :param data: Data to show
    :type data: Dict[ str, Dict[ str, float ] ]
    :param title: Title of the graph
    :type title: str, optional, default = None
    :param legend: Flag to indicate the use of the legend
    :type legend: bool, optional, default = False
    :return: The plotly figure to print
    :rtype: go.Figure
    """

    fig = go.Figure()
    for county in data.keys():
        x_axis = sorted( data[ county ].keys() )
        fig.add_trace( go.Scatter( x=x_axis,
                                   y=[ data[ county ][ x ] for x in x_axis ],
                                   mode="lines+markers",
                                   name=county ) )

    layout = { "showlegend": legend,
               "width": Constants.GRAPH_SIZE[ 0 ],
               "height": Constants.GRAPH_SIZE[ 1 ],
               "yaxis": { "rangemode": "tozero" } }
    if title is not None:
        layout[ "title" ] = title
    fig.update_layout( layout )

    return fig

@st.cache
def load_file( file_name: str ) -> List[ Information ]:
    """ Loading file and caching it to avoid repetitive actions

    :param file_name: File name to read
    :type file_name: str
    :return: The information read from the given file
    :rtype: List[ Information ]
    """

    with open( file_name, "r" ) as input_file:
        file_content = bs4.BeautifulSoup( input_file, features="html.parser" )

    result = [ ]

    for parsed_table, table_title in zip( [ parse_html_table( t ) for t in file_content.find_all( "table" ) ],
                                          [ clean_table_title( t ) for t in file_content.find_all( "h2" ) ] ):

        for row in parsed_table[ "data" ]:
            # Extending the row if needed
            row.extend( [ "" ] * ( 3 - len( row ) ) )
            result.append( Information( row[ 0 ],
                                        row[ 1 ],
                                        row[ 2 ],
                                        table_title ) )

    # Calculating the rates for the counties since they are not provided
    number_cases = sum( [ el.number for el in result if "county" in el.info_type ] )
    for county in [ el for el in result if "county" in el.info_type ]:
        county.rate = county.number / number_cases * 100

    return result


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def main():
    # region Command Line arguments
    # Reading arguments from command line
    arg_parser = argparse.ArgumentParser( description="<description>" )
    arg_parser.add_argument( "--save", dest="save", default=False, action="store_true",
                             help="Flag to indicate if the results have to be saved on file or not" )

    input_args = vars( arg_parser.parse_args() )
    # endregion

    data = { }
    # Read all data from files
    for file_name in glob.glob( "{}/*{}".format( Constants.DIR_DATA, Constants.EXT_HTML ) ):
        data[ os.path.basename( file_name ).replace( Constants.EXT_HTML, "" ) ] = load_file( file_name )

    st.sidebar.title( "Irish virus" )
    selected_date = st.sidebar.selectbox( "Select date: ",
                                          sorted( data.keys(), reverse=True ),
                                          format_func=lambda x: datetime.strptime( x, Constants.DATE_FORMAT_SHORT )
                                                                        .strftime( Constants.DATE_FORMAT_NICE ) )
    show_raw_data = st.sidebar.checkbox( "Show raw data" )

    st.sidebar.markdown( "Data source: {}".format( Constants.DATA_SOURCE ) )

    # Showing the evolution through time
    st.markdown( "## Currently infected: {}".format( sum( [ el.number for el in data[ max( data.keys() ) ]
                                                            if "county" in el.info_type ] ) ) )
    st.markdown( "## Evolution" )
    selected_counties = st.multiselect( "Select counties: ",
                                        sorted( Constants.COUNTY_SETTINGS.keys() ) )

    if not selected_counties:
        evolution_data = { "Total": { d: sum( [ el.number for el in data[ d ] if "county" in el.info_type ] )
                                      for d in data.keys() } }
    else:
        evolution_data = { c: { d: [ el.number for el in data[ d ]
                                     if "county" in el.info_type and el.description == c ][ 0 ]
                                for d in data.keys() }
                           for c in selected_counties }

    st.plotly_chart( plot_line_chart( evolution_data,
                                      legend=True ) )

    # Showing a map of Ireland with the corresponding values per county
    selected_data = [ el for el in data[ selected_date ] if "county" in el.info_type ]
    st.markdown( "## {}".format( datetime.strptime( selected_date,
                                                    Constants.DATE_FORMAT_SHORT )
                                 .strftime( Constants.DATE_FORMAT_NICE ) ) )
    st.markdown( "## Counties" )
    st.markdown( "Infected: {}".format( sum( [ el.number for el in selected_data ] ) ) )
    plot_map( selected_data )
    st.pyplot()
    st.plotly_chart( plot_bar_chart( { el.description: el.number for el in selected_data },
                                     title="County" ) )

    for info in set( [ el.info_type for el in data[ selected_date ] if "county" not in el.info_type ] ):
        selected_data = [ el for el in data[ selected_date ] if el.info_type == info ]

        if "age" in info.lower() or "cluster" in info.lower():
            st.plotly_chart( plot_bar_chart( { el.description: el.number for el in selected_data
                                               if "Total" not in el.description },
                                             title=info ) )

        elif "statistics" in info.lower():
            st.markdown( markdown_table( { "Type": [ el.description for el in selected_data ],
                                           "Number": [ el.number for el in selected_data ],
                                           "Rate": [ "{:.3f}%".format( el.rate ) for el in selected_data ] },
                                         info ) )

        else:
            st.plotly_chart( plot_pie_chart( { el.description: el.number for el in selected_data
                                               if "Total" not in el.description },
                                             title=info,
                                             legend=True ) )

    # Showing all the raw data
    if show_raw_data:
        for info in set( [ el.info_type for el in data[ selected_date ] ] ):
            selected_data = [ el for el in data[ selected_date ] if el.info_type == info ]
            st.markdown( markdown_table( { "Type": [ el.description for el in selected_data ],
                                           "Number": [ el.number for el in selected_data ],
                                           "Rate": [ "{:.3f}%".format( el.rate ) for el in selected_data ] },
                                         info ) )
    
    st.sidebar.markdown( "Reference: [GitHub Project]({})".format( Constants.GITHUB_REPO ) )
    #   st.sidebar.markdown( "[![GitHub Project]({})]({})".format( Constants.GITHUB_LOGO,
    #                                                              Constants.GITHUB_REPO ) )


if __name__ == "__main__":
    main()
