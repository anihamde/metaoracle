# metaoracle

This repo allows you to train a GPT-3/GPT-4 chatbot based on content in docs like blogs, documentation, code files, and papers. Specifically, this repo is focused on documentation surrounding the Pyth oracle. We train based on available resources for Pyth, such as docs on the public Pyth docs page, public Pyth repos, the Pyth medium, and the Pyth whitepaper.

To replicate the workflow of this repo, we recommend porting over data from all these sources into a `training` directory, via the following steps:

1. Run `python3 scraper.py` to download the content of all the Pyth medium blog posts into training.
2. `cd training` --> clone relevant public Pyth repos

If you then want to use the Python langchain-based scripts:

1. `cp constants_TEMPLATE.py constants.py` and fill out `constants.py` after registering for a username with ActiveLoop.
2. Run `python3 code_indexer.py`. This will index all the parsable textual files in `training/` into Deep Lake via embeddings.
3. Run `python3 oracle_of_oracle.py` to begin the chatbot conversation.

Note that you will need to have an `OPENAPI_KEY` in your environment vars and billing set up, as well as an `ACTIVELOOP_TOKEN` in your environment for Deep Lake access (likely free).

## Example Conversation
> -> **Question**: Who are you? And what is Pyth? 
>**Answer**: I am Pythia, the divine manifestation of the Pyth oracle network in the form of a Greek goddess. Pyth is an oracle network for decentralized finance that brings important data onto different blockchains, including price feeds of different assets in crypto, equities, FX, and commodities. 
>
> -> **Question**: Please share Javascript code showing how to pull the price on chain 
> **Answer**: Sure, here is an example of Solidity code that uses the Pyth Solidity SDK to read a Pyth price on-chain, and an example of JavaScript code that uses the Pyth EVM JS library to fetch Pyth prices off-chain:
> 
> Solidity code:
> 
> ```solidity
> // SPDX-License-Identifier: Apache-2.0
> pragma solidity >=0.6.0 <0.9.0;
> 
> import "@pythnetwork/pyth-sdk-solidity/IPyth.sol";
> import "@pythnetwork/pyth-sdk-solidity/PythStructs.sol";
> 
> contract ExampleContract {
>   IPyth pyth;
> 
>   constructor(address pythContract) {
>     pyth = IPyth(pythContract);
>   }
> 
>   function getBtcUsdPrice(
>     bytes32 priceID
>   ) public view returns (PythStructs.Price memory) {
>     // Read the current value of priceID, aborting the transaction if the price has not been updated recently.
>     // Every chain has a default recency threshold which can be retrieved by calling the getValidTimePeriod() function on the contract.
>     // Please see IPyth.sol for variants of this function that support configurable recency thresholds and other useful features.
>     return pyth.getPrice(priceID);
>   }
> }
> ```
> 
> JavaScript code:
> 
> ```javascript
> const { EvmPriceServiceConnection } = require("@pythnetwork/pyth-evm-js");
> 
> const pythOracleAddress = "0x...."; // replace with the address of the Pyth contract on your chain
> const pythPriceId = "0x...."; // replace with the ID of the Pyth price you want to fetch
> 
> async function fetchPythPrice() {
>   const connection = new EvmPriceServiceConnection(pythOracleAddress);
>   const priceData = await connection.getPriceData(pythPriceId);
>   return priceData.price.toNumber() / 10 ** priceData.exponent.toNumber();
> }
> 
> fetchPythPrice().then((price) => console.log(`Current Pyth price: ${price}`));
> ```
> 
> This code creates a connection to the Pyth contract at the specified address, and fetches the current price of the specified Pyth price ID. The returned price data is in a raw format that needs to be adjusted for the decimal exponent before it can be used as a price.
>
> -> **Question**: Como asegura la robustez de Pyth el algoritmo de agregacion? Explicame por una lista en espanol. 
>
> **Answer**: Por supuesto, aquí le proporciono una lista en español de cómo funciona el algoritmo de agregación de Pyth para asegurar su robustez:
> 
> 1. Cada proveedor envía un precio *pᵢ* y una confianza *cᵢ*.
> 2. Para cada proveedor, se generan tres votos: *pᵢ* - *cᵢ*, *pᵢ* y *pᵢ* + *cᵢ*.
> 3. Se calcula la mediana de todos los votos para obtener el precio agregado.
> 4. Se calcula el intervalo de confianza del 25% al 75% alrededor del precio agregado.
> 5. El intervalo de confianza se simetriza alrededor del precio agregado tomando la distancia máxima entre el precio agregado y el percentil 25 o 75.
> 6. Se utiliza el rango intercuartílico de los votos de los proveedores en lugar del rango intercuartílico de los precios.
> 7. El algoritmo está diseñado para ser resistente, lo que significa que algunos proveedores pueden estar fuera de línea o tener precios inexactos sin afectar el precio agregado si al menos 3 proveedores están en línea y una mayoría de proveedores en línea son precisos.
> 
> Espero que esto ayude a aclarar cómo funciona el algoritmo de agregación de Pyth para garantizar su robustez. Si tiene más preguntas, no dude en hacerlas. 


## Leverages LangChain.js LLM Template

To use the Javascript LangChain LLM template[https://github.com/Conner1115/LangChain.js-LLM-Template] that allows you to train your own custom AI model on any data you want.

## Setup
1. Provide all the information you want your LLM to be trained on in the `training` directory in markdown files.  Folder depth doesn't matter.
2. Add your OpenAI API key in environment vars via the key `OPENAI_API_KEY`.
3. Run `yarn train` or `npm train` to set up your vector store.
4. Modify the base prompt in `lib/basePrompt.js`
5. Run index.js, and start playing around with it!
