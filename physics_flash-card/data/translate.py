import pandas as pd
from googletrans import Translator

# Bestandspaden
input_file = "physics.csv"  # Je oorspronkelijke CSV-bestand
output_file = "physics_translated.csv"  # Het bestand met vertalingen

# Lees het CSV-bestand
data = pd.read_csv(input_file)

# Initialiseer de vertaler
translator = Translator()

# Functie om tekst te vertalen
def translate_text(text):
    if isinstance(text, str) and text.strip():  # Alleen niet-lege strings vertalen
        try:
            translated = translator.translate(text, src='nl', dest='en')
            return translated.text
        except Exception as e:
            return text  # Geef originele tekst terug als vertaling mislukt
    return text  # Geen vertaling nodig voor lege waarden

# Pas de vertaling toe op elke cel
translated_data = data.applymap(translate_text)

# Opslaan naar een nieuw CSV-bestand
translated_data.to_csv(output_file, index=False)

print(f"Vertaling voltooid! Het bestand is opgeslagen als {output_file}")
