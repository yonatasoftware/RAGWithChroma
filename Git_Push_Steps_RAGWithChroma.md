# Git Push Steps for the RAGWithChroma Project

## 1. Open a terminal in your project

``` bash
cd /Users/tapasdas/work/workingFolder/LLM_Demo/RAGWithChroma
```

Verify:

``` bash
pwd
```

## 2. Check Git status

``` bash
git status
```

Initialize if needed:

``` bash
git init
```

## 3. Verify the remote

``` bash
git remote -v
```

Add one if missing:

``` bash
git remote add origin https://github.com/<your-github-username>/RAGWithChroma.git
```

## 4. Create a `.gitignore`

``` gitignore
__pycache__/
*.pyc
venv/
.env
chroma_db/
.vscode/
.idea/
.DS_Store
```

## 5. Stage files

``` bash
git add .
git status
```

## 6. Commit

``` bash
git commit -m "Implemented Insurance RAG using ChromaDB and RecursiveCharacterTextSplitter"
```

## 7. Push

First push:

``` bash
git branch -M main
git push -u origin main
```

Subsequent pushes:

``` bash
git push
```

## Troubleshooting

Check remote:

``` bash
git remote -v
```

Change remote:

``` bash
git remote set-url origin https://github.com/<your-github-username>/RAGWithChroma.git
```

Verify excluded files:

-   .env
-   chroma_db/
-   venv/
-   **pycache**/
-   .DS_Store
