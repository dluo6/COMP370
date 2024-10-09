## Downloading Data from Kaggle

### Directly Using the Kaggle CLI

The recommended method to download datasets from Kaggle is to directly use the Kaggle command line tool

1. Connect to your server and install the Kaggle CLI
```
$ ssh -i /path/to/your/key username@xxxxxxx

# Check if pip is correctly mapped to your miniconda
$ whereis pip
/path/to/miniconda/bin/pip

# Install Kaggle CLI
$ pip install kaggle
```

2. Download and Unzip the dataset using Kaggle CLI
```
$ cd /move/to/appropriate/folder
$ kaggle datasets download -d liury123/my-little-pony-transcript
$ unzip my-little-pony-transcript.zip
$ ls
clean_dialog.csv  my-little-pony-transcript.zip  pony_data.csv  pony_song_data.csv  pony_synopsis.csv
```

### Copying Dataset from Your Local Machine to Your Server

Not recommended, but you can also download the dataset first to your local machine from Kaggle, and then use `scp` to copy it to the server

1. Copy files from your local machine to the server
```
$ scp -i /path/to/your/key /path/to/data/on/your/machine/archive.zip username@xxxxxxx:/path/to/appropriate/folder/on/server
```

2. Connect to your server and Unzip the dataset
```
$ ssh -i /path/to/your/key username@xxxxxxx
$ cd /move/to/appropriate/folder
$ unzip archive.zip
$ ls
clean_dialog.csv  archive.zip  pony_data.csv  pony_song_data.csv  pony_synopsis.csv
```

## How big is the dataset?

Count the number of lines in `clean_dialog.csv`

```
$ wc -l clean_dialog.csv
36860 clean_dialog.csv
```

## What's the structure of the data? (i.e., what are the field and what are values in them)

Use commands `head`, `tail`, `more`, `less` to explore the dataset, different fields, and what they contain

```
$ more clean_dialog.csv
```

## How many episodes does it cover?

### Using `csvtool`

Install `csvtool` and use the help command to see what all you can do with this package.
```
$ pip install csvtool
$ csvtool --help
```

The `csvtool` package can pick out specific columns (see the flag `-c`), and can also print the n most common values for each column (see flag `-m`). We can use these two together to count the total number of episodes.

1. Pick only the first column to look at episode names separately
```
$ csvtool -c 1 clean_dialog.csv > episode_names.csv
```

2. Here's the tricky part. The `-m` flag from `csvtool` calculates the counts of all unique values in a column and prints the top `-m` values with their counts. We are going to use this to find all unique values of the column, by giving a very large `-m`. So let's set `-m` to 36860 (size of the dataset), to make sure we cover all possible scenarios.
```
$ csvtool -m 36860 episode_names.csv > episode_counts.csv
```

3. Count the number of lines in `episode_counts.csv` (and then subtract 1 for the header).
```
$ wc -l episode_counts.csv
198 episode_counts.csv
```
Thus, there are 198-1 = 197 episodes covered in the dataset.

4. Alternatively, learn to do it all without creating additional files
```
$ csvtool -c 1 clean_dialog.csv | csvtool -m 36860 | wc -l
198
```

5. Bonus: You can also see the number of different lines from each episode in `episode_counts.csv`.
```
$ more episode_counts.csv
```

### Using `uniq` and `sort`

Get familiar with these interesting command line tools `uniq` and `sort`
```
$ uniq --help
$ sort --help
```

1. Pick only the first column to look at episode names separately
```
$ csvtool -c 1 clean_dialog.csv > episode_names.csv
```

2. Sort the columns using `sort` and then remove duplicates using `uniq`
```
$ sort episode_names.csv > episode_names_sorted.csv
$ uniq episode_names_sorted.csv > episode_names_uniq.csv
```

3. Count the number of lines in `episode_names_uniq.csv` (and then subtract 1 for the header).
```
$ wc -l episode_names_uniq.csv
198 episode_names_uniq.csv
```
Thus, there are 198-1 = 197 episodes covered in the dataset.

4. Alternatively, learn to do it all without creating additional files
```
$ csvtool -c 1 clean_dialog.csv | sort | uniq | wc -l
198
```

## Find an aspect of the dataset that is unexpected

_Note: These are just a few examples of unexpected behavior in the dataset, and not an exhaustive list. You might have found something else that I've missed._

### Some examples of unexpected behavior within the "pony" Column

- Name of a Pony in this column doesn't necessarily mean that Pony was speaking
```
$ csvtool -c 3 clean_dialog.csv | grep "except" | head
All except Rarity
All except Rarity
All except Fluttershy
All except Fluttershy
All except Twilight Sparkle and Fluttershy
Ponies except Twilight Sparkle
```

- The format is not consistent. For instance, sometimes 'All except XX' is used, while at other times 'Ponies except XX' is used. Sometimes just 'All' is used, sometimes just 'Ponies', and sometimes 'Ponies in unison', etc. Similarly, sometimes 'except' is used, at other times 'sans' is used, sometimes even 'but' is used, etc.
```
$ csvtool -c 3 clean_dialog.csv | grep "All" | head
All sans Rarity
All sans Rarity
All except Rarity
All except Rarity
All
All
All
All sans Celestia
All
All but Rarity

$ csvtool -c 3 clean_dialog.csv | grep "Ponies" | head
Ponies
Ponies
Ponies in unison
Ponies in unison
Ponies
Ponies
Ponies
Ponies
Ponies
Ponies
```

### Some examples of unexpected behavior within the "dialog" Column

- Presence of tone markers in some dialogues
```
$ csvtool -c 4 clean_dialog.csv | grep "\[" | head
[sigh] Does that pony do anything except study? I think she's more interested in books than friends.
"No, no, no... no, no, no! [grunts] Spike!"
"Mare, mare... aha! The Mare in the Moon, myth from olden pony times. A powerful pony who wanted to rule Equestria, defeated by the Elements of Harmony and imprisoned in the moon. Legend has it that on the longest day of the thousandth year, the stars will aid in her escape, and she will bring about nighttime eternal! [gasp] Spike! Do you know what this means?"
"Okay, okay! [inhale] There, it's on its way. But I wouldn't hold your breath..."
"[clears throat] My dearest, most faithful student Twilight. You know that I value your diligence and that I trust you completely."
[sigh] Let's get this over with... Good afternoon. My name is Twilight Sparkle<U+0097>
"[clears throat] Well, I am in fact here to supervise preparations for the Summer Sun Celebration. And you're in charge of the food?"
"This here's Apple Fritter. Apple Bumpkin. Red Gala. Red Delicious, Golden Delicious, Caramel Apple, Apple Strudel, Apple Tart, Baked Apples, Apple Brioche, Apple Cinnamon Crisp... [deep breath] Big McIntosh, Apple Bloom and Granny Smith. Up'n'attem, Granny Smith, we got guests."
"[snort] Wha..? Soup's on? I'm up, here I come, ahm comin'..."
"[spit] [nervous laughter] Okay, well, I can see the food situation is handled, so we'll be on our way."
```

- Presence of special characters
```
$ csvtool -c 4 clean_dialog.csv | grep "<U+" | head
No<U+0097> whoa!
[sigh] Let's get this over with... Good afternoon. My name is Twilight Sparkle<U+0097>
"Friends? Actually, I<U+0097>"
"Thanks, but I really need to hurry<U+0097>"
Good afternoon<U+0097>
"Just a moment, please! I'm 'in the zone', as it were. Oh, yes! Sparkle always does the trick, does it not? Why, Rarity, you are a talent. Now, um, how can I help yo<U+0097> [yelp] Oh my stars, darling! Whatever happened to your coiffure?!"
[wincing] I've... been sent... from Canterlot... to<U+0097>
No I don't<U+0097> whoa!
"Isn't this exciting? Are you excited, 'cause I'm excited, I've never been so excited<U+0097> well, except for the time that I saw you walking into town and I went [deep gasp] but I mean really, who can top that?"
I did. And I know who you are. You're the Mare in the Moon <U+0096> Nightmare Moon!
```

## How often each MAIN pony speaks? Calculate the percent of lines that each pony has over the entire dataset

1. Pick the column "pony" and then use `grep` to find the lines where the name of the pony is present
```
$ csvtool -c 3 clean_dialog.csv | grep "Rarity" | wc -l
2722
```
I'm directly combining multiple commands now without piping them each into separate files. Feel free to create intermediate files if you find that more comfortable when getting started, but try to work towards this format over time.

2. Bonus: We're ignoring potential issues discussed above, and assuming that the dataset is perfect. But you can also try to solve some of these problems.

For example, let's try to solve the problem created by descriptions like 'All except Rarity'.
```
$ csvtool -c 3 clean_dialog.csv | grep "Rarity" | grep -v "except\|sans\|but" | wc -l
2713
```
Thus, there were 2722-2713 = 9 lines where we had wrongly attributed the dialog to Rarity, while in reality it was everyone else but Rarity.

Here `grep -v` reverses the grep command (i.e., select lines that DO NOT match), and the regex phrase `except\|sans\|but` is matched if any one of the three terms are present.

3. To calculate the percentages, we need the total number of lines in the dataset
```
$ wc -l clean_dialog.csv
36860 clean_dialog.csv
```
The percentage of lines that Rarity has over the entire dataset is thus, (2722/36860)*100 = 7.39% (Rounded off to two decimals).