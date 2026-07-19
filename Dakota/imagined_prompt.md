# The Grammar That Trains the Machine: A Dakota Star Map

The imagined verbose prompt, in the native Math-To-Manim style: a single
continuous narrative specification, LaTeX-rich, that a coder (human or
model) can implement directly as a Manim scene. Source material: the
grammar of the Dakota language as documented in Stephen Return Riggs,
"Dakota Grammar, Texts, and Ethnography" (1893, field work to 1890),
treated with respect as the living language of the Dakota people.

## The prompt

Open on darkness. A single star ignites at center: label it with the
Dakota word "wichaHpi" (star). Around it, fade in a title: "The Grammar
That Trains the Machine" and a subtitle: "a Dakota star map, 1890". Hold,
then let the title dissolve upward like smoke.

Act I - The Constellation of Rules. Eighteen stars ignite one by one in
a spiral galaxy layout, each star one grammar rule of the Dakota
language, color-coded by type: morphology stars in ice blue, syntax
stars in prairie gold, phonology stars in ember red. As each star lands,
its rule name flashes briefly: "-pi plural", "wa- absolutive", "ki-
dative", "SOV order", "reduplication", "ablaut a/e", "uNk- we",
"postpositions". Draw rivers of faint light between every pair of stars
that share a morpheme: the sky becomes a connected constellation - a
grammar is not a list, it is a graph. Caption at the bottom: "18 rules,
one language: every star constrains its neighbors."

Act II - Three Stars, Up Close. Fly into three stars in sequence.

First star, morphology: the plural enclitic -pi. Show the word
"wiNyaN" (woman) at center. The morpheme "-pi" orbits in from off
screen and docks onto the word, which becomes "wiNyaNpi" (women); below,
the sentence "WiNyaN mani" (the woman walks) transforms into "WiNyaN
manipi" (the women walk), with the moving piece highlighted in gold.
State the rule as an equation of composition:
plural(x) = x + "-pi" for animate x.

Second star, phonology: reduplication. The color word "sapa" (black)
splits like a cell: its first syllable copies itself and the word
reassembles as "sapsapa" (black, here and there - the distributive).
Visualize the copy operation as a mirror: red(x) = sigma_1(x) + x where
sigma_1 extracts the first syllable. Three dots of black ink scatter
across the screen as the word doubles - one blackness becomes many.

Third star, syntax: SOV order. Lay out the sentence
"Wichashta shuNka waNyaNke" word by word: wichashta (man), shuNka
(dog), waNyaNke (sees). Draw a gold arrow from man to sees labeled
"agent", an ice-blue arrow from dog to sees labeled "patient": the verb
stands last, the sentence flows into it like two rivers into a lake.
Contrast flashes briefly: English SVO order rearranges the same three
glosses.

Act III - The Gradient. Pull back to the full constellation. Now the
frame of the original prompt: this ruleset is a training signal. Fade in
the objective over the sky:

    J(theta) = E_{x ~ D_1890} [ sum_r w_r log p_theta(r satisfied | x) ]

and its gradient ascent step:

    theta_{t+1} = theta_t + eta * grad_theta J(theta_t)

A bright particle (the model) drifts through the constellation, and
every star tugs it: render the tugs as thin gradient arrows from the
particle toward each star, strongest toward the stars it violates most.
The particle's path curves - a learning trajectory bending under
grammatical gravity - until it settles into an orbit that threads all
eighteen stars. Caption: "every rule is a gradient; the grammar pulls
the model toward the language."

Coda. All stars flare once, together, then dim to a quiet night sky.
End card, small and unadorned: "Dakhota iapi - the Dakota language.
Documented 1890. Still spoken. Still teaching." Hold three seconds.
Fade to black.

Style notes: deep-space background (#0b0e1a), no gridlines; text in a
serif-feel weight; Dakota words always larger than their English
glosses; motion language of slow drifts and gentle lags, never snappy;
every equation enters by Write, never FadeIn; total duration 70-90
seconds at 1080p30.
