from pathlib import Path
import sys
import os
import shutil

from patchman_parsing import *
from patchman_config import *


pcfg = PatchmanConfig()
wcfg = WorkspaceConfig()
db   = PatchDatabase()


def load():
    if CONFIG_DIR.exists():
        # Load workspaces
        workspaces = {}
        for p in CONFIG_DIR.iterdir():
            if p.is_dir():
                workspaces[p.name] = p
        
        # Load previous state
        pcfg.read()
        wcfg.read(pcfg.get_active_workspace())
        db.read(pcfg.get_active_workspace())
    
    else:
        CONFIG_DIR.mkdir()
        CONFIG_FILE.touch()


def save():
    pcfg.write()
    wcfg.write(pcfg.get_active_workspace())
    db.write(pcfg.get_active_workspace())


def help():
    print("USAGE: patchman")


def init(flags):
    if (flags[CMD_INIT][1] is None):
        print("ERROR -> Missing Required Argument: No workspace path provided.")
        return
    
    # Create user workspace directory if it doesn't already exist
    ws_path = Path(flags[CMD_INIT][1]).absolute()
    if not ws_path.exists():
        ws_path.mkdir()
    
    # Create workspace directory in CONFIG_DIR
    ws_dir = CONFIG_DIR / ws_path.name
    if ws_dir.exists():
        print("ERROR -> Workspace Cannot Be Created: Workspace already exists.")
        return
    ws_dir.mkdir()

    # Create patches directory in workspace directory
    (ws_dir / PATCH_DIR).mkdir()

    # Create patch DB
    patch_db = ws_dir / PATCH_DB_FILE
    patch_db.touch()

    # Create workspace config file
    ws_config = ws_dir / WS_CONFIG_FILE
    ws_config.touch()
    wcfg.set_absolute_user_directory(str(ws_path.absolute()))

    # Set this workspace as the active workspace
    pcfg.set_active_workspace(ws_path.name)


def workspace(flags):
    active_ws = pcfg.get_active_workspace()
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
                wcfg.write(active_ws)
                pcfg.set_active_workspace(ws_name)
                wcfg.read(ws_name)
                ws_dir_found = True
                print(f"Switched to workspace {ws_name}.")
                break

        if not ws_dir_found:
            print(f"ERROR -> Workspace Not Found: The workspace {ws_name} does not exist.")


def check_for_updated_files(user_ws_dir, patch_dir):
    # Collect all tracked files that were modified
    num_modified = 0
    user_ws_dir = Path(user_ws_dir)
    file_extensions = wcfg.get_tracked_file_extensions()
    for p in user_ws_dir.rglob('*', recurse_symlinks=True):
        if p.suffix in file_extensions and db.has_file_updated(p.name, os.path.getmtime(p)):
            db.update(p.name, os.path.getmtime(p))
            shutil.copy(str(p), str(patch_dir / p.name), follow_symlinks=True)
            num_modified += 1
    
    return num_modified


def new(flags):
    if flags[CMD_NEW][1] is None:
        print("ERROR -> Missing Required Argument: No patch name provided.")
        return
    
    patch_name = flags[CMD_NEW][1]
    
    user_ws_dir = wcfg.get_absolute_user_directory()
    if user_ws_dir is None:
        print("FATAL ERROR -> User workspace directory not stored in config file.")
        return
    
    # Create a new folder for this patch in the active workspace
    new_patch_dir = CONFIG_DIR / pcfg.get_active_workspace() / PATCH_DIR / patch_name
    if new_patch_dir.exists():
        print("ERROR -> New Patch Cannot Be Created: Patch already exists. Please provide a unique name or use the 'update' command.")
        return
    
    new_patch_dir.mkdir()
    wcfg.set_active_patch(patch_name)

    num_modified = check_for_updated_files(user_ws_dir, new_patch_dir)
    
    print(f"Patch {patch_name} created. Found {num_modified} modified files.")



def update(flags):
    user_ws_dir = wcfg.get_absolute_user_directory()
    if user_ws_dir is None:
        print("FATAL ERROR -> User workspace directory not stored in config file.")
        return

    patch_name = wcfg.get_active_patch()
    patch_dir = CONFIG_DIR / pcfg.get_active_workspace() / PATCH_DIR / patch_name
    
    num_modified = check_for_updated_files(user_ws_dir, patch_dir)
    
    print(f"Updated {patch_name}. Found {num_modified} modified files.")


def interactive_config(flags):
    print("Interactive Workspace Configuration")
    file_watches = input("File extensions to watch for patches (i.e. '.jar,.class'): ")
    

def config(flags):
    if flags[CMD_CONFIG][1] is None:
        print("ERROR -> Missing Required Argument: No file extensions provided.")
        return
    
    args = flags[CMD_CONFIG][1]
    file_extensions = args.split(",")

    # Add '.' to the beginning of the extension if not already present
    for i in range(len(file_extensions)):
        if file_extensions[i][0] != '.':
            file_extensions[i] = '.' + file_extensions[i]

    wcfg.set_tracked_file_extensions(file_extensions)
    
    user_ws_dir = wcfg.get_absolute_user_directory()
    if user_ws_dir is None:
        print("FATAL ERROR -> User workspace directory not stored in config file.")
        return
    
    # Iterate through the user's workspace and note the last modified timestamps for
    # each file type we're tracking.
    num_tracking = 0
    user_ws_dir = Path(user_ws_dir)
    for p in user_ws_dir.rglob('*', recurse_symlinks=True):
        if p.suffix in file_extensions:
            db.update(p.name, os.path.getmtime(p))
            num_tracking += 1
    
    print(f"Successfully configured {pcfg.get_active_workspace()}. Tracking {num_tracking} files.")



def main():
    # Load configuration or create if it doesn't exist.
    load()

    flags = parse(sys.argv)
    if flags[CMD_ERROR][0]:
        return
    elif flags[CMD_HELP][0]:
        help()
    elif flags[CMD_INIT][0]:
        init(flags)
    elif flags[CMD_WORKSPACE][0]:
        workspace(flags)
    elif flags[CMD_NEW][0]:
        new(flags)
    elif flags[CMD_UPDATE][0]:
        update(flags)
    elif flags[CMD_CONFIG][0]:
        config(flags)
    
    # Save state for the next call
    save()


if __name__ == "__main__":
    #main()

    load()
    update(FLAGS)
    save()