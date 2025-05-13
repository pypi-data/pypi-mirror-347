import torch

def softmax_with_temperature(logits, temperature):
    """
    Applies softmax with a temperature scaling to the input logits.

    This function scales the logits by the given temperature and then applies
    the softmax function to obtain probabilities. Higher temperatures result
    in a softer probability distribution, while lower temperatures make the
    distribution sharper.

    Args:
        logits (torch.Tensor): The input logits tensor.
        temperature (float): The temperature scaling factor.

    Returns:
        torch.Tensor: The softmax probabilities with temperature scaling.
    """
    scaled_logits = logits / temperature
    return torch.softmax(scaled_logits, dim=0)

def generate(model, idx, max_new_tokens, context_size, temperature=0.0, top_k=None, eos_id=None):
    """
    Generates text using a language model.

    This function generates text by iteratively predicting the next token based on
    the current context. It supports temperature scaling and top-k sampling.

    Args:
        model (torch.nn.Module): The language model.
        idx (torch.Tensor): The initial context as a tensor of token IDs.
        max_new_tokens (int): The maximum number of tokens to generate.
        context_size (int): The maximum context size supported by the model.
        temperature (float, optional): The temperature for scaling the logits. Defaults to 0.0 (greedy decoding).
        top_k (int, optional): The number of top-k tokens to consider for sampling. Defaults to None (no top-k sampling).
        eos_id (int, optional): The end-of-sequence token ID. Defaults to None.

    Returns:
        torch.Tensor: A tensor of generated token IDs.
    """
    # idx is (batch, n_tokens) array of indices in the current context
    for _ in range(max_new_tokens):

        # Crop current context if it exceeds the supported context size
        # E.g., if LLM supports only 5 tokens, and the context size is 10
        # then only the last 5 tokens are used as context
        idx_cond = idx[:, -context_size:]
        
        # Get the predictions
        with torch.no_grad():
            logits = model(idx_cond)

        # Focus only on the last time step
        # (batch, n_tokens, vocab_size) becomes (batch, vocab_size)
        logits = logits[:, -1, :]


        if top_k is not None:
            top_logits, _ = torch.topk(logits, top_k)
            min_val = top_logits[:, -1]
            logits = torch.where(
                logits < min_val,
                torch.tensor(float('-inf')).to(logits.device),
                logits
            )

        if temperature > 0.0:
            logits = logits / temperature
            # Apply softmax to get probabilities
            probs = torch.softmax(logits, dim=-1)   # (batch, vocab_size)
            idx_next = torch.multinomial(probs, num_samples=1)
        else:
            # Get the idx of the vocab entry with the highest logits value
            idx_next = torch.argmax(logits, dim=-1, keepdim=True)  # (batch, 1)

        if idx_next == eos_id:
            break

        # Append sampled index to the running sequence
        idx = torch.cat((idx, idx_next), dim=1)  # (batch, n_tokens+1)

    return idx

if __name__ == "__main__":

    import torch
    from llm_bhasa.harmony import generator
    from llm_bhasa.harmony import tokenizer as tokenizer_lib
    from llm_bhasa.harmony import config
    from llm_bhasa.harmony import model

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model_filepath = ""
    model_llm = model.LLMModel(config.GPT_CONFIG_124M)
    model_llm = model.load_model(model_filepath)
    model_llm.to(device)
    model_llm.eval() # disable dropout

    start_context = "Hello, I am"

    tokenizer = tokenizer_lib.get_tokenizer()
    encoded = tokenizer_lib.text_to_token_ids(start_context, tokenizer).to(device)
    token_ids  = generator.generate(model=model_llm, idx=encoded, max_new_tokens=50, context_size=config.GPT_CONFIG_124M["context_length"])
    decoded_text = tokenizer_lib.token_ids_to_text(token_ids, tokenizer)
    decoded_text = decoded_text.replace("\n", " ")

    print(decoded_text)
