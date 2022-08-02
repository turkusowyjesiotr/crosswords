# crosswords
Python crosswords generator/game.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)

## General Information
This is my first project in **Python**. It's a game made with pygame that generates two types of (fairly easy) crosswords: first type has only horizontal words
with one vertically placed final answer and the other has just words that... well, cross with each other. Every word is in Polish and has Polish definitions.
I've chosen this language mainly because it's my mother tongue but also because I wanted some practice with **Selenium** and web scraping.

Every word is scraped from a polish website (http://wordlist.eu) that contains dictionary for crossword puzzles in Polish. And for each word that is used in given
puzzle, definitions are scraped from the same website while the crossword is generating.

It's merely a training exercise type of project, because I wanted to improve upon my programming skills.

## Technologies Used
- Python 3.7
- pygame 2.12
- Selenium 4.1.5

## Features
- two types of crosswords with words randomly chosen from 100k scraped words
- animated loading screen, while the crossword is generating
- animated buttons to generate each type of crossword and to switch between definitions

## Screenshots
<details>
<summary>Typing letters (if letter matches the correct answer its green, otherwise red)</summary>
<img src=./.img/gif.gif>
</details>
<details>
<summary>Screenshots of generated crosswords and whole game window</summary>
<img src=./.img/img1.jpg>
<img src=./.img/img2.jpg>
<img src=./.img/img3.jpg>
<img src=./.img/img4.jpg>
<img src=./.img/img5.jpg>
</details>

## Setup
You can clone this repository or download .zip file and run main.py from IDE. Pygame and Selenium are required.

## Project Status
Project is: _complete-ish_, it works and I am fine with it, but I want to expand it in the future.
## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- algorithm that generates crossword could be improved to make them more dense
- speed could be improved with more use of threading
- aesthetics could be REALLY improved
