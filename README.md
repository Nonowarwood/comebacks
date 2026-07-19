# Comeback Tracker

Le planning des prochains comebacks kpop — plein écran, calendrier interactif,
fiches produit (pochette, tracklist, photos), filtres et export agenda.
En ligne : https://nonowarwood.github.io/comebacks/

## Comment ça marche

- [scripts/update_data.py](scripts/update_data.py) scrape kpopofficial.com
  et régénère [comebacks.json](comebacks.json) : dates, heures KST, pochettes,
  tracklists, photos, réseaux officiels.
- La GitHub Action [update.yml](.github/workflows/update.yml) le lance
  **toutes les 6 h** et commit s'il y a du nouveau → le site se met à jour tout seul.
- La page recharge `comebacks.json` toutes les 30 min et au retour sur l'onglet.
- [data.js](data.js) garde ce qui se gère à la main :
  - `ARTIST_CATS` : catégorie des artistes pour les filtres (`gg`, `bg`, `solo`, `mixte`) ;
  - `MANUAL_COMEBACKS` : sorties à ajouter soi-même (TBA, rumeurs, oublis du scraper).

## Fonctionnalités

- **D-day en direct** : compte à rebours seconde par seconde sur le prochain comeback.
- **Calendrier interactif** : clique un jour → les sorties du jour ; ‹ › pour changer de mois.
- **Fiche produit** : clique une sortie → pochette, tracklist (title track en rouge),
  photos concept, réseaux officiels, bouton « + Mon agenda (.ics) ».
- **Filtres** : Tout / Girl groups / Boy groups / Solistes / Mixte.
- **Deep link** : `#f12` ouvre directement la fiche n°12.
- Heures converties automatiquement en heure française.

## Lancer en local

```bash
python3 -m http.server 8000   # puis http://localhost:8000
python3 scripts/update_data.py   # pour rafraîchir les données à la main
```
