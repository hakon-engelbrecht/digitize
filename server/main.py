import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, text

# Datenbankverbindung und Metadaten Objekt erstellen
engine = create_engine('sqlite:///buchhaltung.db')
metadata = MetaData()

# Tabelle definieren
transaktionen = Table('transaktionen', metadata,
                      Column('Rechnungsnummer', Integer, primary_key=True),
                      Column('Datum', Date),
                      Column('Beschreibung', String),
                      Column('Betrag', Float),
                      Column('Kategorie', String),
                      Column('Zahlungsmethode', String),
                      Column('Fälligkeitsdatum', Date),
                      Column('Bezahlt', String)
                      )

# Tabelle in der Datenbank erstellen
metadata.create_all(engine)

def load_data(filepath):
    return pd.read_excel(filepath)


def insert_data_to_db(df, table_name):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)


def process_excel_to_db(filepath, table_name='transaktionen'):
    data = load_data(filepath)
    if not data.empty:
        insert_data_to_db(data, table_name)
        print("Daten erfolgreich in die Datenbank importiert.")
    else:
        print("Keine Daten zum Importieren gefunden.")


async def process_file(file, table_name='transaktionen'):
    data = await file.read()
    if not data.empty:
        insert_data_to_db(data, table_name)
        print("Daten erfolgreich in die Datenbank importiert.")
    else:
        print("Keine Daten zum Importieren gefunden.")


def generate_guv(df):
    current_year = datetime.now().year
    df_this_year = df[df['Datum'].dt.year == current_year]
    revenue = df_this_year[df_this_year['Betrag'] > 0]['Betrag'].sum()
    expenses = df_this_year[df_this_year['Betrag'] < 0]['Betrag'].sum()
    profit = revenue + expenses
    print('')
    print(f"GuV für das Jahr {current_year}: Einnahmen: {revenue}, Ausgaben: {expenses}, Gewinn: {profit}")
    print('')
    return revenue, expenses, profit


def generate_liquidity_plan(df):
    # Stelle sicher, dass 'Fälligkeitsdatum' als Datum interpretiert wird
    if not pd.api.types.is_datetime64_any_dtype(df['Fälligkeitsdatum']):
        df['Fälligkeitsdatum'] = pd.to_datetime(df['Fälligkeitsdatum'], errors='coerce')

    # Berechnung zukünftiger Forderungen und Verbindlichkeiten mit korrekter Klammersetzung
    future_receivables = df[(df['Fälligkeitsdatum'] > pd.to_datetime('today')) & (df['Betrag'] > 0)]
    future_payables = df[(df['Fälligkeitsdatum'] > pd.to_datetime('today')) & (df['Betrag'] < 0)]
    net_liquidity = future_receivables['Betrag'].sum() + future_payables['Betrag'].sum()

    print(f"Zukünftige Einnahmen: {future_receivables['Betrag'].sum()}, Zukünftige Ausgaben: {future_payables['Betrag'].sum()}, Netto-Liquidität: {net_liquidity}")
    return future_receivables, future_payables, net_liquidity



def validate_data(df):
    if df.isnull().any().any():
        print("Warnung: Es gibt fehlende Werte in den Daten.")
        df = df.fillna(method='ffill')  # Füllen fehlender Werte
    if not pd.api.types.is_datetime64_any_dtype(df['Datum']):
        df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')
    # Stelle sicher, dass 'Fälligkeitsdatum' auch als Datum interpretiert wird
    if not pd.api.types.is_datetime64_any_dtype(df['Fälligkeitsdatum']):
        df['Fälligkeitsdatum'] = pd.to_datetime(df['Fälligkeitsdatum'], errors='coerce')
    return df


def overdue_payments(df):
    # Konvertiere 'Fälligkeitsdatum' sicherheitshalber noch einmal
    if not pd.api.types.is_datetime64_any_dtype(df['Fälligkeitsdatum']):
        df['Fälligkeitsdatum'] = pd.to_datetime(df['Fälligkeitsdatum'], errors='coerce')
    today = pd.to_datetime('today')
    overdue = df[(df['Fälligkeitsdatum'] < today) & (df['Bezahlt'] == 'Nein')]
    return overdue


def load_data_from_database():
    try:
        return pd.read_sql_query('SELECT * FROM transaktionen', con=engine)
    except Exception as e:
        print(f"Ein Fehler ist beim Laden der Daten aufgetreten: {e}")
        return pd.DataFrame()

def detect_duplicates(df):
    duplicates = df[df.duplicated('Rechnungsnummer', keep=False)]
    if not duplicates.empty:
        print("Warnung: Duplikate gefunden.\n", duplicates)
    return df.drop_duplicates('Rechnungsnummer', keep='first')

def correct_data(df):
    df['Betrag'] = pd.to_numeric(df['Betrag'], errors='coerce')
    return df

def save_data_to_database(df):
    df.to_sql('transaktionen_processed', con=engine, if_exists='replace', index=False)

def calculate_sums(df):
    return df.groupby('Kategorie')['Betrag'].sum()

def visualize_data(df):
    sums = calculate_sums(df)
    if not sums.empty:
        sums.plot(kind='bar')
        plt.title('Summen nach Kategorien')
        plt.xlabel('Kategorie')
        plt.ylabel('Betrag')
        plt.savefig('sums_by_category.png')
    else:
        print("Keine Daten zum Visualisieren vorhanden.")


def check_database_data():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM transaktionen"))
        for row in result:
            print(row)

        print('')
        print('')
        print('')


def generate_reports(df):
    sums_report = calculate_sums(df)
    overdue_report = overdue_payments(df)
    return sums_report, overdue_report

def send_reminders(df):
    overdue = overdue_payments(df)
    for index, row in overdue.iterrows():
        print(f"Erinnerung gesendet an: {row['Kunde']} für Rechnung {row['Rechnungsnummer']}")

def process_accounting_data():
    process_excel_to_db('Buchhaltungsdaten.xlsx')
    data = load_data_from_database()
    data = validate_data(data)
    data = detect_duplicates(data)
    data = correct_data(data)
    save_data_to_database(data)
    check_database_data()
    visualize_data(data)
    revenue, expenses, profit = generate_guv(data)
    future_receivables, future_payables, net_liquidity = generate_liquidity_plan(data)

    sums_report, overdue_report = generate_reports(data)
    send_reminders(data)

    print("Finanzbericht nach Kategorien:\n", sums_report)
    if not overdue_report.empty:
        print("Überfällige Zahlungen:\n", overdue_report)
    else:
        print("Keine überfälligen Zahlungen.")

    print("Datenverarbeitung abgeschlossen.")

if __name__ == "__main__":
    process_accounting_data()

#%%

#%%
