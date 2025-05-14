# Task Planner

## Overview

This program is a simple command-line tool for managing tasks. It allows users to add tasks with optional deadlines, list existing tasks, and remove tasks. Task data is stored in a JSON file for persistence.

## Features

- **Add Task**: Create a new task with an optional deadline.
- **List Tasks**: Display all existing tasks along with their deadlines (if any).
- **Remove Task**: Delete a task by specifying its index.
- **Help**: Provides usage instructions for the script.

## Requirements

- Python 3.x
- No additional libraries are required beyond Python's standard library.

## Usage

Run the script from the command line with the following options:

### Adding Tasks

To add a task, run the script with the task name and an optional deadline:


```sh
python todo.py add -d 2 days "Task Name"
```

This command will add a new task named "Task Name" with a deadline 2 days from the current time.

### Listing Tasks

To list all tasks, use:

```sh
python todo.py list
```

### Removing Tasks
To remove a task, run the following command:

```sh
python todo.py remove
```

You will be prompted to provide the index of the task to remove.

### Show Help

To display the help message, use:

```sh

python todo.py help
```
## File Structure

    tasks.json: This file stores the tasks data, including task names and deadlines. It is created if it does not exist.

