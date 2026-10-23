# Ghid utilizare GitHub
## Ce sunt Git si GitHub?
- **Git** – sistem de control al versiunilor, utilizat pentru urmarirea modificarilor dintr-un proiect.
- **GitHub** – platforma online pentru stocarea si colaborarea la proiecte Git.

## Obiective
- Invatarea si utilizarea sistemului de versionare Git.
- Familiarizarea cu platforma GitHub si gestionarea repository-urilor.
- Exersarea comenzilor Git pentru salvarea si actualizarea modificarilor.

## Instalare pentru Windows
Descarca Git de pe [git-scm.com](https://git-scm.com/install/).

Verifica instalarea:
```bash
git --version
```

## Instalare pentru macOS
Instaleaza [homebrew](https://brew.sh) si apoi rulează comanda în terminal:
```bash
brew install git
```

### Comenzile de baza

| Comandă | Utilizare |
|---|---|
| `git init` | Inițializează un repository |
| `git clone URL` | Descarcă un repository |
| `git status` | Verifică modificările |
| `git add .` | Pregătește fișierele |
| `git commit -m "mesaj"` | Salvează modificările |
| `git push` | Încarcă modificările pe GitHub |
| `git pull` | Descarcă modificările de pe GitHub |

### Fluxul de lucru

```bash
git add .
git commit -m "Actualizare proiect"
git push
```

### Resurse utile
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)

