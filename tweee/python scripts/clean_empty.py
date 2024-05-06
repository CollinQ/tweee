import pandas as pd

def clean_csv(file_path, output_file=None):
    """
    Load a CSV file, remove rows where the 'embeddings' column is empty or NaN,
    and save the cleaned data to a new file or overwrite the original file.

    :param file_path: Path to the original CSV file.
    :param output_file: Path to save the cleaned CSV file. If None, overwrite the original.
    """
    # Load the dataset
    df = pd.read_csv(file_path)

    initial_count = len(df)
    print(f"Initial number of rows: {initial_count}")

    df = df.dropna(subset=['Embeddings'])
    df = df[df['Embeddings'].str.strip() != ""]

    final_count = len(df)
    print(f"Number of rows after cleaning: {final_count}")
    print(f"Removed {initial_count - final_count} rows with empty or NaN embeddings.")

    output_file = output_file if output_file else file_path
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

if __name__ == "__main__":
    file_path = 'sample_tweets.csv'
    clean_csv(file_path)
