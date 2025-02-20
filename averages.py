import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
args = parser.parse_args()

if __name__ == "__main__":
    df = pd.read_csv(args.input_file)

    averages = df.iloc[:, 1:].mean()

    print("Averages:")
    print(averages)
