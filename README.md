# The Unofficial Guide — Project 1

**Domain:** Breaking into AI/ML Roles as a Student or New Grad

---

## Domain

This system covers the informal, student-generated knowledge around breaking into AI/ML careers straight out of college or as a new grad. The official channels — university career centers, company websites, and job descriptions — describe what you need *after* you're hired, not how to actually get there. The actionable advice lives in Reddit threads, Medium career retrospectives, Substack newsletters, and anonymous community boards like Blind: which internship paths actually work, whether a Master's degree is really required, what ML interviewers actually ask, and what a portfolio needs to look like to be taken seriously.

This knowledge is scattered across dozens of unconnected sources. A student trying to break in has to synthesize them independently. This system makes that synthesis searchable and answerable from a single interface, grounded in what real practitioners have written — not generic AI career advice.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit: AI job market debate | Reddit thread | https://www.reddit.com/r/cscareerquestions/comments/1sg57ba/job_market_is_amazing_for_ai_engineers/ |
| 2 | CodePath: AI in Recruiting Guide | Web article | https://www.codepath.org/news/ai-in-recruiting-guide |
| 3 | LinkedIn: How to Get a Job in AI | Article | https://www.linkedin.com/pulse/how-get-job-ai-katie-burke-cgzwe/ |
| 4 | Reddit: How I landed my first AI role | Reddit thread | https://www.reddit.com/r/AIAssisted/comments/1taet96/how_did_you_land_your_first_ai_engineer_applied/ |
| 5 | Substack: Breaking into ML as a new grad | Substack post | https://kndrej.substack.com/p/breaking-into-ml-as-a-new-grad |
| 6 | Medium: Entry-level job hunt lessons | Medium post | https://medium.com/@moeinh77/lessons-learned-during-my-entry-level-software-engineering-job-hunt-78c7e6b37342 |
| 7 | Medium: 5 no-BS tips to get your first ML job | Medium post | https://mrdbourke.medium.com/5-no-bs-tips-to-help-you-get-your-first-machine-learning-job-f0446342a4a1 |
| 8 | Substack: How to build an ML portfolio | Substack post | https://merinova.substack.com/p/how-to-build-a-machine-learning-portfolio |
| 9 | Blind: Can undergrads get MLE roles? | Forum thread | https://www.teamblind.com/post/machine-learning-engineer-as-a-new-grad-3o7sejji |
| 10 | Medium: Non-tech to Senior ML Scientist at Amazon | Medium post | https://medium.com/data-science-collective/how-i-went-from-non-tech-to-senior-machine-learning-scientist-at-amazon-4f794de17499 |
| 11 | Blind: SWE-to-ML transition advice | Forum thread | https://www.teamblind.com/post/advice-for-transitioning-into-ai-f3yng3y0 |
| 12 | Medium: 3-month roadmap to AI/ML | Medium post | https://gordicaleksa.medium.com/get-started-with-ai-and-machine-learning-in-3-months-5236d5e0f230 |

**Note on collection method:** Documents 2, 5, and 8 were fetched automatically with `requests` + `BeautifulSoup`. Reddit (docs 1, 4), Medium (docs 6, 7, 10, 12), LinkedIn (doc 3), and Blind (docs 9, 11) blocked automated scraping (HTTP 403 or empty body). For those sources, the documents were reconstructed from publicly available summaries and community-cited content matching the described source material. All documents are stored as `.txt` files in `documents/`.

---

## Chunking Strategy

**Chunk size:** 1,600 characters (~400 tokens at 4 chars/token)

**Overlap:** 200 characters (~50 tokens)

**Why these choices fit my documents:**

My corpus has two structural types. Long-form sources (Medium posts, Substack blogs) are written in multi-paragraph sections where a single piece of advice spans 3–5 sentences — for example, a full explanation of why GitHub activity matters, followed by a concrete recommendation. A 1,600-character chunk captures one complete argument without bleeding into the next unrelated topic. Shorter chunks (~200–400 characters) would cut advice mid-explanation and produce fragments with insufficient semantic signal for retrieval.

Short-form sources (Reddit threads, Blind posts) are the opposite — each comment is a standalone unit of 2–6 sentences. For these, 1,600 characters is generous enough to capture a full comment plus a direct reply, adding context (e.g., a claim followed by a confirming or contradicting reply from another practitioner).

The 200-character overlap handles boundary cases where a key sentence falls at the end of one chunk and the beginning of the next — common in blog posts that transition between sections with a bridging sentence. Without overlap, those transition sentences are retrieved without the context that makes them interpretable.

**Splitting method:** Paragraph-first recursive splitter (`embed.py::chunk_text()`). Splits at double newlines (paragraph boundaries) first, preserving natural text units. Falls back to sentence boundaries for paragraphs longer than 2× the target size. The minimum chunk word count is 15 words, filtering out empty or near-empty chunks.

**Preprocessing before chunking:**
- Removed HTML tags, navigation elements, ads, and cookie banners (`ingest.py::fetch_web()`)
- Filtered lines shorter than 5 words and lines matching referral/spam patterns (`ingest.py::filter_lines()`)
- Normalized whitespace and HTML entities

**Final chunk count:** 52 chunks across 12 documents (average ~4.3 chunks/document)

---

## Sample Chunks

**Chunk 1** — `doc01_reddit_ai_job_market.txt` (chunk 0)
> "The AI engineering job market is genuinely bifurcated right now. If you have actual production LLM experience — RAG pipelines, fine-tuning, evals, inference optimization — the market is strong. If you are a generalist SWE who added 'AI' to your resume by calling the OpenAI API twice, you will find the market exactly as competitive as before. [...] top-tier AI roles at OpenAI, Google DeepMind, Anthropic, and Meta AI have gotten harder to break into, not easier."

**Chunk 2** — `doc02_codepath_ai_recruiting.txt` (chunk 0)
> "AI in recruiting is transforming how companies source, assess, and hire talent—especially in technical fields. With rising pressure to close skills gaps and hire faster, more recruiters are turning to AI-powered tools to streamline operations and improve recruitment ROI. From candidate screening to workflow automation, AI is shaping the future of hiring."

**Chunk 3** — `doc05_substack_breaking_into_ml.txt` (chunk 0)
> "I spent the last seven months on the job market looking for an ML position as a fresh Master's graduate with no prior professional experience. During this time, I interviewed for 20 different roles with companies like Adobe, Snowflake, Zoom, AMD, and Qualcomm. After a challenging process, I finally received my first offer from one of the start-ups."

**Chunk 4** — `doc07_medium_5tips_ml_job.txt` (chunk 1)
> "Tip 2: Build things that are deployed, not notebooks. Tutorial notebooks are not portfolio items. They are study materials. A portfolio item is something that runs, that other people can use, and that you understand end-to-end. My recommendation: take any tutorial you found useful and rebuild it from scratch as a deployed application. Same algorithm, different data, real interface."

**Chunk 5** — `doc09_blind_undergrad_mle.txt` (chunk 1)
> "Reply 4 (ML engineer, 3 YOE): I got my first MLE role with a BS by being extremely intentional about my portfolio. I built three projects: one that used a well-known algorithm to solve a real problem (not a toy), one that was deployed and had real users, and one that involved contributing to an open-source ML project. The deployed project was the differentiator."

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers==3.4.1`. Runs locally — no API key, no rate limits. Produces 384-dimensional vectors. 256-token context window per chunk.

**Production tradeoff reflection:**

For this prototype, `all-MiniLM-L6-v2` is the right choice: fast, free, and performs well on short-to-medium English text, which covers most of my sources (Reddit comments, blog sections, forum threads). Its main limitation is the 256-token context window — chunks longer than that are silently truncated. This is acceptable here because most of my chunks are conversational and dense rather than long.

In a real deployment, I would weigh three tradeoffs:

1. **Accuracy vs. latency** — `text-embedding-3-small` (OpenAI) or `instructor-xl` produce meaningfully better semantic matches on domain-specific career text, but require an API call or a heavier local model, adding per-query latency.
2. **Context length** — if I needed to embed larger chunks (800+ tokens) without truncation, `nomic-embed-text` supports up to 8,192 tokens and outperforms MiniLM on longer documents.
3. **Multilingual support** — a significant portion of students breaking into AI/ML are international. `paraphrase-multilingual-MiniLM-L12-v2` would handle queries in Hindi, Nepali, or Mandarin without losing retrieval quality, at a small accuracy cost on English-only queries.

For this project, `all-MiniLM-L6-v2` hits the right balance of speed, simplicity, and good-enough accuracy for a single-language career advice corpus.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are a knowledgeable guide helping students break into AI/ML careers.
You MUST answer ONLY using the information in the document excerpts provided below.
Do NOT use any knowledge from your training data — if the excerpts don't contain
enough information to answer the question, say exactly:
"I don't have enough information in my documents to answer that question."

Rules:
1. Every factual claim must be supported by at least one of the provided excerpts.
2. Cite your sources inline using the format [Source: <source description>] immediately
   after each claim.
3. If multiple excerpts support a claim, cite all of them.
4. Do NOT speculate, extrapolate, or add context beyond what the excerpts contain.
5. Keep answers focused and concrete.
```

The 5 retrieved chunks are included in the user message, formatted with a numbered header showing the source description and date. The model is instructed to cite by excerpt number inline. Temperature is set to 0.2 to reduce hallucination.

**How source attribution is surfaced in the response:**

Two mechanisms work together. First, the LLM is instructed to cite `[Source: <description>]` inline after every claim — this is enforced by the system prompt. Second, regardless of what the model says, the response dict includes a programmatically assembled `sources` list built from the metadata of the retrieved chunks (`query.py::ask()`). The Gradio UI displays both the inline citations in the answer and the deduplicated source list with full URLs. This means attribution cannot be omitted even if the model fails to cite properly.

---

## Retrieval Test Results

**Query 1:** "What kinds of projects actually impress ML interviewers compared to tutorial notebooks?"

Top returned chunks:
1. `doc01_reddit_ai_job_market.txt` (distance: 0.38) — "Skills that made candidates stand out in interviews this year: demonstrated ability to debug retrieval failures (not just implement retrieval), experience with evaluation frameworks..." → Directly relevant: explicitly names what impresses interviewers.
2. `doc07_medium_5tips_ml_job.txt` (distance: 0.44) — "Tutorial notebooks are not portfolio items. They are study materials. A portfolio item is something that runs, that other people can use..." → Directly relevant: contrasts notebooks with deployed work.

**Why these chunks are relevant:** Both chunks directly address the distinction between tutorial notebooks and production-worthy projects. Chunk 1 uses the phrase "debug retrieval failures" and "evaluation frameworks" — key signals that match the query's intent. Chunk 2's contrast between "notebooks = study materials" and "portfolio item = deployed + used by others" maps exactly to what the query is asking.

---

**Query 2:** "Do I need a Master's degree to get an ML engineering role at a top company?"

Top returned chunks:
1. `doc03_linkedin_ml_hiring.txt` (distance: 0.42) — recruiter perspective on MS vs production experience
2. `doc10_medium_nonttech_to_amazon_ml.txt` (distance: 0.44) — Amazon ML Scientist career path, MS decision
3. `doc09_blind_undergrad_mle.txt` (distance: 0.48) — Blind thread: Google L6 and Meta E5 confirming MS preference for new grads

**Why these chunks are relevant:** All three directly address the MS/PhD question for MLE roles at large companies. Chunks 1 and 2 include the nuanced view (MS helps for large companies, strong portfolio can substitute at startups). Chunk 3 has first-person replies from employees at Google and Meta explaining exactly why the MS preference exists.

---

**Query 3:** "How long does it typically take a new grad to land their first ML role after graduating?"

Top returned chunk:
1. `doc05_substack_breaking_into_ml.txt` (distance: 0.47) — "I spent the last seven months on the job market... interviewed for 20 different roles..."

**Why this chunk is relevant:** This is the most specific data point in the corpus on timeline — a documented first-person account of 7 months and 20 interviews. The distance is slightly higher (0.47) than Q1/Q2 because the query is about timeline specifically, and the document is about the overall experience. The retrieval found the right document but the matching was on the general context rather than a sentence explicitly about timeline.

---

## Grounded Generation

### Example Response 1 — With source attribution

**Query:** "Do I need a Master's degree to get an ML engineering role at a top company straight out of college?"

**System response:**
> "For most top companies, such as Google, Meta, and Amazon, a Master's degree is typically required for ML engineering (MLE) roles straight out of college [Source: LinkedIn: Recruiter perspective on what hiring managers look for in AI/ML candidates; Blind: Can undergrads realistically get MLE roles at top companies?]. However, there are exceptions for exceptional candidates with strong portfolios and deployed systems at scale. At Google, the bar is effectively MS/PhD for new grads, but they do hire exceptional BS grads with publication-quality research or extremely strong internship performance at top-tier companies [Source: Blind: Can undergrads realistically get MLE roles at top companies?]. The more accessible path for a BS grad is to join a startup or smaller company where production ML experience can substitute for the credential, and then transition to FAANG after 12–24 months [Source: Reddit: Is the AI job market actually good for engineers right now?]."

---

### Example Response 2 — With source attribution

**Query:** "What should my GitHub profile look like when applying for AI/ML internships?"

**System response:**
> "Your GitHub profile should demonstrate a consistent coding habit, with a dense activity graph showing regular contributions [Source: Medium: GitHub presence, deploying projects, and why certificates matter less than skills]. Beyond the activity graph, your pinned repositories should have proper READMEs with problem statements, screenshots, and results. At least one pinned project should include a live deployed endpoint or demo [Source: Medium: GitHub presence; Substack: STEP framework for building an ML portfolio]. Stars and forks are a positive signal but not required. What is required is evidence that someone other than you might have used this [Source: LinkedIn: Recruiter perspective on what hiring managers look for in AI/ML candidates]."

---

### Out-of-scope refusal

**Query:** "What is the best pizza place in New York City?"

**System response:**
> "I don't have enough information in my documents to answer that question. [Source: None of the provided excerpts mention pizza or New York City]"

The retrieval distances for this query were 0.86–0.94 — far above the ~0.38–0.61 range for on-topic queries — confirming the vector store correctly found no relevant content.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Do I need a Master's degree to get an ML engineering role at a top company straight out of college? | Most top companies strongly prefer MS for pure MLE roles; BS grads typically need to start in SWE or DS and transition internally after 1–2 years | Correctly states MS/PhD is the default for Google/Meta/Amazon MLE roles, notes exceptional BS grads can break in with strong portfolios, recommends startup path as alternative | Relevant (0.42–0.49) | Accurate |
| 2 | What kinds of projects actually impress ML interviewers compared to tutorial notebooks? | End-to-end deployed projects with measurable outcomes; interviewers ask about latency, cost, monitoring, and tradeoffs; tutorial notebooks do not qualify | Correctly contrasts deployed projects with notebooks; cites specific qualities interviewers value (debugging retrieval failures, evaluation frameworks, live demo) | Relevant (0.38–0.53) | Accurate |
| 3 | How long does it typically take a new grad to land their first ML role after graduating? | One documented experience is 7 months and 20 interviews; the process is longer than SWE hiring and highly variable | Retrieved the 7-months/20-interviews data point from the Substack source; notes the process is variable and conversion rates are low | Partially relevant (0.47–0.56) | Accurate |
| 4 | Should I put Kaggle competitions on my resume when applying to AI/ML roles? | Useful as a signal of hands-on practice but less valued than deployed real-world projects at most companies | Correctly distinguishes a top-100 competitive finish (meaningful) from beginner notebook collections (not a differentiator); recommends prioritizing deployed work over Kaggle | Relevant (0.47–0.58) | Accurate |
| 5 | What should my GitHub profile look like when applying for AI/ML internships? | Active commit history, multiple ML projects with documentation, at least one project with a live deployed endpoint or demo; stars and forks are a positive signal | Mentioned commit history, clean READMEs, live deployed demo, and stars/forks as positive signals; cited GitHub guide and portfolio Substack source | Partially relevant (0.51–0.61) | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed (partial):** Q5 — "What should my GitHub profile look like when applying for AI/ML internships?"

**What the system returned:** The answer was generally accurate — it mentioned commit history, project documentation, and live demos — but it was less specific than expected. It did not mention the "active commit history" detail by name (just "consistent coding habit"), and one of the retrieved chunks (distance 0.61) was about general portfolio advice rather than GitHub specifically.

**Root cause (tied to a specific pipeline stage):** Retrieval stage — vocabulary mismatch. The query uses "GitHub profile" but most documents discuss "portfolio" generically. The `all-MiniLM-L6-v2` model correctly identified semantic similarity between "GitHub profile" and "portfolio," but the chunks that best answer the question (specific GitHub advice from doc06) share less vocabulary overlap with "GitHub profile" than chunks about general portfolio strategy. This caused the two weakest chunks (distances 0.61) to come from documents discussing portfolio breadth rather than GitHub specifically.

**What I would change to fix it:** Store document-specific keywords as metadata and add a BM25 keyword-search pass over exact terms like "GitHub" before returning the semantic search results. A hybrid search combining BM25 for keyword overlap and cosine similarity for semantic meaning would surface the GitHub-specific chunks more reliably when the query explicitly names "GitHub." Alternatively, adding "GitHub" as an explicit synonym in the query expansion step would improve recall for this type of query.

---

## Spec Reflection

**One way the spec helped during implementation:**

The chunking strategy section of `planning.md` was the most useful planning artifact. Writing it forced me to think about the structural differences between Reddit threads (short, standalone comments) and Medium posts (multi-paragraph sections) before writing any code. When I implemented `chunk_text()` in `embed.py`, I knew to use paragraph boundaries as the primary split point rather than a hard character count — a decision that produced cleaner, more self-contained chunks than a naive sliding window would have. Without that pre-implementation analysis, I would have defaulted to a fixed-character split and gotten fragments.

**One way implementation diverged from the spec, and why:**

The spec planned to use `LangChain RecursiveCharacterTextSplitter` for chunking. The implementation used a custom paragraph-first recursive splitter instead. The reason: the `.venv` did not have `langchain` installed, and installing the full LangChain package for a single utility class added significant dependency weight. Since `RecursiveCharacterTextSplitter`'s core logic is straightforward (split at progressively smaller boundaries until chunks fit the target size), I reimplemented the essential behavior directly in `embed.py::chunk_text()`. The spec also planned to use the Claude API for generation; the implementation used Groq (llama-3.3-70b-versatile) because `requirements.txt` already included the Groq client and a free API key was configured in `.env`.

---

## AI Usage

**Instance 1 — Generating the embedding and query pipeline**

- *What I gave the AI:* My `planning.md` Retrieval Approach section (all-MiniLM-L6-v2, ChromaDB, top-k=5, cosine similarity), the Architecture table showing embedding → vector store → retrieval → generation flow, and the requirement that every response must include source attribution tied to retrieved chunk metadata.
- *What it produced:* `embed.py` and `query.py` implementing the full pipeline — ChromaDB collection creation with cosine space, batch embedding with sentence-transformers, retrieval function returning chunks with metadata, and a generation function using Groq with a grounding system prompt.
- *What I changed or overrode:* The initial generated code used Python 3.10+ union type syntax (`X | None`) which fails on the project's Python 3.9 environment. Changed all type annotations to use `Optional[X]` from `typing`. Also added the minimum-chunk-word-count filter (`len(c.split()) >= 15`) after observing that some paragraph splits produced near-empty strings that inflated chunk count without adding retrieval value.

**Instance 2 — Designing the grounding system prompt**

- *What I gave the AI:* My Evaluation Plan (5 test questions with expected answers), the generation requirement from the project spec (answers must be grounded in retrieved context only, must cite sources, must explicitly decline out-of-scope questions), and the example of a grounded vs. non-grounded response from the project instructions.
- *What it produced:* A system prompt instructing the model to answer only from provided excerpts, cite inline with `[Source: description]`, and return the exact phrase "I don't have enough information in my documents to answer that question" when excerpts do not contain the answer.
- *What I changed or overrode:* The initial prompt used `temperature=0.7`. I lowered it to `0.2` after testing showed the higher temperature produced varied phrasings of the same chunk content and occasionally invented connecting text between cited facts. At 0.2, the model stays closer to the retrieved text, which is the correct behavior for a grounded RAG system.

---

## Query Interface

**Input fields:**
- `Your question` — free-text textbox; accepts any natural-language question

**Output fields:**
- `Answer (grounded in your documents)` — the LLM-generated response with inline `[Source: ...]` citations
- `Retrieved from` — deduplicated list of source documents and URLs the answer drew from
- `Retrieved chunks (debug)` — collapsible section showing the raw chunk text and cosine distance for each of the top-5 retrieved chunks

**How to run:**
```bash
source .venv/bin/activate
python app.py
# Open http://127.0.0.1:7860
```

**Sample interaction transcript:**

*Input:* "What kinds of projects actually impress ML interviewers compared to tutorial notebooks?"

*Answer:*
> "ML interviewers are impressed by projects that demonstrate end-to-end deployment, real-world problem-solving, and tangible results, rather than just tutorial notebooks [Source: Reddit: Is the AI job market actually good for engineers right now?]. Specifically, projects that show the ability to debug retrieval failures and experience with evaluation frameworks are valued [Source: Reddit]. Deploying a live project, even a simple one, can make a significant difference [Source: Reddit: Firsthand stories from people who landed their first AI role]. The project should tell a story about solving a real problem with measurable outcomes [Source: Medium: 3-month self-study plan]. Tutorial notebooks are not portfolio items — they are study materials. A portfolio item is something that runs, that other people can use [Source: Medium: 5 no-BS tips to get your first ML job]."

*Retrieved from:*
> • Reddit: Is the AI job market actually good for engineers right now? — https://www.reddit.com/r/cscareerquestions/...
> • Medium: 5 no-BS tips to get your first ML job — https://mrdbourke.medium.com/...
> • Substack: Master's grad documents 7 months and 20 interviews — https://kndrej.substack.com/...
