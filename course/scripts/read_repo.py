import io
import zipfile
import requests
import frontmatter
import json

def read_repo_data(repo_owner, repo_name):
    """
    Télécharge et lit tous les fichiers markdown d'un repo GitHub
    """
    url = f"https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/main"
    resp = requests.get(url)

    if resp.status_code != 200:
        raise Exception(f"Erreur téléchargement: {resp.status_code}")

    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    for file_info in zf.infolist():
        filename = file_info.filename.lower()

        if not (filename.endswith(".md") or filename.endswith(".mdx")):
            continue

        with zf.open(file_info) as f_in:
            content = f_in.read().decode("utf-8", errors="ignore")
            post = frontmatter.loads(content)
            data = post.to_dict()
            data["filename"] = filename
            repository_data.append(data)

    zf.close()
    return repository_data

def save_to_json(data, output_file):
    """
    Sauvegarde les données dans un fichier JSON.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Sauvegardé {len(data)} documents dans {output_file}")



if __name__ == "__main__":
    docs = read_repo_data("DataTalksClub", "faq")
    print(f"Documents trouvés : {len(docs)}")
    print("Exemple du premier document :")
    print(docs[0])

    # Sauvegarde en JSON
    save_to_json(docs, "faq_docs.json")

