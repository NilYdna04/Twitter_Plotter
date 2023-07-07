# plotter.py
# Created by Andrew Lin
# Last edited: 7/5/2023
# 
# The plotter class plots the data of the provided excel file. The file must
# fit the guidlines of the README for this class to function. The class will
# use the data and create bubble charts of the 'Total Tweets' and 
# 'Total Followers' columns. It will then create a word cloud of the most
# frequent words in the user's tweet data. All figures will be saved to a
# directory named 'data'
# 

import pandas as pd
import matplotlib.pyplot as plt
import circlify
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS
import random
import os

class plotter:
    # Variable for the Dataframe
    user_data = None

    def __init__(self):
        pass

    
    # Name: getRandomColor
    # Input: none
    # Output: the code of a color
    # Purpose: Randomly generates a color for use in charts
    def getRandomColor(self):
        color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        return color

    # Name: printBubbleChart
    # Input: name of data to be plotted
    # Output: saves chart to folder named 'data'
    # Purpose: prints out a bubblechart of a column of numerical data
    def printBubbleChart(self, dataType):
        # Sort the data based on which column to be printed
        sorted_data = self.user_data.sort_values(by=[dataType], axis = 0)
        # create the circles for the plot
        circles = circlify.circlify(
            sorted_data[dataType].tolist(), 
            show_enclosure=False, 
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )
        # create the figure
        fig, ax = plt.subplots(figsize=(10,10))
        ax.axis('off')
        ax.set_title(dataType)

        # Find axis boundaries
        lim = max(
            max(
                abs(circle.x) + circle.r,
                abs(circle.y) + circle.r,
            )
            for circle in circles
        )
        plt.xlim(-lim, lim)
        plt.ylim(-lim, lim)

        # Create labels for circles
        labels = sorted_data['Name'].tolist()
        numbers = sorted_data[dataType].tolist()

        # print circles
        for circle, label, number in zip(circles, labels, numbers):
            x, y, r = circle
            ax.add_patch(plt.Circle((x, y), r, alpha=0.2, linewidth=2, facecolor=self.getRandomColor()))
            plt.annotate(
                label + "\n" + str(number),
                (x,y ),
                va='center',
                ha='center'
            )
            # save the figure to folder
            plt.savefig('./data/' + dataType)

    # Name: printWordCloud
    # Input: none
    # Output: saves word cloud to folder named 'data'
    # Purpose: creates a word cloud of the tweets column
    def printWordCloud(self):
        # get text for the word cloud
        text = " ".join(i for i in self.user_data['Tweets'])
        # remove some common words
        stopwords = set(STOPWORDS)
        # create wordcloud
        wordcloud = WordCloud(stopwords=stopwords, background_color="white", width = 1600, height = 800).generate(text)
        plt.figure(figsize=(20,10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        # save the figure to folder
        plt.savefig('./data/Tweets')

    # Name: getData
    # Input: file name
    # Output: none
    # Purpose: saves the data of the excel file to local data frame
    def getData(self, file):
        try:
            self.user_data = pd.read_excel(file)
        except:
            print("Error: file could not be opened")

    def run(self, file):
        # Get the data
        self.getData(file)
        # Create directory if needed
        if(not os.path.exists('./data')):
            os.mkdir('./data')
        # create and save charts
        self.printBubbleChart('Total Tweets')
        self.printBubbleChart('Total Followers')
        self.printWordCloud()