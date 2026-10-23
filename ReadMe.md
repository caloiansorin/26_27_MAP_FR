# Ghid Introductiv GitHub
## Despre platforma
Este o platforma bazata pe cloud destinata gazduirii si colaborarii pe proiecte software utilizand sistemul de control al versiunilor **Git**.

## Obiective:
- Stocarea centralizata a codului sursa in repositories.
- Colaborarea in echipa prin code review si pull requests.
- Automatizarea fluxurilor de lucru prin GitHub Actions (CI/CD).
- Managementul sarcinilor prin Issues si Projects.

## Concepte cheie
| Concept | Descriere |
|---------|-----------|
| Repository (Repo) | Spatiul de stocare pentru fisierele, istoricul si setarile unui proiect |
| Commit | O salvare punctuala a starii fisierelor cu un mesaj explicativ |
| Branch | O linie paralela de dezvoltare separata de codul principal |
| Pull Request (PR) | O cerere oficiala de a integra modificarile dintr-un branch in altul |
| Issue | Un instrument de urmarire a bug-urilor, sarcinilor sau propunerilor |

## Fluxul de baza de lucru
### 1. Clonarea proiectului local
```bash
git clone [https://github.com/utilizator/nume-proiect.git](https://github.com/utilizator/nume-proiect.git)
```
### 2. Crearea unui branch dedicat
```bash
git checkout -b feature/noua-functionalitate
```
### 3. Salvarea modificarilor locale
```bash
git add .
git commit -m "Adaugat functionalitate X"
```
### 4. Trimiterea branch-ului pe GitHub
```bash
git push -u origin feature/noua-functionalitate
```
### 5. Deschiderea unui Pull Request
- Din interfata web GitHub, deschide un PR catre branch-ul `main`.
- Asteapta recenzia colegilor sau rularea testelor automate.

## Resurse utile
[Documentatie Oficiala GitHub](https://docs.github.com/en)  
[GitHub Skills - Cursuri Interactive](https://skills.github.com/)  
[Ghid GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
