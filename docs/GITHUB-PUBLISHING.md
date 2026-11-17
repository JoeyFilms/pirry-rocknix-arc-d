# Publishing this project on GitHub — beginner's guide

The aim is a public project page like the Pirry author's GitHub page: a readable front page, source code, a download link and release notes. You do not need to learn terminal commands or install Git for the initial publication.

Suggested repository: **`JoeyFilms/pirry-rocknix-arc-d`**.

## Part 1: create the project

1. Sign into GitHub as **JoeyFilms**.
2. Open [Create a new repository](https://github.com/new?name=pirry-rocknix-arc-d&visibility=public).
3. Select **JoeyFilms** as the owner.
4. Use repository name **`pirry-rocknix-arc-d`**.
5. Suggested description: **One-step Pirry 1.6.3 installer and native Saturn integration for RG ARC-D on ROCKNIX.**
6. Choose **Public** so friends can read/download without access invitations.
7. Enable **Add a README file**. Leave automatic license and .gitignore choices empty; the prepared project supplies both.
8. Click **Create repository**.

The resulting address should be `https://github.com/JoeyFilms/pirry-rocknix-arc-d`. Send that address back in the ChatGPT conversation. The connected GitHub tools can populate an existing repository; they cannot create the new repository themselves.

If you choose a different name/account, tell the assistant the actual link so it can update the front-page download URL before uploading.

Official reference: [Creating a new repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository).

## Part 2: put the prepared files on GitHub

The upload pack contains a **`github-project`** directory. Its top-level `README.md` is the front page. `docs/SETUP.md` is the detailed setup guide. `downloads/` contains the ready-to-install ZIP. The root scripts and `pirry-arc/` directory are the source code.

The easiest path is to send the repository link back to the assistant and have the files uploaded through the connected GitHub account. You do not need to manually paste code or provide a password/token in chat.

If doing it yourself:

1. Extract the publishing ZIP on your computer.
2. Open your repository, choose **Add file → Upload files**.
3. Drag the contents of **`github-project`** into the upload area, retaining folder structure. Do not upload the outer publishing ZIP as the project source, and do not put everything inside an extra `github-project` folder on GitHub.
4. Use a commit message such as **Add Pirry Complete installer and setup guide**.
5. Commit to `main` if that is offered. If the interface instead proposes a new branch, open and merge the resulting pull request.

After upload, the repository root should include:

| Item | Purpose |
|---|---|
| `README.md` | Front page and download link |
| `docs/SETUP.md` | Detailed handheld setup instructions |
| `downloads/Pirry-Complete-1.6.3-ARC-D.zip` | File friends install |
| `Install-Saturn-Pirry.sh` | Installer source |
| `pirry-arc/` | Launcher, mappings and integration source |
| `LICENSE` and `CREDITS.md` | License and upstream attribution |

Do not upload your handheld's installed settings directory or private logs as source. The prepared pack already contains everything intended for publication.

Official reference: [Adding files using the GitHub website](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

## Part 3: check the page before sharing

Open the repository front page and verify:

- The title is **Pirry Complete for ROCKNIX on RG ARC-D**.
- The download link returns the installer ZIP.
- The setup-guide link opens a formatted document.
- Firmware information clearly says **20261101** as the main documented target and **20261001** as also supported.
- Original emulator authors and ROCKNIX contributors receive credit.
- The initial public version is described honestly as a beta needing a complete fresh-install test.

The download is intentionally small: the scripts fetch the approximately 5 MB emulator from its original GitHub release during installation.

The repository README becomes the project page automatically. A separate GitHub Pages website is optional; it is not required for this download-and-instructions page.

## Part 4: add a downloadable release

The front-page download will already work after the files are uploaded, because the installer ZIP is in `downloads/`. A formal GitHub Release is useful as an additional versioned download page.

1. Open your repository's **Releases** section and choose **Draft a new release**.
2. Create tag **`v1.1.0-beta.1`**, targeting **`main`**.
3. Title: **Pirry Complete for ARC-D — installer v1.1.0-beta.1**.
4. Paste the prepared text from **`docs/RELEASE-NOTES.md`**.
5. Attach **`Pirry-Complete-1.6.3-ARC-D.zip`** from the pack's `github-project/downloads/` folder. Attach `SHA256SUMS` too if desired.
6. Mark it as a **pre-release** for the initial independent installation test.
7. Publish when ready, or save a draft for review.

The tag versions **your integration package**. It does not claim you authored or released the upstream Pirry emulator. That emulator's version remains **1.6.3**.

Official reference: [Managing GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

## Part 5: give your friend one link

Share the project URL:

```text
https://github.com/JoeyFilms/pirry-rocknix-arc-d
```

Ask them to use the **Download the complete installer ZIP** link and follow the setup guide. They should not need older messages, separate patches or your personal SD-card files.

For the first external test, ask them to report their exact handheld model, ROCKNIX version and whether the fresh install completed. If something fails, `Pirry-Install.log` is directly in their `ports` folder.

## Maintaining future versions

- A documentation correction can be made by editing the relevant Markdown file on GitHub.
- Installer code and the downloadable ZIP must stay in sync; changing source alone does not change an already uploaded ZIP.
- `tools/build_release.py` rebuilds the installer ZIP from the repository source and writes its checksum. It is a maintainer utility; your friends do not need to run it.
- Keep older release tags/downloads available for rollback.
- Do not silently switch to the latest Pirry binary. A new upstream version needs a reviewed URL/checksum, the accepted hashes in the menu integration, dependency checks and handheld testing.
- A new ROCKNIX release needs controller and launch-framework checks before adding it to the accepted versions.
- Do not describe a build as tested on other hardware or firmware without evidence.

If GitHub says your connected app cannot see the new repository, grant that GitHub connection access to this repository through GitHub's app settings, then retry. No password or access token needs to be posted in the conversation.
