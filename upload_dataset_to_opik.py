from opik import Opik
import json 

client = Opik()

dataset = client.get_or_create_dataset(name="punjabi_song_lyrics")

# Open and load JSON file
with open('punjabi_lyrics.json', 'r') as file:
    data = json.load(file)

for item in data:
    dataset.insert([
        {"input": item['punjabi_roman_lyrics'], "expected_output": item['english_translation']}
    ])
    




