# Contraband-Game

This is one of the games from the manga "Liar Game". The instructions of the game are in the repository (game_rules.txt). 
Have fun.

![ image alt](https://github.com/andrewisoko/contraband_game/blob/main/images/image%2001.jpg)


# Instructions


* Run the game with "python -m contraband_game.main" (both IDE terminal and Command prompt)
*  Terminate the game by pressing Ctrl + C
* Clear terminal by pressing cls (command prompt) otherwise if running on IDE terminal Ctrl + L
* Name, Surname and email can be invented it is not a real case scenario, I just wanted to add up more stuff in the project.

1) The sign up process creates username and code, mandatory for participating the game.

2) User credentials , generated username and code are stored in json files. *Highly advised to remember the generated credentials for the log in*. 

3) After signing up,  Run the program again, this time select "L" and add the nickname and code created during the sign up process.

4) Although there is no limit for the amount of accounts that can be created, only 4 accounts can partecipate.

5) The game (round according to the manga conventions) has no graphic interface. it requires simple inputs.

6) The input amount of the user/smuggler is not visible, it will appear only after insert it.

# Tests 


1) The tests are not found in the packages, if wanting to try the tests it is advised to download the entire repository.

2) "pip install setuptools" 

3) It is recquired to activate the vritual environment to run the tests.

4) Simply insert "pytest" and run it in the terminal.



# Potential issues


*  To avoid the unlimited waiting time during the tests, it is suggested to comment all the time.sleep in the gamesettings.py module.

*  In case an issue arises with the test functionality, it is suggested to activate the virtual environment inside the tests directory for then returning back to the previous directory (cd..) to ensure the proper usage of pytest. 

* Found some issues with the pkg_resources package. used the pkg_resource function as a value of an instance attribute, thinking that I could reuse the instance across different functions of the class but it did not work, therefore forced to repeat some code.

* If downloading the repository, and wanting to try the sign up process do not add backslash found in user_data_json file generated code. Omit it from the generated code when past it to the terminal.


# Installation instructions


1) Downloading python is required to play the game in your command prompt here is the link for the tutorial https://wiki.python.org/moin/BeginnersGuide/Download

2) Run "pip install setuptools" in your command prompt for configuring the required modules.

3) Run "pip install contraband_game" to install the package.

4) Run  "python -m contraband_game.main" to start the game.


# Additionl notes


* The game can be quite complicated to undertand feel free to drop me a message on LinkedIn www.linkedin.com/in/andrew-isoko for any assistance

* The premise of the game other than winning the round with your country is also not falling into dept. Bonus if you finish as a top earner. Can you do it?





