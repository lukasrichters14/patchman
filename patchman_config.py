from pathlib import Path


CONFIG_DIR = Path.home() / ".patchman"
CONFIG_FILE = CONFIG_DIR / ".patchmanrc"
WS_CONFIG_FILE = ".workspacerc"
PATCH_DB_FILE = "patches.db"
PATCH_DIR = "patches"


class PatchmanConfig:

    def __init__(self):
        self.active_ws = None
    
    def read(self):
        with CONFIG_FILE.open() as cfg:
            self.active_ws = cfg.readline().strip()
        
        if self.active_ws == "None":
            self.active_ws = None

    def write(self):
        if self.active_ws is None:
            CONFIG_FILE.write_text("None\n")
        else:
            CONFIG_FILE.write_text(self.active_ws + "\n")
    
    def get_active_workspace(self):
        return self.active_ws
    
    def set_active_workspace(self, ws):
        self.active_ws = ws


class WorkspaceConfig:

    def __init__(self):
        self.abs_dir = None
        self.file_ext = None
        self.active_patch = None
    
    def read(self, active_ws):
        if active_ws is not None:
            with (CONFIG_DIR / active_ws / WS_CONFIG_FILE).open() as wcf:
                self.abs_dir = wcf.readline().strip()
                self.file_ext = wcf.readline().strip().split(',')
                self.active_patch = wcf.readline().strip()
        
            if self.abs_dir == "None":
                self.abs_dir = None
            if self.file_ext == "None":
                self.file_ext = None
            if self.active_patch == "None":
                self.active_patch = None

    def write(self, active_ws):
        if active_ws is not None:
            with (CONFIG_DIR / active_ws / WS_CONFIG_FILE).open('w') as f:
                if self.abs_dir is None:
                    f.write("None")
                else:
                    f.write(self.abs_dir + "\n")
                
                if self.file_ext is None:
                    f.write("None")
                else:
                    f.write(",".join(self.file_ext) + "\n")
                
                if self.active_patch is None:
                    f.write("None")
                else:
                    f.write(self.active_patch + "\n")

    def get_absolute_user_directory(self):
        return self.abs_dir
    
    def set_absolute_user_directory(self, dir):
        self.abs_dir = dir
    
    def get_tracked_file_extensions(self):
        return self.file_ext
    
    def set_tracked_file_extensions(self, ext):
        self.file_ext = ext
    
    def get_active_patch(self):
        return self.active_patch
    
    def set_active_patch(self, p):
        self.active_patch = p


class PatchDatabase:

    def __init__(self):
        self.entries = {}
    
    def read(self, active_ws):
        if active_ws is not None:
            with (CONFIG_DIR / active_ws / PATCH_DB_FILE).open() as db:
                    for line in db:
                        file, timestamp = line.split(',')
                        file = file.strip()
                        timestamp = timestamp.strip()
                        self.entries[file] = float(timestamp)
    
    def write(self, active_ws):
        if active_ws is not None:
            with (CONFIG_DIR / active_ws / PATCH_DB_FILE).open('w') as db:
                for file, timestamp in self.entries.items():
                    db.write(f"{file},{timestamp}\n")
    
    def update(self, file, timestamp):
        self.entries[file] = timestamp
    
    def has_file_updated(self, file, timestamp):
        if file not in self.entries:
            return True
        
        return self.entries[file] < timestamp
