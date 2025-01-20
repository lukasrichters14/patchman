# Patchman

Patchman is a *very* simplistic CLI *patch man*ager. Without dedicated development pipelines, it often becomes necessary to manually patch development builds for testing. This usually entails multiple iterations of testing, debugging, and patching. Depending on the complexities of your build system, it is possible that simple source changes result in modifications to multiple binaries, or other deliverables, forcing you to spend time tracking down those changes and deploying them to your testing environment. Patchman aims to alleviate some of the tedium required in this time-consuming practice by tracking and organizing your modified deliverables for easy retrieval and deployment.

## Requirements

- Python 3.x installed and included in PATH

- (Optional) [alive-progress](https://github.com/rsalmei/alive-progress) module for improved UI

## Quickstart

1. Add the `patchman` directory to your `PATH`

2. Initialize your patchman workspace

        patchman init <root_project_directory>  // accepts relative paths too

3. Configure your workspace (must provide a list of comma-separated file extensions for patchman to track)

        patchman config .jar,.class

4. Compile your code or make a change to a tracked file.
5. Create a new patch

        patchman new <patch_name>

## Planned Features

- Deliver modified files to user-defined targets:

    - For simple projects, copy all modified files to a directory specified by the user.

    - For more complicated projects, accept a configuration file (preferably YAML) specifying deployment targets for individual files or groups of files. Should also be able to specify most (all?) of the behavior through the CLI.

- Improve `config` command:

    - Pattern matching of filenames (not just based on extension).

    - Exclude files/directories
