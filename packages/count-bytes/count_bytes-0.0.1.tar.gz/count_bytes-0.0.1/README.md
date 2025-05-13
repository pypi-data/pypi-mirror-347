NOTES:

This is a simple Python module that counts the bytes of text and files.

USAGE:

• `checkStr` counts the bytes of a string.
• `checkFile` counts the bytes of a file.

simple code for checking a string:
```python
import count_bytes as cb

string = "Hello, World!"
howManyBytes = cb.checkStr(string, 'utf-8')
print(howManyBytes)```
simple code for checking a file:
```python
import count_bytes as cb

file = "PATH/TO/FILE"
howManyBytes = cb.checkFile(file)
print(howManyBytes)```

REMEMBER:

In `checkStr` always remember to add the encoding at the end.
If you do not know what encoding is, (which is IMPOSSIBLE),
just type 'utf-8' which is the standard encoding, (I think).
