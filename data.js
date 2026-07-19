/*
  COMEBACK TRACKER — réglages manuels
  Les sorties viennent de comebacks.json, régénéré automatiquement
  toutes les 6 h par la GitHub Action (scripts/update_data.py).

  Ici, deux choses à maintenir à la main :

  1. ARTIST_CATS — catégorie des artistes pour les filtres.
     "gg" = girl group · "bg" = boy group · "solo" · "mixte"
     Un artiste absent de la liste apparaît seulement dans "Tout".

  2. MANUAL_COMEBACKS — sorties à ajouter à la main (rumeurs, TBA,
     oublis du scraper). Même format que comebacks.json :
     { artist, title, type, date: "AAAA-MM-JJTHH:MM:00+09:00" }
     ou sans date avec tba: "Août 2026".
*/

const ARTIST_CATS = {
  "yeonjun": "solo",
  "u-know": "solo",
  "sunmi": "solo",
  "picheolin": "solo",
  "huta": "solo",
  "hyolyn": "solo",
  "wonho": "solo",
  "young k": "solo",
  "tiffany young": "solo",
  "aespa": "gg",
  "artms": "gg",
  "illit": "gg",
  "fromis_9": "gg",
  "wooah": "gg",
  "young posse": "gg",
  "bbgirls": "gg",
  "unis": "gg",
  "red velvet": "gg",
  "kiss of life": "gg",
  "hearts2hearts": "gg",
  "izna": "gg",
  "kiiikiii": "gg",
  "nct wish": "bg",
  "nct 127": "bg",
  "wayv": "bg",
  "super junior-83z": "bg",
  "8turn": "bg",
  "lun8": "bg",
  "nouera": "bg",
  "pow": "bg",
  "the wind": "bg",
  "ateez": "bg",
  "p1harmony": "bg",
  "tws": "bg",
  "stray kids": "bg",
  "tomorrow x together": "bg",
  "txt": "bg",
  "zerobaseone": "bg",
  "enhypen": "bg",
  "&team": "bg",
  "kard": "mixte",
};

const MANUAL_COMEBACKS = [
  { artist: "KiiiKiii", title: null, type: "Comeback", tba: "Mi-août 2026" },
];
