# Vejr, Valuta og Nyheder
#### Få de seneste nyheder, vejropdateringer og valutakurser i én og samme app.

### Beskrivelse
Appen er delt op i tre sektioner; Vejr, Valuta og Nyheder, som vil blive beskrevet hver for sig længere nede. Den har en overskuelig og brugervenlig UI, hvor brugeren nemt kan navigere til de forskellige sider via ikonerne i toppen af siden. Appen er mobilvenlig da indholdet tilpasser sig bredden af viewporten. I tests.py er der opstillet tests for brugermodellens password funktioner, samt de API'er der bruges. Hvis appens debug mode er sat til False og der opstår en fejl vil fejlen blive logget til /logs og en email bliver sendt for at underrette admin. Logfilerne roteres således at de er nemmere at håndtere.

#### Vejr
- Byer tilføjes i input feltet. Hvis bruger er logget ind, tilføjes de indtastede byer til databasen og hentes igen næste gang brugeren logger ind. Byerne kan også slettes igen. Hvis bruger ikke er logget ind, vises vejr stadig for indtastet by, men der kan i så fald kun vises en by ad gangen. De indtastede byer hentes via OpenWeatherMap API.

#### Valuta
- Currencylayer API bruges her til at hente seneste valutakurser med euroen som udgangspunkt.

#### Nyheder
- Request og BeautifulSoup bruges til at scrape seneste nyheder fra tre af landets største nyhedssites, hhv. TTV2, Jyllands-Posten of Børsen. Overskrifterne bliver herefter præsenteret på siden med et link til artiklen. Titler på artikler kan ikke altid hentes, derfor tester scriptet om titlen kunne hentes, og hvis ikke, vises link til artiklen istedet.

### Diskussion
Efter som valuta API'en kun tillader anmodninger for de seneste kurser med euroen som udgangspunkt gør det funktionen en smule kedelig. Med en premium version af API'en kan man dog sende mere alsidige anmodninger som f.eks. vælge fra -og til valutaer samt beløb. Dette er meget simpelt at implentere og ville gøre funktionen bedre, men forudsætter at man har en API key der tillader det.

#### Idéer der kunne implementeres:
- Appen kunne udvides ved at tilføje flere nyheds sites, og evt. en side-menu hvor brugeren kunne sortere i aviser.
- Hvis appen havde mange brugere kunne antallet af API anmodninger reduceres ved at lave et script der foretager en API anmodning på fx. de 100 mest anmodede byer hver 10 minut og gemme resultatet i databasen. Når en bruger så indtaster en by vil appen først tjekke databasen og hvis byen ikke findes i db vil den foretage en API anmodning. Dette kan være en foretrukken løsning da mange API'er(som f.eks. den jeg har brugt) har et loft for anmodninger der kan foretages dagligt, og det vil i mange tilfælde også være hurtigere eftersom resultatet vil blive hentet fra db.