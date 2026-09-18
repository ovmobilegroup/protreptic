import json
from pathlib import Path
from data_merger import merge_workspace

# Use a mock workspace path or point to where the parent files were
# The files are likely at the parent task's workspace.
# For now, let's just run it against the target files if I can find where they are.
# Wait, the task says 'scratch' workspace. I should check if the files exist here.
import os
print(os.listdir("."))
