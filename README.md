# Bostadsmarknadsanalys i Norrbotten

## Översikt

Detta projekt syftar till att analysera bostadsmarknaden i Norrbotten med hjälp av data från [Hemnet](https://www.hemnet.se/). Genom att använda data från Hemnet kan vi få insikter om bostadspriser, trender och marknadsdynamik i Norrbotten-regionen.

## Syften
1. **Köra på Server:**
   - Programmet kan köras automatiskt på en server som i mitt fall är en linux server, programmet kan ställas in att köras 1 gång om dagen och om det känner av att det finns en ny annons så kommer man att bli meddelad. För att köras på en linus serveras behövs
     några saker fixas.

2. **Köra Lokalt:**
   - Programmet kan även köras lokalt för att manuellt analysera data och se detaljerade resultat. Detta är användbart för att utföra djupare analyser och visualiseringar utöver den dagliga insamlingen av data på servern.

## Funktioner

- **Datainsamling:** Skript för att hämta bostadsannonser och relevanta data från Hemnet.
- **Dataanalys:** Verktyg och metoder för att analysera insamlad data och identifiera trender.
- **Rapportering:** Meddela ifall en ny annons läggs till.

## Bibliotek och Verktyg

För att köra och utveckla projektet **Bostadsmarknadsanalys i Norrbotten** krävs följande bibliotek och verktyg:

### Nödvändiga Bibliotek

1. **Pandas**
   - **Beskrivning:** Ett bibliotek för databehandling och analys. Pandas används för att hantera och bearbeta data i tabellform (DataFrames) och är särskilt användbart för analys och rapportering.
   - **Installation:**
     ```bash
     pip install pandas
     ```

2. **Selenium**
   - **Beskrivning:** Ett verktyg för webbscraping och automatisering av webbläsare. Selenium används för att interagera med webbsidor och hämta data från dynamiska webbplatser som Hemnet.
   - **Installation:**
     ```bash
     pip install selenium
     ```
   - **Krav:** En webbläsardrivrutin (t.ex., ChromeDriver) måste också installeras och vara tillgänglig i din PATH.

3. **BeautifulSoup**
   - **Beskrivning:** Ett bibliotek för att parsa och extrahera data från HTML- och XML-dokument. BeautifulSoup används för att analysera och extrahera information från webbsidans HTML-kod.
   - **Installation:**
     ```bash
     pip install beautifulsoup4
     ```

4. **SQLAlchemy**
   - **Beskrivning:** Ett SQL-verktyg och ORM (Object Relational Mapper) som gör det möjligt att interagera med databaser på ett objektorienterat sätt. SQLAlchemy används för att definiera databasmodeller och utföra databasoperationer.
   - **Installation:**
     ```bash
     pip install sqlalchemy
     ```

5. **PostgreSQL**
   - **Beskrivning:** En populär relationsdatabas. För att kunna interagera med en PostgreSQL-databas från Python används en kompatibel databasdrivrutin.
   - **Installation:**
     ```bash
     pip install psycopg2-binary
     ```
   - **Alternativ:** Om du använder PostgreSQL som databas, se till att PostgreSQL-servern är installerad och konfigurerad på din server eller lokal maskin.

6. **smtplib**
   - **Beskrivning:** En inbyggd Python-modul för att skicka e-post via SMTP. Används för att skicka e-postmeddelanden som alertmeddelanden.
   - **Installation:** Ingen installation krävs eftersom `smtplib` är en del av Python:s standardbibliotek.

7. **email.mime**
   - **Beskrivning:** En inbyggd modul som används för att skapa och hantera e-postmeddelanden med olika typer av innehåll (t.ex. text, HTML).
   - **Installation:** Ingen installation krävs eftersom `email.mime` är en del av Python:s standardbibliotek.

## Installationsguide

För att installera alla externa bibliotek som nämns ovan kan du köra följande kommando i din terminal:

```bash
pip install -r requirements.txt
```
## Server setup (linux)

FÖr att kunna köra programmet på en server behövs följande:
- clona repot med kommandot
  ```bash
  git clone https://github.com/strandafredde/Bostadsmarknadsanalys
  ```
- Updatera package list
  ```bash
  sudo apt update
  ```
- Installera oython 3
  ```bash
  sudo apt install python3
  ```
- Skapa och aktivera ett Virtual Environment
  ```bash
  python3 -m venv myenv
  source myenv/bin/activate
  ```
- Insallera biblioteken
  ```bash
  pip install -r requirements.txt
  ```
- Installera databasen (Postgresql)
  ```bash
  sudo apt-get install postgresql postgresql-contrib
  ```
- Ladda ner google chrome och en googledriver
  ```bash
  wget https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.119/linux64/chrome-linux64.zip
  sudo dpkg -i google-chrome-stable_current_amd64.deb
  sudo apt-get install -f
  ```
  ```bash
  wget https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.119/linux64/chromedriver-linux64.zip
  unzip chromedriver-linux64.zip
  chmod +x chromedriver
  sudo mv chromedriver /usr/local/bin/
  ```
- Skapa automatiskt script som körs en gång per dag
  ```bash
  crontab -e
  0 6 * * * Bostadsmarknadsanalys/venv/bin/python3 Bostadsmarknadsanalys/main.py >> Bostadsmarknadsanalys/logfile.log 2>&1
  ```
Nu borde programmet köras varje dag kl 06:00 kan variera beroende på tidszon
(Kan behöva ändra filvägarna i crontab -e beroende på vart github repot blev clonat




