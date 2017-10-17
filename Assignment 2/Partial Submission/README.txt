Dylan Parsons
CS 2320
10/05/17

Usage: $python dparsons.py someInput.txt

Information: Currently, my analyzer supports the following:
program
declaration(s)
statement(s)
id
assignment
print
if + else
return
expr (to the extent that you provided — I have changed factor() to support id, but it is otherwise yet unchanged)

I’ve provided a ‘sanity check’ test file, “test.txt”, that demonstrates what is currently implemented/parsable. It includes all of the above, and should run smoothly.

Known Bugs: N/A. Multiple statements between an “if” and “else” segment will be marked as incorrect, but this follows from the production rule for “if”.