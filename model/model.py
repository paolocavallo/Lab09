import copy

import self

from database.regione_DAO import RegioneDAO
from database.tour_DAO import TourDAO
from database.attrazione_DAO import AttrazioneDAO

class Model:
    def __init__(self):
        self.tour_map = {} # Mappa ID tour -> oggetti Tour
        self.attrazioni_map = {} # Mappa ID attrazione -> oggetti Attrazione

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0

        # TODO: Aggiungere eventuali altri attributi
        self._relazioni = {}

        # Caricamento
        self.load_tour()
        self.load_attrazioni()
        self.load_relazioni()

    @staticmethod
    def load_regioni():
        """ Restituisce tutte le regioni disponibili """
        return RegioneDAO.get_regioni()

    def load_tour(self):
        """ Carica tutti i tour in un dizionario [id, Tour]"""
        self.tour_map = TourDAO.get_tour()

    def load_attrazioni(self):
        """ Carica tutte le attrazioni in un dizionario [id, Attrazione]"""
        self.attrazioni_map = AttrazioneDAO.get_attrazioni()

    def load_relazioni(self):
        """
            Interroga il database per ottenere tutte le relazioni fra tour e attrazioni e salvarle nelle strutture dati
            Collega tour <-> attrazioni.
            --> Ogni Tour ha un set di Attrazione.
            --> Ogni Attrazione ha un set di Tour.
        """

        # TODO
        t = TourDAO
        lista = t.get_tour_attrazioni()
        for dizionario in lista:
            id_tour = dizionario['id_tour']
            id_attrazione = dizionario['id_attrazione']
            self.attrazioni_map[id_attrazione].tour.add(id_tour)
            self.tour_map[id_tour].attrazioni.add(id_attrazione)






    def genera_pacchetto(self, id_regione: str, max_giorni: int = None, max_budget: float = None):
        """
        Calcola il pacchetto turistico ottimale per una regione rispettando i vincoli di durata, budget e attrazioni uniche.
        :param id_regione: id della regione
        :param max_giorni: numero massimo di giorni (può essere None --> nessun limite)
        :param max_budget: costo massimo del pacchetto (può essere None --> nessun limite)

        :return: self._pacchetto_ottimo (una lista di oggetti Tour)
        :return: self._costo (il costo del pacchetto)
        :return: self._valore_ottimo (il valore culturale del pacchetto)
        """
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1

        # TODO

        lista_tour = []
        for tour in self.tour_map.values():
            if tour.id_regione == id_regione:
                lista_tour.append(tour)






        self._ricorsione(0, [], 0, 0, 0,
                         set(), lista_tour, max_giorni, max_budget)


        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, start_index: int, pacchetto_parziale: list, durata_corrente: int,
                    costo_corrente: float, valore_corrente: int, attrazioni_usate: set,
                    lista_tour: list, max_giorni: int = None, max_budget: float = None):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""

        # TODO: è possibile cambiare i parametri formali della funzione se ritenuto opportuno

        if start_index >= len(lista_tour):
            return

        if self._valore_ottimo == -1 or valore_corrente > self._valore_ottimo:
            self._valore_ottimo = valore_corrente
            self._costo = costo_corrente
            self._pacchetto_ottimo = copy.deepcopy(pacchetto_parziale)

        for i in range(start_index, len(lista_tour)):
            tour = lista_tour[i]
            valore_culturale_tour = 0
            for id_attrazione in tour.attrazioni:

                oggetto_attrazione = self.attrazioni_map.get(id_attrazione)

                if oggetto_attrazione:
                    valore_culturale_tour += oggetto_attrazione.valore_culturale
            costo_corrente += tour.costo
            durata_corrente += tour.durata_giorni
            if (max_giorni is None or durata_corrente <= max_giorni) and (max_budget is None or costo_corrente <= max_budget):
                pacchetto_parziale.append(tour)
                valore_corrente += valore_culturale_tour

                self._ricorsione(i+1, pacchetto_parziale, durata_corrente, costo_corrente,
                         valore_corrente, attrazioni_usate, lista_tour, max_giorni, max_budget)
                pacchetto_parziale.pop()
