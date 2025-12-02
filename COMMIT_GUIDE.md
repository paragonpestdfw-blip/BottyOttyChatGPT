# Committing Changes to GitHub

Follow these steps to record your updates and publish them to GitHub from this repository.

1. **Check your status**
   ```bash
   git status
   ```
2. **Stage the files you changed**
   ```bash
   git add <files>
   ```
   To stage everything that is modified and tracked, you can run:
   ```bash
   git add -u
   ```
3. **Review what is staged** (optional but recommended)
   ```bash
   git diff --cached
   ```
4. **Create a commit with a clear message**
   ```bash
   git commit -m "Describe the change"
   ```
5. **Push your branch to GitHub**
   ```bash
   git push origin <branch-name>
   ```
6. **Open a Pull Request**
   - Go to GitHub and open a PR from your branch into the main branch.
   - Include a concise summary of what changed and any testing performed.

## Add a GitHub remote (if none exists)

If `git remote -v` shows no entries, connect this repo to GitHub so pushes have a destination.

1. Add the remote (replace `YOUR_REPO_URL` with the HTTPS or SSH URL from GitHub):
   ```bash
   git remote add origin YOUR_REPO_URL
   ```
2. Confirm it was added:
   ```bash
   git remote -v
   ```
3. Set the upstream on first push (example for the current `work` branch):
   ```bash
   git push -u origin work
   ```

## Let the assistant push for you

To allow the assistant to push commits to GitHub on your behalf:

1. **Add the remote** using the steps above.
2. **Provide credentials during the session**:
   - Easiest: share a short-lived GitHub personal access token (PAT) with repo push rights and ask the assistant to run `git push`.
   - Safer: use `gh auth login` in this container with your PAT so the credentials are cached, then tell the assistant to push.
3. **Tell the assistant the branch name** to push (default here is `work`).
4. After the push, you can revoke the PAT or remove cached credentials:
   ```bash
   gh auth logout
   ```

Without a configured remote and valid credentials, the assistant cannot push to GitHub.

If a commit needs to be amended before pushing, you can run:
```bash
git commit --amend
```
and then push with force if the branch was already pushed:
```bash
git push --force-with-lease origin <branch-name>
```
