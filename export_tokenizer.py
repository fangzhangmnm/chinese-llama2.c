from transformers import LlamaTokenizer
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str, help="the output filepath")
    parser.add_argument("-m", "--model", type=str, help="path to the tokenizer model", required=True)
    
    args = parser.parse_args()
    tokenizer = LlamaTokenizer(args.model)
    rtval=tokenizer.save_pretrained(args.filepath)
    print('saved to', rtval)