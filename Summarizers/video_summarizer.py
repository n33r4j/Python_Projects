# YOUTUBE VIDEO SUMMARIZER

# NOTES:
# This only works for videos with a single narrator. For example TED talks.
# For videos with multiple people speaking, try to convert the xml into a usable script. TODO

# dotenv reference (https://saurabh-kumar.com/python-dotenv/)

from pytube import YouTube
import re
import argparse
from openai import OpenAI
from dotenv import load_dotenv
import pyttsx3
import tiktoken


MODEL = "gpt-3.5-turbo"
MAX_LIMIT = 3800 # Actual limit is 4096 tokens (it's actually 16385 tokens ?)


def num_tokens_from_string(in_string: str, encoding_name: str) -> int:
	encoding = tiktoken.encoding_for_model(encoding_name)
	num_tokens = len(encoding.encode(in_string))
	return num_tokens


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
	queries = []
	words = words.split()
	
	while words:
		if len(words) > MAX_LIMIT:
			queries.append(" ".join(words[:MAX_LIMIT]))
			words = words[MAX_LIMIT:]
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

def getSummary(queries, speak=False, force=False, trunc=False):
	if len(queries) > 1 and not force and not trunc:
		print(len(queries))
		for q in queries:
			print(q)
			print(len(q))
		
		print("ChatGPT 3.5 turbo can only accept 4096 tokens. So we either need to trim down this text or use ChatGPT 4.0, which can take up to 20.000 tokens I think.")
		print("If you'd like to try submitting the prompt anyway, try again using the '-f' flag.")

	else:
		isAPIKeyLoaded = load_dotenv()
		client = OpenAI()
		
		if force:
			token_count = num_tokens_from_string(" ".join(queries), MODEL)
			print("token count: ", token_count)
			if token_count > MAX_LIMIT:
				print(f"The number of tokens is greater than the soft limit of {MAX_LIMIT} tokens. Because of this, there's a chance that the response might be incomplete.")
				print("Submitting anyway...")
		
		completion = client.chat.completions.create(
			model=MODEL,
			messages=[
				{"role": "system", "content": "You are an expert in STEM and summarizing a wide variety of topics."},
				{"role": "user", "content": "Summarize the following text in up to 5 bullet points. Also list the key takeaways." + (" ".join(queries))}
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
	parser.add_argument("-f", "--force", help = "Try submitting the query to ChatGPT anyway and hope for the best", action="store_true")
	parser.add_argument("-t", "--trunc", help = "TODO: Submit the first 3000 words as a query to ChatGPT", action="store_true")
	
	args = parser.parse_args()
	
	# TODO
	if args.trunc:
		print("Sorry, --trunc hasn't been implemented yet.")
	
	if args.force and args.trunc:
		print("Both --force and --trunc can't be set at the same time. Please pick one or neither.")
	
	else:
		transcript = getTranscriptAsText(args.link)
		clean_text = getCleanedText(transcript)
		
		if not args.skip:
			prompts = breakIntoPrompts(clean_text)
			getSummary(prompts, speak=True, force=args.force, trunc=args.trunc)
		else:
			print("=== Transcript ===")
			print(clean_text)