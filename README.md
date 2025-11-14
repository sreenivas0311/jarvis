# ⭐ **JARVIS – Personal Desktop Assistant (Python Version)**  

A personal assistant inspired by **Iron Man’s JARVIS**, built completely in **Python**, featuring:

- 🎤 **Speech Mode (Wake-word voice input using Vosk)**  
- ⌨️ **Text Mode (Type commands + Jarvis speaks back)**  
- 🗣️ **Offline text-to-speech (pyttsx3)**  
- 🧠 **Machine Learning NLP Intent Detection**  
- 🌐 **Google & YouTube automation**  
- 📚 **Wikipedia Q&A**  
- 🌍 **Translation (Hindi, Tamil, Telugu, English)**  
- 🧾 **Memory system**  
- 🖥️ **Open/Close desktop applications**  

⚠️ **Note:**  
We originally planned a full web dashboard, but due to STT model issues,  
the final stable version includes:

✔ **Text Mode**  
✔ **Speech Mode**  
❌ **No web dashboard**  

This README reflects the final working version.

---

# 📌 **Features**

## 🎮 Dual-Mode Control

### **1️⃣ Text Mode**
- Type commands  
- Jarvis executes actions  
- Jarvis speaks the reply  
- Type `exit` to return to menu  

### **2️⃣ Voice Mode (Wake Word: *Jarvis*)**
- Vosk listens in the background  
- Say **"Jarvis"** to activate  
- Speak your command  
- Say **exit** to leave voice mode  

---

## 🖥️ App Control
Jarvis can open/close:

- Chrome  
- Brave  
- Discord  
- Notepad  

Examples:

```
open chrome
close notepad
open discord
```

---

## 🌐 Website Opener

```
open google
open youtube
open amazon
open flipkart
open instagram
open github.com
open reddit.com
```

---

## 🔍 Google Search

```
google python tutorial
google how to cook pasta
```

---

## 🎵 YouTube Search & Music

```
youtube lofi beats
play arijit singh songs
play tamil songs
```

---

## 📚 Wikipedia Answers

```
wikipedia virat kohli
wikipedia what is python
wikipedia who is abdul kalam
```

---

## 🌍 Translation

Supports:
- Hindi  
- Tamil  
- Telugu  
- English  

Examples:

```
translate hello to hindi
translate how are you to tamil
translate vanakkam to english
```

---

## 💾 Jarvis Memory

```
remember that I like football
remember my exam is on monday
what do you remember
```

Memory is stored in a JSON file.

---

## 🧠 NLP Intent Classification

ML model trained to understand:

- open_app  
- close_app  
- open_website  
- google_search  
- youtube_search  
- translation  
- wikipedia  
- general chat  

Using:
- `TfidfVectorizer`  
- `LogisticRegression`  

---

## 🗣️ Offline Text-to-Speech

`pyttsx3` is used to:

- Speak replies  
- Give confirmations  
- Read out summaries  

Works completely offline.

---

# ⚙️ **Installation**

## 1️⃣ Clone repository
```
git clone https://github.com/yourusername/jarvis-assistant
cd jarvis-assistant
```

## 2️⃣ Create virtual environment
```
python -m venv venv
```

## 3️⃣ Activate environment
```
venv\Scripts\activate
```

## 4️⃣ Install dependencies
```
pip install -r requirements.txt
```

## 5️⃣ Download Vosk Model (for speech mode)

Download:

```
vosk-model-en-us-0.22-lgraph
```

Place inside project:

```
/jarvis-assistant/
    vosk-model-en-us-0.22-lgraph/
```

## 6️⃣ Run Jarvis
```
python jarvis.py
```

---

# 🏁 **Usage Guide**

## When Jarvis starts:
```
Select Mode:
1 → Voice Mode
2 → Text Mode
```

---

## 📘 Text Mode Commands

```
open discord
google best budget laptops
youtube lofi songs
translate I am fine to telugu
remember I like pizza
what do you remember
wikipedia ms dhoni
exit
```

---

## 🎤 Voice Mode Commands

Say:

**“Jarvis”** → wake word  
Then:

- “open chrome”  
- “search google for python basics”  
- “play music”  
- “exit”  

---

# ❗ Known Limitations

- Vosk accuracy varies with accent  
- Text mode is more stable than speech mode  
- Web dashboard was intentionally skipped  
- Discord/other apps may require correct install paths  

---

# 🚀 Future Enhancements

- Web dashboard (HTML+Flask)  
- Whisper.cpp for better speech accuracy  
- Face recognition login  
- Offline OCR  
- GPT-style LLM mode  
- Auto-app-detection  
- GUI desktop app  

---


