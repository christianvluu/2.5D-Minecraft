# 2.5D-Minecraft

## Overview:
Welcome! This is a game similar to the real Minecraft! But it is drawn Isometrically (2.5D graphics). It’s a simplified version of the full game.


Explore the world, find things, build houses, and magnificent structures! Enjoy!


There is random generation of worlds based on a seed, just like the real game! There are tree biomes that are generated with the provided seed.


You can change perspectives to more easily view the world as well as place and destroy various blocks.


## Installation/Getting Started:
All the necessary game files (other than external modules) are in the .zip folder downloaded, specifically in the game folder. Just unzip it!
1. Ensure you have python 3 installed (written specifically in 3.7.4)
2. Install the numpy and pygame modules with pip
3. Open the main2.py file in the MainGame folder in a python editor
4. Edit the seed (if you want) near the top of the file, the variable name is SEED. It is clearly labelled
5. Run the main.py file to start Isometric Minecraft
6. Saved worlds will be in the MainGame folder under the name myworld.txt (there can only be one saved world at a time)


## Instructions:
* Use WASD to move the player (imagine a top down view perspective)
   * W moves the player to the top-left
   * S moves the player to the bottom-right
   * A moves the player to the bottom-left
   * D moves the player to the top-right
* Use Arrow keys to place blocks in whichever direction you want
   * Directions are the same as WASD
   * Modifiers
      * With no modifiers, arrow keys will place block at the feet of the player
      * Holding shift will destroy blocks at the feet of the player
      * Holding control will place blocks at the head height of the player
      * Holding option/alt will destroy blocks at the head height of the player
* Use Number keys (1, 2, 3, 4, etc.) to choose from different blocks to place (look at top-left to see which block is selected)
* Press Q to cycle the view of the player (look at the top-left to see which perspective)
* Press ctrl+r to go back to main screen (this will not save current world)
* Press ctrl+s to save world (game will be unresponsive for a few seconds)


## Game Tutorial
* You can jump blocks up to one block high. No higher (just like in the real Minecraft). Build if you need to reach higher places.
* The world ONLY renders 15 blocks surrounding the player. This is to save processing power and speed up rendering. Move the player around to see more.
