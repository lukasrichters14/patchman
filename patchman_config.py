from pathlib import Path


CONFIG_DIR = Path.home() / ".patchman"
CONFIG_FILE = CONFIG_DIR / ".patchmanrc"
WS_CONFIG_FILE = ".workspacerc"
PATCHES_DB_FILE = "patches.db"


class PatchmanConfig:

    def __init__(self):
        self.active_ws = None
    
    def read(self):
        with CONFIG_FILE.open() as cfg:
            self.active_ws = cfg.readline()
        
        if self.active_ws == "None":
            self.active_ws = None

    def write(self):
        CONFIG_FILE.write_text(self.active_ws)
    
    def get_active_workspace(self):
        return self.active_ws
    
    def set_active_workspace(self, ws):
        self.active_ws = ws


class WorkspaceConfig:

    def __init__(self):
        self.abs_dir = None
        self.file_ext = None
    
    def read(self, active_ws):
        if active_ws is not None:
            with (CONFIG_DIR / active_ws / WS_CONFIG_FILE).open() as wcf:
                self.abs_dir = wcf.readline()
                self.file_ext = wcf.readline()
        
            if self.abs_dir == "None":
                self.abs_dir = None
            if self.file_ext == "None":
                self.file_ext = None

    def write(self, active_ws):
        if active_ws is not None:
            (CONFIG_DIR / active_ws / WS_CONFIG_FILE).write_text(f"{self.abs_dir}\n{",".join(self.file_ext)}")

    def get_absolute_user_directory(self):
        return self.abs_dir
    
    def get_tracked_file_extensions(self):
        return self.file_ext
    
    def set_tracked_file_extensions(self, ext):
        self.file_ext = ext