# MemeGenerator
Collective Intelligence FInal Project 
Cody Molho, Dongmin Park, &  Kassandra Munguia

## Inspiration

After learning abot sentiment analysis through Tweets, we decided to build on that by creating a memebot generator on Twitter. 

This memebot, @comp440cdk, will be able to reply in real time with an appropriate meme to the users who has tweeted at it. Any user can tweet at @comp440cdk and our program is able to determine whether the sentiment behind the tweet was postive, negative or neutral. Once the feeling is determined, the program chooses a random meme image from the apprpriate image folder and tweets back at the user with the image and a little saying. For example: 
<p align="center">
  <img src="memebotExample.png" width="350"/>
 </p>

## How does this work?

Our program uses a sentiment classifer that determines the sentiment on a -1 to 1 scale. We have determined the intervals for each feeling: -1 to -0.3 Negative, -0.3 to 0.3 Neutral, 0.3 to 1.0 Positve. 

From there, we implement a Word2Vec analysis. We check the distance each word in the tweet has with each tag in the appropriate file. The meme that is chosen is the one with the max distance with the tweet. 

The memes have a csv file in each folder with a string of words that relate to a meme.
<p align="center">
  <img src="/Images/negative/negative-d.jpg" width="350"/>
 </p>
So if the meme is about the weekend ending, like the one above, the tags for this image are: cat, grumpy, Monday, sarcasm, Sunday, work, school. Tags and memes were chosen by us. 


