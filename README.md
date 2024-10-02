# Python Git Lab

In this lab, I'm going to force you to learn git and make you play with some
lists.

## Phase 1 - Cloning the repo
I don't know how much you remember - but version control in repositiories is the
way to keep track of code in a team. In this lab, we're going to pretend that
I'm the project lead hosting the repository, and you are an engineer who's going
to add features.

### Generating an SSH Key
In order for `github.com` to know who you are, you have to authenticate either
by username & password or by SSH keys - but I don't love the way github handles
username/password. So I want you to use SSH keys. With SSH keys, you generate a
private key and a public key. Then you can share the public key with anyone on
the internet, and they can verify if they are talking to you by asking you a
challenge that only someone with the private key could answer. So let's get to
it.

1. First, you need to generate a keypair. In a handy dandy terminal, run the
`ssh-keygen` command:
```
ssh-keygen -t ed25519 -f ~/.ssh/github
```
In this command, `-t` is specifying the type of encryption (rsa and ed25519 are
the most well-used I believe). `-f` is telling the output location. So when I
run the command, it creates two files: `~/.ssh/github` (private key) and
`~/.ssh/github.pub` (public key).

2. Now we have to tell github about this key. Go to https://github.com
3. Click on the profile icon in the top right and go to **Settings**
![](./images/github_profile_icon.jpg)
![](./images/github_settings.jpg)
4. Now click on **SSH and GPG keys** on the left
![](./images/github_ssh_and_gpg.jpg)
5. Now click **New SSH key** in the top right
![](./images/github_new_ssh_key.jpg)
6. In the **Title** field, we're just giving a name to the key for our own
reference, so choose whatever name you want - maybe named after the computer
you'll be ssh'ing from.
7. Now copy the contents of the public key file you generated (should be the
file `github.pub`) to the **Key** box

### Managing an SSH Agent
Now that you have a key that you can use to verify your identity and told github
about it, you need to tell ssh that you are going to use that key. You do that
by running an `ssh-agent` and adding your key to it. Since your key is encryted
with a secret, you'll have to redo this every time you restart your computer or
your shell loses configuration.

1. In a terminal, start your agent
```
ssh-agent > ~/.ssh/agent.sh
```
`ssh-agent` creates an agent process on your computer and prints some
environment variables that your shell can store to keep track of your agent. In
this case, the `>` operator redirects the output to a file at `~/.ssh/agent.sh`.

2. Have your shell run/save environment variables from that file by running
```
source ~/.ssh/agent.sh
```
`source` is a command built into your shell that executes a script in your shell (aka updates your environment variables).

3. Add the private key you created
```
ssh-add ~/.ssh/github
```

Now, you can see what keys you have added with `ssh-add -l`. If you're ever not
sure if you have a key added, you can check there. It'll also tell you if you
don't have an agent running if it looks like this:
```
> ssh-add -l
Error connecting to agent: Connection refused
```
If your shell lost your agent environment variables but the agent is still
running, you can restore the running agent by re-`source`-ing the file.
```
# ps: list running processes -eaf are some arguments to force listing all
# programs => grep: search the results for "ssh-agent"
> ps -eaf | grep ssh-agent      
miccox3   2367    14  0 12:04 ?        00:00:00 ssh-agent -t 10h

# does our agent file still exist?
> ls -l ~/.ssh/agent.sh
-rw-r--r-- 1 miccox3 miccox3 133 Oct  1 12:07 /home/miccox3/.ssh/agent.sh

# re-source
> source ~/.ssh/agent.sh
Agent pid 2698

# is our key still added?
> ssh-add -l
The agent has no identities.
```
To stop an agent (ex. you finished working and want to clean up running
processes), use `ssh-agent -k`. This will use the same environment variables to
kill the running agent process and then clean the environment.

### Cloning the repo
Now that we've told github about the key and added it to an agent, we can use
the program git to clone this repo.

1. On this repo in github, click on the **Code** button in the top right.
2. A popup window should appear that says **Clone** and has a couple tabs. Click
on the SSH tab and copy the URL that appears.
![](./images/github_clone.jpg)
3. Now we just have to tell git what to do - in your terminal again, run the following command.
```
git clone <repo_url>
```
That should clone the repository from github onto your computer.

### Phase 1 Command Reference

| Command  | Description  | Example  | Example Explanation  |
|----------|--------------|----------|----------------------|
| `ssh-keygen`  | Generates ssh keypairs (public & private)  | `ssh-keygen -t ed25519 -f my_key`  | Generate an ed25519 key pair to `my_key` and `my_key.pub` in your current directory  |
| `ssh-agent`  | Creates, kills, and manages ssh agents  | `ssh-agent -t 10h > ~/.ssh/agent.sh`  | Create an ssh agent that removes keys after 10 hours and redirect it from the terminal to a file at `~(your home)/.ssh/agent.sh`  |
| `ssh-add`  | Add (and remove/manage) ssh keys from your agent  | `ssh-add ~/.ssh/my_private_key`  | Add the private key in the file `~/.ssh/my_private_key` to your agent  |
| `ps`  | List running processes  | `ps -eaf | grep search_string`  | List details about all running processes and search that list for `search_string`  |
| `source`  | Run a shell script in your shell to update shell settings/environment variables  | `source ~/.zshrc`  | Re-load your `zshrc` - the script that configures `zsh` everytime you start a shell  |

#### ssh-keygen
| Option  | Description  | Example  |
|---------|--------------|----------|
| `-t <type>`  | Generate a key with a specified type  | `ssh-keygen -t ed25519`  |
| `-f <filename>`  | Output keys to `filename` and `filename.pub`  | `ssh-keygen -t ed25519 -f ~/.ssh/my_key`  |
| `-b <number_bits>`  | Set a number of bits for the encryption algorithm  | `ssh-keygen -t rsa -b 4096`  |

#### ssh-agent
| Option  | Description  | Example  |
|---------|--------------|----------|
| `-t  <time>{smhdw}`  | Create an agent that expires added keys after they've been added for `time` seconds/minutes/hours/days/weeks  | `ssh-agent -t 10h`  |
| `-k`  | Kill the running agent  | `ssh-agent -k`  |

#### ps
`ps` is a weird command with a weird history - I forget the details but
basically it has 2 entirely different ways of using it. There's a set of
arguments for using the program with BSD syntax (without the `-`), and there's a
set of arguments with the `-` like most other GNU/linux programs. That's not
crazy, but the other crazy part is that the same letter can mean different
things depending on if it has a `-` or not.  give another set of arguments if
you have the preceding `-`.

| Option  | Description  | Example  |
|---------|--------------|----------|
| `-e`  | Select all processes  | `ps -e`  |
| `-a`  | Select all processes except session leaders (processes associated with the terminal)  | `ps -eaf'  |
| `-f`  | Full format listing  | `ps -eaf`  |

Generally with `ps`, 99% of the time I'm going to just throw the entire `-eaf`
to get a full listing.

## Phase 2 - Tic Tac Toe
This time, I've made a really quick version of tic tac toe. I decided to
represent the whole game as `class TicTacToe`. As you somewhat know, classes are
a way to group data and group some functions as specifically attached to that
class.

### The Data
When you define a class, you can then create an **instance** of a class by
assigning it to a variable.
```
class TicTacToe:
    # some definition of what it means to be a tic tac toe

# making a specific instance and storing it as my_tictactoe
my_tictactoe = TicTacToe()
```

**Instance variables** are variables unique to each instance of the class.
**Static variables** are variables that are the same across all instances of a
*class.

Both types are referenced by `my_tictactoe.variable`, but static variables can
also be referenced with `TicTacToe.variable` since the variable is the same for
the class as a whole. In my `TicTacToe` class, all of the data is stored in
**instance variables**. In Python, unlike a lot of other languages, instance
variables are defined in the initializer (also called constructors in other
languages) - a special function called `__init__()` that you define to tell
python how to setup a class.

So you can see the data in `tictactoe.py`:
```
class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.game_state = GameState.NOT_FINISHED
```

There are two variables - `self.board` and `self.game_state` (`self` is a way to
refer to an instance from functions defined in the class - when a function takes
`self` as the first argument, it uses `self.variable` or `self.function()` to
access its instance variables and functions)
- `self.board` is a list with 9 characters that should be either "X", " ", or "O".
- `self.game_state` is an enum that represents what state the game is in (more on enums later)

### So what's the lab?
Since we're learning git/github, I've decided to tell you what to do through
**issues** - github's way to report bugs or request features in the repository.

I'll try to be descriptive about each thing I want you to do in this repo's [issues](https://github.com/finger-prints/python_git_lab/issues).

### How to track your progress
Once you've cloned the repo and picked an issue to start on (hopefully the one
labeled good for newcomers), you can start writing code for that issue in
`tictactoe.py`.

#### Issue Tracking
Once I've added you to the repo and you've accepted, you should be able to
assign yourself to issues to claim that you're working on that. Feel free to
make comments on what you're thinking or tracking your progress.

#### git diff
If you want to see what you've changed, you can run `git diff`:
```
git diff tictactoe.py
```
Git will try to tell you what you've changed - lines that are green or start
with `+` are added, lines that are red or start with `-` have been removed. It
references where it is in code with a header `@@` with a line number/position
and some extra unchanged lines at the beginning and end.

If you've already staged a file, you can see changes to that with `--staged`:
```
git diff --staged tictactoe.py
```

#### git status
If you want to see what files you've changed in the repository, you can run
`git status`:
```
> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        my_key
        my_key.pub

no changes added to commit (use "git add" and/or "git commit -a")
```
- **Changes not staged for commit** displays files that are tracked in the
repository that you have changed without committing. 
- **Untracked files** displays files that you have made that don't exist in the
repo.

#### Staging / git add
Once you've written enough that you can describe what you did briefly and have
some progress, you'll want to add and commit your changes. `git add` tells git
that you want your next commit to have the changes you've made to the files you
add:
```
git add README.py
```
After running that command, running `git status` gives:
```
> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        my_key
        my_key.pub
```
Now `README.md` appears under **Changes to be committed**.

#### Committing changes
Now you can commit your changes. Of course you don't necessarily need to run
`git status` on every side, but it doesn't hurt to double check your commits.
You can make tracking changes in github a little easier by referencing issue
numbers in your commits. If you were working on issue #1 and have finished, you
could make the following commit and github will automatically close the commit.
```
git commit -m "implemented x. closes #1"
```

#### Updating remotes (github)
Now the only thing left is to push your changes back to github using `git push`:
```
git push
```
If you have your SSH keys added correctly, this should update github's copy of
the repo with your commits.

### Phase 2 Command Reference

#### git subcommands
| Git Command  | Description  | Example  |
|--------------|--------------|----------|
| `git status`  | Get a status of the current repo/directory.  | `git status`  |
| `git diff`  | Get changes between two versions of a file.  | `git diff tictactoe.py`  |
| `git add`  | Stage files for committing.  | `git add tictactoe.py`  |
| `git commit`  | Commit changes locally.  | `git commit -m "my commit message"`  |
| `git push`  | Push your local commits to a remote repository.  | `git push`  |
| `git rm`  | Untrack a file and delete it.  | `git rm README.md`  |
| `git log`  | Get a list of commits that have been made to the repo.  | `git log`  |

#### git diff
| Option  | Description  | Example  |
|---------|--------------|----------|
| `--staged`  | Show changes between the staged version of a file and the commit you're on  | `git diff --staged tictactoe.py`  |

#### git commit
| Option  | Description  | Example  |
|---------|--------------|----------|
| `-m`  | Provide a message describing your commit.  | `git commit -m "fixed #29"`  |