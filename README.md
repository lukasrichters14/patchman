# Patchman

Patchman is a *very* simplistic CLI *patch man*ager. The driving idea behind patchman is that frequently we want to test changes to our programs before officially commiting them to our version control software. But without dedicated development pipelines, it often becomes necessary to manually patch a development build as a final qualification step. Patchman aims to alleviate some of the tedium required in this time consuming practice by tracking and organizing your modified deliverables for easy retrieval and deployment.

## Quickstart

1. Add the `patchman` directory to your `PATH`

2. Initialize your patchman workspace

        patchman init <root_project_directory>  // accepts relative paths too

3. Configure your workspace (must provide a list of comma-separated file extensions for patchman to track)

        patchman config .jar,.class

4. Compile your code or make a change to a tracked file.
5. Create a new patch

        patchman new <patch_name>

Currently, patchman only supports tracking and storing user-configured files, but some of the planned features are listed below.

* Automatic deployment to user-configured targets
* Improved UI (progress bars, colors, etc.)
