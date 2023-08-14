# Šachy 3x3
Program na vstupu od uživatele přijme nynější stav šachovnice. Pokud pak existuje řešení za předpokladu toho, že první byl na řadě hráč s bílými figurami a pak až hráč s modrými figurami a že hráč s bílými figurkami se do tohoto stavu dostal co nejmenším počtem kroků, tak na výstup zvlášť vrátí tahy 1. hráče s bílými figurkami a tahy 2. hráče s modrými figurkami takové, aby hra dospěla z počáteční pozice do stavu zadaného uživatelem. Pak také pomocí animace tyto tahy postupně vizualizuje. Zároveň jsou do jednoho souboru nazvaného temp zapisovány všechny případy, které program vyzkoušel a do dalšího souboru nazvaného results je zapsán výsledek. Pokud pak řešení neexistuje, tak program vypíše na output: „No solution found!" a do souboru temp zapíše všechny vyzkoušené případy.

Pozn.: Pro rychlejší běh programu se předpokládá, že král může vstoupit do šachu.

<div align="left">
  <p>Počáteční pozice:</p>
  <img src="https://github.com/theosa88/3x3_chess/assets/141501863/f822db65-8e6a-4898-90f9-d88904c1060e">
</div>

## Uživatelská část
### Spuštění
Před samotným spuštěním je potřeba nainstalovat Python a v adresáři projektu spustit pip install -r requirements.txt. Hra se pak následně spustí přikazem python3 index.py v adresáři projektu.

### Umístění bílých figurek
Klikáním myší na jednotlivá políčka šachovnice uživatel zadá nejdříve stav bílých figurek (opětovným klikáním na dané políčko se nejdříve na daném políčku objeví pěšec, pak že se na políčku nic nenachází, střelec, opět že se tam na něm nic nenachází a nakonec král). Pokud je tam již umístěna jedna figurka, tak již nelze na šachovnici umístit tu stejnou figurku stejné barvy.

### Umístění modrých figurek
Po umístění všech bílých figurek pak po kliknutí na políčko Change Color může následně uživatel umístit tím samým způsobem modré figurky.

## Programátorská část
Celý kód se nachází v souboru nazvaném index. Popis jednotlivých proměnných nebo toho, co dělají jednotlivé funkce v programu, je buď uveden přímo v kódu nebo je z něj přímo patrné, co značí či dělají. 

Použité externí knihovny jsou: wx, deque from collections.

### Index
Využívá externí knihovnu wxPython k vytvoření grafického uživatelského rozhraní (GUI) pro šachovnici 3x3, na kterou pak uživatel může umístit nejvýše 6 figurek buď modré nebo bílé barvy (pěšec, střelec, král). To může učinit klikáním na jednotlivá tlačítka reprezentující jednotlivá pole na šachovnici, přičemž při kliknutí na prázdné políčko se figurky cyklicky mění a při kliknutí na figurku je možné jí odebrat.

Dále je tam tlačítko Change Color pro změnu barvy a tlačítko Return, po jehož stisknutí dojde k vrácení aktuálních pozic šachových figurek hráčů spolu s informací o tom, o jaké figurky se jedná.

Pak dochází k postupnému generování možných budoucích stavů hry, a to na základě pravidel, jak se mohou dané figurky na šachovnici pohybovat. Pokud se současný generovaný stav shoduje s tím, který byl zadán uživatelem, tak se výpočet zastaví a dojde k vypsání všech provedených tahů figurkami i ke spuštění animace, která postupně ukazuje i dané pohyby figurek na šachovnici.

### Datové struktury
Použité datové struktury jsou:
- lists of lists: uložení tlačítek na šachovnici (self.button_grid), barev tlačítek (self.button_colors), obrázků nacházejících se na tlačítkách (self.button_images) a navíc ještě dostupných figurek pro každou barvu (self.unused_pieces)
- strings (identifikace barvy (bílá/modrá), typ figurky (pěšec, střelec, král))
- slovníky: unused_pieces (keys - barvy, values - seznamy, v nichž jsou indexy obrázků figurek), movement_rules (klíče: názvy šachových figurek, values - možné tahy figurky po šachovnici), počáteční a konečný stav hry (keys - pozice na šachovnici, values - šachové figurky na daných pozicích)
- sets: ukládání již navštívených stavů
- deque: ukládání stavů hry, které ještě mají být prohledány
- seznamy: uložení aktuálních pozic bílých a modrých šachových figurek, počátečních pozic šachových figurek, sekvence výsledných tahů 
- tuples: pozice + název figurky, zaznamenání tahů

### Algoritmy
- BFS: V programu je použito prohledávání do šířky (BFS), což je algoritmus  určený k průchodu všech vrcholů daného grafu, který se často využívá k hledání nejkratší cesty mezi dvěma vrcholy grafu. Při uplatnění tohoto algoritmu nejdříve dojde k prozkoumání všech sousedů výchozího vrcholu, pak k prozkoumání všech sousedů jednoho ze sousedů výchozího vrcholu apod. (přitom se však musí kontrolovat, zda se do jednoho vrcholu nepřišlo vícekrát), a to do té doby, dokud nedojde k nalezení cílového vrcholu nebo k dokud nedojde k prozkoumání všech vrcholů v daném grafu. V rámci tohoto algoritmu navíc dochází k využití fronty, ve které jsou uloženy dosud nenavštívené vrcholy.
V tomto programu je graf reprezentován pomocí stavů hry (ty představují vrcholy grafu) a možných tahů z jednoho stavu do druhého (hrany). Dochází k postupnému procházení všech stavů hry dostupných z aktuálního stavu, přičemž se začíná z počátečního stavu, a to až do doby nalezení stavu, který odpovídá stavu zadaného uživatelem. 

- rekurze: průchod všech možných tahů z aktuálního stavu
- hashování: kontrola, zda byl již daný stav hry prozkoumán
