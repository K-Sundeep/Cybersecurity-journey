-> pwd , stands for "print working directory". It displays your current location in the file system.

-> ~ . This represents the home directory.

-> echo ~ , This command displays the path to  the home directory.

-> ls , This lists the files and directories in the current working directory.

-> ls ~ , This command lists the contents of home directory.

-> ls \*.txt , list all files ending with .txt

Linux uses what we call a "hierarchical file system".

-> cd .. , this moves up one level to the parent directory.

-> cd ~ , This shortcut is used to move to home directory.

-> cd /home/labex/project , This type of cmd is called absolute path. Since it shows the full path.

-> touch , This command is used to create an empty file. If the file already exists, it updates the file's timestamp without changing its content.

-> echo "Hello, Linux" > file2.txt , The echo command prints the text in double quotes into file2.txt . The > symbol redirects the output of echo into a file named file2.txt. If the file doesn't exist, it's created. If it does exist, its content is replaced.

-> echo "Hidden file" > .hiddenfile , This creates a hidden file.

In Linux any file or folder starting with dot is considered hidden.

-> mkdir dir\_name , The mkdir command (short for "make directory") creates a new directory with dir\_name.

-> ls -l , The -l option (that's a lowercase L, not the number 1) provides a "long" format listing. You'll see additional details like file permissions, owner, size, and modification date.

-> ls -a , This shows all files, Including the hidden files.

-> ls -la , This combines the long format (-l) with showing all files (-a).

-> ls -l dir\_name , This lists the contents of the directory we want.

-> cp file1.txt file1\_copy.txt , This creates a copy of file1.txt named file1\_copy.txt in the current directory.

-> cp file2.txt testdir/ , This copies file2.txt into the testdir directory.

-> cp -r testdir testdir\_copy , The -r option stands for "recursive". It's necessary when copying directories to ensure all contents are copied.

-> ~/.zshrc: A hidden configuration file in your home directory.

-> ~/Code: A directory containing source code.

-> To run multiple commands in a single line, you can use the semicolon (;) to separate them.

 	ls; ls testdir; ls testdir\_copy

 	also by using this method

 		ls \&\& ls testdir \&\& ls testdir\_copy

-> mv file1.txt newname.txt , This renames file1.txt to newname.txt

-> mv newname.txt testdir/ , This moves newname,txt to the testdir directory.

-> mv testdir\_copy new\_testdir , This renames testdir\_copy to new\_testdir.

-> mv testdir/newname.txt ./original\_file1.txt , This moves newname.txt out of testdir and renames it to original\_file1.txt in the current directory. ( ./) represents current directory. (Single dot): The current directory.

.. (Double dot): The parent directory (one level up).

~ (Tilde): Your home directory (/home/labex).

Deletions made with rm are usually permanent.

-> rm original\_file1.txt , The rm command deletes the file.

-> rm -i file2.txt , The -i option prompts you for confirmation before deleting each file. Type y (for yes) and press Enter to confirm the deletion. If you type n or anything else, the file will not be deleted.

-> rmdir dir\_name , rmdir removes only empty directories.

-> rm -r dir\_name , This removes the directory and everything inside it. It is done recursively.

The rm -rf command is extremely powerful and potentially dangerous. It removes directories recursively (-r) and forces removal without prompting (-f).Be ABSOLUTELY SURE you know what you are deleting before running rm -rf. A small typo could delete critical system files or your personal data. There is no undo. For example, rm -rf / could attempt to delete your entire system (if you have permissions). Always double-check the path.

 we used -R (uppercase) with ls instead of -r (lowercase) like we did with cp and rm. This is not just a case difference - they are completely different options! For ls, -R means "recursive listing" (list subdirectories), while -r means "reverse sort order". For cp and rm, the recursive option is -r (lowercase).

In Linux command line, deleted files are generally gone forever. Use rm carefully!.

-> Wildcards are special characters that help you work with multiple files at once. They're like search patterns for file names. Let's practice using them. The \* is a wildcard that matches any number of characters.

-> touch note\_{1..5}.txt . This creates note\_1.txt, note\_2.txt, note\_3.txt, note\_4.txt, and note\_5.txt all at once!

-> The most common wildcards are:



\*: Matches any number of characters

?: Matches any single character

\[abc]: Matches any one character listed in the brackets.



-> List of Strings:

 	Instead of a range, you can provide a comma-separated list of specific names inside the braces. This is perfect for 	creating different types of files at once.

 	touch project\_{docs,code,tests}.txt , Creates project\_docs.txt, project\_code.txt, and project\_tests.txt

-> Nesting Braces:

 	You can put braces inside other braces to create complex combinations.



 	Example: touch {jan,feb}\_{01..02}.log

 	Result: Creates four files: jan\_01.log, jan\_02.log, feb\_01.log, and feb\_02.log.

-> Step Values (Increments)

 	In a range, you can add a third part to specify a "step" or "skip" value.



 	Example: touch file\_{1..10..2}.txt

 	Result: Creates file\_1.txt, file\_3.txt, file\_5.txt, file\_7.txt, and file\_9.txt (skipping by 2).

-> Creating Directories

 	Brace expansion works with other commands too, like mkdir (make directory). This is a common way to set up a project 	structure quickly.



 	Example: mkdir -p project/{src,bin,lib}

 	Result: Creates a project folder with three subfolders: src, bin, and lib.

-> Command Line Shortcuts:

 	Use the up arrow key (↑) to recall the last command you typed. Try pressing it now – you should see your last command 	appear!



 	Use Tab completion:

 	Type cat h and then press the Tab key. It should auto-complete to cat hello.txt.

 	This feature saves a lot of typing and helps prevent spelling mistakes.



 	Use Ctrl+C to interrupt a running command:

 	Type the following command and press Enter:



 	tail -f /dev/null(Usually, tail -f is used to watch a file as it grows (like a live log file). However, /dev/null is a 	special "empty" file in Linux that returns nothing.)

 	This command will wait for input indefinitely. Now press Ctrl+C to stop it. This is useful when a command is taking 	too long or you want to stop a continuous output.



 	Use Ctrl+L to clear the screen:

 	Your terminal might be getting cluttered. Press Ctrl+L to clear it and give yourself a fresh view.









# User Account Management:

-> sudo useradd joker ,

 	-> sudo is a command that gives you temporary superuser (administrator) privileges. We use it because creating a new 	user requires these higher-level permissions.

 	-> useradd is the command to create a new user.

 	-> joker is the username we're creating.

-> sudo grep -w 'joker' /etc/passwd , (grep: Search for a specific pattern.

 	-w: Look for the whole word only. (This prevents it from accidentally finding a user named "joker\_admin" if one 	existed).

 	'joker': The specific word you are looking for.

 	/etc/passwd: The file you want to search inside.

 	-> The /etc/passwd file is like a phonebook for user accounts. Each line represents one user account, with different 	pieces of information separated by colons (:).

 	-> Output: joker:x:5001:5001::/home/joker:/bin/sh.

 	-> Username: joker

 	Password: x (the actual password is stored securely elsewhere)

 	User ID: 5001

 	Group ID: 5001

 	Home Directory: /home/joker, but it hasn't been created yet

 	Default Shell: /bin/sh

-> sudo useradd -m bob ,

 	-> The -m option tells the system to create a home directory for the user. A home directory is like a personal folder 	where a user can store their files and settings.

-> sudo ls -ld /home/bob ,

 	-> Output : drwxr-x--- 2 bob bob 57 Jan 19 13:33 /home/bob

 	-> d at the start means it's a directory

 	rwxr-x--- shows who can read, write, or execute in this directory

 	The two bob entries show that both the user and group owner of this directory is bob

 	57 is the size of the directory in bytes

 	Jan 19 13:33 is when the directory was created

 	/home/bob is the location of the directory

-> sudo passwd joker ,

 	-> The password will not be displayed as you type it. This is a security feature in Linux to prevent others from 	seeing your password as you type it. If you accidentally enter the wrong password, you can try again.

 	-> Linux stores encrypted passwords in a secure file called /etc/shadow. This is more secure than storing them in the 	/etc/passwd file where anyone could see them.

 	-> /etc/shadow, which is only readable by the root user (or via sudo).

 	-> If you were to look at /etc/shadow (don't worry, you don't have to), you wouldn't see "password123". You would see 	a long, random-looking string of characters. This is a hash. Linux "scrambles" your password so that even if someone 	steals the file, they can't easily see what your password is.

 	-> When you run sudo passwd joker, you might think your keyboard is broken because nothing appears on the screen. This 	is called "Silent Feedback" or "Blind Typing".



 	It prevents "shoulder surfers" from counting the number of characters in your password.

 	It is a standard security practice across almost all Unix-like systems.

###     -> The passwd Command:

 	If you just type passwd (without a username), it tries to change your own password.

 	By typing sudo passwd joker, you are using your administrator powers to set a password for someone else.

####      -> Configuring password aging:

 	In Linux, you primarily use the chage (Change Age) command to manage these settings.



 	Using the chage Command

 	To see the current password aging information for your new user "joker", you can run: sudo chage -l joker ,

 	Common Configuration Options

You can set specific rules by using different flags with chage:



Set Maximum Password Age (-M):

Force the user to change their password every 90 days:



sudo chage -M 90 joker

Set Minimum Password Age (-m):

Prevent the user from changing their password again for at least 5 days (this stops users from immediately changing it back to their old password):



sudo chage -m 5 joker

Set Warning Days (-W):

Give the user a warning 7 days before their password expires:



sudo chage -W 7 joker

Force Change on Next Login (-d 0):

This is very common when you create a temporary password for a new user. It forces them to pick their own private password the moment they log in:



sudo chage -d 0 joker

Where is this stored?

All of these settings are stored in the same secure file I mentioned earlier: /etc/shadow.



Each line in that file has several fields separated by colons (:). After the username and the encrypted password, the following numbers represent:



Last password change date

Minimum days before change

Maximum days before change

Warning days

By using chage, you are simply updating those specific numbers in the /etc/shadow file!

