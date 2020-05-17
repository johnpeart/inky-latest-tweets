####################
## IMPORT MODULES ##
####################
# Built in modules

import sys # This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
import datetime # The datetime module supplies classes for manipulating dates and times.

# Third party modules

import keys # This module stores API credentials for use with the Twitter Developer API
import twitter # This module handles interactions with the Twitter Developer API
from accounts import accounts # This module stores a list of accounts to check
from PIL import Image, ImageFont, ImageDraw # This module handles creation of images and text, which are sent to the display
from inky import InkyWHAT # This module makes the e-ink display work and renders the image

##################################################
## IMPORT THE TWITTER DEVELOPER API CREDENTIALS ##
##################################################
# This sets your Twitter Developer API credentials.
# It imports the keys from 'keys.py', which is not included in the repository.
# The keys are in this format:
# 
# twitter = {
#     "consumer_key": "YOUR KEY HERE",
#     "consumer_secret": "YOUR KEY HERE",
#     "access_token_key": "YOUR KEY HERE",
#     "access_token_secret": "YOUR KEY HERE"
# }

api = twitter.Api(
    consumer_key = keys.twitter["consumer_key"],
    consumer_secret = keys.twitter["consumer_secret"],
    access_token_key = keys.twitter["access_token_key"],
    access_token_secret = keys.twitter["access_token_secret"]
)

##################################
## SET UP THE INKY WHAT DISPLAY ##
##################################
# Set the display type and colour
# InkyPHAT is for the smaller display and InkyWHAT is for the larger display.
# Accepts arguments 'red', 'yellow' or 'black', based on the display you have. 
# (You can only use 'red' with the red display, and 'yellow' with the yellow; but 'black' works with either).

inky = InkyWHAT("yellow")

img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
draw = ImageDraw.Draw(img)

#################
## REFLOW TEXT ##
#################
# This function reflows text across multiple lines.
# It is adapted from the Pimoroni guidance for the Inky wHAT.

def reflow_text(textToReflow, width, font):
    words = textToReflow.split(" ")
    reflowed = ''
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n" + word

    return reflowed

##########################
## IMPORT FONTS FOR USE ##
##########################
# ImageFont.truetype accepts two arguments, (1, 2):
# 1. "path/to/font" - where path/to/font is the path to the .ttf file
# 2. font size - as an integer

headerFontSize = 18
tweetFontSize = 16
accountFontSize = 16
updateFont = 12

headerFont = ImageFont.truetype("/home/pi/inky-twitter/fonts/iAWriterMonoS-Bold.ttf", headerFontSize)
tweetFont = ImageFont.truetype("/home/pi/inky-twitter/fonts/iAWriterMonoS-Regular.ttf", tweetFontSize)
accountFont = ImageFont.truetype("/home/pi/inky-twitter/fonts/iAWriterMonoS-Bold.ttf", accountFontSize)
updateFont = ImageFont.truetype("/home/pi/inky-twitter/fonts/iAWriterMonoS-Bold.ttf", updateFont)

###########################
## ADD BACKGROUND STYLES ##
###########################

headerText = "Latest tweets"
headerTextWidth, headerTextHeight = headerFont.getsize(headerText)
headerPadding = 5
headerWidth, headerHeight = inky.WIDTH, headerTextHeight + (headerPadding * 2)

ImageDraw.Draw(img).rectangle([(0, 0), (headerWidth, headerHeight)], fill = inky.YELLOW, outline=None)
draw.text((headerPadding, headerPadding), headerText, inky.WHITE, headerFont)

###############################
## GET AND RENDER THE TWEETS ##
###############################
# For each account defined in 'accounts.py', this function gets the latest tweet and prepares it for rendering.
# Note that this function uses inky.YELLOW as I'm using a Yellow Inky wHAT; use that, .BLACK or .RED as appropriate for yours.

startDraw = 0 # Sets a variable to track the vertical height of the drawn content

for twitterUsername, twitterDisplayname in accounts.items():
    print('Twitter handle: ', twitterUsername)
    print('Display name: ', twitterDisplayname)
    def displayTweets(handle):
        statuses = api.GetUserTimeline(screen_name=twitterUsername)
        return statuses[0].text
    if __name__ == "__main__":
        latest_tweet = displayTweets(sys.argv[1] if len(sys.argv) > 1 else 0)
        reflowed_latest_tweet = reflow_text(latest_tweet, inky.WIDTH, tweetFont)
        startDraw = startDraw + headerHeight + headerPadding
        draw.text((0, startDraw), twitterDisplayname, inky.YELLOW, accountFont)
        accountTextWidth, accountTextHeight = accountFont.getsize(twitterDisplayname)
        startDraw = startDraw + accountTextHeight + (headerPadding / 2)
        draw.text((0, startDraw), reflowed_latest_tweet, inky.BLACK, tweetFont)
        tweetTextWidth, tweetTextHeight = accountFont.getsize(reflowed_latest_tweet)
        startDraw = startDraw + tweetTextHeight + accountTextHeight + (headerPadding * 4)


#################################
## ADD THE TIME OF LAST UPDATE ##
#################################
# The following inserts the last updated time in the bottom right corner.


now = datetime.datetime.now()
tweet_update = "Updated: " + now.strftime("%d %b %H:%M")

updateTextWidth, updateTextHeight = accountFont.getsize(tweet_update)
draw.text(((inky.WIDTH - updateTextWidth), (headerHeight - updateTextHeight)), tweet_update, inky.WHITE, updateFont)

########################
## FINALISE THE IMAGE ##
########################
# Set a PIL image, numpy array or list to Inky's internal buffer. The image dimensions should match the dimensions of the pHAT or wHAT you're using.
# You should use PIL to create an image. PIL provides an ImageDraw module which allow you to draw text, lines and shapes over your image. 
# See: https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html

inky.set_image(img)

###############################
## SET DISPLAY BORDER COLOUR ##
###############################
# .set_border(colour) sets the colour at the edge of the display
# colour should be one of 'inky.RED', 'inky.YELLOW', 'inky.WHITE' or 'inky.BLACK' with available colours depending on your display type.

inky.set_border(inky.WHITE)

########################
## UPDATE THE DISPLAY ##
########################
# Once you've prepared and set your image, and chosen a border colour, you can update your e-ink display with .show()

inky.show()