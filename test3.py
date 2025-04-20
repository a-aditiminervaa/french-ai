import csv

def create_csv_file(file_path):
    # Sample words; replace these with your actual list of 250 French words
    words = ["Bonjour", "Merci", "Pomme", "Chien", "Chat"]

    # Create and write to the CSV file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write each word on a new line
        for word in words:
            writer.writerow([word])

# Specify the path for the new CSV file
csv_file_path = "frenchWordsDataset.csv"  # This will create the file in the current directory

# Create the CSV file
create_csv_file(csv_file_path)

print(f"CSV file '{csv_file_path}' created successfully.")
