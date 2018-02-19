# CircleHDL
An Analog Hardware Definition Language with a focus in schematic capture

## Why?

I've heard from @ravenexp that a good reason to use LaTeX is that it can 
generate nice looking documents while still being git/version-control friendly.
Word documents are essentially zipped XML files inside that describe the document.

Electrical schematics have exactly the same problem. 
They are basically incompatible with git-style version control.
Much like Word documents, the EDA software renders a circuit diagram, "compiles"
to some weird text file and that's what you have to put on git. By having the
EDA parser/renderer sit between the actual output file and what you edit,
you aren't guaranteed that the deltas generated by your edit is "readable" 
without opening the EDA and inspecting the deltas manually.

For instance, let's say you have 5 resistors in series, and you want to add 
another in the middle of them. You move them apart, add a new one in, and bam,
you "recompile" the circuit diagram in your EDA and the diagram file
might have a ton of deltas, even though the actual change was minimal. 
These deltas would include the resistors' locations being updated for one, and
depending on how the EDA package orders circuit elements inside the circuit file,
your resistors may have different orders, and even have different orders between
other circuit elements, making the deltas basically unreadable.

It's hard to see what actually changed just from the git deltas. The only thing
you can rely on is git comments and actually opening the circuit diagram in EDA
and manually verifying what just changed. That's kind of a pain point. 

Wouldn't it be great if we could create sensible abstractions of schematic 
capture with a human-written code? Analog HDLs have been tried before, but maybe
with enough code to hook it up to existing toolsets, it might at least be 
*usable*. 

Of course, this would mean the circuit diagram abstraction, that literally 
anyone who has business with circuit design knows. This is a major minus, which
is the reason analog HDLs got nowhere. 

This language will probably not be an exception to the above, and I don't expect
this project to go anywhere close to major adoption. But it's cool, and I think
it's cool, I hope you do too, and I hope you like what I make. 

## Long Term Goals

* Transpile to SPICE netlists
* Interoperability with KiCAD

## Timeline

* turn vague ideas into solid example code
* formalize language grammar
* use python and some library to generate a parser
* figure out a way to nicely represent netlists internally
* transpiling to SPICE
