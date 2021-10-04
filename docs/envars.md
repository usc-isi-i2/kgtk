## Environment Variables

The KGTK commands use environment variables to provide the default value for
certain command options.

| Command | Option | Environment Variable | Value Type | Default | Description |
| ------- | ------ | -------------------- | ---------- | ------- | ----------- |
| (all) | `--debug` | `KGTK_OPTION_DEBUG` | boolean | false | When true, enable debug mode. When errors occur, more complete error traces are written. |
| (all) | `--expert` | `KGTK_OPTION_EXPERT` | boolean | false | When true, enable expert mode.  In expert mode, additional command options may be provided to `--help`. |
| (many) | `--graph-cache` | `KGTK_GRAPH_CACHE` | string | The location of the graph cache file. |
| `add-labels` `lift` | `--label-file` | `KGTK_LABEL_FILE` | string | The location of the KGTK file containing label values. |
| (all) | `--pipedebug` | `KGTK_OPTION_PIPEDEBUG` | boolean | false | When true, enable pipe debug mode. Additional feedback is provided during the execution of  KGTK command pipes. |
| (all) | `--progress` | `KGTK_OPTION_PROGRESS` | boolean | false | When true, enable progress monitoring. The `pv` command is used to monitor command execution. |
| (all) | `--progress-tty` | `KGTK_OPTION_PROGRESS_TTY` | string | /dev/tty | The tty device for progress monitoring output. |
| (all) | `--timing` | `KGTK_OPTION_TIMING` | boolean | false | When true, enable timing measurements.  A summary of process time is printed. |

| Function | Option | Environment Variable | Value type | Default | Description |
| ------- | ------ | -------------------- | ---------- | ------- | ----------- |kgtk()
| `kgth()` `kypher()` | `auto_display_html` | `KGTK_AUTO_DISPLAY_HTML` | boolean | true | When true, display HTML output.  When false, print HTML output. |
| `kgth()` `kypher()` | `auto_display_json` | `KGTK_AUTO_DISPLAY_JSON` | boolean | true | When true, display JSON output.  When false, print JSON output. |
| `kgth()` `kypher()` | `auto_display_md` | `KGTK_AUTO_DISPLAY_MD` | boolean | false | When true, display Markdown output (`md`, `table`).  When false, print Markdown output. |
| `kgth()` `kypher()` | `bash_command` | `KGTK_BASH_COMMAND` | string | bash | The shell script interpreter used for subcommand execution. |
| `kgth()` `kypher()` | `kgtk_command` | `KGTK_KGTK_COMMAND` | string | kgtk | The kgtk command used for subcommand execution. This option may also be used to invoke timing (`time kgtk`) or to pass options to the `kgtk` command (`kgtk --debug`). |
