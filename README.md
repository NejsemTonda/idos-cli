# IDOS command line interface

Vítejte v IDOS CLI, nástroji pro pohodlné a rychlé vyhledávání spojů pomocí webové aplikace iDOS. Tento prográmek vám umožňuje snadno a efektivně plánovat cesty a získávat informace o veřejné dopravě přímo z příkazové řádky.

## Dependencies

* bs4
* requests

## Usage

* Pro vyhledání spoje ze zastávku `FromStation` do zastávky `ToStation`:

        `python main.py FromStation - ToStation`

    - např. vyhledaní spoje z Kuchyňky na Malostranské náměstí:

          `python main.py Kuchyňka - Malostranské Náměstí`

  (argument musí obsahovat pomlčku)

* Místo celého názvu zastávky, lze zadat i jeho zkrácená forma:

        `python main.py kuch - malo nam`

* Já mám na main nastavený sim lin:   

        `ln -s ~/path/to/main/main.py idos`
        `idos kuch - malo nam`

K dispozici je několik flagů:
*  `-d`, `--department` čas odjezdu (např. now, 16:37, 20min)
*  `-a`, `--arrival`    čas příjezdu (např. now, 16:37, 20min)
*  `-v`, `--via`        přes zastávky
*  `-x`, `--exclude `   vyjma doprvaních prostředků (může být: bus, tram, metro, vlak)
*  `-o`, `--only`       jenom tyto dopravní porstředky (může být: bus, tram, metro, vlak)

Např:
* Z dvorců na hlavní nádraží bez metra:

        `python main.py dvorce - hl nad -x metro`
  
* Z Budějovické na Malostranské náměstí s příjezdem v 9:10 :

          `python main.py bude - malo nam -a 9:10
  

### TODO

* Vyhledávání spoje
    * správný request ✅
    * select timetables ✅
    * pretty output ✅
    * víc než první tři
* doplnění celého jména (např. sm n --> smíchovské nádraží) ✅
* čas (-t now, 20min, 16:37, ...)
    * -a and -d flagy pro konkrétní časy (hh:mm) ✅
* přes
* filtrování (jenom tramvaje, bez metra, ...)✅
* tvoření aliasů "ms = Malostranské náměstí"
* fix bug "idos arbes - narodni div"
