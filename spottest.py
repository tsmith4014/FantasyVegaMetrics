import csv

def read_csv_to_dict(filename):
    with open(filename, mode='r') as file:
        csv_file = csv.DictReader(file)
        return [row for row in csv_file]

def validate_columns_exist(dataset, columns_to_compare):
    sample_row = dataset[0]  # Take a sample row to check the columns
    for col in columns_to_compare:
        if col not in sample_row:
            return False, f"Column '{col}' not found in dataset"
    return True, "All columns exist"

def compare_datasets(dataset1, dataset2, columns_to_compare):
    # Validate the columns exist in both datasets
    valid1, message1 = validate_columns_exist(dataset1, columns_to_compare)
    valid2, message2 = validate_columns_exist(dataset2, columns_to_compare)

    if not valid1:
        return message1
    if not valid2:
        return message2

    # Datasets can have different lengths
    min_length = min(len(dataset1), len(dataset2))

    for i in range(min_length):
        for col in columns_to_compare:
            if dataset1[i][col] != dataset2[i][col]:
                return f"Mismatch found at index {i} in column {col}. {dataset1[i][col]} != {dataset2[i][col]}"

    return "All specified columns match in the overlapping range."

if __name__ == "__main__":
    dataset1 = read_csv_to_dict('full_player_game_stats.csv')
    dataset2 = read_csv_to_dict('staticdata.csv')

    # Specify the column names you want to compare
    columns_to_compare = ['Date', 'Year', 'Week', 'Age', 'Tm', 'Opp', 'Result', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'Int', 'Rate']

    result = compare_datasets(dataset1, dataset2, columns_to_compare)
    print(result)
