# Bostadsmarknadsanalys i Norrbotten

## Översikt

Detta projekt syftar till att analysera bostadsmarknaden i Norrbotten med hjälp av data från [Hemnet](https://www.hemnet.se/). Genom att använda data från Hemnet kan vi få insikter om bostadspriser, trender och marknadsdynamik i Norrbotten-regionen.

## Funktioner

- **Datainsamling:** Skript för att hämta bostadsannonser och relevanta data från Hemnet.
- **Dataanalys:** Verktyg och metoder för att analysera insamlad data och identifiera trender.
- **Visualisering:** Diagram och grafer som illustrerar marknadstrender och pristrender i Norrbotten.
- **Rapportering:** Generera rapporter baserade på analyserna.

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
