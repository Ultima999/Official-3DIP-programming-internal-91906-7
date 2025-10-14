# Official-3DIP-programming-internal-91906-7
This is my 5 Iteration Fitness Manager App, where you can create a scientifically optimal workout schedule, with flexible exercises, days, purposes, and intensities.

Iterations work as followed=>
V1: Baseline code; user can choose specific days of the week as workout days and rest are automatically assigned as rest days.

V2: Improvements and JSON file implementation; Improved Baseline code of create_schedule() to assign muscles (purposes) to each workout day. Also, 2 JSON files are added, one containing muscle groups and sub-muscles, and the other containing muscle groups and exercises. 2 New functions are added=> accessing exercises, and accessing muscle groups.

V3: Futher Improvement to logic and JSON file Revamp; JSON files replaces, one containing all exercises, and muscle/sub_muscles, and a schedule (template) JSON file for schedule to be uploaded to. Improving baseline code of create_schedule() to adhere to new JSON files. Combining 2 functions of accessing exercises and muscle groups to display both at once (to prepare for later iterations)

V4: GUI implementation and improvement in Code logic to adhere to new GUI; Creating a structured, functional GUI with slight improvements required, that can cleanly run through popups and create schedule for user, upload to JSON, then display for user.

V5: Final iteration, GUI Improvements and Implementation of OOP, Classes, and Inheritance; Implementing OOP to each exercise in the JSON file, in the for of itensities, so that the users can add their own exercises, customize it best suited towards their needs, and overall easily create a scientifically optimal exercise with only a few buttons with incredible code logic.
