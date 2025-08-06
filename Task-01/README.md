
# The Command Line Cup 🏆

## Part 1: Getting Started
To tackle **Part 1** of the task, I began by cloning the GitHub repository provided in the documentation. I created a folder named `codes` on my local machine and organized all tasks related to AmFOSS into a main folder called `Amfoss-Tasks` to keep everything in one place.

Before diving into the task, I took some time to explore the command line on the Linux terminal. I quickly revised and practiced various commands to refresh my knowledge. During this process, I also learned a few new commands and became more comfortable navigating the terminal.

After understanding the task requirements from the provided `README.md`, I was ready to proceed to the next part.

---

## Part 2: The First Spell
In **Part 2**, I figured out that the first perfect number is **6**, so the code was located in the directory named `06`. The spell file was identified as the 5th one (`Spell_05.py`) by differentiating the given equation as described in the `README.md` file.

Using the command `python3`, I executed the Python file to get the secret code. I then stored this code in a file named `part_02.txt` within the `codes` folder.

With this part completed, I was ready to move on to the next challenge.

---

## Part 3: Semiconductor Secrets
For **Part 3**, I determined that the first element used to make semiconductors is **silicon**, which has an atomic number of **14**:
- Units place digit: \( y = 4 \)
- Tenths place digit: \( x = 1 \)

Thus, the required file was in the folder `04`, with the spell file being `Spell_01.py`.

To access the file, I switched to the appropriate Git branch using the command:
```bash
git checkout defenseAgainstTheDarkArts
```
I found the file and copied it to the main branch using:
```bash
git checkout <remote branch> <path to the file>
```
By following this approach, I successfully completed this part of the task.

---

## Part 4: Hidden Spells in Commit Logs
For **Part 4**, the task involved finding a hidden spell code within the commit logs. I used the following commands to carefully examine the logs:
- `git log`
- `git log --oneline`

With these commands, I was able to locate the required spell code and successfully complete this part of the task.

---

## Part 5: Combining the Codes
In the final part, I combined all the codes obtained from the previous parts. Using the `base64 -d` command, I decoded the concatenated codes to reveal a GitHub repository link:
```bash
echo <base64_encoded_string> | base64 --decode
```

After cloning the repository, I navigated to the `.txt` file within it. The file displayed a final message confirming that I had successfully overcome all obstacles and completed the task! 

---

## Highlights :
- **Organized workflow**: Created a structured folder setup for task management.
- **Revised and learned commands**: Strengthened Linux terminal skills.
- **Efficient Git usage**: Utilized branching, log commands, and file management.
- **Problem-solving**: Tackled challenges step by step to complete the task.

It was an exciting journey full of learning and challenges! 

