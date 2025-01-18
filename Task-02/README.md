# Pixelated Problem Solver ✨

## The Approach 🛠️
For this task, my primary goal was to **extract text from an image**, perform the suitable operation on it, and return the final answer. Here's how I tackled the problem step by step:

### Step 1: Setting Up the Environment 🌐
To ensure a clean and isolated workspace, I needed to **set up a virtual environment**. This allowed me to manage dependencies for the task efficiently without affecting the global Python installation.

- **Command to Create Virtual Environment:**
  ```bash
  python3 -m venv myvenv
  ```
- **Activating the Virtual Environment:**
  ```bash
  source myvenv/bin/activate
  ```
- **Installing Required Libraries:**
  ```bash
  pip install pillow pytesseract
  ```

### Use Case of Virtual Environment for This Task 🎯
The virtual environment ensured that:
1. All necessary libraries like `Pillow` and `Pytesseract` were installed in an isolated space.
2. There were no conflicts with other projects or system-wide dependencies.
3. I could easily replicate the environment for others to work on the same task by sharing the `requirements.txt` file.

### Step 2: Importing Required Libraries 📚
I started by importing the **Image** module from the `Pillow` (PIL) library. During this process, I came across a new and interesting module called `pytesseract`. This module is specifically designed for **text extraction** from images, which was exactly what I needed for this task.

### Step 3: Extracting Text from the Image 🖼️
- First, I opened the image using the `Image.open()` function from the `Pillow` library.
- Then, I utilized the `pytesseract` module to extract the text from the image. This was a key step, as it allowed me to retrieve the information embedded in the image with ease.

### Step 4: Performing Operations on the Numbers ➕➖✖️➗
- Once the text was extracted, I analyzed it to identify the numbers and the operation that needed to be performed.
- Using Python's **`eval()` function**, I calculated the result of the operation dynamically. The `eval()` function made it convenient to execute the operation directly from the extracted text.

### Final Output ✅
The result of the operation was successfully returned, marking the completion of the task.

---

## Highlights 🌟
- **Libraries Used:**
  - Pillow (PIL) 🖼️
  - Pytesseract 📜
- **Key Function:** `eval()` for executing operations on extracted numbers.
- **Virtual Environment:** Ensured a clean and conflict-free workspace.

### Learning Outcome 📖
This task introduced me to the powerful `pytesseract` module and reinforced my understanding of image processing, text extraction, and virtual environment usage. 

It was an exciting challenge that combined **image processing** and **dynamic operations**, and I thoroughly enjoyed solving it! 🧠✨

