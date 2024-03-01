# YOUTUBE VIDEO SUMMARIZER

# NOTES:
# This only works for videos with a single narrator. For example TED talks.
# For videos with multiple people speaking, try to convert the xml into a usable script. TODO

from pytube import YouTube
import re
import argparse
from openai import OpenAI
from dotenv import load_dotenv
import pyttsx3



def getTranscriptAsText(link):
	video_link = link
	yt = YouTube(video_link)
	yt.bypass_age_gate()

	print("title: ", yt.title)
	print("streams: ", len(yt.streams))
	print("available captions: ", yt.captions)

	# print(yt.captions['a.en'].generate_srt_captions()) # See https://github.com/pytube/pytube/issues/1085 for fix.
	captions_xml = yt.captions['a.en'].xml_captions
	
	text = re.sub("[\<].*?[\>]"," ", captions_xml)
	return text

def getCleanedText(text):

	custom_replacements = {
		# "qar":"Q-star",
		"\n": "",
		"&#39;": "'",
		# "Ai": "AI",
		# "open AI": "OpenAI",
	}

	for r in custom_replacements.keys():
		text = text.replace(r,custom_replacements[r])

	words = text.split()
	# print(words)
	word_count = len(words)
	print(f"Word Count: {word_count}\n")
	clean_text = " ".join(words)

	return clean_text

def breakIntoPrompts(words, print_prompts=False):
	# To feed ChatGPT
	LIMIT = 2950 # Actual limit is 3000 words
	queries = []
	words = words.split()
	
	while words:
		if len(words) > LIMIT:
			queries.append(" ".join(words[:LIMIT]))
			words = words[LIMIT:]
		else: 
			queries.append(" ".join(words[:-1]))
			words = []

	if print_prompts:
		for q in queries:
			print(" ".join(q), end="\n\n")
			
	return queries

def speakText(prose):
	engine = pyttsx3.init('sapi5')

	voices = engine.getProperty('voices')
	rate = engine.getProperty('rate')
	volume = engine.getProperty('volume')

	# for v in voices:
		# print(v.name)

	engine.setProperty('voice', voices[1].id)
	# print(f"rate: {rate}")
	engine.setProperty('rate', rate)
	engine.setProperty('volume', volume-0.25)
	
	engine.say(prose)
	engine.runAndWait()

def getSummary(queries, speak=False):
	if len(queries) > 1:
		print(len(queries))
		for q in queries:
			print(q, len(q))
		
		print("Since ChatGPT only takes prompts upto 3000 words, we have to break up this transcript into several parts. This functionality is yet to be implemented here.")
	else:
		isAPIKeyLoaded = load_dotenv()
		client = OpenAI()
		
		completion = client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are an expert in STEM and summarizing a wide variety of topics."},
				{"role": "user", "content": "Summarize the following text in up to 5 bullet points. Also list the key takeaways." + queries[0]}
			]
		)

		response = completion.choices[0].message.content
		print(response)
		
		if speak:
			speakText(response)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="VideoSummarizer-v1",
									description="Gets the captions of a Youtube video and summarizes it.",
									epilog="")
	
	parser.add_argument("-l", "--link", help = "Link to the YouTube video.", required = True)
	parser.add_argument("-s", "--skip", help = "Skip the summarization", action="store_true")
	
	args = parser.parse_args()
	
	transcript = getTranscriptAsText(args.link)
	clean_text = getCleanedText(transcript)
	
	if not args.skip:
		prompts = breakIntoPrompts(clean_text)
		getSummary(prompts, speak=True)
	else:
		print("=== Transcript ===")
		print(clean_text)