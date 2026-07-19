# Comeback Tracker

Le planning des prochains comebacks kpop, avec comptes à rebours en direct.
En ligne : https://nonowarwood.github.io/comebacks/

## Ajouter / modifier un comeback

Tout se passe dans [data.js](data.js) — une ligne par comeback :

```js
{ artist: "Stray Kids", title: "THIS & THAT", type: "Mini album", date: "2026-08-07T13:00:00+09:00" },
```

- `date` : format `AAAA-MM-JJTHH:MM:00+09:00` (le `+09:00` = heure coréenne/japonaise)
- titre pas encore annoncé → `title: null`
- date pas encore annoncée → pas de `date`, mettre `tba: "Août 2026"`

Le tri par date, les badges D-day, le prochain comeback en vedette et le passage
en « Out now » des sorties passées sont automatiques.
