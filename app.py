import streamlit as st
import pandas as pd
import pyperclip

# Set page config
st.set_page_config(page_title="Kommandoreferens för utvecklare", layout="wide")

# Define the commands data
commands_data = {
    "Git & GitHub": [
        ("git init", "Initiera ett nytt Git-repository"),
        ("git clone [url]", "Klona ett repository"),
        ("git add [fil]", "Lägg till filer för commit"),
        ("git commit -m \"[meddelande]\"", "Commita ändringar"),
        ("git push", "Pusha ändringar till remote repository"),
        ("git pull", "Hämta och merga ändringar från remote repository"),
        ("git branch", "Lista, skapa eller ta bort branches"),
        ("git checkout [branch-namn]", "Byt till en annan branch"),
        ("git merge [branch]", "Merga en branch till den aktiva branchen"),
    ],
    "VS Code": [
        ("Ctrl+P (Cmd+P på Mac)", "Öppna snabbsökning"),
        ("Ctrl+Shift+P (Cmd+Shift+P)", "Öppna kommandopalett"),
        ("Ctrl+` (Ctrl+`)", "Öppna/stäng integrerad terminal"),
        ("Ctrl+B (Cmd+B)", "Visa/dölj sidofältet"),
        ("Ctrl+, (Cmd+,)", "Öppna inställningar"),
    ],
    "Python": [
        ("python [filnamn.py]", "Kör en Python-fil"),
        ("pip install [paketnamn]", "Installera paket"),
        ("python -m venv [miljönamn]", "Skapa en virtuell miljö"),
        ("source [miljönamn]/bin/activate", "Aktivera virtuell miljö (Unix)"),
        ("[miljönamn]\\Scripts\\activate.bat", "Aktivera virtuell miljö (Windows)"),
    ],
    "Node.js & npm": [
        ("node [filnamn.js]", "Kör en JavaScript-fil med Node.js"),
        ("npm init", "Initiera ett nytt npm-projekt"),
        ("npm install [paketnamn]", "Installera paket"),
        ("npm start", "Starta utvecklingsservern"),
        ("npm run build", "Bygg projektet för produktion"),
    ],
    "React & TypeScript": [
        ("npx create-react-app [projektnamn]", "Skapa ett nytt React-projekt"),
        ("npx create-react-app [projektnamn] --template typescript", "Skapa React-projekt med TypeScript"),
        ("npm start", "Starta utvecklingsserver"),
        ("npm test", "Kör tester"),
        ("npm run build", "Bygga för produktion"),
    ],
    "Heroku": [
        ("heroku login", "Logga in på Heroku CLI"),
        ("heroku create", "Skapa en ny Heroku-app"),
        ("git push heroku main", "Deploya din app till Heroku"),
        ("heroku ps:scale web=1", "Skala din app till en web dyno"),
        ("heroku open", "Öppna din app i webbläsaren"),
    ],
    "Docker": [
        ("docker build -t [image-name] .", "Bygg en Docker-image från en Dockerfile"),
        ("docker run [image-name]", "Kör en container från en image"),
        ("docker ps", "Lista körande containers"),
        ("docker-compose up", "Starta tjänster definierade i docker-compose.yml"),
    ],
    "SQL": [
        ("SELECT * FROM [table_name];", "Hämta alla rader från en tabell"),
        ("INSERT INTO [table_name] (column1, column2) VALUES (value1, value2);", "Lägg till en ny rad i en tabell"),
        ("UPDATE [table_name] SET column1 = value1 WHERE condition;", "Uppdatera data i en tabell"),
    ],
    "REST API": [
        ("GET /api/resource", "Hämta en resurs"),
        ("POST /api/resource", "Skapa en ny resurs"),
        ("PUT /api/resource/:id", "Uppdatera en befintlig resurs"),
        ("DELETE /api/resource/:id", "Ta bort en resurs"),
    ],
    "Bash/Terminal": [
        ("ls", "Lista filer och mappar"),
        ("cd [directory]", "Byt katalog"),
        ("mkdir [directory]", "Skapa en ny mapp"),
        ("touch [filename]", "Skapa en ny fil"),
    ],
    "Streamlit": [
        ("streamlit run [app.py]", "Kör en Streamlit-applikation"),
        ("Ctrl + Shift + P", "Öppna kommandopaletten i VS Code"),
        ("Python: Select Interpreter", "Välj Python-tolk med Streamlit installerat (via kommandopaletten)"),
        ("Terminal: Create New Terminal", "Öppna en ny terminal i VS Code (via kommandopaletten)"),
        ("Ctrl + C", "Stoppa den körande Streamlit-appen i terminalen"),
        ("Ctrl + S", "Spara ändringar (Streamlit uppdateras automatiskt)"),
        ("Ctrl + F5", "Kör Python-filen utan debugging (kan användas för Streamlit-appar)"),
        ("ext install ms-python.python", "Installera Python-tillägget i VS Code (kör i VS Code-terminalen)"),
        ("pip install streamlit", "Installera Streamlit i din Python-miljö (kör i VS Code-terminalen)"),
    ],
}

# Function to filter commands based on search query
def filter_commands(df, query):
    return df[df['Command'].str.contains(query, case=False) | df['Description'].str.contains(query, case=False)]

# Function to copy command to clipboard
def copy_to_clipboard(command):
    pyperclip.copy(command)
    st.success(f"Kommando kopierat: {command}")

# Title
st.title("Kommandoreferens för utvecklare")

# Search box
search_query = st.text_input("Sök efter kommandon...")

# Convert commands_data to a DataFrame
all_commands = [(cmd, desc, category) for category, commands in commands_data.items() for cmd, desc in commands]
df = pd.DataFrame(all_commands, columns=['Command', 'Description', 'Category'])

# Filter commands based on search query
filtered_df = df.copy()
if search_query:
    filtered_df = filter_commands(df, search_query)

# Function to add a copy button next to each command
def render_command(command, unique_key):
    st.code(command)
    if st.button("Kopiera", key=f"{unique_key}"):
        copy_to_clipboard(command)

# Create tabs
if not filtered_df.empty:
    tabs = st.tabs(["Alla"] + list(commands_data.keys()))

    # Display commands in the "Alla" tab
    with tabs[0]:
        for index, row in filtered_df.iterrows():
            render_command(row['Command'], f"All-{index}")
            st.write(row['Description'])
            st.write("---")

    # Display commands in each category-specific tab
    for i, (category, commands) in enumerate(commands_data.items(), start=1):
        with tabs[i]:
            category_df = df[df['Category'] == category].reset_index(drop=True)
            if search_query:
                category_df = filter_commands(category_df, search_query)
            if not category_df.empty:
                for index, row in category_df.iterrows():
                    render_command(row['Command'], f"{category}-{index}")
                    st.write(row['Description'])
                    st.write("---")
            else:
                st.write(f"Inga kommandon hittades i kategorin {category}.")
else:
    st.write("Inga kommandon hittades för söktermen.")

# Improve the layout with CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background-color: #E8EAF6;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        text-align: center;
        color: #1a237e;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3F51B5;
        color: white;
    }
</style>
""", unsafe_allow_html=True)
