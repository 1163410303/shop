# Contributing Guidelines  

### Basic guidelines

All packages you commit or submit by pull-request should follow these simple guidelines:

* Package a version which is still maintained by the upstream author and will be updated regularly with supported versions.
* Have no dependencies outside the OpenWrt core packages or this repository feed.
* Have been tested to compile with the correct includes and dependencies. Please also test with "Compile with full language support" found under "General Build Settings" set if language support is relevant to your package.
* Best of all -- it works as expected!


#### Commits in your pull-requests should:

* Have a useful description prefixed with the package name

### Advice on pull requests:

Pull requests are the easiest way to contribute changes to git repos at Github. They are the preferred contribution method, as they offer a nice way for commenting and amending the proposed changes.

* You need a local "fork" of the Github repo.
* Use a "feature branch" for your changes. That separates the changes in the pull request from your other changes and makes it easy to edit/amend commits in the pull request. Workflow using "feature_x" as the example:
  - Update your local git fork to the tip (of the master, usually)
  - Create the feature branch with `git checkout -b feature_x`
  - Edit changes and commit them locally
  - Push them to your Github fork by `git push -u origin feature_x`. That creates the "feature_x" branch at your Github fork and sets it as the remote of this branch
  - When you now visit Github, you should see a proposal to create a pull request

* If you later need to add new commits to the pull request, you can simply commit the changes to the local branch and then use `git push` to automatically update the pull request.

* If you need to change something in the existing pull request (e.g. to add a missing signed-off-by line to the commit message), you can use `git push -f` to overwrite the original commits. That is easy and safe when using a feature branch. Example workflow:
  - Checkout the feature branch by `git checkout feature_x`
  - Edit changes and commit them locally. If you are just updating the commit message in the last commit, you can use `git commit --amend` to do that
  - If you added several new commits or made other changes that require cleaning up, you can use `git rebase -i HEAD~X` (X = number of commits to edit) to possibly squash some commits
  - Push the changed commits to Github with `git push -f` to overwrite the original commits in the "feature_x" branch with the new ones. The pull request gets automatically updated

### If you have commit access:

* Do NOT use git push --force.
* Do NOT commit to other maintainer's packages without their consent.
* Use Pull Requests if you are unsure and to suggest changes to other maintainers.


### Release Branches:

* Branches named "for-XX.YY" (e.g. for-14.07) are release branches.
* These branches are built with the respective OpenWrt release and are created
  during the release stabilisation phase.
* If you are unsure if your change is suitable, please use a pull request.
