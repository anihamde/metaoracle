# metaoracle

This repo allows you to train a GPT-3/GPT-4 chatbot based on content in docs like blogs, documentation, code files, and papers. Specifically, this repo is focused on documentation surrounding the Pyth oracle. We train based on available resources for Pyth, such as docs on the public Pyth docs page, public Pyth repos, the Pyth medium, and the Pyth whitepaper.

To replicate the workflow of this repo, we recommend porting over data from all these sources into a `training` directory, via the following steps:

1. Run `python3 scraper.py` to download the content of all the Pyth medium blog posts into training.
2. `mkdir training` --> `cd training` --> clone relevant public Pyth repos

If you then want to use the Python langchain-based scripts:

1. `cp constants_TEMPLATE.py constants.py` and fill out `constants.py` after registering for a username with ActiveLoop.
2. Run `python3 code_indexer.py`. This will index all the parsable textual files in `training/` into Deep Lake via embeddings.
3. Run `python3 oracle_of_oracle.py` to begin the chatbot conversation.

Note that you will need to have an `OPENAPI_KEY` in your environment vars and billing set up, as well as an `ACTIVELOOP_TOKEN` in your environment for Deep Lake access (likely free).

## Leverages LangChain.js LLM Template

To use the Javascript LangChain LLM template[https://github.com/Conner1115/LangChain.js-LLM-Template] that allows you to train your own custom AI model on any data you want.

## Setup
1. Provide all the information you want your LLM to be trained on in the `training` directory in markdown files.  Folder depth doesn't matter.
2. Add your OpenAI API key in environment vars via the key `OPENAI_API_KEY`.
3. Run `yarn train` or `npm train` to set up your vector store.
4. Modify the base prompt in `lib/basePrompt.js`
5. Run index.js, and start playing around with it!
