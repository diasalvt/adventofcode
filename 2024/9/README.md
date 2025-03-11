# Day 9

Part 2 took more time. I had this idea to buid an "algebra" of memories. A way to combine (merge two consecutives memories) 
pop elements, insert left most, etc...
So the algo was to pop a file in the reversed order (starting at the end), try to insert in the memory growing from the right.
Problem is that all these operations where nice isolated but taking way too long together.

# Idea
Then I thought about optimizing by having a structure for free spaces, indexed by size and referrencing a sorting list of positions.
But come on, it is only day 9. So I went back with the example and even decided to manipulate a string. I was interested if this could do the trick.
You can not really move the file ids directly (e.g. file id '14' is taking more than one character).
In the end I could be manipulating the list directly there was no trick with the string. The string is just used to get the leftmost match of free space (search from left to right in the sorted list).
Also moving the block is done by creating a new string while we could be updating in a similar fashion the list.
