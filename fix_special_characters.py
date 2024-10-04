import pandas as pd
import re

# Read the CSV file with mixed special characters
try:
    df = pd.read_csv('Pysakointivirheet_Vantaalla.csv', encoding='ISO-8859-1', sep=';')
except UnicodeDecodeError:
    df = pd.read_csv('Pysakointivirheet_Vantaalla.csv', encoding='Windows-1252', sep=';')

# Fix special characters
def fix_special_chars(text):
    if isinstance(text, str):
        # Replace common incorrect characters with the correct ones
        text = text.replace('ï¿½', 'ä')
        text = text.replace('ï', 'ä')
        text = text.replace('¿', 'ö')
        text = text.replace('½', 'å')
    return text

# Iterate through each column and fix special characters
for column in df.columns:
    df[column] = df[column].apply(fix_special_chars)

# Save the corrected file
df.to_csv('Pysakointivirheet_Vantaalla_fixed.csv', encoding='utf-8', index=False, sep=';')

print("Corrected file saved: Pysakointivirheet_Vantaalla_fixed.csv")