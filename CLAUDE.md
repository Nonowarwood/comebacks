# CLAUDE.md — Comeback Tracker

Contexte pour reprendre le travail exactement où on en est. Répondre en **français**.

## Le projet

Tracker de comebacks kpop par Nonowarwood (fan de TXT/Yeonjun, fait des edits vidéo).
- Local : `~/Desktop/dev/comebacks` · Repo : `Nonowarwood/comebacks` · En ligne : https://nonowarwood.github.io/comebacks/
- Site statique vanilla (une seule page `index.html`, CSS+JS inline), déployé par GitHub Pages à chaque push sur `main`.
- Projet frère : la vitrine `~/Desktop/dev/vitrine` (repo `nonowarwood.github.io`) — même DA.

## Direction artistique (à respecter absolument)

Esthétique « fiche technique d'album imprimée » inspirée du packaging YEONJUN « NO LABELS »
(voir `~/Desktop/dev/vitrine/inspi/`) :
- Couleurs (variables CSS dans `:root`) : papier `#f1eee6`, papier-2 `#eae6db`, navy `#1e2a4a`, rouge brique `#8b2318`.
- Thème sombre « Encre » via `[data-theme="ink"]` : fond `#0e1528`, texte crème, rouge `#d8503e`. **Tout passe par les variables**, ne jamais coder une couleur en dur.
- Typos : Archivo (900 pour les titres, capitales, letter-spacing négatif) + Archivo Narrow (labels, letter-spacing large).
- Motifs print : grain papier SVG, filets fins `--line`, tampons rouges penchés (`.stamp`), filigranes outline (`.wm`), repères de calage (`.reg`), code-barres, sections « PART XX », rubalise marquee fixée en bas.
- Animations « grand jeu » : intro tampon (1× par session, sessionStorage `cbt-intro`), reveals au scroll (`.rv` + IntersectionObserver), pochette 3D dans les fiches, chiffres du compte à rebours qui claquent. Toujours respecter `prefers-reduced-motion`.

## Architecture

- `index.html` — toute l'app. Gros blocs JS : dico `I18N` (fr/en/ko/ja), helpers dates civiles
  (`civil()` via `Intl.formatToParts` dans le fuseau choisi), `loadData()` (fetch `comebacks.json`
  + merge `MANUAL_COMEBACKS`), rendus (`renderHero/List/Calendar/DayPanel/Settings/Marquee`),
  `openSheet()` (fiche produit), `downloadICS()`.
- `comebacks.json` — données. Généré par `scripts/update_data.py` (scrape kpopofficial.com :
  page `/kpop-comebacks/`, blocs `<li class="gspbgrid_item ... type-album">`, puis chaque fiche
  album pour artiste exact, heure, tracklist, réseaux). Garde J-14 → futur.
- `.github/workflows/update.yml` — relance le scraper **toutes les 6 h** et commit si changement.
- `data.js` — maintenu à la main : `ARTIST_CATS` (catégories `gg`/`bg`/`solo`/`mixte` pour les
  filtres, clé = nom en minuscules sans parenthèses) et `MANUAL_COMEBACKS` (TBA/rumeurs/oublis).

## Réglages utilisateur

localStorage `cbt-settings` `{lang, tz, theme}` + query params `?lang=ko&tz=kst&theme=ink`
(pratique pour tester et partager). Langues fr/en/ko/ja · fuseaux `fr`(Europe/Paris)/`kst`/`jst`
· thèmes `paper`/`ink`. Deep link `#fN` ouvre la fiche produit de l'entrée N (ordre trié par date).

## Commandes

```bash
python3 -m http.server 8656          # test local (lancer DEPUIS ~/Desktop/dev/comebacks !)
python3 scripts/update_data.py       # régénérer comebacks.json à la main (~1 min)
# capture d'écran :
"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" --headless --disable-gpu \
  --window-size=1600,2000 --hide-scrollbars --virtual-time-budget=12000 \
  --screenshot=/tmp/x.png "http://localhost:8656/"
```

## Pièges connus

- **Le bot de l'Action commit toutes les 6 h** → toujours `git pull --rebase origin main` avant
  de push. Conflit sur `comebacks.json` : prendre n'importe quelle version (régénéré sous 6 h).
- La date d'une fiche album ne sert qu'à préciser l'**heure** du jour donné par la grille, jamais
  à changer le jour (sinon les sorties multiples d'un même artiste héritent d'une mauvaise date).
- Brave headless : viewport min ~500px (une capture 390px semble déborder à tort) ; l'attribut
  `hidden` est écrasé par un `display:flex` d'auteur → prévoir `.x[hidden]{display:none}`.
- KST = JST = UTC+9 : mêmes heures, seul le label change (choix assumé).
- Le shell Claude Code réinitialise le cwd entre commandes → chemins absolus ou `cd &&`.
- Vignettes : `onerror` inline ne doit contenir que des quotes simples (pas de HTML imbriqué
  avec guillemets doubles).

## Fait (au 19/07/2026)

Scraper + Action 6 h · page plein écran · calendrier interactif (clic jour → sorties) · fiches
produit (pochette seule, tracklist avec title track en rouge, réseaux, .ics unitaire) · filtres
gg/bg/solo/mixte · i18n 4 langues · 3 fuseaux · 2 thèmes · intro tampon · héros monumental avec
compte à rebours segmenté · reveals scroll · pochette 3D · code-barres/repères/filigranes.

## Roadmap validée par Noah (« ajoute tout »)

- [x] **Mes artistes (favoris)** — étoile sur chaque ligne + dans la fiche ; clé = artiste
  normalisé (minuscules, sans `(JP)` etc.) ; localStorage `cbt-favs` (array) ; chip de filtre
  « ★ » ajouté aux filtres → `visible()` filtre dessus, le héros suit automatiquement.
- [x] **Calendrier abonnable** — `update_data.py` génère aussi `comebacks.ics` (un VEVENT par
  sortie, UID stable `artiste+date`, durée 1 h) ; bouton « S'abonner » (webcal://…/comebacks.ics)
  dans le footer/réglages, traduit dans les 4 langues.
- [x] **PWA + favicon + OG** — `icon.svg` (tampon « CT » rouge sur papier), `manifest.json`,
  `sw.js` minimal (network-first, fallback cache), meta OG + twitter card avec une image
  `og.png` (capture 1200×630 du site, thème papier).
- [x] **Teaser / MV** — vérifier si les fiches album kpopofficial contiennent des embeds YouTube
  (`youtube.com/embed/…`) ; si oui les scraper (`e.mv`) et bouton « ▶ MV » dans la fiche.
- [x] **Carte de partage** — bouton dans la fiche : canvas 1080×1350 dans la DA (papier, navy,
  tampon D-x, nom artiste, titre, date, code-barres, URL) → téléchargement PNG. Attendre
  `document.fonts.ready` avant de dessiner.
- [x] **Perf vignettes** — les thumbs 46px chargent des images 800px+ ; utiliser la variante
  WordPress `-150x150` (insérer avant l'extension), avec repli sur l'originale via `onerror`
  (flag data-* pour éviter les boucles).

Après chaque étape : tester en local (captures), puis commit + `git pull --rebase` + push.
