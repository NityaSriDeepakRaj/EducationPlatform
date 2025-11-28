# from openai import OpenAI
# from gtts import gTTS
# # Try to import playsound, fallback to pygame if not available
# try:
#     from playsound import playsound
# except ImportError:
#     try:
#         import pygame
#         pygame.mixer.init()
#         def playsound(file):
#             pygame.mixer.music.load(file)
#             pygame.mixer.music.play()
#             while pygame.mixer.music.get_busy():
#                 pygame.time.Clock().tick(10)
#     except ImportError:
#         def playsound(file):
#             print(f"⚠️ Audio playback not available. Audio file saved: {file}")
# import subprocess, threading, re, time

# # ===========================
# # 🔑 API CONFIG
# # ===========================
# #API_KEY = "your groq api key"
# MODEL = "moonshotai/kimi-k2-instruct-0905"

# client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")


# # ===========================
# # 🧠 SUMMARY
# # ===========================
# def summarize_topic(topic):
#     prompt = f"Summarize the concept '{topic}' in 100 words in a simple narration style."

#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content.strip()


# # ===========================
# # 📝 MCQ Question Generator
# # ===========================
# def generate_questions(topic):
#     prompt = f"""
# Create 3 MCQ questions about '{topic}'.
# Format EXACTLY like this:

# 1) Question text?
# A) Option
# B) Option
# C) Option
# D) Option
# Answer: X

# 2) ...
# (Continue same format)
# """

#     res = client.chat.completions.create(
#         model=MODEL,
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return res.choices[0].message.content.strip()


# # ===========================
# # 🔊 TEXT → SPEECH
# # ===========================
# def text_to_speech(text, filename):
#     print("\n🔊 Generating speech...")
#     tts = gTTS(text=text, lang="en", slow=False)
#     tts.save(filename)
#     print(f"🎧 Audio saved as: {filename}")


# # ===========================
# # 🎬 MANIM RENDER FUNCTION
# # ===========================
# def render_video(topic):
#     print("\n🎬 Generating animation script...")

#     manim_code = generate_manim_code(topic)
#     filename = re.sub(r"[^A-Za-z0-9_]", "_", topic) + ".py"

#     with open(filename, "w", encoding="utf-8") as f:
#         f.write(manim_code)

#     print("\n🛠 Rendering video... (this may take time)\n")

#     # Run manim using python -m manim (most reliable method)
#     import sys
#     python_cmd = sys.executable
#     cmd = f"{python_cmd} -m manim -pql {filename} AutoTeach"
#     print(f"Running: {cmd}")
#     try:
#         subprocess.Popen(cmd, shell=True)
#     except Exception as e:
#         print(f"⚠️ Error running Manim: {e}")
#         print(f"   Please ensure Manim is installed: pip install manim")
#         print(f"   Or run manually: {cmd}")


# # ===========================
# # 🤖 AI → MANIM GENERATOR
# # ===========================
# def generate_manim_code(topic):
#     prompt = f"""
# Write a complete working Manim CE v0.19+ script explaining '{topic}'.

# Rules:
# - Must contain class AutoTeach(Scene)
# - Must use from manim import *
# - Should animate text, arrows, transitions
# - No comments or markdown
# - Avoid LaTeX (NO Tex(), NO MathTex()), use only Text()
# """

#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content.strip()


# # ===========================
# # 🚀 MAIN
# # ===========================
# if __name__ == "__main__":
#     import sys
#     import io
#     # Fix encoding for Windows console
#     if sys.platform == 'win32':
#         sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
#         sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
#     topic = input("\nEnter topic: ")

#     # STEP 1 → SUMMARY
#     summary = summarize_topic(topic)
#     print("\n📄 SUMMARY:\n", summary)

#     # STEP 2 → AUDIO
#     audio_filename = re.sub(r'[^A-Za-z0-9_]', '_', topic) + ".mp3"
#     text_to_speech(summary, audio_filename)

#     # STEP 3 → START VIDEO GENERATION
#     thread = threading.Thread(target=render_video, args=(topic,))
#     thread.start()

#     # STEP 4 → PLAY AUDIO
#     print("\n▶ Playing narration while video renders...\n")
#     playsound(audio_filename)

#     # WAIT FOR VIDEO
#     print("\n⏳ Waiting for video rendering to complete...")
#     thread.join()

#     # STEP 5 → MCQ QUIZ GENERATOR
#     print("\n🧠 Generating quick test...")
#     quiz = generate_questions(topic)

#     print("\n==============================")
#     print("📚 QUIZ ON TOPIC:")
#     print("==============================\n")
#     print(quiz)

#     print("\n🎉 DONE — Video rendering, narration, and quiz complete!\n")