
I was wanting to experiment with OCR and seeing how well AI could generate code based on the prompts. 

After 2-3 itterations and going back and forth with Google AI Studio, I feel it did pretty well (based on my inputs).

I chose EasyOCR as it ran locally which doesn't require sending any info back out to the internet. 
However, the program has some limitations with the base model. In as such the program matches about 95% of the time.

Some of this I blame on the font DuoLingo uses, EasyOCR misses a lot of phrases that begin with "I", like "I want" will
return as just "want".
In other cases it sometimes splits phrases into two groups instead of returing just the one. 
"Trop de" returns as "trop" and "de".
There are also cases where the OCR does not include the puncuation. "C'est" may return as "Cest"

I hope at some point I will either figure out better settings to pass through to EasyOCR or to train the base model with 
images taken from the game. Though EasyOCR doesn't seem to be under any active development.

