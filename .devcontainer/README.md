# Latex Development container

Latex Development container that can be used with VSCode.

## Requirements
- [VS code](https://code.visualstudio.com/download)
- [VS code remote containers
  extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Docker](https://www.docker.com/products/docker-desktop)

## Setup

1. Open the command palette in VS Code (CTRL+SHIFT+P).
2. Select `Remote-Containers: Open Folder in Container...` and choose the
   project directory.
3. VS Code deploys the container and mounts the project directory as a volume
   automatically. Just open a terminal in VS Code (CTRL+SHIFT+`) to run
   commands.

## Miscellaneous
- To rebuild the image, open the command palette (CTRL+SHIFT+P), and select
  `Remote-Containers: Rebuild and reopen in container`
- You can customize VS Code settings through the `devcontainer.json` file
## To sync with Overleaf

1. Create project on Overleaf
2. Clone it locally with the Overleaf `git` URL
3. Create/Update `.devcontainer` and `.vscode` with your parameters, push them to Overleaf if you want your collaborators to have access to the same configuration
4. You can now push/pull with Overleaf as remote
5. As a bonus, you can also synchronize your repo on another remote (like Gitlab):
`git remote add gitlab <SSH URL.git>`
