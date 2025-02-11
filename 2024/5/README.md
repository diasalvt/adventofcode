# Day 5

Here the ""tricky"" part is to understand that the requirement list is complete.
If we are given a list $[a_1, ..., a_n]$ all the rules of the form $a_i | a_j$ for $i < j$ are given.
E.g. if the list is [12, 10, 15] then we have for rules "12 | 10, 12 | 15, 10 | 15".
But we could have less rules and still be able to sort correctly: "12 | 10, 10 | 15".
This is due to transitivity. But this problem is simpler if you spot this (or may be it is in the story).
