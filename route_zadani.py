##############
#
# Hledani cesty v grafu (Semestralka)
#
##############

# Podle zadani vytvorte tridu Map, ktera ma metody:
#
# add_single_connection(start, end, dist) 
# - prida do nasi mapy OBOUSMERNE spojeni mezi start a end (stringy) se vzdalenosti dist
# - tzn. napr add_single_connection("A", "B", 10) prida spojeni A->B a zaroven B->A s delkou 10
# - start a end muze mit ruznou velikost pismen, ukladejte ale pro jednoduchost vse malymi pismeny
# - dist musi byt nezaporne cislo, jinak vyhodte vyjimku ValueError s vhodnym textem

# add_multiple_connections(conn)
# - prida do mapy vice spojeni najednou
# - argument je list trojic [(start1, end1, dist1), (start2, end2, dist2), ...]
# - pravidla jinak stejna jako pro add_single_connection
# nejkratsi vzdalenosti mezi start a end
#   a route jen seznam (list) uzlu od start do end (vysledek vse malymi pismeny)
# - pokud cesta neexistuje, vratte (None, [])
# - Pokud start nebo end v mape neexistuje, vyhodte vyjimku ValueError s vhodnym textem

from math import inf


# Nastaveni

# testovat i moznost, ze cesta neexistuje (neni nutne na zapocet)
# pokud si ale chcete zkusit trosku vylepsit algoritmus, tak to muzete prepnout na True
TEST_ROUTE_NOT_EXIST = False

# vypisovat vysledky hledani tras a dalsi texty (pro ladeni se to hodi)
PRINT_RESULTS = True



# zde dokoncete tridu Map, tak aby fungovala s testovacim kodem dole
# temer jiste budete potrebovat vic metod/funkci, nez ty tri ze zadani
# doplnte, jak budete potrebovat

class Map:
    def __init__(self): # TODO: vytvori prazdnou Mapu
        self.mat = []
        self.cities = []
        self.size = 0

    # TODO: sem nejake pomocne metody, atd...
    # ...
    # ...

    # TODO: Zde dokoncete metodu podle zadani
    def add_single_connection(self, start:str, end:str, dist:float):
        start_ = start.lower()
        end_ = end.lower()
        if dist < 0:
            raise ValueError('Distance cannot be negative!')
        if start_ not in self.cities:
            self.cities.append(start_)
            self.size += 1
            self.mat.append([0 for _ in range(self.size)])
            for row in range(self.size-1):
                self.mat[row].append(0)
        if end_ not in self.cities:
            self.cities.append(end_)
            self.size += 1
            self.mat.append([0 for _ in range(self.size)])
            for row in range(self.size-1):
                self.mat[row].append(0)
        self.mat[self.cities.index(start_)][self.cities.index(end_)] = dist 
        self.mat[self.cities.index(end_)][self.cities.index(start_)] = dist


    # TODO: Zde doplnte metodu dle zadani
    def add_multiple_connections(self, conn:list):
        for connection in conn:
            self.add_single_connection(connection[0], connection[1], connection[2])

    def get_current_city(self, distances: list, visited: list) -> int:     #returns index of current city
        min_distance = inf
        current_city = None     #index of city in self.cities
        for i in range(self.size):
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]
                current_city = i
        return current_city

    def djikstra(self, start: str, end: str) -> list:
        start_city = self.cities.index(start.lower())
        end_city = self.cities.index(end.lower())
        distances = [inf for _ in range(self.size)]
        predecessors = [None]*self.size
        distances[start_city] = 0      #minimal distances from city start to all other cities (indexed as in self.cities)
        visited = [False]*self.size

        for _ in range(self.size):
            current_city = self.get_current_city(distances, visited)

            if current_city is None or current_city == end_city:
                break

            visited[current_city] = True

            for v in range(self.size):
                dis = self.mat[current_city][v]        #distance from current city to v
                if dis != 0 and not visited[v] and distances[v] > distances[current_city] + dis:
                    distances[v] = distances[current_city] + dis
                    predecessors[v] = current_city

        return (distances, predecessors)

    def get_route(self, predecessors: list, start: str, end: str):
        start_ = start.lower()
        end_ = end.lower()
        route = []
        city = self.cities.index(end_)  #index of city
        while city is not None:
            route.insert(0, self.cities[city])
            city = predecessors[city]
            if city == self.cities.index(start_):
                route.insert(0, start_)
                break
        return route
            
    # TODO: Zde doplnte metodu dle zadani
    def find_route(self, start:str, end:str) -> tuple:
        if start.lower() not in self.cities or end.lower() not in self.cities:
            raise ValueError('The input contains invalid cities!')
        distances, predecessors = self.djikstra(start.lower(), end.lower())
        distance_start_to_end = distances[self.cities.index(end.lower())]
        route = self.get_route(predecessors, start, end)
        return (distance_start_to_end, route)

#############
#
# TESTOVACI KOD
#
# - Nemente testovaci kod
# - musi to projit bez problemu, pokud tridu Map implementujete spravne
#
#############

m = Map()   # Nase nova mapa

# pridavani hran do grafu po jedne (nezalezi na velikosti pismen)
# vzdy se pridaji oba smery (tam i zpet)

print("Pridani jednotlivych spojeni.")
m.add_single_connection("Praha", "Brno", 200)
m.add_single_connection("Praha", "Kolín", 60)
m.add_single_connection("Kolín", "Brno", 170)
m.add_single_connection("Kolín", "Nymburk", 30)
m.add_single_connection("Nymburk", "Mladá Boleslav", 40)

# test pridani zaporne vzdalenosti (musi vyhodit vyjimku ValueError)
try:
    m.add_single_connection("Praha", "Tokyo", -5)
except ValueError as e:
    if PRINT_RESULTS:
        print(e)

print("OK")

# pridavani vice hran. Je to seznam trojic (tuple)
print("Pridavani vice spojeni najednou.")
m.add_multiple_connections([("Praha", "Ústí nad Labem", 80),
                            ("Ústí nad Labem", "Děčín", 20),
                            ("Děčín", "Liberec", 50),
                            ("Liberec", "Mladá Boleslav", 50),
                            ("Mladá Boleslav", "Praha", 60)])

if TEST_ROUTE_NOT_EXIST:
    m.add_multiple_connections([("Jaroměř", "Turnov", 50), ("Turnov", "Trutnov", 50), ("Trutnov", "Jaroměř", 50)])

# test pridani zaporne vzdalenosti (musi vyhodit vyjimku ValueError)
try:
    m.add_multiple_connections([("Praha", "Tuklaty", 25), ("Tuklaty", "Rostoklaty", -10)])
except ValueError as e:
    if PRINT_RESULTS:
        print(e)

print("OK")

print("Testovani hledani trasy.")
try:
    x = m.find_route("Praha", "Mladá Boleslav")
    if PRINT_RESULTS:
        print(x)
    assert(x==(60, ['praha', 'mladá boleslav']))
    x = m.find_route("nymburk", "brno")
    if PRINT_RESULTS:
        print(x)
    assert(x==(200, ['nymburk', 'kolín', 'brno']))

    x = m.find_route("brno", "liberec")
    if PRINT_RESULTS:
        print(x)
    assert(x==(290, ['brno', 'kolín', 'nymburk', 'mladá boleslav', 'liberec']))

# zde by mela byt vyhozena vyjimka ValueError, protoze Oslo neni v mape
    print(m.find_route("Nymburk", "Oslo"))

except ValueError as e:
    if PRINT_RESULTS:
        print(x)

try:
    # zde by mela byt vyhozena vyjimka ValueError, protoze Tokyo neni v mape
    x = m.find_route("Tokyo", "Kozomín")

except ValueError as e:
    if PRINT_RESULTS:
        print(x)

try:
    # zde by mela byt vyhozena vyjimka ValueError, protoze Rostoklaty nejsou v mape
    x = m.find_route("Praha", "Rostoklaty")

except ValueError as e:
    if PRINT_RESULTS:
        print(e)

# testovani, zda algoritmus funguje, i kdyz cesta neexistuje
if TEST_ROUTE_NOT_EXIST:    
    x = m.find_route("Jaroměř", "Praha")
    if PRINT_RESULTS:
        print(x)
    assert(x == (None, []))
print("OK")

################
#
# Slozitejsi testovani, nutne sestavit graf
#
################

# mame k dispozici seznam linek prazskych tramvaji.
# Nejprve vlozte tyto stanice do mapy tak, ze kazde dve nasledujici tvori hranu grafu s delkou 1
# Neco jako: 
# m.add_single_connection("Sidliste Petriny", "Petriny", 1)
# m.add_single_connection("Petriny", "Vetrnik", 1)
# m.add_single_connection("Vetrnik", "Vojenska nemocnice", 1)
# atd... Je to samozrejme treba udelat pres cykly a automaticky

linky = {}
linky[1] = [
    "SÍDLIŠTĚ PETŘINY",
    "Petřiny",
    "Větrník",
    "Vojenská nemocnice",
    "Baterie",
    "Ořechovka",
    "Sibeliova",
    "Vozovna Střešovice",
    "Hradčanská",
    "Sparta",
    "Korunovační",
    "Letenské náměstí",
    "Kamenická",
    "Strossmayerovo náměstí",
    "Vltavská",
    "Pražská tržnice",
    "Tusarova",
    "Dělnická",
    "Maniny",
    "Libeňský most",
    "Palmovka",
    "Krejcárek",
    "Ohrada",
    "Vozovna Žižkov",
    "Strážní",
    "Chmelnice",
    "Kněžská luka",
    "SPOJOVACÍ"
]

linky[2] = [
    "SÍDLIŠTĚ PETŘINY",
    "Petřiny",
    "Větrník",
    "Vojenská nemocnice",
    "Baterie",
    "Ořechovka",
    "Sibeliova",
    "Vozovna Střešovice",
    "Prašný most",
    "Hradčanská",
    "Chotkovy sady",
    "Malostranská",
    "Staroměstská",
    "Karlovy lázně",
    "Národní divadlo",
    "Národní třída",
    "Novoměstská radnice",
    "Karlovo náměstí",
    "Moráň",
    "Palackého náměstí",
    "Výtoň",
    "Podolská vodárna",
    "Kublov",
    "Dvorce",
    "Přístaviště",
    "Pobřežní cesta",
    "NÁDRAŽÍ BRANÍK"
]

linky[3] = [
    "BŘEZINĚVESKÁ",
    "Kobylisy",
    "Ke Stírce",
    "Okrouhlická",
    "Vychovatelna",
    "Bulovka",
    "Vosmíkových",
    "U Kříže",
    "Stejskalova",
    "Divadlo pod Palmovkou",
    "Palmovka",
    "Invalidovna",
    "Urxova",
    "Křižíkova",
    "Karlínské náměstí",
    "Florenc",
    "Bílá labuť",
    "Masarykovo nádraží",
    "Jindřišská",
    "Václavské náměstí",
    "Vodičkova",
    "Lazarská",
    "Karlovo náměstí",
    "Moráň",
    "Palackého náměstí",
    "Výtoň",
    "Podolská vodárna",
    "Kublov",
    "Dvorce",
    "Přístaviště",
    "Pobřežní cesta",
    "NÁDRAŽÍ BRANÍK"
]

linky[4] = [
    "SÍDLIŠTĚ BARRANDOV",
    "Poliklinika Barrandov",
    "Chaplinovo náměstí",
    "K Barrandovu",
    "Geologická",
    "Hlubočepy",
    "Zlíchov",
    "Lihovar",
    "ČSAD Smíchov",
    "Smíchovské nádraží",
    "Plzeňská",
    "Na Knížecí",
    "Anděl",
    "Zborovská",
    "Palackého náměstí",
    "Karlovo náměstí",
    "I. P. Pavlova",
    "Náměstí Míru",
    "Jana Masaryka",
    "Ruská",
    "Vršovické náměstí",
    "ČECHOVO NÁMĚSTÍ"
]

linky[5] = [
    "SÍDLIŠTĚ BARRANDOV",
    "Poliklinika Barrandov",
    "Chaplinovo náměstí",
    "K Barrandovu",
    "Geologická",
    "Hlubočepy",
    "Zlíchov",
    "Lihovar",
    "ČSAD Smíchov",
    "Smíchovské nádraží",
    "Plzeňka",
    "Na Knížecí",
    "Anděl",
    "Zborovská",
    "Jiráskovo náměstí",
    "Myslíkova",
    "Lazarská",
    "Vodičkova",
    "Václavské náměstí",
    "Jindřišská",
    "Hlavní nádraží",
    "Husinecká",
    "Lipanská",
    "Olšanské náměstí",
    "Flora",
    "Olšanské hřbitovy",
    "Želivského",
    "Vinohradské hřbitovy",
    "Krematorium Strašnice",
    "Vozovna Strašnice",
    "Vinice",
    "Solidarita",
    "Zborov-Strašnické divadlo",
    "Nové Strašnice",
    "Černokostelecká",
    "Depo Hostivař",
    "Malešická továrna",
    "Na Homoli",
    "ÚSTŘEDNÍ DÍLNY DP"
]

linky[6] = [
    "PALMOVKA",
    "Libeňský most",
    "Maniny",
    "U Průhonu",
    "Dělnická",
    "Ortenovo náměstí",
    "Nádraží Holešovice",
    "Výstaviště Holešovice",
    "Veletržní palác",
    "Strossmayerovo náměstí",
    "Nábřeží Kpt. Jaroše",
    "Dlouhá třída",
    "Náměstí Republiky",
    "Masarykovo nádraží",
    "Jindřišská",
    "Václavské náměstí",
    "Vodičkova",
    "Lazarská",
    "Novoměstská radnice",
    "Karlovo náměstí",
    "Štěpánská",
    "I. P. Pavlova",
    "Bruselská",
    "Pod Karlovem",
    "Nuselské schody",
    "Otakarova",
    "Nádraží Vršovice",
    "Bohemians",
    "Koh-i-noor",
    "Slavia",
    "KUBÁNSKÉ NÁMĚSTÍ"
]

linky[7] = [
    "RADLICKÁ",
    "Škola Radlice",
    "Laurová",
    "Braunova",
    "Křížová",
    "Na Knížecí",
    "Anděl",
    "Zborovská",
    "Palackého náměstí",
    "Výtoň",
    "Albertov",
    "Ostrčilovo náměstí",
    "Svatoplukova",
    "Divadlo Na Fidlovačce",
    "Otakarova",
    "Nádraží Vršovice",
    "Bohemians",
    "Koh-i-noor",
    "Slavia",
    "Kubánské náměstí",
    "Průběžná",
    "Strašnická",
    "Nad Primaskou",
    "Vozovna Strašnice",
    "Vinice",
    "Solidarita",
    "Zborov-Strašnické divadlo",
    "Nové Strašnice",
    "ČERNOKOSTELECKÁ"
]

linky[8] = [
    "NÁDRAŽÍ PODBABA",
    "Zelená",
    "Lotyšská",
    "Vítězné náměstí",
    "Hradčanská",
    "Sparta",
    "Korunovační",
    "Letenské náměstí",
    "Kamenická",
    "Strossmayerovo náměstí",
    "Nábřeží Kpt. Jaroše",
    "Dlouhá třída",
    "Náměstí Republiky",
    "Bílá labuť",
    "Florenc",
    "Karlínské náměstí",
    "Křižíkova",
    "Urxova",
    "Invalidovna",
    "Palmovka",
    "Balabenka",
    "Ocelářská",
    "Multiaréna Praha",
    "Nádraží Libeň",
    "Podkovářská",
    "U Elektry",
    "Nademlejnská",
    "STARÝ HLOUBĚTÍN"
]

linky[9] = [
    "SÍDLIŠTĚ ŘEPY",
    "Blatiny",
    "Slánská",
    "Hlušičkova",
    "Krematorium Motol",
    "Motol",
    "Vozovna Motol",
    "Hotel Golf",
    "Poštovka",
    "Kotlářka",
    "Kavalírka",
    "Klamovka",
    "U Zvonu",
    "Bertramka",
    "Anděl",
    "Arbesovo náměstí",
    "Švandovo divadlo",
    "Újezd",
    "Národní divadlo",
    "Národní třída",
    "Lazarská",
    "Vodičkova",
    "Václavské náměstí",
    "Jindřišská",
    "Hlavní nádraží",
    "Husinecká",
    "Lipanská",
    "Olšanské náměstí",
    "Olšanská",
    "Nákladové nádraží Žižkov",
    "Biskupcova",
    "Ohrada",
    "Vozovna Žižkov",
    "Strážní",
    "Chmelnice",
    "Kněžská luka",
    "SPOJOVACÍ"
]

linky[10] = [
    "SÍDLIŠTĚ ĎÁBLICE",
    "Třebenická",
    "Štěpničná",
    "Ládví",
    "Kyselova",
    "Střelničná",
    "Kobylisy",
    "Ke Stírce",
    "Okrouhlická",
    "Vychovatelna",
    "Bulovka",
    "Vosmíkových",
    "U kříže",
    "Stejskalova",
    "Divadlo pod Palmovkou",
    "Palmovka",
    "Krejcárek",
    "Biskupcova",
    "Nákladové nádraží Žižkov",
    "Mezi Hřbitovy",
    "Želivského",
    "Olšanské hřbitovy",
    "Flora",
    "Orionka",
    "Perunova",
    "Vinohradská vodárna",
    "Šumavská",
    "Náměstí Míru",
    "I. P. Pavlova",
    "Štěpánská",
    "Karlovo náměstí",
    "Moráň",
    "Palackého náměstí",
    "Zborovská",
    "Anděl",
    "Bertramka",
    "U zvonu",
    "Klamovka",
    "Kavalírka",
    "Kotlářka",
    "Poštovka",
    "Hotel Golf",
    "Motol",
    "Vozovna Motol",
    "Krematorium Motol",
    "Hlušičkova",
    "Slánská",
    "Blatiny",
    "SÍDLIŠTĚ ŘEPY"
]


linky[11] = [
    "SPOJOVACÍ",
    "Kněžská Luka",
    "Chmelnice",
    "Strážní",
    "Vozovna Žižkov",
    "Ohrada",
    "Biskupcova",
    "Nákladové nádraží Žižkov",
    "Mezi Hřbitovy",
    "Želivského",
    "Olšanské Hřbitovy",
    "Flora",
    "Radhošťská",
    "Jiřího z Poděbrad",
    "Vinohradská tržnice",
    "Italská",
    "Muzeum",
    "I. P. Pavlova",
    "Bruselská",
    "Pod Karlovem",
    "Nuselské schody",
    "Náměstí Bratří Synků",
    "Horky",
    "Pod Jezerkou",
    "Michelská",
    "Plynárna Michle",
    "Chodovská",
    "Teplárna Michle",
    "SPOŘILOV"
]

linky[12] = [
    "SÍDLIŠTĚ BARRANDOV",
    "Poliklinika Barrandov",
    "Chaplinovo náměstí",
    "K Barrandovu",
    "Geologická",
    "Hlubočepy",
    "Zlíchov",
    "Lihovar",
    "ČSAD Smíchov",
    "Smíchovské nádraží",
    "Plzeňská",
    "Na Knížecí",
    "Anděl",
    "Arbesovo náměstí",
    "Švandovo divadlo",
    "Újezd",
    "Hellichova",
    "Malostranské náměstí",
    "Malostranská",
    "Chotkovy sady",
    "Sparta",
    "Korunovační",
    "Letenské náměstí",
    "Strossmayerovo náměstí",
    "Vltavská",
    "Pražská tržnice",
    "Tusarova",
    "Dělnická",
    "U Průhonu",
    "Ortenovo náměstí",
    "Nádraží Holešovice",
    "VÝSTAVIŠTĚ HOLEŠOVICE"
]

linky[13] = [
    "ČERNOKOSTELECKÁ",
    "Nové Strašnice",
    "Zborov-Strašnické divadlo",
    "Solidarita",
    "Vinice",
    "Vozovna Strašnice",
    "Krematorium Strašnice",
    "Vinohradské hřbitovy",
    "Želivského",
    "Olšanské hřbitovy",
    "Flora",
    "Radhošťská",
    "Jiřího z Poděbrad",
    "Vinohradská tržnice",
    "Italská",
    "Muzeum",
    "I. P. Pavlova",
    "Náměstí Míru",
    "Jana Masaryka",
    "Krymská",
    "Ruská",
    "Vršovické náměstí",
    "ČECHOVO NÁMĚSTÍ"
]

linky[14] = [
    "SPOŘILOV",
    "Teplárna Michle",
    "Chodovská",
    "Plynárna Michle",
    "Chodovská",
    "Pod Jezerkou",
    "Horky",
    "Náměstí Bratří Synků",
    "Divadlo Na Fidlovačce",
    "Svatoplukova",
    "Ostrčilovo náměstí",
    "Albertov",
    "Botanická zahrada",
    "Moráň",
    "Karlovo náměstí",
    "Novoměstská radnice",
    "Lazarská",
    "Vodičkova",
    "Václavské náměstí",
    "Jindřišská",
    "Masarykovo nádraží",
    "Bílá labuť",
    "Těšnov",
    "Vltavská",
    "Pražská tržnice",
    "Tusarova",
    "Dělnická",
    "Maniny",
    "Libeňský most",
    "Palmovka",
    "Balabenka",
    "Divadlo Gong",
    "Poliklinika Vysočany",
    "NÁDRAŽÍ VYSOČANY",
    "VYSOČANSKÁ"
]

linky[15] = [
    "KOTLÁŘKA",
    "Kavalírka",
    "Klamovka",
    "U Zvonu",
    "Bertramka",
    "Anděl",
    "Arbesovo náměstí",
    "Švandovo divadlo",
    "Újezd",
    "Hellichova",
    "Malostranské náměstí",
    "Malostranská",
    "Čechův most",
    "Dlouhá třída",
    "Náměstí Republiky",
    "Masarykovo nádraží",
    "Hlavní nádraží",
    "Husinecká",
    "Lipanská",
    "Olšanské náměstí",
    "Flora",
    "OLŠANSKÉ HŘBITOVY"
]

linky[16] = [
    "SÍDLIŠTĚ ŘEPY",
    "Blatiny",
    "Slánská",
    "Hlušičkova",
    "Krematorium Motol",
    "Motol",
    "Vozovna Motol",
    "Hotel Golf",
    "Poštovka",
    "KOTLÁŘKA",
    "Kavalírka",
    "Klamovka",
    "U Zvonu",
    "Bertramka",
    "Anděl",
    "Zborovská",
    "Palackého náměstí",
    "Moráň",
    "Karlovo náměstí",
    "Štěpánská",
    "I. P. Pavlova",
    "Náměstí Míru",
    "Šumavská",
    "Vinohradská vodárna",
    "Perunova",
    "Orionka",
    "Flora",
    "Olšanské hřbitovy",
    "Želivského",
    "Mezi Hřbitovy",
    "Nákladové nádraží Žižkov",
    "Biskupcova",
    "Krejcárek",
    "Palmovka",
    "Balabenka",
    "Divadlo Gong",
    "Poliklinika Vysočany",
    "Nádraží Vysočany",
    "Špitálská",
    "Poštovská",
    "Kolbenova",
    "Nový Hloubětín",
    "Vozovna Hloubětín",
    "Starý Hloubětín",
    "Kbelská",
    "Hloubětín",
    "Sídliště Hloubětín",
    "LEHOVEC"
]

linky[17] = [
    "VOZOVNA KOBYLISY",
    "Vozovna Kobylisy",
    "Líbeznická",
    "Březiněveská",
    "Kobylisy",
    "Ke Stírce",
    "Hercovka",
    "Nad Trojou",
    "Trojská",
    "Nádraží Holešovice",
    "VÝSTAVIŠTĚ HOLEŠOVICE",
    "Veletržní palác",
    "Strossmayerovo náměstí",
    "Nábřeží Kpt. Jaroše",
    "Čechův most",
    "Právnická fakulta",
    "Staroměstská",
    "Karlovy lázně",
    "Národní divadlo",
    "Jiráskovo náměstí",
    "Palackého náměstí",
    "Výtoň",
    "Podolská vodárna",
    "Kublov",
    "Dvorce",
    "Přístaviště",
    "Pobřežní cesta",
    "Nádraží Braník",
    "Černý kůň",
    "Belárie",
    "Modřanská škola",
    "Nádraží Modřany",
    "Čechova čtvrť",
    "Poliklinika Modřany",
    "U Libušského potoka",
    "Modřanská rokle",
    "Sídliště Modřany",
    "LEVSKÉHO"
]

linky[18] = [
    "NÁDRAŽÍ PODBABA",
    "Zelená",
    "Lotyšská",
    "Vítězné náměstí",
    "Hradčanská",
    "Chotkovy sady",
    "Malostranská",
    "Staroměstská",
    "Karlovy lázně",
    "Národní divadlo",
    "Národní třída",
    "Karlovo náměstí",
    "Moráň",
    "Botanická zahrada",
    "Albertov",
    "Ostrčilovo náměstí",
    "Svatoplukova",
    "Divadlo Na Fidlovačce",
    "Náměstí Bratří Synků",
    "Nuselská radnice",
    "Palouček",
    "Pražského povstání",
    "Na Veselí",
    "VOZOVNA PANKRÁC"
]

linky[19] = [
    "Radošovická",
    "Nádraží Strašnice",
    "Na Hroudě",
    "Strašnická",
    "Nad Primaskou",
    "Vozovna Strašnice",
    "Krematorium Strašnice",
    "Vinohradské hřbitovy",
    "Želivského",
    "Mezi Hřbitovy",
    "Nákladové nádraží Žižkov",
    "Biskupcova",
    "Krejcárek",
    "Palmovka",
    "Balabenka",
    "Divadlo Gong",
    "Poliklinika Vysočany",
    "Nádraží Vysočany",
    "Špitálská",
    "Poštovská",
    "Kolbenova",
    "Nový Hloubětín",
    "Vozovna Hloubětín",
    "Starý Hloubětín",
    "Kbelská",
    "Hloubětín",
    "Sídliště Hloubětín",
    "Lehovec"
]

linky[20] = [
    "DIVOKÁ ŠÁRKA",
    "Vozovna Vokovice",
    "Nad Džbánem",
    "Nádraží Veleslavín",
    "Červený Vrch",
    "Sídliště Červený Vrch",
    "Bořislavka",
    "Na Pískách",
    "Hadovka",
    "Thákurova",
    "Dejvická",
    "Vítězné náměstí",
    "Hradčanská",
    "Chotkovy sady",
    "Malostranská",
    "Malostranské náměstí",
    "Hellichova",
    "Újezd",
    "Švandovo divadlo",
    "Arbesovo náměstí",
    "Anděl",
    "Na Knížecí",
    "Plzeňka",
    "Smíchovské nádraží",
    "ČSAD Smíchov",
    "Lihovar",
    "Zlíchov",
    "Hlubočepy",
    "Geologická",
    "K Barrandovu",
    "Chaplinovo náměstí",
    "Poliklinika Barrandov",
    "SÍDLIŠTĚ BARRANDOV"
]


linky[21] = [
    "RADLICKÁ",
    "Škola Radlice",
    "Laurová",
    "Braunova",
    "Křížová",
    "Na Knížecí",
    "Anděl",
    "Zborovská",
    "Palackého náměstí",
    "Výtoň",
    "Podolská vodárna",
    "Kublov",
    "Dvorce",
    "Přístaviště",
    "Pobřežní cesta",
    "Nádraží Braník",
    "Černý kůň",
    "Belárie",
    "Modřanská škola",
    "Nádraží Modřany",
    "Čechova čtvrť",
    "Poliklinika Modřany",
    "U Libušského potoka",
    "Modřanská rokle",
    "SÍDLILŠTĚ MODŘANY",
    "LEVSKÉHO"
]

linky[22] = [
    "BÍLÁ HORA",
    "Malý Břevnov",
    "Obora Hvězda",
    "VYPICH",
    "Říčanova",
    "Břevnovský klášter",
    "U Kaštanu",
    "Drinopol",
    "Marjánka",
    "Malovanka",
    "Pohořelec",
    "Brusnice",
    "Pražský hrad",
    "Královský letohrádek",
    "Malostranská",
    "Malostranské náměstí",
    "Hellichova",
    "Újezd",
    "Národní divadlo",
    "Národní třída",
    "Novoměstská radnice",
    "Karlovo náměstí",
    "Štěpánská",
    "I. P. Pavlova",
    "Náměstí Míru",
    "Jana Masaryka",
    "Krymská",
    "Ruská",
    "Vršovické náměstí",
    "Čechovo náměstí",
    "Koh-i-noor",
    "Slavia",
    "Kubánské náměstí",
    "Průběžná",
    "Na Hroudě",
    "NÁDRAŽÍ STRAŠNICE",
    "RADOŠOVICKÁ",
    "Dubečská",
    "Na Padesátém",
    "Zahradní Město",
    "Sídliště Zahradní Město",
    "Obchodní centrum Hostivař",
    "Na Groši",
    "Hostivařská",
    "NÁDRAŽÍ HOSTIVAŘ"
]

linky[23] = [
    "Královka",
    "Malovanka",
    "Hládkov",
    "Brusnice",
    "Pražský hrad",
    "Královský letohrádek",
    "Malostranská",
    "Malostranské náměstí",
    "Hellichova",
    "Újezd",
    "Národní divadlo",
    "Národní třída",
    "Karlovo náměstí",
    "Štěpánská",
    "I. P. Pavlova",
    "Bruselská",
    "Zvonařka"
]

linky[24] = [
    "KUBÁNSKÉ NÁMĚSTÍ",
    "Slavia",
    "Koh-i-noor",
    "Bohemians",
    "Nádraží Vršovice",
    "Otakarova",
    "Divadlo Na Fidlovačce",
    "Svatoplukova",
    "Ostrčilovo náměstí",
    "Albertov",
    "Botanická zahrada",
    "Moráň",
    "Karlovo náměstí",
    "Novoměstská radnice",
    "Lazarská",
    "Vodičkova",
    "Václavské náměstí",
    "Jindřišská",
    "Masarykovo nádraží",
    "Bílá labuť",
    "Florenc",
    "Karlínské náměstí",
    "Křižíkova",
    "Urxova",
    "Invalidovna",
    "Palmovka",
    "Divadlo pod Palmovkou",
    "Stejskalova",
    "U Kříže",
    "Vosmíkových",
    "Bulovka",
    "Vychovatelna",
    "Okrouhlická",
    "Ke Stírce",
    "KOBYLISY",
    "BŘEZINĚVESKÁ"
]

linky[25] = [
    "BÍLÁ HORA",
    "Malý Břevnov",
    "Obora Hvězda",
    "Vypich",
    "Říčanova",
    "Břevnovský klášter",
    "U Kaštanu",
    "Drinopol",
    "Marjánka",
    "Malovanka",
    "Hládkov",
    "Vozovna Střešovice",
    "Hradčanská",
    "Sparta",
    "Korunovační",
    "Letenské náměstí",
    "Kamenická",
    "Strossmayerovo náměstí",
    "Vltavská",
    "Pražská tržnice",
    "Tusarova",
    "Dělnická",
    "Maniny",
    "Libeňský most",
    "Palmovka",
    "Balabenka",
    "Ocelářská",
    "Multiaréna Praha",
    "Nádraží Libeň",
    "Kabešova",
    "Podkovářská",
    "U Elektry",
    "Nademlejnská",
    "Kbelská",
    "Hloubětín",
    "Sídliště Hloubětín",
    "LEHOVEC"
]

linky[26] = [
    "DIVOKÁ ŠÁRKA",
    "Vozovna Vokovice",
    "Nad Džbánem",
    "Nádraží Veleslavín",
    "Červený Vrch",
    "Sídliště Červený Vrch",
    "Bořislavka",
    "Na Pískách",
    "Hadovka",
    "Thákurova",
    "Dejvická",
    "Vítězné náměstí",
    "Hradčanská",
    "Sparta",
    "Korunovační",
    "Letenské náměstí",
    "Kamenická",
    "Strossmayerovo náměstí",
    "Nábřeží Kpt. Jaroše",
    "Dlouhá třída",
    "Náměstí Republiky",
    "Masarykovo nádraží",
    "Hlavní nádraží",
    "Husinecká",
    "Lipanská",
    "Olšanské náměstí",
    "Olšanská",
    "Nákladové nádraží Žižkov",
    "Mezi Hřbitovy",
    "Želivského",
    "Vinohradské hřbitovy",
    "Krematorium Strašnice",
    "Vozovna Strašnice",
    "Nad Primaskou",
    "Strašnická",
    "Na Hroudě",
    "Nádraží Strašnice",
    "Radošovická",
    "Dubečská",
    "Na Padesátém",
    "Zahradní Město",
    "Sídliště Zahradní Město",
    "Obchodní centrum Hostivař",
    "Na Groši",
    "Hostivařská",
    "NÁDRAŽÍ HOSTIVAŘ"
]

# Vytvorime novou mapu s nazvem tram
tram = Map()

# Zde pridat nejakym zpusobem trasy linek do nasi Mapy tram
# TODO: pridat data ze slovniku linky do tram
for key in linky.keys():
    linka = linky[key]
    for index in range(0, len(linka)-1):
        tram.add_single_connection(linka[index], linka[index+1], 1)
        
# Testovani tramvajovych dat, odsud zase nemenit!!

# testovani existujicich tras
print("Testovani tramvajovych spojeni.")
x = tram.find_route("Palouček", "I. P. Pavlova")
if PRINT_RESULTS:
    print(x)
assert(x == (6, ['palouček', 'nuselská radnice', 'náměstí bratří synků', 'nuselské schody', 'pod karlovem', 'bruselská', 'i. p. pavlova']))

x = tram.find_route("Moráň", "Divoká Šárka")
if PRINT_RESULTS:
    print(x)
assert(x == (20, ['moráň', 'karlovo náměstí', 'národní třída', 'národní divadlo', 'karlovy lázně', 'staroměstská', 'malostranská', 'chotkovy sady', 'hradčanská', 'vítězné náměstí', 'dejvická', 'thákurova', 'hadovka', 'na pískách', 'bořislavka', 'sídliště červený vrch', 'červený vrch', 'nádraží veleslavín', 'nad džbánem', 'vozovna vokovice', 'divoká šárka']))

x = tram.find_route("Dejvická", "Dělnická")
if PRINT_RESULTS:
    print(x)
assert(x == (10, ['dejvická', 'vítězné náměstí', 'hradčanská', 'sparta', 'korunovační', 'letenské náměstí', 'strossmayerovo náměstí', 'vltavská', 'pražská tržnice', 'tusarova', 'dělnická']))

x = tram.find_route("Masarykovo Nádraží", "Orionka")
if PRINT_RESULTS:
    print(x)
assert(x == (6, ['masarykovo nádraží', 'hlavní nádraží', 'husinecká', 'lipanská', 'olšanské náměstí', 'flora', 'orionka']))

x = tram.find_route("Sídliště Petřiny", "Nádraží Hostivař")
if PRINT_RESULTS:
    print(x)
assert(x == (36, ['sídliště petřiny', 'petřiny', 'větrník', 'vojenská nemocnice', 'baterie', 'ořechovka', 'sibeliova', 'vozovna střešovice', 'hradčanská', 'chotkovy sady', 'malostranská', 'staroměstská', 'karlovy lázně', 'národní divadlo', 'národní třída', 'karlovo náměstí', 'i. p. pavlova', 'náměstí míru', 'jana masaryka', 'ruská', 'vršovické náměstí', 'čechovo náměstí', 'koh-i-noor', 'slavia', 'kubánské náměstí', 'průběžná', 'na hroudě', 'nádraží strašnice', 'radošovická', 'dubečská', 'na padesátém', 'zahradní město', 'sídliště zahradní město', 'obchodní centrum hostivař', 'na groši', 'hostivařská', 'nádraží hostivař']))

# Test neexistujici stanice
try:
    tram.find_route("Moráň", "Shibuya")
except ValueError as e:
    if PRINT_RESULTS:
        print(x)
print("OK")
print("Vse hotovo, skocte si pro zapocet.")

