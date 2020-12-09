# ommc

__prerequisites__
1. (git) https://git-scm.com/downloads
2. (python *3.9*) https://www.python.org/downloads/

__instructions__
1. navigate to any folder. right click and open a terminal in that location (either cmd or powershell). if you don't see that option, open one of them manually, and type this command instead:
```
cd C:/path/to/that/folder/you/just/selected
```

2. clone the repository on your own system. this command will create an additional folder named "ommc" into the folder you created, if you did the previous step correctly. here is the clone command:
```
git clone https://github.com/ap-1/ommc
```

3. navigate into the folder that was recently created. your path in the terminal should now end with `/ommc`. if it worked, set up and enter a python virtual environment to install the dependencies:
```
cd ommc
python3 -m venv venv
```
at this point, you should see the "venv" folder pop up in the "ommc" folder. now, you can enter it using this command. make sure you pick the right one depending on what terminal you're using:
```
./venv/Scripts/Activate.ps1 # for powershell
venv\Scripts\activate :: for cmd
```
you should now see an indicator marking that you've entered the venv. the color of the marker depends on what terminal you're using. it shold show "(venv) " before the name of the path.

4. install dependencies. a `requirements.txt` already included, so you can tell `pip3` to use this when installing the dependencies.
```
pip3 install -r requirements.txt
```

note: if you get a warning like this:
```
WARNING: You are using pip version x.x.x; however, version x.x.x is available.
You should consider upgrading via the 'c:\<path>\ommc\venv\scripts\python.exe -m pip install --upgrade pip' command.
```
then run the command that it tells you to run. (copy it from your own terminal, not this one, because it gives you the proper path in your own terminal)

5. test to make sure if all dependencies are properly installed. run this command:
```
flask --version
```
this should respond with the flask version, python version, and werkzeug version. if it errors out instead, you might have done something wrong previously. alternatively, if it gives you a warning to add a path to your system environment variables, follow the instructions it gives you to add it to PATH.

6. run the server. use this command:
```
flask run
```
this should respond with a message saying the site is live. it is actually live on your own network, so others will not be able to see it.

7. go to this link in your browser: http://127.0.0.1:5000/. it should show the contents of the site. you are now browsing the site without publishing it to an actual website. this way, you can make local changes and test it in your own browser, instead of publishing code that may be broken. when making changes, TEST FIRST! you can publish it to git once you're done.

small note: if you've made changes in the `static` folder, you must do `Ctrl+F5` on the website for them to update.

8. resume on this step once you've made changes. if the server is still running, you'll notice that it was logging traffic to your website. if you are unable to type, simply press `Ctrl+C` to end the logging. this will allow you to type again. make sure you've saved all changed files. then, you can commit them. these commands may take a while to complete (up to a couple minutes at max), so make sure not to interrupt them.
```
git checkout -b anynamehere
git add .
git commit -am "any commit message here, make sure it is descriptive"
```

don't push your changes now, because it will overwrite what is already there. instead, you can create a new branch.

9. use git to create another branch to push your changes to. DON'T commit to master. make sure the name of your branch isn't already taken. once you create the alternative branch, you can push to that branch instead of master. make sure NAME is the same in both commands. this will also take a while.
```
git checkout -b NAME
git push origin NAME
```
