# Project 1 Planning: The Unofficial Guide

## Domain
Breaking into AI/ML Roles as a Student or New Grad
AI/ML is one of the most sought-after career paths for CS students, yet the requirements are inconsistently defined across companies — some want research experience, some want projects, some want Kaggle rankings, and some just want strong Python and system design skills. There is no official roadmap, and university career centers rarely have domain-specific guidance for AI roles.

The most actionable advice lives in scattered, informal places — Reddit threads, personal blogs, Discord servers, and Glassdoor interview reviews — not on any university or company website. Official job postings describe what companies want after hiring, not how to actually get there. A student trying to break in has to synthesize dozens of sources just to understand what a competitive profile looks like, which internships are realistic targets, and how to prepare for ML-specific interviews.


## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->
| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit thread | Community debate on whether the AI job market is actually good for engineers right now | https://www.reddit.com/r/cscareerquestions/comments/1sg57ba/job_market_is_amazing_for_ai_engineers/ |
| 2 | CodePath guide | How AI is changing recruiting and what students can do to stand out in AI-screened hiring pipelines | https://www.codepath.org/news/ai-in-recruiting-guide |
| 3 | LinkedIn article | Recruiter perspective on what hiring managers actually look for in AI/ML candidates | https://www.linkedin.com/pulse/how-get-job-ai-katie-burke-cgzwe/ |
| 4 | Reddit thread | Firsthand stories from people who landed their first AI engineer or applied scientist role | https://www.reddit.com/r/AIAssisted/comments/1taet96/how_did_you_land_your_first_ai_engineer_applied/ |
| 5 | Substack blog | Master's grad documents 7 months and 20 interviews — what actually works breaking into ML as a new grad | https://kndrej.substack.com/p/breaking-into-ml-as-a-new-grad |
| 6 | Medium post | Practical tips on GitHub presence, deploying projects, and why certificates matter less than skills | https://medium.com/@moeinh77/lessons-learned-during-my-entry-level-software-engineering-job-hunt-78c7e6b37342 |
| 7 | Medium post | 5 no-BS tips to get your first ML job — widely cited advice on learning in public and building real projects | https://mrdbourke.medium.com/5-no-bs-tips-to-help-you-get-your-first-machine-learning-job-f0446342a4a1 |
| 8 | Substack guide | Community-sourced STEP framework for building an ML portfolio that stands out to recruiters | https://merinova.substack.com/p/how-to-build-a-machine-learning-portfolio |
| 9 | Blind thread | Candid community debate on whether undergrads can realistically get MLE roles at top companies | https://www.teamblind.com/post/machine-learning-engineer-as-a-new-grad-3o7sejji |
| 10 | Medium post | Career breakdown from non-tech background to Senior ML Scientist at Amazon, internship by internship | https://medium.com/data-science-collective/how-i-went-from-non-tech-to-senior-machine-learning-scientist-at-amazon-4f794de17499 |
| 11 | Blind thread | SWE new grad trying to transition into ML — honest peer advice on what moves actually work | https://www.teamblind.com/post/advice-for-transitioning-into-ai-f3yng3y0 |
| 12 | Medium roadmap | 3-month self-study plan from one engineer who went from SWE to DeepMind Research Engineer | https://gordicaleksa.medium.com/get-started-with-ai-and-machine-learning-in-3-months-5236d5e0f230 |
---

## Chunking Strategy

**Chunk size:**
400 tokens
**Overlap:**
50 tokens

**Reasoning:**

My source documents fall into two structural categories that informed these numbers. Long-form sources (Medium posts, Substack blogs) are written in multi-paragraph sections where a single piece of advice spans 3–5 sentences. A 400-token chunk captures one complete thought or argument — for example, a full explanation of why GitHub activity matters — without bleeding into the next unrelated topic. Chunks smaller than ~300 tokens risk cutting advice mid-explanation, which would make retrieval return incomplete answers.

Short-form sources (Reddit threads, Blind posts) are the opposite — each comment is its own standalone unit, often just 2–4 sentences. For these, 400 tokens is generous enough to capture a full comment plus a direct reply, which adds useful context (e.g. a claim followed by a pushback or confirmation from another person).

The 50-token overlap handles boundary cases where a key sentence falls at the end of one chunk and the beginning of the next — common in blog posts that transition between sections with a summary sentence. Without overlap, those transition sentences would be lost from one chunk entirely and retrieved without context
in the other.

## Retrieval Approach
**Embedding model:**
sentence-transformers==3.4.1
**Top-k:**
5

**Production tradeoff reflection:**
For this prototype, all-MiniLM-L6-v2 is the right choice — it is fast, runs
locally for free, and performs well on short to medium-length English text,
which matches most of my sources (Reddit comments, blog sections, Blind threads).
Its main limitation is a 256-token context window, meaning chunks longer than
that get silently truncated during embedding. This is acceptable here since most
of my chunks are conversational and dense rather than long.

In a real deployment with no cost constraint, I would weigh three tradeoffs:

1. Accuracy vs latency — text-embedding-3-small (OpenAI) or instructor-xl produce
   meaningfully better semantic matches on domain-specific career text, but require
   an API call or a heavier local model, adding latency per query.

2. Context length — if I wanted to embed larger chunks (800+ tokens) without
   truncation, nomic-embed-text supports up to 8192 tokens and outperforms
   MiniLM on longer documents.

3. Multilingual support — a significant portion of students breaking into AI/ML
   are international. paraphrase-multilingual-MiniLM-L12-v2 would handle queries
   in Hindi, Nepali, or Mandarin without losing retrieval quality, at a small
   accuracy cost on English-only queries.

For this project, all-MiniLM-L6-v2 hits the right balance of speed, simplicity,
and good-enough accuracy for a single-language career advice corpus.


## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Do I need a Master's degree to get an ML engineering role at a top company straight out of college? | Most top companies strongly prefer MS for pure MLE roles; BS grads typically need to start in SWE or DS and transition internally after 1–2 years |
| 2 | What kinds of projects actually impress ML interviewers compared to tutorial notebooks? | End-to-end deployed projects with measurable outcomes — interviewers ask about latency, cost, monitoring, and tradeoffs; tutorial notebooks and Colab demos do not qualify |
| 3 | How long does it typically take a new grad to land their first ML role after graduating? | One documented experience is 7 months and 20 interviews before a first offer; the process is longer than SWE hiring and highly variable |
| 4 | Should I put Kaggle competitions on my resume when applying to AI/ML roles? | Useful as a signal of hands-on practice but less valued than deployed real-world projects at most companies; helpful for early-career candidates with no internship experience |
| 5 | What should my GitHub profile look like when applying for AI/ML internships? | Active commit history, multiple ML projects with documentation, at least one project with a live deployed endpoint or demo — stars and forks are a positive signal to recruiters |

## Anticipated Challenges

1. **Noisy community threads producing low-quality chunks:** Reddit and Blind threads
   mix genuinely useful advice with off-topic replies, jokes, one-word responses,
   and recruiting spam (e.g. "DM me for a referral"). If these are chunked as-is,
   the vector store will contain noise that competes with real advice during retrieval
   — a query like "how do I build an ML portfolio" could return a chunk that is just
   "DM for Google" with no useful content. Mitigation: pre-process all thread sources
   before chunking by filtering out comments under 30 words and removing lines that
   are purely referral solicitations or usernames.

2. **Outdated advice being retrieved with false confidence:** Several sources are from
   2022–2023, and the AI job market has shifted significantly since then — hiring
   freezes, the rise of LLM-specific roles, and changing expectations around projects
   have all changed what a competitive profile looks like. The system has no built-in
   way to signal that a retrieved chunk may be stale, so it could confidently return
   advice that no longer reflects current hiring. Mitigation: store publication date
   as chunk metadata and include it in the prompt context so the generation step can
   flag older advice to the user.

3. **Key advice split across chunk boundaries:** Long-form blog posts often structure
   advice as a setup sentence followed by a concrete example in the next paragraph —
   for instance, "here is what interviewers actually ask" followed by a bullet list
   in the next section. A hard chunk boundary between these two parts would cause the
   system to retrieve either the claim without the evidence or the evidence without
   the context. Mitigation: the 50-token overlap helps, but for sources with clear
   section headers, chunking by logical section rather than fixed token count will
   produce cleaner boundaries.
## Architecture

```
Document Ingestion
┌─────────────────────────────────────┐
│  Sources: Reddit, Medium, Substack, │
│           Blind, LinkedIn           │
│  Tool:    requests + BeautifulSoup  │
│  Output:  clean .txt files          │
└──────────────────┬──────────────────┘
                   │
                   ▼
Chunking
┌─────────────────────────────────────┐
│  Tool:    LangChain                 │
│           RecursiveCharacterText    │
│           Splitter                  │
│  Size:    400 tokens                │
│  Overlap: 50 tokens                 │
│  Output:  list of text chunks       │
└──────────────────┬──────────────────┘
                   │
                   ▼
Embedding
┌─────────────────────────────────────┐
│  Model:   all-MiniLM-L6-v2          │
│  Library: sentence-transformers     │
│  Output:  384-dimensional vectors   │
└──────────────────┬──────────────────┘
                   │
                   ▼
Vector Store
┌─────────────────────────────────────┐
│  Tool:    ChromaDB (local)          │
│  Stores:  chunk text + metadata     │
│           (source URL, date)        │
│  Output:  persistent collection     │
└──────────────────┬──────────────────┘
                   │
                   ▼
Retrieval
┌─────────────────────────────────────┐
│  Method:  cosine similarity         │
│  Top-k:   5 chunks                  │
│  Input:   user query                │
│  Output:  5 relevant chunks         │
└──────────────────┬──────────────────┘
                   │
                   ▼
Generation
┌─────────────────────────────────────┐
│  Model:   Claude API (claude-haiku) │
│  Input:   user query + 5 chunks     │
│  Output:  grounded answer with      │
│           source attribution        │
└─────────────────────────────────────┘
```

**Stage summary:**

| Stage | Tool / Library | Input | Output |
|---|---|---|---|
| Document Ingestion | requests, BeautifulSoup | Source URLs | Clean .txt files |
| Chunking | LangChain RecursiveCharacterTextSplitter | .txt files | Text chunks |
| Embedding | sentence-transformers all-MiniLM-L6-v2 | Text chunks | 384-dim vectors |
| Vector Store | ChromaDB | Vectors + metadata | Persistent local collection |
| Retrieval | ChromaDB cosine similarity | User query | Top-5 matching chunks |
| Generation | Claude API (claude-haiku-3) | Query + chunks | Grounded answer |

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**
Tool: Claude
Input: I will paste my Sources table (all 12 URLs), my Chunking Strategy section
(400 tokens, 50 overlap, RecursiveCharacterTextSplitter), and the Anticipated
Challenges section (noise filtering for Reddit/Blind threads).
Expected output: A working ingest.py that fetches each URL using requests and
BeautifulSoup, strips noise (comments under 30 words, referral spam lines),
saves clean text to a /data folder as .txt files, and a chunk.py that implements
chunk_text() using LangChain RecursiveCharacterTextSplitter with my specified
chunk size and overlap.
Verification: I will manually open 2–3 output .txt files and confirm noise is
stripped, then print the first 5 chunks from a Medium post and a Reddit thread
to confirm chunk boundaries look clean and no chunk is under 50 tokens.

**Milestone 4 — Embedding and retrieval:**
Tool: Claude
Input: I will paste my Retrieval Approach section (all-MiniLM-L6-v2,
sentence-transformers==3.4.1, ChromaDB, top-k=5) and my Architecture stage
summary table (Embedding and Vector Store rows).
Expected output: An embed.py that loads chunks from Milestone 3, generates
384-dimensional vectors using all-MiniLM-L6-v2, and stores them in a local
ChromaDB collection with metadata fields (source URL, publication date). A
retrieve.py that accepts a plain-English query string, embeds it using the
same model, and returns the top-5 matching chunks with their source metadata.
Verification: I will run 3 of my 5 evaluation questions through retrieve.py
and manually confirm the returned chunks are topically relevant and include
correct source URLs in their metadata.

**Milestone 5 — Generation and interface:**
Tool: Claude
Input: I will paste my Evaluation Plan (all 5 questions and expected answers),
my Architecture Generation row (Claude API claude-haiku-3, query + 5 chunks,
grounded answer with source attribution), and the requirement that responses
must cite which source each claim came from.
Expected output: A generate.py that takes a user query, calls retrieve.py to
get top-5 chunks, constructs a prompt that includes the query and chunks as
context, calls the Claude API, and returns an answer with inline source
citations. A simple CLI interface where a user can type a question and receive
a grounded answer.
Verification: I will run all 5 evaluation questions and compare system output
against my expected answers table. A response is correct if it contains the
right core claim and cites at least one relevant source. I will also test one
out-of-domain question (e.g. "what is the best pizza in NYC") to confirm the
system responds with "I don't have enough information" rather than hallucinating.

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
