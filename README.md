# todoist_log_exe

This is a small script that runs from your computer and communicates with the Todoist server to create a log of completed tasks. There are more glamourous ways to accomplish this, but this is the simplest and most secure because you will not need to insert your api token into any webforms. The complete code is [here](https://www.github.com/ShayHill/todoist_log_exe) for review.

When you double click the executable file, a terminal window will open and ask you for the following:

* Enter your Todoist API token:
* Start date (YYMMDD)? (Enter for default: 8 day(s) ago):
* Start time (HH:MM:SS)? (Enter for default: 00:00:00):
* End date (YYMMDD)? (Enter for default: 1 day(s) ago):
* End time (HH:MM:SS)? (Enter for default: 23:59:59):

By default, the script will create a log of all tasks completed in the last seven days, starting eight days ago at midnight and ending yesterday at 11:59:59 pm.

## Where is my API Token?

You can get your API token from the Todoist website by clicking

1. your profile icon in the top left
2. Settings
3. Integrations
4. Developer

Copy this and paste it into the terminal window. Do not share your API token with anyone.

## Output

The script will write a file to the same location as the executable. The file will be named something like `todoist_2023-01-24T00-00-00_2023-01-31T23-59-59.TXT` and will contain, in tab-delimited fields

* the time and date of completion
* project name
* section name
* task content
* any notes you made on the task

You can open this is a text editor or in Excel as a spreadsheet. This file is the only thing the program will change. It will read your Todoist database but will not make changes.

## Limitations

This script will ignore archived projects.

This script will list recurring tasks only on the last date they were completed. So, if you complete a recurring task (e.g., walk the dog) every day, it will only show on the most recently completed day.

If you enter a large timeframe, the script might take several seconds to complete. The Todoist server paces API calls so people don't overwhelm it with bots.

I HAVE NO IDEA IF THIS WILL WORK WITH A FREE ACCOUNT. PAY YOUR $4 A MONTH!

## License: MIT

The MIT License (MIT)
Copyright © 2023 <Shay Hill>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## To Create an EXE

`pyinstaller src\todoist_log_exe\main.py --upx-dir . --onefile`
