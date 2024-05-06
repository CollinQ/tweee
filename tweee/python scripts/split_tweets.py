import ijson
import json
from decimal import Decimal

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Convert Decimal instances to string to preserve precision
        return json.JSONEncoder.default(self, obj)

def split_json_file(input_file, output_file1, output_file2):
    with open(input_file, 'rb') as file:
        items = ijson.items(file, 'item')
        count = 0
        total_items = sum(1 for _ in ijson.items(file, 'item'))  # Efficient count without loading data
        half_point = total_items // 2
        file.seek(0)  # Reset file pointer to the beginning after counting

        with open(output_file1, 'w') as file1, open(output_file2, 'w') as file2:
            file1.write('[')
            file2.write('[')
            first = True  # Track the first item to manage commas in JSON array

            for i, item in enumerate(items):
                if i < half_point:
                    if not first:
                        file1.write(',')
                    json.dump(item, file1, cls=CustomEncoder, indent=4)
                else:
                    if not first:
                        file2.write(',')
                    json.dump(item, file2, cls=CustomEncoder, indent=4)
                first = False
            
            file1.write(']')
            file2.write(']')

    print(f"Split the file into {output_file1} and {output_file2}.")

if __name__ == "__main__":
    input_file = 'modified_concatonated_tweets.json'
    output_file1 = 'part1.json'
    output_file2 = 'part2.json'
    split_json_file(input_file, output_file1, output_file2)
