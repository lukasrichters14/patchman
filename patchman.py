from pathlib import Path
import sys

from patchman_parsing import *

CONFIG_DIR = Path.home() / ".patchman"
CONFIG_FILE = CONFIG_DIR / ".patchmanrc"

def load():
    if CONFIG_DIR.exists():
        # Load workspaces
        workspaces = {}
        for p in CONFIG_DIR.iterdir():
            if p.is_dir():
                workspaces[p.name] = p
        
        # Load previous state
        with CONFIG_FILE.open() as cfg:
            active_workspace = cfg.readline()
        
        return active_workspace, workspaces
    
    else:
        CONFIG_DIR.mkdir()
        CONFIG_FILE.touch()
    
    return "", {}


def help():
    print("USAGE: patchman")


def init(flags):
    if (flags[CMD_INIT][1] is None):
        print("ERROR -> Missing Required Argument: No workspace path provided.")
        return
    
    # Create user workspace directory if it doesn't already exist
    ws_path = Path(flags[CMD_INIT][1])
    if not ws_path.exists():
        ws_path.mkdir()
    
    # Create workspace directory in CONFIG_DIR
    ws_dir = CONFIG_DIR / ws_path.name
    if ws_dir.exists():
        print("ERROR -> Workspace Cannot Be Created: Workspace already exists.")
        return
    ws_dir.mkdir()

    # Create patches directory in CONFIG_DIR
    (ws_dir / "patches").mkdir()

    # Create patch DB
    patch_db = ws_dir / "patches.db"
    patch_db.touch()


def workspace(flags, active_ws):
    args = flags[CMD_WORKSPACE][1]
    if args is None and active_ws != "":
        print(active_ws)
    elif args is None and active_ws == "":
        print("No active workspace.")
    else:
        ws_name = args[0]
        ws_dir_found = False
        for p in CONFIG_DIR.iterdir():
            if p.name == ws_name:
                CONFIG_FILE.write_text(ws_name)
                ws_dir_found = True
        if not ws_dir_found:
            print(f"ERROR -> Workspace Not Found: The workspace {ws_name} does not exist.")


def new(flags):
    print(CMD_NEW)


def update(flags):
    print(CMD_UPDATE)


def interactive_config(flags):
    print("Interactive Workspace Configuration")
    file_watches = input("File extensions to watch for patches (i.e. '.jar,.class'): ")
    

def config(flags, active_ws):
    if flags[CMD_CONFIG][1] is None:
        flags = interactive_config(flags)
    
    args = flags[CMD_CONFIG][1]


def main():
    # Load configuration or create if it doesn't exist.
    active_ws, workspaces = load()

    flags = parse(sys.argv)
    if flags[CMD_ERROR][0]:
        return
    elif flags[CMD_HELP][0]:
        help()
    elif flags[CMD_INIT][0]:
        init(flags)
    elif flags[CMD_WORKSPACE][0]:
        workspace(flags, active_ws)
    elif flags[CMD_NEW][0]:
        new(flags)
    elif flags[CMD_UPDATE][0]:
        update(flags)
    elif flags[CMD_CONFIG][0]:
        config(flags, active_ws)


if __name__ == "__main__":
    main()