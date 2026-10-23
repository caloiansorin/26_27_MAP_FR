# Pasii de utilizare GitHub
## Creeaza cont si repository

Intra pe github.com, fa-ti cont si apasa pe New repository. Pune-i un nume si lasa-l Public sau Private.

## Configureaza Git pe calculator
Deschide terminalul si seteaza identitatea:
```bash
git config --global user.name "Numele Tau"

git config --global user.email "email@exemplu.com"
```

## Cloneaza sau initializeaza proiectul

Daca iei repo-ul de pe GitHub:
```bash

git clone [https://github.com/user/repo.git](https://github.com/user/repo.git)

```
Daca pornesti dintr-un folder local existent:
```bash
git init

git remote add origin [https://github.com/user/repo.git](https://github.com/user/repo.git)
```
### 1. Salveaza modificarile (Commit)

Dupa ce ai modificat sau adaugat fisiere:

```bash
git add .

git commit -m "Mesaj scurt despre modificari"

```

### 2. Trimite pe GitHub (Push)

```bash
git push -u origin main
```
### 3. Descarca modificarile noi (Pull)

Cand lucrezi in echipa sau de pe alt PC:

```bash 

git pull

```


## SPOR LA TREABA
