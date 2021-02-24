## Concatenating commands in pipes

KGTK has a pipelining architecture based on [Unix pipes](https://linux.die.net/man/7/pipe) that allows chaining all the commands included in the framework. 

Pipelining increases efficiency by avoiding the need to write files to disk and supporting parallelism, allowing downstream commands to process data before upstream commands complete.  

To use pipes, you just need to use the shortcut pipe operator `/`. For example, the following command calculates the number of instances of each class in a KGTK file `edges.tsv` by first filtering all P31 (instance of) edges and then counting them with the `unique` command. The result is stored in a file named `class_count.tsv`:

```bash
kgtk filter -i edges.tsv -p " ; P31 ; " / unique --column node2 -o class_count.tsv
```

!!! note
    If you need to read from stdin you will need to use `-i -`