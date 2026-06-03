# GitHub upload steps

Suggested repository:

- Owner: `Luciky-Leo`
- Repository name: `Luciky-Leo-mregdc-tls-ov`
- Visibility: public before submission if possible; private with reviewer access only if the journal allows it.
- Description: `Reproducibility package for TLS-associated LAMP3+CCR7+ mregDC states in ovarian cancer`

## Option A: GitHub web upload

1. Open `https://github.com/new`.
2. Create repository `Luciky-Leo-mregdc-tls-ov` under `Luciky-Leo`.
3. Do not initialize with a README, license, or .gitignore because this folder already contains them.
4. Upload all files from this folder:
   `E:\Reserch\MregDC\JTM_final_upload_20260603\02_github_reproducibility_repo_MregDC_TLS_OVC`
5. Commit with message:
   `Initial reproducibility package for MregDC TLS ovarian cancer study`
6. Create a release:
   - Tag: `v1.0.0`
   - Release title: `Peer-review reproducibility package`

## Option B: GitHub Desktop

1. In GitHub Desktop, choose `File -> Add local repository`.
2. Select:
   `E:\Reserch\MregDC\JTM_final_upload_20260603\02_github_reproducibility_repo_MregDC_TLS_OVC`
3. If prompted, create repository from this folder.
4. Commit all files.
5. Publish to `Luciky-Leo/Luciky-Leo-mregdc-tls-ov`.

## Option C: command line after creating the empty GitHub repository

This local folder is already initialized as a git repository and has the remote configured:

```bash
git remote -v
git push -u origin main
```

Use this only after creating the empty repository at:

```text
https://github.com/Luciky-Leo/Luciky-Leo-mregdc-tls-ov
```

## Zenodo DOI

After the GitHub repository is public:

1. Log into Zenodo with GitHub.
2. Enable the `Luciky-Leo/Luciky-Leo-mregdc-tls-ov` repository.
3. Create a GitHub release `v1.0.0`.
4. Zenodo will archive the release and generate a DOI.
5. Replace the manuscript Code availability placeholder with the GitHub URL and DOI.

Do not add a DOI to the manuscript until Zenodo or another archive has actually generated it.
