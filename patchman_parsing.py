CMD_HELP      = 'help'
CMD_INIT      = 'init'
CMD_WORKSPACE = 'workspace'
CMD_UPDATE    = 'update'
CMD_NEW       = 'new'
CMD_ERROR     = 'error'
CMD_CONFIG    = 'config'

ALIASES = {
    '-h'     : CMD_HELP,
    '--help' : CMD_HELP
}

FLAGS = {
    CMD_HELP      : (False, None),  # Show help dialog
    CMD_INIT      : (False, None),  # Initialize workspace, required: directory
    CMD_WORKSPACE : (False, None),  # List workspaces, optional: workspace directory (select workspace)
    CMD_UPDATE    : (False, None),  # Update current patch with new changes
    CMD_NEW       : (False, None),  # Create new patch and update with new changes
    CMD_ERROR     : (False, None),  # Indicates the parser encountered an error and other flags should be ignored
    CMD_CONFIG    : (False, None),  # Allows the user to configure the active workspace
}

def parse(argv: list):
    
    # No commands, just program name
    if len(argv) == 1:
        FLAGS[CMD_HELP] = (True, None)
        return FLAGS
    
    # Ignore the first command line parameter (name)
    argv = argv[1:]
    i = 0
    while i < len(argv):
        if argv[i] in ALIASES or argv[i] in FLAGS:
            if argv[i] in ALIASES:
                cmd = ALIASES[argv[i]]
            else:
                cmd = argv[i]
            
            if i+1 < len(argv) and not (argv[i+1] in ALIASES or argv[i+1] in FLAGS):
                i += 1
                param = argv[i]
            else:
                param = None

            FLAGS[cmd] = (True, param)    
            
            
        else:
            FLAGS[CMD_ERROR] = (True, None)
            print(f"ERROR -> Unknown Parameter: {argv[i]}. Use 'patchman -h' for help.")
            break
        
        i += 1
    
    return FLAGS
