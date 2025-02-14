import argparse
import json
import csv
import requests

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("--url", default="http://localhost:8000")
parser.add_argument("--output", default="output.csv")
args = parser.parse_args()

def get_rogue_score(candidate, reference):
    response = requests.post(f"{args.url}/rogue_score", json={"candidate": candidate, "reference": reference})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching rogue score: {response.status_code}")
        return None

def get_bert_score(candidate, reference):
    response = requests.post(f"{args.url}/bert_score", json={"candidate": candidate, "reference": reference})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching BERT score: {response.status_code}")
        return None

def process_jsonl_file(input_file: str):
    with open(input_file, "r", encoding="utf-8") as infile, open(args.output, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["key", "rouge1", "rouge2", "rougeL", "bert_score"])
        
        for line in infile:
            data = json.loads(line)
            key = data["key"]
            candidate = data["candidate"]
            reference = data["reference"]
            
            rogue_scores = get_rogue_score(candidate, reference)
            bert_scores = get_bert_score(candidate, reference)
            
            if rogue_scores and bert_scores:
                writer.writerow([
                    key,
                    rogue_scores["rouge1"]["f1"],
                    rogue_scores["rouge2"]["f1"],
                    rogue_scores["rougeL"]["f1"],
                    bert_scores["f1"]
                ])
            else:
                print(f"Skipping key {key} due to an error.")

if __name__ == "__main__":
    process_jsonl_file(args.input_file)
