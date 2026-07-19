/*
  COMEBACK TRACKER — données
  Pour ajouter un comeback : une ligne { artist, title, type, date }.
  - date : "AAAA-MM-JJTHH:MM:00+09:00" (+09:00 = heure coréenne/japonaise)
  - titre pas encore annoncé : title: null
  - date pas encore annoncée : pas de date, mettre tba: "Août 2026"
  Le tri, les D-day et l'archivage des sorties passées sont automatiques.
*/
const COMEBACKS = [
  { artist: "U-KNOW (TVXQ)", title: "Time's Tickin'", type: "Single", date: "2026-07-20T18:00:00+09:00" },
  { artist: "WONHO", title: "CORE", type: "EP", date: "2026-07-21T18:00:00+09:00" },
  { artist: "8TURN", title: "8.X", type: "Single album", date: "2026-07-21T18:00:00+09:00" },
  { artist: "fromis_9", title: "Glow ME", type: "2e album", date: "2026-07-21T18:00:00+09:00" },
  { artist: "Picheolin (DINO)", title: "미쳐 미쳐", type: "Pré-release", date: "2026-07-22T18:00:00+09:00" },
  { artist: "LUN8", title: "Off the Grid", type: "4e mini album", date: "2026-07-22T18:00:00+09:00" },
  { artist: "HYOLYN", title: "OriginaLyn", type: "4e mini album", date: "2026-07-22T18:00:00+09:00" },
  { artist: "ARTMS", title: null, type: "Pré-release", date: "2026-07-24T13:00:00+09:00" },
  { artist: "aespa (JP)", title: "KISS N TELL", type: "1er mini album JP", date: "2026-07-24T00:00:00+09:00" },
  { artist: "ILLIT (JP)", title: "I Got Your Back", type: "2e single JP", date: "2026-07-26T00:00:00+09:00" },
  { artist: "Young K (DAY6)", title: "YOUNGEST", type: "2e album", date: "2026-07-27T18:00:00+09:00" },
  { artist: "NouerA", title: ".exe", type: "4e mini album", date: "2026-07-27T18:00:00+09:00" },
  { artist: "POW", title: "FLAVOR", type: "Single album", date: "2026-07-28T18:00:00+09:00" },
  { artist: "KARD", title: "Where To Now? (Part.2) : NOWHERE", type: "1er album", date: "2026-07-28T18:00:00+09:00" },
  { artist: "THE WIND", title: "Second Wind : S# 00", type: "4e mini album", date: "2026-07-29T18:00:00+09:00" },
  { artist: "ATEEZ (JP)", title: null, type: "5e single JP", date: "2026-07-29T00:00:00+09:00" },
  { artist: "P1Harmony (JP)", title: "UNIQUE Japan Edition", type: "Mini album JP", date: "2026-07-29T00:00:00+09:00" },
  { artist: "UNIS (JP)", title: null, type: "1er mini album JP", date: "2026-07-31T00:00:00+09:00" },
  { artist: "EMOTI:M", title: "CONNECT", type: "1er single album", date: "2026-07-31T18:00:00+09:00" },
  { artist: "Red Velvet", title: "Velvet Summer", type: "Mini album d'été", date: "2026-08-03T18:00:00+09:00" },
  { artist: "Picheolin (DINO)", title: "吉BOARD", type: "1er mini album", date: "2026-08-03T18:00:00+09:00" },
  { artist: "TWS (JP)", title: "SODA SODA", type: "2e single JP", date: "2026-08-04T00:00:00+09:00" },
  { artist: "AEN", title: "A NEW ERA OF NOW", type: "1er EP", date: "2026-08-05T18:00:00+09:00" },
  { artist: "Stray Kids", title: "THIS & THAT", type: "Mini album", date: "2026-08-07T13:00:00+09:00" },
  { artist: "ARTMS", title: "Hyper-Ego", type: "2e mini album", date: "2026-08-07T13:00:00+09:00" },
  { artist: "Hearts2Hearts (JP)", title: "ICONIC HEART", type: "1er single JP", date: "2026-08-12T00:00:00+09:00" },
  { artist: "TXT (JP)", title: "Setsuna Hanabi", type: "5e single JP", date: "2026-08-17T00:00:00+09:00" },
  { artist: "ZEROBASEONE (JP)", title: "回帰LOVE", type: "2e EP JP", date: "2026-08-19T00:00:00+09:00" },
  { artist: "Tiffany Young", title: "Edge of Calm", type: "1er album", date: "2026-08-20T18:00:00+09:00" },
  { artist: "ENHYPEN", title: "THE SIN : BLISS", type: "8e mini album", date: "2026-08-21T13:00:00+09:00" },
  { artist: "NCT 127", title: null, type: "7e album", date: "2026-08-24T18:00:00+09:00" },
  { artist: "izna (JP)", title: "HANDLE WITH CARE", type: "1er mini album JP", date: "2026-09-02T00:00:00+09:00" },
  { artist: "&TEAM", title: "Mark on Me", type: "2e mini album", date: "2026-09-08T18:00:00+09:00" },
  { artist: "KISS OF LIFE", title: null, type: "Comeback", tba: "Août 2026" },
  { artist: "KiiiKiii", title: null, type: "Comeback", tba: "Mi-août 2026" },
];
