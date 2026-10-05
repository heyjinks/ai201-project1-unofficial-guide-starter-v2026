# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

This is a RAG-based system using the city_guides corpus to answer questions about specific destinations, including transportation, food, attractions, and practical travel advice. It retrieves the most relevant section of a city guide based on the user's question and uses that information to generate a grounded answer. If the retrieved information is not relevant enough, the system refuses to answer rather than making up information. Each generated answer also identifies the source documents used.

## Chunking Strategy

**Chunk size:** Delimited by ## per chunk 
**Overlap:** None

I chose section-based chunking instead of a fixed character size because the city_guides documents are already organized into clearly labeled sections such as ## Getting there, ## Eat and drink, and ## Practical notes. In the starter version, the 800-character chunker sometimes split directly through these sections and even cut words in half, while other chunks contained several unrelated sections together.

Using each ## section as one chunk keeps the content grouped by topic and gives each chunk enough context to stand on its own. I did not use overlap because the section headings already create natural boundaries, and repeating text from neighboring sections would mix separate topics unnecessarily.

<!-- What about YOUR documents made you pick these numbers? Short posts    and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

======================================================================
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
======================================================================
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

======================================================================
Chunk 2  |  source: guide_corry_vale.md#6  |  produced by: chunker.py::split_documents
======================================================================
## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.

======================================================================
Chunk 3  |  source: guide_givens_mill.md#3  |  produced by: chunker.py::split_documents
======================================================================
## Eat and drink

A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.

======================================================================
Chunk 4  |  source: guide_kestrelford.md#6  |  produced by: chunker.py::split_documents
======================================================================
## When to go

Late spring and early autumn. The Saturday market runs year-round but is much reduced from November to February. August is busy with walkers. The single-track approach road is genuinely difficult in snow and the town can be cut off for a day or two most winters.

======================================================================
Chunk 5  |  source: guide_regional_transport.md#1  |  produced by: chunker.py::split_documents
======================================================================
## The railway

The line runs along the river valley, connecting Brightwater to the regional
hub in 50 minutes. Eleven services a day on weekdays, six on Sundays. The line
north of Brightwater closed in 1963 and everything beyond it is bus or car.

Tickets are cheaper booked the day before than on the day, and considerably
cheaper than that booked a week ahead. There is no ticket office at
Brightwater station outside weekday mornings; the machine on the platform takes
cards only.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** "When is it recommended to go to Pellew Sands for a less crowded beach?"

**Answer:** June and September are recommended to visit Pellew Sands for the beach without the crowds (guide_pellew_sands.md).

```
python app.py ask "When is it recommended to go to Pellew Sands for a less crowded beach?" --show-prompt
  (best distance 0.389, cutoff 0.55)

June and September are recommended to visit Pellew Sands for the beach without the crowds (guide_pellew_sands.md).

Sources retrieved: guide_accessibility.md, guide_elder_ness.md, guide_halden_bay.md, guide_pellew_sands.md

```

**My relevance cutoff:** .55

The five questions I asked had a distance range of 0.231 - 0.486. The out-of-scope questions I asked ranged from 0.754 - 0.899. I chose .55 because this gives leeway to questions where relevancy may not be as strong based on the answer that had a distance of 0.486.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude to write my chunking function based on my criterion on section delimiting and my notes. It was particularly useful in generating the regex for my function. 

**2.** I asked ChatGPT to explain how to choose a usefulgit remote -v relevance cutoff for retrieval. It explained that I should compare the best distances from questions covered by my corpus with the distances from out-of-scope questions and place the cutoff between the two groups. Rather than using the example cutoff it suggested, I tested my own questions and used the distances produced by my retrieval system to determine the cutoff for my project.

**3.** I used ChatGPT to help me identify where I could improve the RAG system based on the failed 5th criterion. 

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | MET
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | MET
| 4. Chunks should be delimited by the section header noted by the ##. 5 of 5 | 5/5 | 5/5 | 5/5| met 
| 5. A location should be named in the answer. 4 of 5 | 4/5 | 4/5 | 4/5 | MET   

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->
## 1. Retrieved chunks contain the answer
app.py::cmd_retrieve

### When is it recommended to go to Pellew Sands for a less crowded beach? — run 3

- Best distance: 0.3920 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_elder_ness.md, guide_pellew_sands.md

```
It is recommended to go in June and September to enjoy the beach without the crowds (guide_pellew_sands.md).
```


## 2. Every answer names a source
generate.py::answer_from_chunks
### What ways can one get to Brightwater? — run 1

- Best distance: 0.3944 (passed the gate)
- Sources retrieved: guide_marchwood.md, guide_pellew_sands.md, guide_regional_transport.md, guide_walking.md

```
Based on the provided documents, one can get to Brightwater by train from the regional hub (which takes 50 minutes, per `guide_regional_transport.md`) or from Marchwood (trains run every 40 minutes until 11pm, per `guide_marchwood.md`). Additionally, one can drive from Pellew Sands (taking 50 minutes, per `guide_pellew_sands.md`).
```
## 3. The relevance gate stops out-of-corpus questions
run_eval.py::check_out_of_scope
| What is the recommended dosage of ibuprofen for a headache? | 0.846 | refused |

## 4. Something about your chunks
chunker.py::split_documents
======================================================================
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
======================================================================
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

## 5. A location should be named in the answer. 
generate.py::answer_from_chunks

- Best distance: 0.2306 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_brightwater.md, guide_givens_mill.md

```
Givens Mill is known as a village of 700 people built around a working watermill that still grinds flour commercially. Additionally, most people visit for the tearoom attached to the mill, which sells bread made from the flour ground nearby. (Source: `guide_givens_mill.md`)
```


## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer  | MET | The criteria was met for all runs and questions, the retrieved chunks contained the answer
| 2 | Every answer names a source | MET | Every single answer contained a source for all runs and questions|
| 3 | The relevance gate stops out-of-corpus questions | MET | Every out-of-corpus question was refused |
| 4 | Chunks should be delimited by the section header noted by the ##. | MET | The chunks are all correctly delimited |
| 5 | A location should be named in the answer.  | MET  | A location relevant is named in 4/5 of the questions' runs |

## Diagnoses
The only miss was on Criterion 5, which required the answer to explicitly name a location. The question asked, “When is it recommended to go to Pellew Sands for a less crowded beach?” The retrieved chunk was correct and contained the answer, but the generated response said “the beach” instead of repeating “Pellew Sands.” This was therefore a generation-stage issue: the model understood the location from the question and treated it as already established, so it used a pronoun-like reference instead of explicitly naming the place.



<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement


**What I changed:** I tightened the grounding instruction in generate.py to require the answer to explicitly name the relevant location rather than referring to it indirectly with phrases such as “the beach,” “there,” or “the area.” I also tightened the wording of the criterion itself.

**Why I picked it:** I chose this change because retrieval was already working correctly and the relevant Pellew Sands chunk was being returned. The failure happened only in how the model phrased the final answer. Requiring the location name in the generated response directly addresses Criterion 5 without changing chunking or retrieval behavior that was already performing well.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | MET
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | MET
| 4. Chunks should be delimited by the section header noted by the ##. 5 of 5 | 5/5 | 5/5 | 5/5| met 
| 5. Explicitly name the location the question is asking about. 5 of 5 | 5/5 | 5/5 | 5/5 | MET  

**Did it help?**

Yes. After tightening the grounding instruction to require the model to explicitly name the relevant location, Criterion 5 improved because the generated answers named the location instead of referring to it indirectly as “the beach” or “there.” I know the change helped because the after evaluation showed the location-naming criterion passing consistently across the test questions.

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->



## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

     It did not miss afterwards. 

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

     I would have tightened the wording to be more strict and specific, as "a location should be named" is vague. A different location irrelevant to the answer could be named and this would have still passed the criterion.
