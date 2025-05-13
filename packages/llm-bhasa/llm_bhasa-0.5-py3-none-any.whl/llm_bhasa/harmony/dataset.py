import torch
import tiktoken
from torch.utils.data import IterableDataset, Dataset, DataLoader
from llm_bhasa.harmony import data

class CustomDataset(IterableDataset):
    """
    Custom dataset for preparing text data for language model training.

    This dataset processes text data from multiple files, tokenizes it, and
    creates input-target pairs using a sliding window approach. Each input
    sequence is a fixed-length chunk of tokens, and the corresponding target
    sequence is the same chunk shifted by one token to the right.

    This class inherits from `torch.utils.data.IterableDataset`, making it
    suitable for handling large datasets that may not fit entirely in memory.

    Args:
        filepaths (list): A list of filepaths to text files.
        tokenizer (tiktoken.Encoding): The tokenizer used to convert text to tokens.
        max_length (int): The maximum length of each input and target sequence.
        stride (int): The step size for the sliding window.

    Yields:
        tuple: A tuple containing two tensors:
            - input_sequence (torch.Tensor): A tensor of token IDs representing the input sequence.
            - target_sequence (torch.Tensor): A tensor of token IDs representing the target sequence.

    Raises:
        FileNotFoundError: If any of the specified filepaths do not exist.
        IOError: If there is an error reading any of the files.
    """
    def __init__(self, filepaths, tokenizer, max_length, stride):
        """
        Initializes the CustomDataset.

        Args:
            filepaths (list): A list of filepaths to text files.
            tokenizer (tiktoken.Encoding): The tokenizer used to convert text to tokens.
            max_length (int): The maximum length of each input and target sequence.
            stride (int): The step size for the sliding window.
        """
        self.filepaths = filepaths
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.stride = stride

    def __iter__(self):
        """
        Iterates through the dataset, yielding input-target pairs.

        This method reads each file, tokenizes its content, and then applies
        a sliding window to create input-target pairs.

        Yields:
            tuple: A tuple containing two tensors:
                - input_sequence (torch.Tensor): A tensor of token IDs representing the input sequence.
                - target_sequence (torch.Tensor): A tensor of token IDs representing the target sequence.
        """
        for filepath in self.filepaths:
            try:

                # In case filepath is an URI directly read text from URI                
                status, text = data.read_from_url(filepath) if filepath.startswith("http") else data.read_from_file(filepath)
                if not status:
                    continue

                token_ids = self.tokenizer.encode(text)  # Tokenize the text
                """
                Sliding window on length (max_length) and jump (stride) to
                store input and target to be used later.
                Note: Since all data is loaded into memory with large dataset
                this can cause implementation issues
                """
                for i in range(0, len(token_ids) - self.max_length, self.stride):
                    x = token_ids[i:i + self.max_length]
                    y = token_ids[i + 1: i + self.max_length + 1]
                    yield torch.tensor(x, dtype=torch.long), torch.tensor(y, dtype=torch.long)
            except Exception as err:
                print(f"Error processing {filepath}: {err}")

def create_dataloader(filepaths, batch_size=4, max_length=256, stride=128,
                      drop_last=True, num_workers=0):
    """
    Creates a DataLoader for training a language model.

    This function takes a list of filepaths, tokenizes the text data in each file,
    and prepares it for training by creating a DataLoader that yields batches
    of input-target pairs.

    Args:
        filepaths (list): A list of filepaths to text files.
        batch_size (int, optional): The number of samples per batch. Defaults to 4.
        max_length (int, optional): The maximum length of each input and target sequence. Defaults to 256.
        stride (int, optional): The step size for the sliding window. Defaults to 128.
        drop_last (bool, optional): Whether to drop the last incomplete batch. Defaults to True.
        num_workers (int, optional): The number of subprocesses to use for data loading. Defaults to 0.

    Returns:
        torch.utils.data.DataLoader: A DataLoader that yields batches of input-target pairs.
    """

    # Initialize the tokenizer
    tokenizer = tiktoken.get_encoding("gpt2")

    # Creates dataset
    dataset = CustomDataset(filepaths, tokenizer, max_length, stride)

    # drop_last=True drops the last batch if it is shorter than the specified batch_size
    # to prevent loss spikes during training.
    # num_workers - The number of CPU processes to use for preprocessing
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        drop_last=drop_last,
        num_workers=num_workers
    )
    return dataloader

if __name__ == "__main__":

    # import os
    # import sys
    # path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../")
    # sys.path.append(path)

    gutenberg_book_ids = range(9)  # 100

    # Download file in localstorage
    # filepaths = data.download_sample_text(gutenberg_book_ids=gutenberg_book_ids, verbose=False)

    # Direct download in memory
    base_url = "https://www.gutenberg.org/files/{}/{}-0.txt"
    filepaths = [base_url.format(book_id, book_id) for book_id in gutenberg_book_ids]

    dataloader = create_dataloader(filepaths, batch_size=1, max_length=4, stride=1)
    for i, batch in enumerate(dataloader):
        if i % 1000 == 0:
            print(i)
    print(i)